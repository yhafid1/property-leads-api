"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.routes import properties, leads, investors
from app.api.rate_limit import limiter
from app.config import settings
from app.database.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DFW Property Leads API",
    description="Real estate investment property aggregation and lead generation API for Dallas-Fort Worth",
    version="1.0.0"
)

# Rate limiting (per API key when present, otherwise per client IP).
# Backed by Redis (same instance used for Celery) when reachable, with an
# in-memory fallback for local dev without Redis running.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(properties.router, prefix="/api/properties", tags=["Properties"])
app.include_router(leads.router, prefix="/api/leads", tags=["Leads"])
app.include_router(investors.router, prefix="/api/investors", tags=["Investors"])

@app.get("/")
def root():
    return {
        "name": "DFW Property Leads API",
        "version": "1.0.0",
        "description": "Real estate investment property aggregation and lead generation"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
