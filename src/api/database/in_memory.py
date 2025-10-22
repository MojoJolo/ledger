from api.models import Transaction, Entry
from .base import DatabaseRepository


class InMemoryRepository(DatabaseRepository):
    """In-memory implementation of the database repository.
    
    This implementation stores all data in memory using dictionaries.
    Data is lost when the application stops.
    """
    
    def __init__(self):
        """Initialize empty in-memory storage."""
        self._transactions: dict[str, Transaction] = {}
        self._entries: dict[str, list[Entry]] = {}
    
    def save_transaction(self, transaction: Transaction) -> Transaction:
        """Save a transaction with all its entries.
        
        Args:
            transaction: Transaction object to save
            
        Returns:
            The saved transaction object
        """
        # Store the transaction
        self._transactions[transaction.txn_id] = transaction
        
        # Store entries associated with this transaction
        self._entries[transaction.txn_id] = transaction.entries.copy()
        
        return transaction
    
    def get_transaction(self, txn_id: str) -> Transaction | None:
        """Retrieve a transaction by ID.
        
        Args:
            txn_id: Transaction ID to retrieve
            
        Returns:
            Transaction object if found, None otherwise
        """
        return self._transactions.get(txn_id)
    
    def save_entry(self, entry: Entry, txn_id: str) -> Entry:
        """Save an entry associated with a transaction.
        
        Args:
            entry: Entry object to save
            txn_id: Transaction ID this entry belongs to
            
        Returns:
            The saved entry object
        """
        if txn_id not in self._entries:
            self._entries[txn_id] = []
        
        self._entries[txn_id].append(entry)
        return entry
    
    def get_entries_by_transaction(self, txn_id: str) -> list[Entry]:
        """Retrieve all entries for a transaction.
        
        Args:
            txn_id: Transaction ID
            
        Returns:
            List of Entry objects for the transaction
        """
        return self._entries.get(txn_id, [])
