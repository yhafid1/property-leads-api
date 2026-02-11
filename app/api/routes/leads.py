"""Lead API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database.session import get_db
from app.schemas import LeadResponse, LeadWithProperty, LeadUpdate
from app.models import HighEquityLead

router = APIRouter()

@router.get("/", response_model=List[LeadWithProperty])
def get_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    min_equity: Optional[float] = None,
    city: Optional[str] = None,
    county: Optional[str] = None,
    min_motivation: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(HighEquityLead)
    
    if min_equity:
        query = query.filter(HighEquityLead.equity_amount >= min_equity)
    if min_motivation:
        query = query.filter(HighEquityLead.motivation_score >= min_motivation)
    if status:
        query = query.filter(HighEquityLead.lead_status == status)
    
    leads = query.offset(skip).limit(limit).all()
    return leads

@router.get("/{lead_id}", response_model=LeadWithProperty)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(HighEquityLead).filter(HighEquityLead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.patch("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: int, lead_update: LeadUpdate, db: Session = Depends(get_db)):
    lead = db.query(HighEquityLead).filter(HighEquityLead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    for key, value in lead_update.model_dump(exclude_unset=True).items():
        setattr(lead, key, value)
    
    db.commit()
    db.refresh(lead)
    return lead

@router.get("/stats/summary")
def get_lead_stats(db: Session = Depends(get_db)):
    total_leads = db.query(HighEquityLead).count()
    total_equity = db.query(func.sum(HighEquityLead.equity_amount)).scalar() or 0
    avg_motivation = db.query(func.avg(HighEquityLead.motivation_score)).scalar() or 0
    
    return {
        "total_leads": total_leads,
        "total_equity": float(total_equity),
        "average_motivation_score": float(avg_motivation)
    }
