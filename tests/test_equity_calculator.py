# unit tests for equity and the respective motivation scoring 

from decimal import Decimal

from app.utils.equity_calculator import (
    calculate_equity,
    calculate_equity_percentage,
    calculate_motivation_score,
)


def test_calculate_equity_with_known_mortgage_balance():
    equity = calculate_equity(
        market_value=Decimal("300000"),
        mortgage_balance=Decimal("120000"),
    )
    assert equity == Decimal("180000")


def test_calculate_equity_falls_back_to_assessed_value_estimate():
    # No mortgage_balance given -> function estimates one as 80% of assessed_value
    equity = calculate_equity(
        market_value=Decimal("300000"),
        assessed_value=Decimal("250000"),
    )
    assert equity == Decimal("100000")  # 300000 - (250000 * 0.80)


def test_calculate_equity_with_nothing_but_market_value():
    equity = calculate_equity(market_value=Decimal("300000"))
    assert equity == Decimal("300000")


def test_calculate_equity_percentage():
    pct = calculate_equity_percentage(
        equity=Decimal("150000"),
        market_value=Decimal("300000"),
    )
    assert pct == Decimal("50")


def test_calculate_equity_percentage_avoids_division_by_zero():
    pct = calculate_equity_percentage(equity=Decimal("0"), market_value=Decimal("0"))
    assert pct == Decimal("0")


def test_motivation_score_long_ownership_high_equity():
    score = calculate_motivation_score(years_owned=25, equity_percentage=Decimal("80"))
    assert score == 55  # 25 (>=20 yrs) + 30 (>70% equity)


def test_motivation_score_caps_at_100():
    score = calculate_motivation_score(
        years_owned=25,
        equity_percentage=Decimal("80"),
        out_of_state_owner=True,
        tax_delinquent=True,
        vacant=True,
    )
    assert score == 100  # raw total would be 130 (25+30+20+30+25), capped


def test_motivation_score_short_ownership_low_equity_scores_zero():
    score = calculate_motivation_score(years_owned=1, equity_percentage=Decimal("10"))
    assert score == 0