from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://warehouse_user:warehouse_password@warehouse-db:5432/warehouse_db"
    
    # JWT
    secret_key: str = "warehouse-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Logging
    log_level: str = "INFO"
    
    # Application
    app_name: str = "Warehouse Service"
    debug: bool = True
    
    # Auth service
    auth_service_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"


_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 