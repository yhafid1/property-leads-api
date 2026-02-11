"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import properties, leads
from app.database.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DFW Property Leads API",
    description="Real estate investment property aggregation and lead generation API for Dallas-Fort Worth",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(properties.router, prefix="/api/properties", tags=["Properties"])
app.include_router(leads.router, prefix="/api/leads", tags=["Leads"])

@app.get("/")
def root():
    return {
        "message": "DFW Property Leads API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
