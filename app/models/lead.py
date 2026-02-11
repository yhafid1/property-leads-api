"""High equity lead database model."""

from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database.session import Base

class HighEquityLead(Base):
    __tablename__ = "high_equity_leads"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False, unique=True, index=True)
    
    equity_amount = Column(Numeric(12, 2), index=True)
    equity_percentage = Column(Numeric(5, 2))
    motivation_score = Column(Integer, index=True)
    
    lead_status = Column(String(50), default="new", index=True)
    notes = Column(Text)
    last_contacted = Column(Date)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    property = relationship("Property", backref="lead")

    def __repr__(self):
        return f"<HighEquityLead(property_id={self.property_id}, equity={self.equity_amount})>"
