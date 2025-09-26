# app/core/config.py
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # for RS256
    # PRIVATE_KEY_PATH: str
    # PUBLIC_KEY_PATH: str
    # ALGORITHM: str = "RS256"

    class Config:
        extra = "allow"  # This ignores unknown env vars
        # Use ENV_FILE if defined, otherwise fall back to .env
        env_file = os.getenv("ENV_FILE", ".env")


settings = Settings()
