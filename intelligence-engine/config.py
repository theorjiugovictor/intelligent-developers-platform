"""
Configuration settings for the Intelligence Engine
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://idp_user:idp_pass@postgres:5432/idp_intelligence"

    # Redis
    REDIS_URL: str = "redis://redis:6379"

    # Observability Stack
    LOKI_URL: str = "http://loki:3100"
    MIMIR_URL: str = "http://mimir:9009"
    TEMPO_URL: str = "http://tempo:3200"

    # Model settings
    MODEL_PATH: str = "/app/models"
    RETRAIN_INTERVAL_HOURS: int = 24

    # Analysis settings
    BREAKING_CHANGE_THRESHOLD: float = 0.7
    ANOMALY_THRESHOLD: float = 0.8
    PERFORMANCE_DEGRADATION_THRESHOLD: float = 0.15

    # Self-healing settings
    AUTO_HEAL_ENABLED: bool = True
    AUTO_HEAL_DRY_RUN: bool = False

    # Feature flags
    ENABLE_BREAKING_CHANGE_DETECTION: bool = True
    ENABLE_ANOMALY_DETECTION: bool = True
    ENABLE_PERFORMANCE_PREDICTION: bool = True
    ENABLE_SELF_HEALING: bool = True

    # Claude API (optional)
    CLAUDE_API_KEY: Optional[str] = None
    CLAUDE_MODEL: str = "claude-sonnet-4-5-20250514"
    CLAUDE_MAX_TOKENS: int = 4096

    # Startup tolerance
    ALLOW_DB_INIT_FAILURE: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
