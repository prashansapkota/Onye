from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "onye-ehr-backend"
    env: str = "development"
    api_prefix: str = "/api"
    google_api_key: str = ""
    anthropic_api_key: str = ""
    api_key: str = "dev-key"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
