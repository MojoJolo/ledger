from datetime import datetime, timezone
from decimal import Decimal
from pydantic import BaseModel, Field


class EntryRequest(BaseModel):
    request_id: str
    amount: Decimal
    currency: str
    metadata: str | None = None
    effective_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
