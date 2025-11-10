import os
from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Pydantic V2 configuration
    model_config = ConfigDict(case_sensitive=True, env_file=".env")

    PROJECT_NAME: str = "AI Multi-Model Assistant Backend"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # --- AI Provider Default Settings ---
    # Change these values in your .env file to switch default models
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
    DEFAULT_VISION_PROVIDER: str = os.getenv("DEFAULT_VISION_PROVIDER", "openai")
    DEFAULT_STT_PROVIDER: str = os.getenv("DEFAULT_STT_PROVIDER", "openai")
    DEFAULT_TTS_PROVIDER: str = os.getenv("DEFAULT_TTS_PROVIDER", "openai")
    DEFAULT_EMBEDDING_MODEL: str = os.getenv(
        "DEFAULT_EMBEDDING_MODEL", "all-MiniLM-L6-v2"
    )

    # --- API Keys ---
    # Hugging Face
    HF_API_TOKEN: str = os.getenv("HF_API_TOKEN", "")

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Pinecone (for future use in Fase D)
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")

    # --- Infrastructure ---
    # Database (Neon)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Background Tasks (Celery & Redis)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # --- External Services ---
    # Authentication (Clerk)
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY", "")

    # File Storage (Cloudinary)
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")


settings = Settings()
