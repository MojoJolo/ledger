# Database Layer Documentation

## Overview

The ledger system now includes a **DB-agnostic layer** that separates business logic from database implementation. This design allows you to switch between different database backends (in-memory, PostgreSQL, MongoDB, etc.) without changing the API code.

## Architecture

The database layer follows the **Repository Pattern**, which provides:

1. **Abstraction**: A common interface for all database operations
2. **Flexibility**: Easy switching between different database implementations
3. **Testability**: Mock database implementations for testing
4. **Maintainability**: Clear separation of concerns

### Structure

```
src/api/database/
├── __init__.py          # Module exports
├── base.py              # Abstract DatabaseRepository interface
└── in_memory.py         # In-memory implementation
```

## DatabaseRepository Interface

The `DatabaseRepository` abstract base class defines the contract that all database implementations must follow:

### Methods

#### `save_transaction(transaction: Transaction) -> Transaction`
Saves a complete transaction with all its entries to the database.

**Parameters:**
- `transaction`: A validated `Transaction` object

**Returns:**
- The saved `Transaction` object

**Example:**
```python
transaction = Transaction(
    txn_id="txn_001",
    ledger_id="ledger_001",
    effective_at=datetime.now(timezone.utc),
    entries=[...]
)
saved_txn = db_repository.save_transaction(transaction)
```

#### `get_transaction(txn_id: str) -> Transaction | None`
Retrieves a transaction by its ID.

**Parameters:**
- `txn_id`: Transaction ID to retrieve

**Returns:**
- `Transaction` object if found, `None` otherwise

**Example:**
```python
transaction = db_repository.get_transaction("txn_001")
if transaction is None:
    print("Transaction not found")
```

#### `save_entry(entry: Entry, txn_id: str) -> Entry`
Saves a single entry associated with a transaction.

**Parameters:**
- `entry`: An `Entry` object
- `txn_id`: The transaction ID this entry belongs to

**Returns:**
- The saved `Entry` object

**Note:** This method is typically used for internal operations. Use `save_transaction()` to save complete transactions.

#### `get_entries_by_transaction(txn_id: str) -> list[Entry]`
Retrieves all entries for a specific transaction.

**Parameters:**
- `txn_id`: Transaction ID

**Returns:**
- List of `Entry` objects (empty list if none found)

**Example:**
```python
entries = db_repository.get_entries_by_transaction("txn_001")
print(f"Found {len(entries)} entries")
```

## Current Implementation: InMemoryRepository

The `InMemoryRepository` is the default implementation that stores all data in memory using Python dictionaries.

### Characteristics

- ✅ **Fast**: No I/O operations, all data in RAM
- ✅ **Simple**: No external dependencies
- ❌ **Non-persistent**: Data is lost when application stops
- ❌ **Not scalable**: Limited by available RAM
- ❌ **Single-process**: Data not shared across processes

### Storage Structure

```python
self._transactions: dict[str, Transaction]  # txn_id -> Transaction
self._entries: dict[str, list[Entry]]       # txn_id -> [Entry, ...]
```

### Use Cases

The in-memory implementation is ideal for:
- Development and testing
- Proof-of-concepts
- Demo applications
- Temporary data that doesn't need persistence

## Usage in API

The database layer is integrated into the FastAPI application:

```python
from api.database import InMemoryRepository

# Initialize on app startup
db_repository = InMemoryRepository()

@app.post("/ledger/transaction/create")
def insert_entry(transactionRequest: TransactionRequest):
    # ... validation code ...
    
    # Save using DB-agnostic layer
    saved_transaction = db_repository.save_transaction(transaction)
    return saved_transaction

@app.get("/ledger/transaction/{txn_id}")
def get_transaction(txn_id: str):
    transaction = db_repository.get_transaction(txn_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
```

## Adding New Database Implementations

To add support for a new database (e.g., PostgreSQL, MongoDB):

1. **Create a new file** in `src/api/database/` (e.g., `postgres.py`)

2. **Implement the DatabaseRepository interface:**

```python
from api.database.base import DatabaseRepository
from api.models import Transaction, Entry

class PostgresRepository(DatabaseRepository):
    def __init__(self, connection_string: str):
        # Initialize database connection
        self.conn = create_postgres_connection(connection_string)
    
    def save_transaction(self, transaction: Transaction) -> Transaction:
        # Implement PostgreSQL-specific logic
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (txn_id, ledger_id, effective_at) VALUES (%s, %s, %s)",
            (transaction.txn_id, transaction.ledger_id, transaction.effective_at)
        )
        
        for entry in transaction.entries:
            cursor.execute(
                "INSERT INTO entries (txn_id, account_id, amount, ...) VALUES (%s, %s, %s, ...)",
                (transaction.txn_id, entry.account_id, entry.amount, ...)
            )
        
        self.conn.commit()
        return transaction
    
    def get_transaction(self, txn_id: str) -> Transaction | None:
        # Implement PostgreSQL-specific retrieval
        # ...
```

3. **Export the new implementation** in `src/api/database/__init__.py`:

```python
from .postgres import PostgresRepository

__all__ = [
    "DatabaseRepository",
    "InMemoryRepository",
    "PostgresRepository",  # Add new implementation
]
```

4. **Update main.py to use the new implementation:**

```python
# Change from:
db_repository = InMemoryRepository()

# To:
db_repository = PostgresRepository(connection_string="postgresql://...")
```

## Best Practices

1. **Always use the abstract interface**: Write code against `DatabaseRepository`, not specific implementations
2. **Validate before saving**: Use Pydantic models to validate data before calling database methods
3. **Handle errors**: Catch database-specific exceptions and convert them to appropriate HTTP responses
4. **Use dependency injection**: Pass the repository instance as a dependency for better testability

## Example: Switching Implementations

```python
import os
from api.database import InMemoryRepository, PostgresRepository

# Choose implementation based on environment
if os.getenv("ENV") == "production":
    db_repository = PostgresRepository(
        connection_string=os.getenv("DATABASE_URL")
    )
else:
    db_repository = InMemoryRepository()
```

## Testing with Mock Repository

For testing, you can create a mock implementation:

```python
class MockRepository(DatabaseRepository):
    def __init__(self):
        self.saved_transactions = []
    
    def save_transaction(self, transaction: Transaction) -> Transaction:
        self.saved_transactions.append(transaction)
        return transaction
    
    # ... implement other methods ...

# In tests
def test_transaction_creation():
    mock_db = MockRepository()
    # ... test code ...
    assert len(mock_db.saved_transactions) == 1
```

## Future Enhancements

Potential improvements to the database layer:

1. **Add more methods**: `list_transactions()`, `update_transaction()`, `delete_transaction()`
2. **Add filtering**: Query transactions by date range, ledger_id, etc.
3. **Add pagination**: Support for large result sets
4. **Add caching**: Layer Redis or similar between API and database
5. **Add connection pooling**: For database implementations
6. **Add transaction support**: Rollback on errors
7. **Add audit logging**: Track who/when data was modified
