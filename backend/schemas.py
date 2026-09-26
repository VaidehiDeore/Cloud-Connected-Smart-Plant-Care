from datetime import datetime
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: str
    password: str

class SensorPayload(BaseModel):
    device_id: str = Field(min_length=1, max_length=80)
    soil_moisture: float = Field(ge=0, le=100)
    temperature: float = Field(ge=-20, le=70)
    humidity: float = Field(ge=0, le=100)
    light_level: float = Field(default=50, ge=0, le=100)
    water_tank_level: float | None = Field(default=None, ge=0, le=100)
    timestamp: datetime | None = None

class DeviceCreate(BaseModel):
    device_id: str = Field(min_length=2, max_length=80)
    plant_name: str = Field(min_length=1, max_length=120)
    plant_type: str = Field(min_length=1, max_length=80)
    location: str = "Indoor"
    moisture_threshold: float = Field(default=30, ge=1, le=99)
    water_tank_level: float = Field(default=100, ge=0, le=100)

class ThresholdUpdate(BaseModel):
    moisture_threshold: float = Field(ge=1, le=99)

class WaterRequest(BaseModel):
    duration_seconds: int | None = Field(default=None, ge=1, le=10)
