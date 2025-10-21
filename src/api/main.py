import uuid
from datetime import datetime, timezone
from decimal import Decimal
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field


class EntryRequest(BaseModel):
    request_id: str
    amount: Decimal
    currency: str
    metadata: str | None = None
    effective_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


app = FastAPI()


@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    request.state.trace_id = trace_id
    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id

    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/entry/insert")
def insert_entry(request: EntryRequest):
    return {
        "request_id": request.request_id,
        "amount": request.amount,
        "currency": request.currency,
        "metadata": request.metadata,
        "effective_at": request.effective_at,
    }
