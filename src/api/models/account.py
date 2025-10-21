from pydantic import BaseModel


class Account(BaseModel):
    account_id: str
    ledger_id: str
    name: str
    currency: str
    description: str | None = None
