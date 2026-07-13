# Property Leads API

A REST API for the DFW real estate market. It pulls county appraisal data for Dallas and Collin County, estimates equity on each property, and scores leads by how likely the owner is to sell.

![Swagger docs](docs/property-api-01-swagger.png)

## Features

- Property data aggregation from Dallas and Collin County appraisal districts
- Equity calculation with mortgage estimation, plus a motivation score for ranking leads
- Investor-portfolio lookup (properties grouped by owner)
- API key auth and per-key rate limiting on every endpoint
- Lead status tracking and notes

## Tech stack

FastAPI, SQLAlchemy, PostgreSQL, Redis (rate limiting), Celery

## Setup

```bash
python -m pip install -r requirements.txt
docker-compose up -d          # Postgres + Redis
cp .env.example .env          # defaults work for local dev
uvicorn app.main:app --reload
```

API: `http://localhost:8000` | Docs: `http://localhost:8000/docs` | Health: `http://localhost:8000/health`

To populate the database with real property data, see `DATA_SETUP.md` for downloading county CSV files.

## Authentication

Every `/api/*` route requires an `X-API-Key` header matching a key from the `API_KEYS` env var (comma-separated for multiple keys). Generate one with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Requests are also rate-limited (60/min per key by default, set via `RATE_LIMIT_PER_MINUTE`). The limiter uses Redis when it's reachable and falls back to in-memory tracking if not.

```bash
# no key -> 401
curl http://localhost:8000/api/leads/

# valid key -> 200
curl -H "X-API-Key: your-key-here" http://localhost:8000/api/leads/
```

CORS is restricted to an allowlist via `ALLOWED_ORIGINS` (comma-separated, no wildcard).

## API Endpoints

**Properties**
- `GET /api/properties/`: list properties
- `GET /api/properties/{id}`: get by ID
- `GET /api/properties/address/{address}`: get by address

**Leads**
- `GET /api/leads/`: list high-equity leads
- `GET /api/leads/{id}`: get by ID
- `PATCH /api/leads/{id}`: update status/notes
- `GET /api/leads/stats/summary`: lead stats

**Investors**
- `GET /api/investors/`: properties grouped by owner
- `GET /api/investors/{owner_name}`: one investor's portfolio
- `GET /api/investors/{owner_name}/export`: export as CSV
- `GET /api/investors/stats/summary`: investor stats

## License

MIT
