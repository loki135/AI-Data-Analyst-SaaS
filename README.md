# AI Data Analyst SaaS

AI-powered data analysis platform built with FastAPI.

## Project Structure

```
app/
├── auth/            # Authentication & user management
├── data_ingestion/  # File parsing, validation, upload handling
├── analysis/        # Descriptive statistics, correlations, outlier detection
├── visualization/   # Chart specification builders
├── reports/         # Report generation & templates
├── config.py        # Application settings
└── main.py          # FastAPI entry-point
```

## Quick Start

```bash
# Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies (including dev tools)
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Lint & type-check
ruff check .
mypy app/
```

## API

```bash
uvicorn app.main:app --reload
```

Health check: `GET /health`
