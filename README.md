# DFW Property Leads API

Real estate investment property aggregation and lead generation API for the dfw metroplex. Automates the discovery of high-equity wholesale opportunities by aggregating county appraisal data and identifying motivated sellers.

# Features

- Automated property data aggregation from Dallas and Collin County appraisal districts
- ID high-equity leads and score them
- RESTful API for querying properties and leads
- Property valuation 
- Equity calculation with mortgage estimation
- Lead status tracking and notes

# Tech Stack

- FastAPI - Modern Python web framework
- PostgreSQL - Property data storage
- Redis - Caching layer for comp results
- SQLAlchemy - ORM for database operations
- Docker - Containerized databases

# Prereqs

- Python 3.10+
- Docker Desktop
- Git


# Properties

- GET /api/properties - List all properties
- GET /api/properties/{id} - Get property by ID
- GET /api/properties/address/{address} - Get property by address

# Leads

- GET /api/leads - List high-equity leads
- GET /api/leads/{id} - Get lead by ID
- PATCH /api/leads/{id} - Update lead status/notes
- GET /api/leads/stats/summary - Lead statistics



# Database Commands

- View Logs

docker-compose logs -f postgres


- Connect to Database

docker exec -it property_leads_db psql -U postgres -d property_leads


- Stop Databases

docker-compose down


- Reset Database

docker-compose down -v
docker-compose up -d


# License

Proprietary - All Rights Reserved
