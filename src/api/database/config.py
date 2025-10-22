"""Database configuration and initialization.

This module handles database selection and initialization based on
Pydantic Settings configuration. It provides a factory function that returns
the appropriate database repository implementation.
"""

from config import settings
from .base import DatabaseRepository
from .in_memory import InMemoryRepository


def get_database_repository() -> DatabaseRepository:
    """Get the configured database repository instance.
    
    This function determines which database implementation to use based on
    the settings loaded from environment variables. It can be extended to
    support multiple database backends (PostgreSQL, MongoDB, etc.).
    
    Environment Variables:
        DB_TYPE: Type of database to use (default: "in_memory")
            - "in_memory": Use in-memory storage
            - "postgres": Use PostgreSQL (requires implementation)
            - "mongodb": Use MongoDB (requires implementation)
        
        # PostgreSQL settings (when DB_TYPE="postgres")
        POSTGRES_HOST: PostgreSQL host
        POSTGRES_PORT: PostgreSQL port
        POSTGRES_DB: PostgreSQL database name
        POSTGRES_USER: PostgreSQL username
        POSTGRES_PASSWORD: PostgreSQL password
        
        # MongoDB settings (when DB_TYPE="mongodb")
        MONGODB_URI: MongoDB connection URI
        MONGODB_DB: MongoDB database name
    
    Returns:
        DatabaseRepository: An instance of the configured database repository
    
    Examples:
        >>> # Uses settings from environment variables or .env file
        >>> db = get_database_repository()
    """
    db_type = settings.db_type.lower()
    
    if db_type == "in_memory":
        return InMemoryRepository()
    elif db_type == "postgres":
        # Future implementation for PostgreSQL
        # connection_string = (
        #     f"postgresql://{settings.postgres_user}:"
        #     f"{settings.postgres_password}@"
        #     f"{settings.postgres_host}:{settings.postgres_port}/"
        #     f"{settings.postgres_db}"
        # )
        # return PostgresRepository(connection_string)
        raise NotImplementedError("PostgreSQL support not yet implemented")
    elif db_type == "mongodb":
        # Future implementation for MongoDB
        # return MongoDBRepository(
        #     uri=settings.mongodb_uri,
        #     database=settings.mongodb_db
        # )
        raise NotImplementedError("MongoDB support not yet implemented")
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
