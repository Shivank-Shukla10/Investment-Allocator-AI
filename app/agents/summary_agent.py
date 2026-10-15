from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from ..models.schemas import FinalSummaryOutput


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="qwen/qwen3.8-27b",
    temperature=0.3
)


def final_summary(state):
    profile = state["profile"]
    risk = state["risk"]
    allocation = state["allocation"]
    etfs = state["etf_recommendations"]
    prices = state["etf_prices"]

    etf_text = "\n".join(
        f"{etf.ticker} - {etf.name} "
        f"({etf.asset_class}): {etf.reason}"
        for etf in etfs.recommendations
    )

    prompt = f"""
    Create a concise final investment plan summary.

    INVESTOR
    Age: {profile.age}
    Goal: {profile.goal}
    Investment Horizon: {profile.investment_horizon} years
    Income: {profile.income}

    RISK
    Level: {risk.risk_level}
    Score: {risk.risk_score}
    Explanation: {risk.explanation}

    ALLOCATION
    Stocks: {allocation.stocks}%
    Bonds: {allocation.bonds}%
    Gold: {allocation.gold}%
    Cash: {allocation.cash}%

    ETF RECOMMENDATIONS
    {etf_text}

    MARKET DATA
    {prices}

    Return:
    - investor_summary
    - risk_summary
    - allocation_summary
    - etf_summary
    - market_data_summary
    - disclaimer

    Keep the summaries concise and easy for a normal user to understand.

    The disclaimer must clearly state that this is educational
    information and not personalized financial advice.
    """

    structured_llm = llm.with_structured_output(FinalSummaryOutput)

    response = structured_llm.invoke(prompt)

    state["final_summary"] = response

    return state