from config import settings
from .base import DatabaseRepository
from .in_memory import InMemoryRepository
from api.logging_config import get_logger

logger = get_logger(__name__)


def get_database_repository() -> DatabaseRepository:
    db_type = settings.db_type.lower()
    logger.info(f"Initializing database repository: type={db_type}")

    if db_type == "in_memory":
        logger.info("Using InMemoryRepository")
        return InMemoryRepository()
    else:
        logger.error(f"Unsupported database type: {db_type}")
        raise ValueError(f"Unsupported database type: {db_type}")
