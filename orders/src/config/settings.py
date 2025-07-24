from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Orders Service"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://user:password@orders-db:5432/orders_db"
    
    # JWT - используем тот же secret_key, что и auth сервис
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Logging
    log_level: str = "INFO"
    
    # Auth service
    auth_service_url: str = "http://auth-service:8000"
    
    # Fleet service
    fleet_service_url: str = "http://fleet-service:8000"
    
    # Warehouse service
    warehouse_service_url: str = "http://warehouse-service:8000"
    
    # RabbitMQ
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"
    rabbitmq_exchange: str = "cargo_track_events"
    
    class Config:
        env_file = ".env"


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 