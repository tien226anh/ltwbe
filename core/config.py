from typing import List

from pydantic import AnyHttpUrl, BaseSettings

class Settings(BaseSettings):
    APP_TITLE: str = "BOOK API"
    APP_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    # APP_ORIGINS: List[AnyHttpUrl] = ["*"]
    # APP_HOST: str = "0.0.0.0"
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    APP_STATIC_DIR: str = "static"
    
    PRIVATE_KEY: str
    PUBLIC_KEY: str
    
    MONGO_DETAILS: str = "mongodb://localhost:27017/"
    DATABASE_NAME: str = "books_db"
    
    ROOT_PATH: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        secrets_dir = "./secrets"
        case_sensitive = True
        
settings = Settings()