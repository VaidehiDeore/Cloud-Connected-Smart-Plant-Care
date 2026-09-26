from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Device, SensorReading, WateringEvent, Alert
from schemas import *
from security import *
from config import settings
from services import process, water

router = APIRouter()


def utcnow():
    return datetime.utcnow()


@router.post("/auth/register")
def register(p: RegisterRequest, db=Depends(get_db)):
    if db.query(User).filter(User.email == p.email.lower()).first():
        raise HTTPException(409, "Email already registered")
    u = User(name=p.name, email=p.email.lower(), password_hash=hash_password(p.password))
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"access_token": token_for(u.user_id), "token_type": "bearer"}


@router.post("/auth/login")
def login(p: LoginRequest, db=Depends(get_db)):
    u = db.query(User).filter(User.email == p.email.lower()).first()
    if not u or not verify_password(p.password, u.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": token_for(u.user_id), "token_type": "bearer"}


@router.post("/sensors/data")
def sensor(p: SensorPayload, x_api_key: str | None = Header(default=None), db=Depends(get_db)):
    if not x_api_key:
        raise HTTPException(401, "x-api-key required")
    d = db.get(Device, p.device_id)
    if not d:
        raise HTTPException(404, "Unknown device")
    if not compare(device_hash(x_api_key), device_hash(settings.default_device_api_key)):
        raise HTTPException(401, "Invalid device API key")
    reading, result = process(db, d, p)
    return {
        "ok": True,
        "duplicate": result == "duplicate",
        "automation": result,
        "reading_id": getattr(reading, "reading_id", None),
    }


def owned(device_id, db, user):
    d = db.get(Device, device_id)
    if not d:
        raise HTTPException(404, "Device not found")
    owner(d, user)
    return d


def device_dict(d, status):
    return {
        "device_id": d.device_id,
        "user_id": d.user_id,
        "plant_name": d.plant_name,
        "plant_type": d.plant_type,
        "location": d.location,
        "moisture_threshold": d.moisture_threshold,
        "last_seen": d.last_seen,
        "pump_on": d.pump_on,
        "water_tank_level": d.water_tank_level,
        "created_at": d.created_at,
        "status": status,
    }


@router.get("/devices")
def devices(db=Depends(get_db), user=Depends(current_user)):
    out = []
    now = utcnow()
    for d in db.query(Device).filter(Device.user_id == user.user_id).all():
        offline = d.last_seen is None or (now - d.last_seen) > timedelta(seconds=settings.offline_after_seconds)
        out.append(device_dict(d, "OFFLINE" if offline else "ONLINE"))
    return out


@router.post("/devices")
def create(p: DeviceCreate, db=Depends(get_db), user=Depends(current_user)):
    if db.get(Device, p.device_id):
        raise HTTPException(409, "Device already exists")
    d = Device(user_id=user.user_id, **p.model_dump())
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


@router.get("/devices/{device_id}")
def device(device_id, db=Depends(get_db), user=Depends(current_user)):
    d = owned(device_id, db, user)
    now = utcnow()
    offline = d.last_seen is None or (now - d.last_seen) > timedelta(seconds=settings.offline_after_seconds)
    return device_dict(d, "OFFLINE" if offline else "ONLINE")


@router.get("/devices/{device_id}/latest")
def latest(device_id, db=Depends(get_db), user=Depends(current_user)):
    d = owned(device_id, db, user)
    r = db.query(SensorReading).filter(SensorReading.device_id == d.device_id).order_by(SensorReading.timestamp.desc()).first()
    if not r:
        return None
    return {
        "soil_moisture": r.soil_moisture,
        "temperature": r.temperature,
        "humidity": r.humidity,
        "light_level": r.light_level,
        "timestamp": r.timestamp,
    }


@router.get("/devices/{device_id}/history")
def history(device_id, limit: int = 100, db=Depends(get_db), user=Depends(current_user)):
    d = owned(device_id, db, user)
    rows = db.query(SensorReading).filter(SensorReading.device_id == d.device_id).order_by(SensorReading.timestamp.desc()).limit(min(limit, 500)).all()
    return [
        {
            "timestamp": r.timestamp,
            "soil_moisture": r.soil_moisture,
            "temperature": r.temperature,
            "humidity": r.humidity,
            "light_level": r.light_level,
        }
        for r in reversed(rows)
    ]


@router.put("/devices/{device_id}/threshold")
def threshold(device_id, p: ThresholdUpdate, db=Depends(get_db), user=Depends(current_user)):
    d = owned(device_id, db, user)
    d.moisture_threshold = p.moisture_threshold
    db.commit()
    return {"ok": True, "moisture_threshold": d.moisture_threshold}


@router.post("/devices/{device_id}/water")
def manual(device_id, p: WaterRequest, db=Depends(get_db), user=Depends(current_user)):
    d = owned(device_id, db, user)
    r = db.query(SensorReading).filter(SensorReading.device_id == d.device_id).order_by(SensorReading.timestamp.desc()).first()
    before = r.soil_moisture if r else 50
    e, after = water(db, d, before, p.duration_seconds or settings.default_watering_duration_seconds, "MANUAL")
    return {"ok": True, "event_id": e.event_id, "moisture_after": after}


@router.get("/devices/{device_id}/watering-history")
def watering_history(device_id, db=Depends(get_db), user=Depends(current_user)):
    d = owned(device_id, db, user)
    rows = db.query(WateringEvent).filter(WateringEvent.device_id == d.device_id).order_by(WateringEvent.timestamp.desc()).limit(100).all()
    return [
        {
            "event_id": x.event_id,
            "trigger_type": x.trigger_type,
            "moisture_before": x.moisture_before,
            "moisture_after": x.moisture_after,
            "duration": x.duration,
            "timestamp": x.timestamp,
        }
        for x in rows
    ]


@router.get("/alerts")
def alerts(db=Depends(get_db), user=Depends(current_user)):
    ds = db.query(Device).filter(Device.user_id == user.user_id).all()
    ids = [d.device_id for d in ds]
    now = utcnow()
    for d in ds:
        if d.last_seen is None or (now - d.last_seen) > timedelta(seconds=settings.offline_after_seconds):
            exists = db.query(Alert).filter(
                Alert.device_id == d.device_id,
                Alert.alert_type == "DEVICE_OFFLINE",
                Alert.status == "ACTIVE",
            ).first()
            if not exists:
                db.add(Alert(
                    device_id=d.device_id,
                    alert_type="DEVICE_OFFLINE",
                    level="CRITICAL",
                    message=f"No sensor data received from {d.device_id} during the expected interval.",
                ))
    db.commit()
    if not ids:
        return []
    rows = db.query(Alert).filter(Alert.device_id.in_(ids)).order_by(Alert.created_at.desc()).limit(100).all()
    return [
        {
            "alert_id": a.alert_id,
            "device_id": a.device_id,
            "alert_type": a.alert_type,
            "level": a.level,
            "message": a.message,
            "status": a.status,
            "created_at": a.created_at,
        }
        for a in rows
    ]


@router.put("/alerts/{alert_id}/acknowledge")
def acknowledge(alert_id: int, db=Depends(get_db), user=Depends(current_user)):
    a = db.get(Alert, alert_id)
    if not a:
        raise HTTPException(404, "Alert not found")
    owner(db.get(Device, a.device_id), user)
    if a.status != "ACTIVE":
        return {"ok": True, "status": a.status}
    a.status = "ACKNOWLEDGED"
    a.acknowledged_at = utcnow()
    db.commit()
    return {"ok": True, "status": a.status}
