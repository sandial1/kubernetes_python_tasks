"""Configuration settings for the FastAPI application."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Dictionary API"
    app_version: str = "1.0.0"
    database_url: str = "mysql://demo:demo@db:3306/demo"
    
    class Config:
        env_file = ".env"


settings = Settings()