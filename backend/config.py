from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    groq_api_key: str = ""
    gemini_api_key: str = ""
    anthropic_api_key: str = ""
    database_url: str = "sqlite:///./transplant.db"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()