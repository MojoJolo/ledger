"""Configuration settings for the ledger application.

This module uses Pydantic Settings to manage application configuration
from environment variables, following FastAPI best practices.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    Environment Variables:
        DB_TYPE: Database type to use (default: "in_memory")
            Options: "in_memory", "postgres", "mongodb"
        
        # PostgreSQL settings (when DB_TYPE="postgres")
        POSTGRES_HOST: PostgreSQL host (default: "localhost")
        POSTGRES_PORT: PostgreSQL port (default: 5432)
        POSTGRES_DB: PostgreSQL database name (default: "ledger")
        POSTGRES_USER: PostgreSQL username (default: "ledger_user")
        POSTGRES_PASSWORD: PostgreSQL password (default: "")
        
        # MongoDB settings (when DB_TYPE="mongodb")
        MONGODB_URI: MongoDB connection URI (default: "mongodb://localhost:27017")
        MONGODB_DB: MongoDB database name (default: "ledger")
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Database settings
    db_type: str = "in_memory"
    
    # PostgreSQL settings
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "ledger"
    postgres_user: str = "ledger_user"
    postgres_password: str = ""
    
    # MongoDB settings
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "ledger"


# Global settings instance
settings = Settings()
