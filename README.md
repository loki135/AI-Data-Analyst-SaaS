# AI Data Analyst SaaS

AI-powered data analysis platform. Upload datasets and get instant insights via natural language queries.

## Architecture

```
├── backend/          # FastAPI (Python 3.11+)
│   ├── app/
│   │   ├── api/      # Route handlers (thin — delegate to services)
│   │   ├── core/     # Shared utilities: config, exceptions, response, security, database
│   │   ├── models/   # SQLAlchemy models (inherit shared BaseModel)
│   │   ├── services/ # Business logic: AI service, dataset processing
│   │   └── utils/    # Reusable helpers: pagination, validators
│   └── tests/
├── frontend/         # Next.js 14 (TypeScript)
│   └── src/
│       ├── app/          # Pages (App Router)
│       ├── components/ui # Shared UI components
│       ├── hooks/        # Shared React hooks (useApi, useAuth)
│       ├── lib/          # Shared logic: API client, validators, formatters
│       └── types/        # Shared TypeScript types
└── docker-compose.yml
```

## Shared Utilities (Anti-Duplication Design)

### Backend (`backend/app/core/` & `backend/app/utils/`)

| Module | Purpose |
|--------|---------|
| `core/exceptions.py` | Hierarchy of typed errors with a single error handler — no duplicated try/catch formatting |
| `core/response.py` | `ok()` and `paginated()` helpers ensure every endpoint returns a consistent envelope |
| `core/database.py` | Single async session factory used by all routes via dependency injection |
| `core/security.py` | JWT + password hashing in one place — auth logic never repeated across routes |
| `utils/pagination.py` | Reusable `PaginationParams` dependency for all list endpoints |
| `utils/validators.py` | Email, password, and general validation — shared by auth and user routes |
| `services/ai_service.py` | AI provider abstraction — swap providers by changing one module |
| `services/dataset_service.py` | File parsing/metadata extraction — reused by upload, preview, and analysis |

### Frontend (`frontend/src/lib/` & `frontend/src/hooks/`)

| Module | Purpose |
|--------|---------|
| `lib/api-client.ts` | Single fetch wrapper with auth injection and error parsing |
| `lib/validators.ts` | Client-side validation mirroring backend rules |
| `lib/formatters.ts` | Date, number, file size formatting — used across all views |
| `hooks/use-api.ts` | Generic loading/error/data state management hook |
| `hooks/use-auth.ts` | Centralized auth state and token management |
| `components/ui/*` | Shared UI primitives (ErrorMessage, LoadingSpinner, Pagination) |
| `types/api.ts` | TypeScript interfaces matching the backend response envelope |

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+ (or use Docker)

### Quick Start (Docker)

```bash
docker compose up -d
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### Running Tests

```bash
cd backend && pytest
cd frontend && npm run lint && npm run typecheck
```
