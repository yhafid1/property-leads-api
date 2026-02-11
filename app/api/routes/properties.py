"""Property API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.schemas import PropertyResponse
from app.models import Property

router = APIRouter()

@router.get("/", response_model=List[PropertyResponse])
def get_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    city: Optional[str] = None,
    county: Optional[str] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Property)
    
    if city:
        query = query.filter(Property.city == city)
    if county:
        query = query.filter(Property.county == county)
    if min_value:
        query = query.filter(Property.market_value >= min_value)
    if max_value:
        query = query.filter(Property.market_value <= max_value)
    
    properties = query.offset(skip).limit(limit).all()
    return properties

@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router.get("/address/{address}", response_model=PropertyResponse)
def get_property_by_address(address: str, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.address == address).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property
