# service to score properties and generate leads based on equity

from datetime import date
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Property, HighEquityLead
from app.utils.equity_calculator import (
    calculate_equity,
    calculate_equity_percentage,
    calculate_motivation_score,
)


class LeadGeneratorService:
    def __init__(self, db: Session):
        self.db = db

    def generate_leads_for_properties(
        self,
        property_ids: Optional[List[int]] = None
    ) -> List[HighEquityLead]:
        query = self.db.query(Property)
        if property_ids:
            query = query.filter(Property.id.in_(property_ids))
        properties = query.all()

        leads = []
        for prop in properties:
            lead = self.score_property(prop)
            if lead:
                leads.append(lead)

        self.db.commit()
        return leads

    def score_property(self, prop: Property) -> Optional[HighEquityLead]:
        if not prop.market_value:
            return None

        equity_amount = calculate_equity(
            market_value=prop.market_value,
            assessed_value=prop.assessed_value
        )
        equity_percentage = calculate_equity_percentage(
            equity=equity_amount,
            market_value=prop.market_value
        )

        motivation_score = calculate_motivation_score(
            years_owned=self.years_owned_from_sale_date(prop.last_sale_date),
            equity_percentage=equity_percentage,
            out_of_state_owner=self.is_out_of_state(prop.mailing_state),
            tax_delinquent=bool(prop.tax_delinquent),
            vacant=False
        )

        lead = self.db.query(HighEquityLead).filter(
            HighEquityLead.property_id == prop.id
        ).first()

        if lead is None:
            lead = HighEquityLead(property_id=prop.id)
            self.db.add(lead)

        lead.equity_amount = equity_amount
        lead.equity_percentage = equity_percentage
        lead.motivation_score = motivation_score

        return lead

    @staticmethod
    def years_owned_from_sale_date(last_sale_date) -> float:
        if last_sale_date is None:
            return 0
        return (date.today() - last_sale_date).days / 365.25

    @staticmethod
    def is_out_of_state(mailing_state: Optional[str]) -> bool:
        if not mailing_state:
            return False
        return mailing_state.strip().upper() != "TX"