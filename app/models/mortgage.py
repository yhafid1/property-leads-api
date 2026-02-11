"""Mortgage database model."""

from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.session import Base

class Mortgage(Base):
    __tablename__ = "mortgages"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False, index=True)
    
    loan_amount = Column(Numeric(12, 2))
    loan_date = Column(Date)
    lender = Column(String(255))
    estimated_balance = Column(Numeric(12, 2))
    interest_rate = Column(Numeric(5, 2))
    loan_term = Column(Integer)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    property = relationship("Property", backref="mortgages")

    def __repr__(self):
        return f"<Mortgage(property_id={self.property_id}, loan_amount={self.loan_amount})>"
