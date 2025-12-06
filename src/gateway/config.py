# src/gateway/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "Pharmacy Gateway"
    DEBUG: bool = False
    
    # Browser Config
    HEADLESS: bool = True
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    
    # Credentials (werden aus .env geladen)
    CANNALEO_USER: str
    CANNALEO_PASS: str
    
    # Paths
    DOWNLOAD_DIR: str = "./data/downloads"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()