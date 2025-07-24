from shared.utils.auth_utils import (
    get_current_user as shared_get_current_user,
    require_role as shared_require_role,
    require_any_role as shared_require_any_role,
    AuthServiceClient as SharedAuthServiceClient
)
from config.settings import get_settings
import structlog

settings = get_settings()
logger = structlog.get_logger(__name__)

# Создаем функции с настройками orders сервиса
def get_current_user():
    logger.info("Creating get_current_user function", secret_key=settings.secret_key[:10] + "...", algorithm=settings.algorithm)
    return shared_get_current_user(settings.secret_key, settings.algorithm)

def require_role(required_role: str):
    logger.info("Creating require_role function", required_role=required_role, secret_key=settings.secret_key[:10] + "...", algorithm=settings.algorithm)
    return shared_require_role(required_role, settings.secret_key, settings.algorithm)

def require_any_role(required_roles: list[str]):
    logger.info("Creating require_any_role function", required_roles=required_roles, secret_key=settings.secret_key[:10] + "...", algorithm=settings.algorithm)
    return shared_require_any_role(required_roles, settings.secret_key, settings.algorithm)

# Создаем клиент для auth сервиса
def get_auth_service_client() -> SharedAuthServiceClient:
    return SharedAuthServiceClient(settings.auth_service_url) 