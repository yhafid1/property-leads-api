"""Equity and motivation scoring utilities."""

from decimal import Decimal
from datetime import date, datetime
from typing import Optional

def calculate_equity(
    market_value: Decimal,
    mortgage_balance: Optional[Decimal] = None,
    assessed_value: Optional[Decimal] = None
) -> Decimal:
    if mortgage_balance is not None:
        return market_value - mortgage_balance
    
    if assessed_value:
        estimated_mortgage = assessed_value * Decimal('0.80')
        return market_value - estimated_mortgage
    
    return market_value

def estimate_mortgage_balance(
    original_loan: Decimal,
    loan_date: date,
    interest_rate: Decimal = Decimal('0.07'),
    loan_term_years: int = 30
) -> Decimal:
    years_elapsed = (datetime.now().date() - loan_date).days / 365.25
    
    if years_elapsed >= loan_term_years:
        return Decimal('0')
    
    monthly_rate = interest_rate / 12
    n_payments = loan_term_years * 12
    payments_made = int(years_elapsed * 12)
    
    if monthly_rate == 0:
        monthly_payment = original_loan / n_payments
    else:
        monthly_payment = original_loan * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
    
    remaining_balance = original_loan
    for _ in range(payments_made):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
    
    return max(Decimal('0'), remaining_balance)

def calculate_motivation_score(
    years_owned: float,
    equity_percentage: Decimal,
    out_of_state_owner: bool = False,
    tax_delinquent: bool = False,
    vacant: bool = False
) -> int:
    score = 0
    
    if years_owned >= 20:
        score += 25
    elif years_owned >= 10:
        score += 15
    elif years_owned >= 5:
        score += 10
    
    if equity_percentage > 70:
        score += 30
    elif equity_percentage > 50:
        score += 20
    elif equity_percentage > 30:
        score += 10
    
    if out_of_state_owner:
        score += 20
    
    if tax_delinquent:
        score += 30
    
    if vacant:
        score += 25
    
    return min(score, 100)

def calculate_equity_percentage(equity: Decimal, market_value: Decimal) -> Decimal:
    if market_value == 0:
        return Decimal('0')
    return (equity / market_value) * 100
