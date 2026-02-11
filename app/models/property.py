"""Property database model."""

from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from app.database.session import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), unique=True, nullable=False, index=True)
    owner_name = Column(String(255))
    city = Column(String(100), index=True)
    zip_code = Column(String(10))
    county = Column(String(50), index=True)
    
    assessed_value = Column(Numeric(12, 2))
    market_value = Column(Numeric(12, 2))
    
    square_feet = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Numeric(3, 1))
    year_built = Column(Integer)
    property_type = Column(String(50))
    
    last_sale_date = Column(Date)
    last_sale_price = Column(Numeric(12, 2))
    
    tax_amount = Column(Numeric(10, 2))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Property(address='{self.address}', city='{self.city}')>"
