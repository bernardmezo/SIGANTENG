import os
from typing import List

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Multi-Model Assistant Backend"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Hugging Face
    HF_API_TOKEN: str = os.getenv("HF_API_TOKEN", "")

    # Database (Neon)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "") # PostgreSQL connection string

    # Authentication (Clerk)
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY", "")

    # File Storage (Cloudinary)
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
