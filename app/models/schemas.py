from pydantic import BaseModel
from typing import List


class ProfileOutput(BaseModel):
    age: int
    goal: str
    investment_horizon: int
    income: float
    risk_preference: str
    profile_summary: str


class RiskOutput(BaseModel):
    risk_level: str
    risk_score: int
    explanation: str


class AllocationOutput(BaseModel):
    stocks: int
    bonds: int
    gold: int
    cash: int
    explanation: str

    @property
    def total_percentage(self) -> int:
        return self.stocks + self.bonds + self.gold + self.cash


class ETFRecommendation(BaseModel):
    ticker: str
    name: str
    asset_class: str
    reason: str


class ETFOutput(BaseModel):
    recommendations: List[ETFRecommendation]



class FinalSummaryOutput(BaseModel):
    investor_summary: str
    risk_summary: str
    allocation_summary: str
    etf_summary: str
    market_data_summary: str
    disclaimer: str
