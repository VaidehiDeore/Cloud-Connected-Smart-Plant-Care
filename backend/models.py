from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


def now():
    # SQLite stores DateTime values without timezone information.
    return datetime.utcnow()


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Device(Base):
    __tablename__ = "devices"
    device_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), index=True)
    plant_name: Mapped[str] = mapped_column(String(120))
    plant_type: Mapped[str] = mapped_column(String(80))
    location: Mapped[str] = mapped_column(String(120), default="Indoor")
    moisture_threshold: Mapped[float] = mapped_column(Float, default=30)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    pump_on: Mapped[bool] = mapped_column(Boolean, default=False)
    water_tank_level: Mapped[float] = mapped_column(Float, default=100)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class SensorReading(Base):
    __tablename__ = "sensor_readings"
    reading_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[str] = mapped_column(ForeignKey("devices.device_id"), index=True)
    soil_moisture: Mapped[float] = mapped_column(Float)
    temperature: Mapped[float] = mapped_column(Float)
    humidity: Mapped[float] = mapped_column(Float)
    light_level: Mapped[float] = mapped_column(Float, default=50)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    reading_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)


class WateringEvent(Base):
    __tablename__ = "watering_events"
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[str] = mapped_column(ForeignKey("devices.device_id"), index=True)
    trigger_type: Mapped[str] = mapped_column(String(40))
    moisture_before: Mapped[float] = mapped_column(Float)
    moisture_after: Mapped[float | None] = mapped_column(Float)
    duration: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class Alert(Base):
    __tablename__ = "alerts"
    alert_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[str] = mapped_column(ForeignKey("devices.device_id"), index=True)
    alert_type: Mapped[str] = mapped_column(String(50))
    level: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
