from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # loaded from .env automatically
    database_url: str = "postgresql://appuser:app_password@localhost:5432/appdb"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
