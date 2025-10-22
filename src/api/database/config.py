"""Database configuration and initialization.

This module handles database selection and initialization based on configuration
file settings. It provides a factory function that returns the appropriate
database repository implementation.
"""

import tomllib
from pathlib import Path
from .base import DatabaseRepository
from .in_memory import InMemoryRepository


def _load_config() -> dict:
    """Load configuration from config.toml file.
    
    Returns:
        dict: Configuration dictionary
        
    Raises:
        FileNotFoundError: If config.toml is not found
        tomllib.TOMLDecodeError: If config.toml is invalid
    """
    # Look for config.toml in the project root
    config_path = Path(__file__).parent.parent.parent.parent / "config.toml"
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            "Please create a config.toml file in the project root."
        )
    
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def get_database_repository() -> DatabaseRepository:
    """Get the configured database repository instance.
    
    This function determines which database implementation to use based on
    the configuration file (config.toml). It can be extended to support
    multiple database backends (PostgreSQL, MongoDB, etc.).
    
    Configuration (config.toml):
        [database]
        type = "in_memory"  # Options: "in_memory", "postgres", "mongodb"
        
        # PostgreSQL configuration (when type = "postgres")
        [database.postgres]
        host = "localhost"
        port = 5432
        database = "ledger"
        user = "ledger_user"
        password = "your_password"
        
        # MongoDB configuration (when type = "mongodb")
        [database.mongodb]
        uri = "mongodb://localhost:27017"
        database = "ledger"
    
    Returns:
        DatabaseRepository: An instance of the configured database repository
    
    Examples:
        >>> # Uses configuration from config.toml
        >>> db = get_database_repository()
    """
    config = _load_config()
    db_config = config.get("database", {})
    db_type = db_config.get("type", "in_memory").lower()
    
    if db_type == "in_memory":
        return InMemoryRepository()
    elif db_type == "postgres":
        # Future implementation for PostgreSQL
        # postgres_config = db_config.get("postgres", {})
        # connection_string = (
        #     f"postgresql://{postgres_config.get('user')}:"
        #     f"{postgres_config.get('password')}@"
        #     f"{postgres_config.get('host')}:{postgres_config.get('port')}/"
        #     f"{postgres_config.get('database')}"
        # )
        # return PostgresRepository(connection_string)
        raise NotImplementedError("PostgreSQL support not yet implemented")
    elif db_type == "mongodb":
        # Future implementation for MongoDB
        # mongodb_config = db_config.get("mongodb", {})
        # return MongoDBRepository(
        #     uri=mongodb_config.get("uri"),
        #     database=mongodb_config.get("database")
        # )
        raise NotImplementedError("MongoDB support not yet implemented")
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
