from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    app_name: str = "Law Assistant"
    environment: str = "dev"
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @field_validator("database_url")
    @classmethod
    def must_have_db_url(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("DATABASE_URL تنظیم نشده! فایل .env را درست کن.")
        return v

settings = Settings()
