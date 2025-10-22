from config import settings
from .base import DatabaseRepository
from .in_memory import InMemoryRepository


def get_database_repository() -> DatabaseRepository:
    db_type = settings.db_type.lower()

    if db_type == "in_memory":
        return InMemoryRepository()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
