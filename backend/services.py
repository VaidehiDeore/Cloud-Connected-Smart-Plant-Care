from datetime import datetime, timedelta
import hashlib
import logging
from sqlalchemy.orm import Session
from config import settings
from models import Device, SensorReading, WateringEvent, Alert

log = logging.getLogger("plant-care")


def utcnow():
    return datetime.utcnow()


def reading_hash(p):
    raw = f"{p.device_id}|{p.soil_moisture:.3f}|{p.temperature:.3f}|{p.humidity:.3f}|{p.light_level:.3f}|{p.timestamp}"
    return hashlib.sha256(raw.encode()).hexdigest()


def unresolved_alert(db, device_id, kind):
    return db.query(Alert).filter(
        Alert.device_id == device_id,
        Alert.alert_type == kind,
        Alert.status.in_(["ACTIVE", "ACKNOWLEDGED"]),
    ).first()


def alert(db, device_id, kind, level, message):
    old = unresolved_alert(db, device_id, kind)
    if old:
        return old
    item = Alert(device_id=device_id, alert_type=kind, level=level, message=message)
    db.add(item)
    db.commit()
    db.refresh(item)
    log.warning("ALERT %s: %s", kind, message)
    return item


def resolve(db, device_id, kind):
    rows = db.query(Alert).filter(
        Alert.device_id == device_id,
        Alert.alert_type == kind,
        Alert.status.in_(["ACTIVE", "ACKNOWLEDGED"]),
    ).all()
    if rows:
        for item in rows:
            item.status = "RESOLVED"
        db.commit()


def water(db, device, before, duration, trigger):
    duration = min(duration, settings.max_watering_duration_seconds)
    device.pump_on = True
    after = min(100, before + duration * 2)
    device.water_tank_level = max(0, device.water_tank_level - duration * 0.5)
    event = WateringEvent(
        device_id=device.device_id,
        trigger_type=trigger,
        moisture_before=before,
        moisture_after=after,
        duration=duration,
        timestamp=utcnow(),
    )
    db.add(event)
    device.pump_on = False
    db.commit()
    db.refresh(event)
    # Do not resolve the alert here. The user can acknowledge it, and the
    # next healthy sensor reading will resolve it automatically.
    return event, after


def process(db: Session, device, payload):
    ts = payload.timestamp or utcnow()
    if ts.tzinfo is not None:
        ts = ts.replace(tzinfo=None)

    rh = reading_hash(payload)
    if db.query(SensorReading).filter(SensorReading.reading_hash == rh).first():
        return None, "duplicate"

    reading = SensorReading(
        device_id=device.device_id,
        soil_moisture=payload.soil_moisture,
        temperature=payload.temperature,
        humidity=payload.humidity,
        light_level=payload.light_level,
        timestamp=ts,
        reading_hash=rh,
    )
    db.add(reading)
    device.last_seen = utcnow()

    if payload.water_tank_level is not None:
        device.water_tank_level = payload.water_tank_level

    if payload.soil_moisture < device.moisture_threshold:
        alert(
            db,
            device.device_id,
            "LOW_SOIL_MOISTURE",
            "WARNING",
            f"{device.plant_name} moisture dropped below {device.moisture_threshold:.0f}%.",
        )
    if payload.temperature > 38:
        alert(
            db,
            device.device_id,
            "HIGH_TEMPERATURE",
            "CRITICAL",
            f"{device.plant_name} temperature exceeded 38 C.",
        )
    else:
        resolve(db, device.device_id, "HIGH_TEMPERATURE")

    db.commit()

    last = db.query(WateringEvent).filter(
        WateringEvent.device_id == device.device_id
    ).order_by(WateringEvent.timestamp.desc()).first()
    now = utcnow()
    cooldown = last and (now - last.timestamp) < timedelta(seconds=settings.watering_cooldown_seconds)

    if (
        payload.soil_moisture < device.moisture_threshold
        and device.water_tank_level > settings.min_water_tank_level
        and not device.pump_on
        and not cooldown
    ):
        water(
            db,
            device,
            payload.soil_moisture,
            settings.default_watering_duration_seconds,
            "AUTO_THRESHOLD",
        )
        return reading, "watered"

    return reading, "accepted"

