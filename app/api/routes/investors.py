"""Investor finder API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.services.investor_finder import InvestorFinderService
from pydantic import BaseModel
import csv
import io

router = APIRouter()

class InvestorResponse(BaseModel):
    owner_name: str
    property_count: int
    total_portfolio_value: float
    avg_property_value: float
    cities: str

class PropertySummary(BaseModel):
    address: str
    city: Optional[str]
    zip_code: Optional[str]
    assessed_value: float
    square_feet: Optional[int]
    year_built: Optional[int]

class InvestorDetailResponse(BaseModel):
    owner_name: str
    property_count: int
    total_portfolio_value: float
    avg_property_value: float
    cities: str
    properties: List[PropertySummary]

@router.get("/", response_model=List[InvestorResponse])
def get_investors(
    min_properties: int = Query(5, ge=1, le=100, description="Minimum number of properties owned"),
    max_properties: int = Query(50, ge=1, le=1000, description="Maximum number of properties owned"),
    county: Optional[str] = Query(None, description="Filter by county (Dallas or Collin)"),
    exclude_corporations: bool = Query(True, description="Exclude utilities, banks, government entities"),
    investor_type: str = Query("all", enum=["all", "individual", "company"], description="Type of investor to return"),
    min_avg_value: Optional[float] = Query(None, description="Minimum average property value"),
    max_avg_value: Optional[float] = Query(None, description="Maximum average property value"),
    cities: Optional[str] = Query(None, description="Comma-separated list of cities (e.g., 'PLANO,FRISCO,ALLEN')"),
    min_cities: Optional[int] = Query(None, ge=1, description="Minimum number of different cities owned in"),
    owner_state: Optional[str] = Query(None, description="Filter by owner state (TX, CA, etc.) or use !TX for non-Texas"),
    db: Session = Depends(get_db)
):
    # Parse cities if provided
    city_list = [c.strip() for c in cities.split(',')] if cities else None
    
    service = InvestorFinderService(db)
    investors = service.find_investors(
        min_properties=min_properties,
        max_properties=max_properties,
        county=county,
        exclude_corporations=exclude_corporations,
        investor_type=investor_type,
        min_avg_value=min_avg_value,
        max_avg_value=max_avg_value,
        cities=city_list,
        min_cities=min_cities,
        owner_state=owner_state
    )
    return investors

@router.get("/{owner_name}", response_model=InvestorDetailResponse)
def get_investor_detail(
    owner_name: str,
    county: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = InvestorFinderService(db)
    investor = service.get_investor_summary(owner_name, county)
    
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    
    return investor

@router.get("/{owner_name}/export")
def export_investor_properties(
    owner_name: str,
    county: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = InvestorFinderService(db)
    properties = service.get_investor_properties(owner_name, county)
    
    if not properties:
        raise HTTPException(status_code=404, detail="Investor not found or has no properties")
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['owner_name', 'address', 'city', 'zip_code', 'county', 'assessed_value', 'square_feet', 'year_built'])
    
    # Write property rows
    for prop in properties:
        writer.writerow([
            owner_name,
            prop['address'],
            prop['city'] or '',
            prop['zip_code'] or '',
            county or '',
            prop['assessed_value'],
            prop['square_feet'] or '',
            prop['year_built'] or ''
        ])
    
    # Prepare file for download
    output.seek(0)
    
    # Create filename
    safe_name = owner_name.replace(' ', '_').replace('&', 'and')
    filename = f"{safe_name}_properties.csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/stats/summary")
def get_investor_stats(
    min_properties: int = Query(5, ge=1),
    county: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = InvestorFinderService(db)
    investors = service.find_investors(
        min_properties=min_properties,
        max_properties=1000,
        county=county,
        exclude_corporations=True
    )
    
    total_investors = len(investors)
    total_properties = sum(i['property_count'] for i in investors)
    total_value = sum(i['total_portfolio_value'] for i in investors)
    
    return {
        "total_investors": total_investors,
        "total_properties_owned": total_properties,
        "total_portfolio_value": total_value,
        "avg_properties_per_investor": total_properties / total_investors if total_investors > 0 else 0
    }
