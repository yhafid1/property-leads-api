# property-leads-api

This project was made to injest Dallas County and Collin County appraisal district CSV data, calculates property equity, scores wholesale leads, and expose a FastAPI REST interface for querying properties and managing the lead pipeline.

## What it does

County appraisal districts publish property data as CSV exports. This API reads those files, joins them by account number, and loads the results into PostgreSQL. From there, an equity calculator estimates remaining mortgage balance (using last sale price and year built) and flags high-equity properties as leads. A separate investor finder identifies properties held by LLCs and non-owner-occupied addresses.

Three API routers:

- `/api/properties` — query the full property database with filters
- `/api/leads` — list high-equity leads, get by ID, patch status and notes, and pull a summary aggregation
- `/api/investors` — investor-owned property lookup

## Tech stack

- Python 3.10+, FastAPI, uvicorn
- SQLAlchemy + psycopg2 (PostgreSQL)
- Docker Compose
- County CSV files as the data source (Dallas and Collin County)

## Running locally

**Step 1:** Download the county CSV files per the instructions in `DATA_SETUP.md`. You need `Account_Info.csv`, `Account_Appraisal_Year.csv`, and `Res_Detail.csv` from Dallas County.

**Step 2:** Set up your environment:

```bash
git clone https://github.com/yhafid1/property-leads-api.git
cd property-leads-api
cp .env.example .env
# fill in your DATABASE_URL
docker compose up --build
```

The API starts at `http://localhost:8000`. Interactive docs are at `/docs`.

**Step 3:** Run the scrapers to populate the database:

```bash
docker compose exec api python -m app.scrapers.dallas_scraper
docker compose exec api python -m app.scrapers.collin_scraper
```

**Without Docker:**

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Data model

The `properties` table has 15 fields including assessed value, market value, last sale price, last sale date, owner name, and square footage. The `leads` table adds equity score, status (new/contacted/qualified/closed), and notes. Each lead record links back to its source property.

## The problem it solves

Real estate wholesalers in DFW spend hours manually pulling public records and cross-referencing spreadsheets to find motivated sellers. The goal is to automate the data collection and scoring so you can filter a 100,000-property dataset down to 50 high-equity leads in seconds.
