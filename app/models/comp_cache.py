"""Comp finder results cache database model."""

from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from app.database.session import Base

class CompCache(Base):
    __tablename__ = "comp_cache"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False, unique=True, index=True)
    
    estimated_value = Column(Numeric(12, 2))
    comp_properties = Column(JSON)
    confidence_score = Column(Numeric(3, 2))
    
    calculated_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, index=True)
    
    property = relationship("Property", backref="comp_cache")

    def __repr__(self):
        return f"<CompCache(property_id={self.property_id}, value={self.estimated_value})>"
