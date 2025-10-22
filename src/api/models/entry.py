from pydantic import BaseModel


class Entry(BaseModel):
    account_id: str
    amount: int
    decimal_places: int
    currency: str
    metadata: str | None = None
