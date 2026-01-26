from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/healthcare"
    redis_url: str = "redis://localhost:6379"

    # Security
    jwt_secret: str = "your-super-secret-jwt-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    # HIPAA
    audit_log_enabled: bool = True
    session_timeout_minutes: int = 15
    phi_encryption_enabled: bool = True

    # ML
    ml_model_path: str = "./models"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
