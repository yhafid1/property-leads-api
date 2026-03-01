# Property Leads API

A real estate investment property aggregation and lead generation API for the dfw metroplex. Automates the discovery of high-equity wholesale opportunities by aggregating county appraisal data and identifying motivated sellers.

## Features

- Automated property data aggregation from Dallas and Collin County appraisal districts (for now)
- High-equity lead identification and scoring
- RESTful API for querying properties and leads
- Property valuation integration
- Equity calculation with mortgage estimation
- Lead status tracking and notes

## Prerequisites

- Python 3.10+
- Docker Desktop
- Git

## Setup Instructions

### 1. Clone Repository

### 2. Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start Databases

```bash
docker-compose up -d
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

#License
MIT
