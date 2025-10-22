from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from .entry import Entry


class Transaction(BaseModel):
    txn_id: str = Field(pattern=r"^txn_.*")
    ledger_id: str
    effective_at: datetime | None = None
    entries: list[Entry] = Field(min_length=2)

    @field_validator('entries')
    @classmethod
    def validate_entries_balance(cls, entries: list[Entry]) -> list[Entry]:
        """Validate that entries balance per currency"""
        # Group entries by currency
        balances: dict[str, int] = {}

        for entry in entries:
            if entry.currency not in balances:
                balances[entry.currency] = 0
            balances[entry.currency] += entry.amount

        # Check that all currencies balance to zero
        for currency, balance in balances.items():
            if balance != 0:
                raise ValueError(
                    f"Entries for currency {currency} do not balance. "
                    f"Sum is {balance}, expected 0"
                )

        return entries
