from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    node_env: str = "development"

    model_config = SettingsConfigDict(env_file=".env")