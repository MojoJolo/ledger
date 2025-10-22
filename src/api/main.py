import uuid
from fastapi import FastAPI, Request

from api.models import TransactionRequest, Transaction, Entry
from api.database import get_database_repository
from api.logging_config import setup_logging, set_trace_id, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)

app = FastAPI()

# Initialize the database repository using the configuration
db_repository = get_database_repository()

logger.info("Application started successfully")


@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    request.state.trace_id = trace_id
    
    # Set trace_id in logging context
    set_trace_id(trace_id)
    logger.info(f"Request started: {request.method} {request.url.path}")
    
    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    
    logger.info(f"Request completed: {request.method} {request.url.path} - Status: {response.status_code}")
    return response


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}


# @app.post("/entry/insert")
# def insert_entry(request: EntryRequest):
#     return request


@app.post("/ledger/transaction/create")
def insert_entry(transactionRequest: TransactionRequest):
    logger.info(f"Creating transaction: txn_id={transactionRequest.txn_id}, ledger_id={transactionRequest.ledger_id}")
    
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
    
    logger.debug(f"Mapped {len(entries)} entries for transaction {transactionRequest.txn_id}")

    # Map TransactionRequest to Transaction
    transaction = Transaction(
        txn_id=transactionRequest.txn_id,
        ledger_id=transactionRequest.ledger_id,
        effective_at=transactionRequest.effective_at,
        entries=entries,
    )

    # Save transaction using the DB-agnostic layer
    saved_transaction = db_repository.save_transaction(transaction)
    
    logger.info(f"Transaction created successfully: txn_id={saved_transaction.txn_id}")
    return saved_transaction
