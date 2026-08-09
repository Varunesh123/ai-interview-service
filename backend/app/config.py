from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Interview Copilot"
    environment: str = "development"

    huggingface_api_key: str
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()