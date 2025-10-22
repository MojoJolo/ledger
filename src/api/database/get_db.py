"""Database connection module for dependency injection."""


class DatabaseConnection:
    """Simple database connection class for demonstration."""

    def __init__(self):
        self.connected = False

    def connect(self):
        """Establish database connection."""
        self.connected = True
        return self

    def disconnect(self):
        """Close database connection."""
        self.connected = False


# Global database instance
_db_instance = None


def get_database():
    """Get or create database connection instance.

    This function provides dependency injection for FastAPI endpoints.

    Returns:
        DatabaseConnection: Active database connection instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnection().connect()
    return _db_instance


def reset_database():
    """Reset the database connection (useful for testing)."""
    global _db_instance
    if _db_instance:
        _db_instance.disconnect()
    _db_instance = None
