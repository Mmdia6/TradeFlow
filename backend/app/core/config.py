from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "TradeFlow"
    environment: str = "development"
    secret_key: str = "change-me"
    access_token_minutes: int = 15
    refresh_token_days: int = 30
    database_url: str = "mysql+pymysql://tradeflow:tradeflow@mysql:3306/tradeflow"
    redis_url: str = "redis://redis:6379/0"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
