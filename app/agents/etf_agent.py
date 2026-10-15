from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import yfinance as yf

from ..models.schemas import ETFOutput


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="qwen/qwen3.8-27b",
    temperature=0.3
)


def investment_suggestion(state):
    allocation = state["allocation"]
    risk = state["risk"]

    prompt = f"""
    Recommend suitable ETFs based on this portfolio allocation.

    Risk Level: {risk.risk_level}
    Risk Score: {risk.risk_score}

    Portfolio Allocation:
    Stocks: {allocation.stocks}%
    Bonds: {allocation.bonds}%
    Gold: {allocation.gold}%
    Cash: {allocation.cash}%

    Recommend ETFs for the relevant asset classes.

    For every recommendation provide:
    - ticker: valid US ETF ticker symbol
    - name: ETF name
    - asset_class: Stocks, Bonds, or Gold
    - reason: short explanation

    Prefer well-known, liquid ETFs.
    Do not recommend individual stocks.
    """

    structured_llm = llm.with_structured_output(ETFOutput)

    response = structured_llm.invoke(prompt)

    state["etf_recommendations"] = response

    return state


def fetch_etf_prices(state):
    etf_output = state["etf_recommendations"]

    prices = {}

    for recommendation in etf_output.recommendations:
        ticker = recommendation.ticker

        try:
            data = yf.Ticker(ticker).history(period="5d")

            if data.empty:
                prices[ticker] = {}
                continue

            prices[ticker] = {
                str(date.date()): round(float(price), 2)
                for date, price in data["Close"].items()
            }

        except Exception as e:
            prices[ticker] = {
                "error": str(e)
            }

    state["etf_prices"] = prices

    return state