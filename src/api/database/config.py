"""Database configuration and initialization.

This module handles database selection and initialization based on environment
configuration. It provides a factory function that returns the appropriate
database repository implementation.
"""

import os
from .base import DatabaseRepository
from .in_memory import InMemoryRepository


def get_database_repository() -> DatabaseRepository:
    """Get the configured database repository instance.
    
    This function determines which database implementation to use based on
    environment variables or configuration. It can be extended to support
    multiple database backends (PostgreSQL, MongoDB, etc.).
    
    Environment Variables:
        DB_TYPE: Type of database to use (default: "in_memory")
            - "in_memory": Use in-memory storage
            - "postgres": Use PostgreSQL (requires implementation)
            - "mongodb": Use MongoDB (requires implementation)
    
    Returns:
        DatabaseRepository: An instance of the configured database repository
    
    Examples:
        >>> # Use default in-memory database
        >>> db = get_database_repository()
        
        >>> # Use PostgreSQL (when implemented)
        >>> os.environ["DB_TYPE"] = "postgres"
        >>> db = get_database_repository()
    """
    db_type = os.getenv("DB_TYPE", "in_memory").lower()
    
    if db_type == "in_memory":
        return InMemoryRepository()
    elif db_type == "postgres":
        # Future implementation for PostgreSQL
        # connection_string = os.getenv("DATABASE_URL")
        # return PostgresRepository(connection_string)
        raise NotImplementedError("PostgreSQL support not yet implemented")
    elif db_type == "mongodb":
        # Future implementation for MongoDB
        # connection_string = os.getenv("MONGODB_URL")
        # return MongoDBRepository(connection_string)
        raise NotImplementedError("MongoDB support not yet implemented")
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
