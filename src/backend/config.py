"""Configuration settings for the FastAPI application."""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    app_name: str = "Dictionary API"
    app_version: str = "1.0.0"
    database_url: str = "mysql://demo:demo@db:3306/demo"


settings = Settings()