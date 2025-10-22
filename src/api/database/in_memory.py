from api.models import Transaction, Entry
from .base import DatabaseRepository
from api.logging_config import get_logger

logger = get_logger(__name__)


class InMemoryRepository(DatabaseRepository):
    def __init__(self):
        self._transactions: dict[str, Transaction] = {}
        self._entries: dict[str, list[Entry]] = {}
        logger.info("InMemoryRepository initialized")

    def save_transaction(self, transaction: Transaction) -> Transaction:
        logger.info(f"Saving transaction: txn_id={transaction.txn_id}, ledger_id={transaction.ledger_id}")
        
        # Store the transaction
        self._transactions[transaction.txn_id] = transaction

        # Store entries associated with this transaction
        self._entries[transaction.txn_id] = transaction.entries.copy()
        
        logger.info(f"Transaction saved successfully: txn_id={transaction.txn_id}, entries_count={len(transaction.entries)}")
        return transaction

    def get_transaction(self, txn_id: str) -> Transaction | None:
        """Retrieve a transaction by ID.

        Args:
            txn_id: Transaction ID to retrieve

        Returns:
            Transaction object if found, None otherwise
        """
        logger.info(f"Retrieving transaction: txn_id={txn_id}")
        transaction = self._transactions.get(txn_id)
        if transaction:
            logger.info(f"Transaction found: txn_id={txn_id}")
        else:
            logger.warning(f"Transaction not found: txn_id={txn_id}")
        return transaction

    def save_entry(self, entry: Entry, txn_id: str) -> Entry:
        logger.info(f"Saving entry for transaction: txn_id={txn_id}, account_id={entry.account_id}")
        
        if txn_id not in self._entries:
            self._entries[txn_id] = []

        self._entries[txn_id].append(entry)
        logger.info(f"Entry saved successfully: txn_id={txn_id}, account_id={entry.account_id}")
        return entry

    def get_entries_by_transaction(self, txn_id: str) -> list[Entry]:
        logger.info(f"Retrieving entries for transaction: txn_id={txn_id}")
        entries = self._entries.get(txn_id, [])
        logger.info(f"Retrieved {len(entries)} entries for transaction: txn_id={txn_id}")
        return entries
