import uuid
from fastapi import FastAPI, Request

from api.models import TransactionRequest


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
    return transactionRequest
