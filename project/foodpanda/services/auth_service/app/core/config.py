"""Settings read from environment variables or an env file (ENV_FILE, default ".env")."""
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str  # HS256: one shared secret signs and verifies. Fine while only this service checks tokens.
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # extra="ignore": skip env vars we don't use (e.g. POSTGRES_* in .env, which are for the DB container)
    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE", ".env"), extra="ignore")


settings = Settings()
