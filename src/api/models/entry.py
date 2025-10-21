from datetime import datetime, timezone
from pydantic import BaseModel, Field


class EntryRequest(BaseModel):
    request_id: str
    ledger_id: str
    amount: int
    decimal_places: int
    currency: str
    metadata: str | None = None
    effective_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
