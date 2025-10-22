from abc import ABC, abstractmethod
from api.models import Transaction, Entry


class DatabaseRepository(ABC):
    """Abstract base class for database operations.
    
    This interface defines the contract for any database implementation,
    making the system DB-agnostic.
    """
    
    @abstractmethod
    def save_transaction(self, transaction: Transaction) -> Transaction:
        """Save a transaction with all its entries.
        
        Args:
            transaction: Transaction object to save
            
        Returns:
            The saved transaction object
        """
        pass
    
    @abstractmethod
    def get_transaction(self, txn_id: str) -> Transaction | None:
        """Retrieve a transaction by ID.
        
        Args:
            txn_id: Transaction ID to retrieve
            
        Returns:
            Transaction object if found, None otherwise
        """
        pass
    
    @abstractmethod
    def save_entry(self, entry: Entry, txn_id: str) -> Entry:
        """Save an entry associated with a transaction.
        
        Args:
            entry: Entry object to save
            txn_id: Transaction ID this entry belongs to
            
        Returns:
            The saved entry object
        """
        pass
    
    @abstractmethod
    def get_entries_by_transaction(self, txn_id: str) -> list[Entry]:
        """Retrieve all entries for a transaction.
        
        Args:
            txn_id: Transaction ID
            
        Returns:
            List of Entry objects for the transaction
        """
        pass
