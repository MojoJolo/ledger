import logging
import sys
from contextvars import ContextVar

# Context variable to store trace_id across async contexts
trace_id_context: ContextVar[str | None] = ContextVar("trace_id", default=None)


class TraceIdFilter(logging.Filter):
    """Custom filter to add trace_id to log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        trace_id = trace_id_context.get()
        record.trace_id = trace_id if trace_id else "no-trace-id"
        return True


def setup_logging() -> None:
    """Configure logging with trace_id support."""
    # Create formatter with trace_id
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - trace_id=%(trace_id)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(TraceIdFilter())

    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name."""
    return logging.getLogger(name)


def set_trace_id(trace_id: str) -> None:
    """Set the trace_id for the current context."""
    trace_id_context.set(trace_id)


def get_trace_id() -> str | None:
    """Get the trace_id from the current context."""
    return trace_id_context.get()
