from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "DFIR Automation Framework"
    environment: str = "development"
    database_url: str = "sqlite:///./dfir.db"
    secret_key: str = "change-this-in-production"
    access_token_expire_minutes: int = 60
    cors_origins: str = "http://localhost:3000,http://localhost:8000"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
