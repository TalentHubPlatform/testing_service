from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class APIV0Prefix(BaseModel):
    pass


class APIPrefix(BaseModel):
    prefix: str = "/api"
    v0: APIV0Prefix = APIV0Prefix()


class DatabaseConfig(BaseModel):
    url: str = "mongodb://testing_service_mongo:27017"
    db_name: str = "contest_db"


class CachingConfig(BaseModel):
    url: RedisDsn = "redis://localhost:6379/0"


class SecurityConfig(BaseModel):
    key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    api: APIPrefix = APIPrefix()
    logging: LoggingConfig = LoggingConfig()
    db: DatabaseConfig = DatabaseConfig()
    caching: CachingConfig = CachingConfig()
    security: SecurityConfig = SecurityConfig()


settings = Settings()
