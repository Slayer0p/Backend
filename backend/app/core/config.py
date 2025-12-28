from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Career Companion"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./career.db"

    # Security
    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 🔥 AI / LLM
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "allow"   # default, but explicit is good


@lru_cache
def get_settings():
    return Settings()
