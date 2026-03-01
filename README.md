# DFW Property Leads API

Real estate investment property aggregation and lead generation API for Dallas-Fort Worth metroplex. Automates the discovery of high-equity wholesale opportunities by aggregating county appraisal data and identifying motivated sellers.

## Features

- Automated property data aggregation from Dallas and Collin County appraisal districts
- High-equity lead identification and scoring
- RESTful API for querying properties and leads
- Property valuation integration
- Equity calculation with mortgage estimation
- Lead status tracking and notes

## Tech Stack

- FastAPI - Modern Python web framework
- PostgreSQL - Property data storage
- Redis - Caching layer for comp results
- SQLAlchemy - ORM for database operations
- Docker - Containerized databases

## Prerequisites

- Python 3.10+
- Docker Desktop
- Git

## Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd dfw-property-leads-api
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or if pip isn't recognized:

```bash
python -m pip install -r requirements.txt
```

### 3. Start Databases

```bash
docker-compose up -d
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379

Verify they're running:

```bash
docker ps
```

### 4. Configure Environment

```bash
cp .env.example .env
```

The defaults work for local development. Edit .env if needed.

### 5. Setup Data Files (Optional)

To populate the database with property data, see DATA_SETUP.md for instructions on downloading county CSV files.

### 6. Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API Endpoints

### Properties

- GET /api/properties - List all properties
- GET /api/properties/{id} - Get property by ID
- GET /api/properties/address/{address} - Get property by address

### Leads

- GET /api/leads - List high-equity leads
- GET /api/leads/{id} - Get lead by ID
- PATCH /api/leads/{id} - Update lead status/notes
- GET /api/leads/stats/summary - Lead statistics

## Project Structure

```
dfw-property-leads-api/
├── app/
│   ├── api/routes/          # API endpoint definitions
│   ├── models/              # SQLAlchemy database models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic layer
│   ├── scrapers/            # County data collection
│   ├── tasks/               # Background ETL jobs
│   ├── database/            # Database connection
│   ├── utils/               # Helper functions
│   ├── config.py            # Configuration management
│   └── main.py              # FastAPI application
├── tests/                   # Unit and integration tests
├── docker-compose.yml       # Database containers
├── requirements.txt         # Python dependencies
└── README.md
```

## Database Commands

### View Logs

```bash
docker-compose logs -f postgres
```

### Connect to Database

```bash
docker exec -it property_leads_db psql -U postgres -d property_leads
```

### Stop Databases

```bash
docker-compose down
```

### Reset Database

```bash
docker-compose down -v
docker-compose up -d
```

## License

MIT
