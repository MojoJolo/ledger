# Ledger Models Documentation

This document explains the data models for the ledger system.

## Overview

The ledger system consists of four main models:
- **Ledger**: A container for transactions and accounts
- **Account**: A named account belonging to a ledger
- **Transaction**: A financial transaction with multiple entries
- **Entry**: A single line item in a transaction

## Model Relationships

```
Ledger
  ├── Accounts (1 to many)
  └── Transactions (1 to many)
       └── Entries (1 to many, minimum 2)
           └── Account (each entry references one account)
```

## Models

### Ledger

A ledger is a container for organizing accounts and transactions.

```python
class Ledger(BaseModel):
    ledger_id: str
    name: str
    description: str | None = None
```

**Example:**
```python
ledger = Ledger(
    ledger_id="ledger_001",
    name="Main Ledger",
    description="Company's main accounting ledger"
)
```

### Account

An account belongs to a ledger and is used to categorize entries.

```python
class Account(BaseModel):
    account_id: str
    ledger_id: str  # Reference to parent ledger
    name: str
    currency: str
    description: str | None = None
```

**Example:**
```python
cash_account = Account(
    account_id="acc_001",
    ledger_id="ledger_001",
    name="Cash",
    currency="USD",
    description="Company cash account"
)

revenue_account = Account(
    account_id="acc_002",
    ledger_id="ledger_001",
    name="Revenue",
    currency="USD",
    description="Revenue from sales"
)
```

### Entry

An entry is a single line item in a transaction, referencing an account.

```python
class Entry(BaseModel):
    account_id: str  # Reference to an account
    amount: int  # Amount in smallest currency unit (e.g., cents)
    decimal_places: int  # Number of decimal places
    currency: str
    metadata: str | None = None
```

**Example:**
```python
entry1 = Entry(
    account_id="acc_001",
    amount=10000,  # $100.00 in cents
    decimal_places=2,
    currency="USD",
    metadata="Payment received"
)

entry2 = Entry(
    account_id="acc_002",
    amount=-10000,  # -$100.00 in cents
    decimal_places=2,
    currency="USD",
    metadata="Revenue recognition"
)
```

### Transaction

A transaction represents a financial transaction with multiple entries that must balance.

```python
class Transaction(BaseModel):
    txn_id: str  # Must start with "txn_"
    ledger_id: str  # Reference to parent ledger
    effective_at: datetime | None = None
    entries: list[Entry]  # Minimum 2 entries required
```

**Validation Rules:**
1. `txn_id` must start with "txn_"
2. Must have at least 2 entries
3. Entries must balance per currency (sum to zero)

**Example:**
```python
from datetime import datetime

transaction = Transaction(
    txn_id="txn_001",
    ledger_id="ledger_001",
    effective_at=datetime(2025, 10, 21, 12, 0, 0),
    entries=[
        Entry(
            account_id="acc_001",
            amount=10000,
            decimal_places=2,
            currency="USD"
        ),
        Entry(
            account_id="acc_002",
            amount=-10000,
            decimal_places=2,
            currency="USD"
        )
    ]
)
```

## Multi-Currency Transactions

Transactions can contain entries in multiple currencies, as long as each currency balances independently.

**Example:**
```python
multi_currency_txn = Transaction(
    txn_id="txn_002",
    ledger_id="ledger_001",
    entries=[
        # USD entries (must balance)
        Entry(account_id="acc_usd_1", amount=10000, decimal_places=2, currency="USD"),
        Entry(account_id="acc_usd_2", amount=-10000, decimal_places=2, currency="USD"),
        # EUR entries (must balance)
        Entry(account_id="acc_eur_1", amount=5000, decimal_places=2, currency="EUR"),
        Entry(account_id="acc_eur_2", amount=-5000, decimal_places=2, currency="EUR"),
    ]
)
```

## Error Handling

### Invalid Transaction ID
```python
# This will raise a validation error
Transaction(
    txn_id="invalid_001",  # Must start with "txn_"
    ledger_id="ledger_001",
    entries=[...]
)
# ValidationError: txn_id must match pattern ^txn_.*
```

### Unbalanced Entries
```python
# This will raise a validation error
Transaction(
    txn_id="txn_003",
    ledger_id="ledger_001",
    entries=[
        Entry(account_id="acc_001", amount=10000, decimal_places=2, currency="USD"),
        Entry(account_id="acc_002", amount=-5000, decimal_places=2, currency="USD"),
    ]
)
# ValueError: Entries for currency USD do not balance. Sum is 5000, expected 0
```

### Too Few Entries
```python
# This will raise a validation error
Transaction(
    txn_id="txn_004",
    ledger_id="ledger_001",
    entries=[
        Entry(account_id="acc_001", amount=0, decimal_places=2, currency="USD"),
    ]
)
# ValidationError: entries must have at least 2 items
```

## Usage in FastAPI

All models are available for import:

```python
from api.models import Account, Entry, Ledger, Transaction

@app.post("/transactions")
def create_transaction(transaction: Transaction):
    # Transaction is validated automatically
    return {"status": "created", "txn_id": transaction.txn_id}
```
