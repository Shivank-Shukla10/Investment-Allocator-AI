from typing import TypedDict, Any


class InvestmentState(TypedDict, total=False):
    user_input: dict

    profile: Any
    risk: Any
    allocation: Any
    etf_recommendations: Any
    etf_prices: dict

    profile_summary: str
    risk_profile: str
    final_summary: Any