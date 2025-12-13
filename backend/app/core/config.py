from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional, List

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Fal.ai Gateway"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # API
    API_V1_PREFIX: str = "/api/v1"

    # Fal.ai
    FAL_API_KEY: str
    FAL_API_BASE_URL: str = "https://fal.run"
    FAL_API_TIMEOUT: int = 300

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_MAX_CONNECTIONS: int = 50

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    MAX_CONCURRENT_REQUESTS: int = 5

    # Caching
    CACHE_TTL_MODELS: int = 3600  # 1 hour
    CACHE_TTL_GENERATION: int = 86400  # 24 hours

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    model_config = SettingsConfigDict(
        env_file=[".env.local", ".env"],  # Try .env.local first, then .env
        case_sensitive=True,
        env_file_encoding="utf-8"
    )   

@lru_cache()
def get_settings() -> Settings:
    return Settings()
