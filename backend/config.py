from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str = "change-this-local-secret"
    database_url: str = "sqlite:///./plant_care.db"
    default_device_api_key: str = "change-device-key"
    offline_after_seconds: int = 30
    default_moisture_threshold: float = 30
    default_watering_duration_seconds: int = 5
    max_watering_duration_seconds: int = 10
    watering_cooldown_seconds: int = 30
    min_water_tank_level: float = 10
    cors_origins: list[str] = ["http://localhost:5173"]
    use_firestore: bool = False
    google_application_credentials: str | None = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
