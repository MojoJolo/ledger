from pydantic import BaseModel


class Ledger(BaseModel):
    ledger_id: str
    name: str
    description: str | None = None
