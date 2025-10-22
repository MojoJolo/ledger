import uuid
from fastapi import FastAPI, Request

from api.models import TransactionRequest, Transaction, Entry


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


# @app.post("/entry/insert")
# def insert_entry(request: EntryRequest):
#     return request


@app.post("/ledger/transaction/create")
def insert_entry(transactionRequest: TransactionRequest):
    # Map EntryRequest list to Entry list
    entries = [
        Entry(
            account_id=entry_req.account_id,
            amount=entry_req.amount,
            decimal_places=entry_req.decimal_places,
            currency=entry_req.currency,
            metadata=entry_req.metadata,
        )
        for entry_req in transactionRequest.entries
    ]

    # Map TransactionRequest to Transaction
    transaction = Transaction(
        txn_id=transactionRequest.txn_id,
        ledger_id=transactionRequest.ledger_id,
        effective_at=transactionRequest.effective_at,
        entries=entries,
    )

    return transaction
