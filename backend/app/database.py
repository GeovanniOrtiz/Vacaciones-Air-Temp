"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os

# Set encoding for PostgreSQL client on Windows
os.environ["PGCLIENTENCODING"] = "UTF8"


class Settings(BaseSettings):
    """Application settings"""
    DATABASE_URL: str = "postgresql://postgres:Airtemp@127.0.0.1:5432/vacaciones_db"
    
    class Config:
        env_file = ".env"


settings = Settings()

# Create engine
engine = create_engine(settings.DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
