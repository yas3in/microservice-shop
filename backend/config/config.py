from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "MicroShop E-Commerce"
    DEBUG: bool = True

    # Security / JWT Configuration
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Database Configuration (supports sqlite+aiosqlite and postgresql+asyncpg)
    DATABASE_URL: str = "sqlite+aiosqlite:///./microshop.db"

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"

    # Gateway Routing & Internal Microservice URLs
    GATEWAY_PORT: int = 8000
    AUTH_SERVICE_PORT: int = 8001
    CATALOGUE_SERVICE_PORT: int = 8002
    PRODUCT_SERVICE_PORT: int = 8002
    ORDER_SERVICE_PORT: int = 8003

    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    CATALOGUE_SERVICE_URL: str = "http://catalogue-service:8002"
    PRODUCT_SERVICE_URL: str = "http://catalogue-service:8002"
    ORDER_SERVICE_URL: str = "http://order-service:8003"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings: Settings = Settings()
