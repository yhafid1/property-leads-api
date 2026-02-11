"""Application configuration and environment settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/property_leads"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    DALLAS_CAD_URL: str = "https://www.dallascad.org/dataproducts.aspx"
    COLLIN_CAD_API: str = "https://data.texas.gov/resource/7ugx-vxwc.json"
    
    ETL_SCHEDULE_CRON: str = "0 2 * * 0"
    COMP_CACHE_DAYS: int = 90
    
    MIN_EQUITY_THRESHOLD: int = 50000
    HIGH_EQUITY_THRESHOLD: int = 100000
    MIN_MOTIVATION_SCORE: int = 50

settings = Settings()
