from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Alemeno Transaction Pipeline"
    app_env: str = "dev"

    database_url: str = "postgresql://postgres:postgres@localhost:5432/alemeno_db"
    redis_url: str = "redis://localhost:6379/0"

    gemini_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()