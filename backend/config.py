import os
from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # API settings
    API_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./music_recommender.db"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Feature extraction settings
    AUDIO_FEATURE_DIMENSIONS: int = 128
    IMAGE_FEATURE_DIMENSIONS: int = 512
    TEXT_FEATURE_DIMENSIONS: int = 384
    
    # Model settings
    AUDIO_MODEL_PATH: str = "./models/audio_model.h5"
    IMAGE_MODEL_PATH: str = "./models/image_model.h5"
    TEXT_MODEL_PATH: str = "./models/text_model.h5"
    
    # Data settings
    AUDIO_SAMPLES_DIR: str = "../data/audio_samples"
    IMAGES_DIR: str = "../data/images"
    METADATA_DIR: str = "../data/metadata"
    
    # Recommendation settings
    TOP_K_RECOMMENDATIONS: int = 5
    SIMILARITY_THRESHOLD: float = 0.5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()

# Override settings with environment variables if they exist
if os.environ.get("DATABASE_URL"):
    settings.DATABASE_URL = os.environ.get("DATABASE_URL")

if os.environ.get("SECRET_KEY"):
    settings.SECRET_KEY = os.environ.get("SECRET_KEY")