# ledger

A Python project structured with [uv](https://github.com/astral-sh/uv) as the dependency manager.

## Project Structure

```
ledger/
├── src/
│   └── ledger/
│       └── __init__.py
├── pyproject.toml
├── uv.lock
└── .python-version
```

## Setup

This project uses `uv` for dependency management. To get started:

1. Install uv (if not already installed):
   ```bash
   pip install uv
   ```

2. Sync dependencies:
   ```bash
   uv sync
   ```

## Usage

Run the ledger command:
```bash
uv run ledger
```

Or use it as a Python module:
```bash
uv run python -c "import ledger; ledger.main()"
```

## Development

- Add dependencies: `uv add <package-name>`
- Remove dependencies: `uv remove <package-name>`
- Run Python scripts: `uv run python <script.py>`
- Run commands in the virtual environment: `uv run <command>`

## Python Version

This project requires Python >=3.12 as specified in `pyproject.toml`.