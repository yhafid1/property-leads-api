"""Property API request and response schemas."""

from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import date, datetime
from typing import Optional

class PropertyBase(BaseModel):
    address: str
    owner_name: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    county: Optional[str] = None
    assessed_value: Optional[Decimal] = None
    market_value: Optional[Decimal] = None
    square_feet: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[Decimal] = None
    year_built: Optional[int] = None
    property_type: Optional[str] = None
    last_sale_date: Optional[date] = None
    last_sale_price: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    address: Optional[str] = None

class PropertyResponse(PropertyBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime
