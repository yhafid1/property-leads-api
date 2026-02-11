"""Lead API request and response schemas."""

from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import date, datetime
from typing import Optional
from app.schemas.property import PropertyResponse

class LeadBase(BaseModel):
    property_id: int
    equity_amount: Decimal
    equity_percentage: Decimal
    motivation_score: int
    lead_status: str = "new"
    notes: Optional[str] = None
    last_contacted: Optional[date] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    lead_status: Optional[str] = None
    notes: Optional[str] = None
    last_contacted: Optional[date] = None

class LeadResponse(LeadBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime

class LeadWithProperty(LeadResponse):
    property: PropertyResponse
