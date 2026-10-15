from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from ..models.schemas import AllocationOutput


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="qwen/qwen3.8-27b",
    temperature=0.3
)


def asset_allocator(state):
    profile = state["profile"]
    risk = state["risk"]

    prompt = f"""
    Create an investment asset allocation for this investor.

    Investor Profile:
    Age: {profile.age}
    Goal: {profile.goal}
    Investment Horizon: {profile.investment_horizon} years
    Income: {profile.income}
    Risk Preference: {profile.risk_preference}

    Risk Assessment:
    Risk Level: {risk.risk_level}
    Risk Score: {risk.risk_score}
    Explanation: {risk.explanation}

    Allocate the portfolio across:
    - stocks
    - bonds
    - gold
    - cash

    IMPORTANT:
    The four percentages MUST add up to exactly 100%.
    """

    structured_llm = llm.with_structured_output(AllocationOutput)

    response = structured_llm.invoke(prompt)

    if response.total_percentage != 100:
        raise ValueError(
            f"Invalid allocation: total is "
            f"{response.total_percentage}% instead of 100%"
        )

    state["allocation"] = response

    return state