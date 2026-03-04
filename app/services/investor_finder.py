"""Service to identify and analyze multi-property owners (investors)."""

from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from app.models import Property
from decimal import Decimal

class InvestorFinderService:
    def __init__(self, db: Session):
        self.db = db
    
    def find_investors(
        self,
        min_properties: int = 5,
        max_properties: int = 50,
        county: Optional[str] = None,
        exclude_corporations: bool = True,
        investor_type: str = "all",
        min_avg_value: Optional[float] = None,
        max_avg_value: Optional[float] = None,
        cities: Optional[List[str]] = None,
        min_cities: Optional[int] = None,
        owner_state: Optional[str] = None
    ) -> List[Dict]:
        query = self.db.query(
            func.upper(Property.owner_name).label('owner_name'),
            func.count(Property.id).label('property_count'),
            func.sum(Property.assessed_value).label('total_portfolio_value'),
            func.avg(Property.assessed_value).label('avg_property_value'),
            func.string_agg(func.distinct(Property.city), ', ').label('cities'),
            func.count(func.distinct(Property.city)).label('city_count')
        )
        
        # Only residential properties
        query = query.filter(Property.property_type == 'Residential')
        
        if county:
            query = query.filter(Property.county == county)
        
        # City filtering
        if cities:
            city_filter = [func.upper(Property.city).like(f'%{city.upper()}%') for city in cities]
            query = query.filter(func.or_(*city_filter))
        
        query = query.group_by(func.upper(Property.owner_name))
        query = query.having(func.count(Property.id) >= min_properties)
        query = query.having(func.count(Property.id) <= max_properties)
        
        # Average value filtering
        if min_avg_value:
            query = query.having(func.avg(Property.assessed_value) >= min_avg_value)
        if max_avg_value:
            query = query.having(func.avg(Property.assessed_value) <= max_avg_value)
        
        # Minimum cities (diversity)
        if min_cities:
            query = query.having(func.count(func.distinct(Property.city)) >= min_cities)
        
        # Investor type filtering
        if investor_type == "individual":
            # Individual investors: no business keywords
            business_keywords = [
                '%LLC%', '%INC%', '%CORP%', '%LP%', '%LTD%',
                '%COMPANY%', '%CO %', '%INVESTMENT%', '%CAPITAL%',
                '%PROPERTIES%', '%REALTY%', '%GROUP%', '%PARTNERS%'
            ]
            for keyword in business_keywords:
                query = query.filter(~func.upper(Property.owner_name).like(keyword))
        
        elif investor_type == "company":
            # Investment companies: must have LLC/Corp AND investment-related keywords
            # Must have business structure
            business_structure = func.or_(
                func.upper(Property.owner_name).like('%LLC%'),
                func.upper(Property.owner_name).like('%INC%'),
                func.upper(Property.owner_name).like('%CORP%'),
                func.upper(Property.owner_name).like('%LP%'),
                func.upper(Property.owner_name).like('%LTD%')
            )
            query = query.filter(business_structure)
            
            # Must have investment-related keywords
            investment_keywords = func.or_(
                func.upper(Property.owner_name).like('%INVESTMENT%'),
                func.upper(Property.owner_name).like('%CAPITAL%'),
                func.upper(Property.owner_name).like('%PROPERTIES%'),
                func.upper(Property.owner_name).like('%HOMES%'),
                func.upper(Property.owner_name).like('%REALTY%'),
                func.upper(Property.owner_name).like('%REAL ESTATE%'),
                func.upper(Property.owner_name).like('%VENTURE%'),
                func.upper(Property.owner_name).like('%ACQUISITION%'),
                func.upper(Property.owner_name).like('%RENTAL%'),
                func.upper(Property.owner_name).like('%HOUSING%')
            )
            query = query.filter(investment_keywords)
        
        if exclude_corporations and investor_type == "all":
            exclusions = [
                # Business entities
                '%LLC%', '%INC%', '%CORP%', '%LP%', '%LTD%', '%CO %',
                # Investment/financial (keep some, exclude others)
                '%TRUST%', '%BANK%', '%FINANCIAL%', '%CAPITAL%', '%FUND%',
                # Property management (exclude mega-companies)
                '%HOMES%', '%PROPERTIES%', '%INVESTMENTS%', '%REALTY%',
                '%REAL ESTATE%', '%ASSET%', '%MANAGEMENT%', '%LEASING%',
                # Government/public
                '%DISTRICT%', '%COUNTY%', '%CITY OF%', '%STATE OF%',
                '%ISD%', '%SCHOOL%', '%MUNICIPAL%', '%AUTHORITY%',
                # Utilities/services
                '%WIRELESS%', '%ENERGY%', '%SERVICES%', '%SYSTEMS%',
                '%INSURANCE%', '%ELECTRIC%', '%WATER%', '%GAS%',
                # Associations/organizations
                '%HOA%', '%ASSOCIATION%', '%COMMUNITY%', '%SOCIETY%',
                '%FOUNDATION%', '%CHURCH%', '%MINISTRY%',
                # Business structures
                '%NATIONAL%', '%COMPANY%', '%DEVELOPMENT%', '%BUILDERS%',
                '%CONSTRUCTION%', '%ASSOCIATES%', '%GROUP%', '%PARTNERS%',
                '%HOLDINGS%', '%ENTERPRISES%', '%VENTURE%'
            ]
            
            for exclusion in exclusions:
                query = query.filter(~func.upper(Property.owner_name).like(exclusion))
        
        query = query.order_by(func.count(Property.id).desc())
        
        results = query.all()
        
        investors = []
        for row in results:
            investors.append({
                'owner_name': row.owner_name,
                'property_count': row.property_count,
                'total_portfolio_value': float(row.total_portfolio_value or 0),
                'avg_property_value': float(row.avg_property_value or 0),
                'cities': row.cities
            })
        
        return investors
    
    def get_investor_properties(
        self,
        owner_name: str,
        county: Optional[str] = None
    ) -> List[Dict]:
        query = self.db.query(Property).filter(Property.owner_name == owner_name)
        
        # Only residential properties
        query = query.filter(Property.property_type == 'Residential')
        
        if county:
            query = query.filter(Property.county == county)
        
        properties = query.all()
        
        return [
            {
                'address': prop.address,
                'city': prop.city,
                'zip_code': prop.zip_code,
                'assessed_value': float(prop.assessed_value or 0),
                'square_feet': prop.square_feet,
                'year_built': prop.year_built
            }
            for prop in properties
        ]
    
    def get_investor_summary(
        self,
        owner_name: str,
        county: Optional[str] = None
    ) -> Dict:
        properties = self.get_investor_properties(owner_name, county)
        
        if not properties:
            return None
        
        total_value = sum(p['assessed_value'] for p in properties)
        cities = list(set(p['city'] for p in properties if p['city']))
        
        return {
            'owner_name': owner_name,
            'property_count': len(properties),
            'total_portfolio_value': total_value,
            'avg_property_value': total_value / len(properties) if properties else 0,
            'cities': ', '.join(sorted(cities)),
            'properties': properties
        }
