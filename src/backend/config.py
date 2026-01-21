"""Configuration settings for the FastAPI application."""

from pydantic import ConfigDict, Field, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Dictionary API"
    app_version: str = "1.0.0"
    # Individual DB components are easier to manage in K8s Secret/ConfigMaps
    DB_USER: str = Field(default="demo")
    DB_PASSWORD: str = Field(default="demo")
    DB_HOST: str = Field(default="mariadb-operator-instance")  # Matches your K8s Service name
    DB_PORT: str = Field(default="3306")
    DB_NAME: str = Field(default="dictionary-db")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        # Properly formatted for SQLAlchemy + PyMySQL
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
