from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Interview Copilot"
    environment: str = "development"

    huggingface_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()