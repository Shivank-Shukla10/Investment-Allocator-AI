from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from ..models.schemas import RiskOutput


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="qwen/qwen3.8-27b",
    temperature=0.3
)


def risk_model(state):
    profile = state["profile"]

    prompt = f"""
    Determine the investor's risk profile based on:

    Age: {profile.age}
    Goal: {profile.goal}
    Investment Horizon: {profile.investment_horizon} years
    Income: {profile.income}
    Risk Preference: {profile.risk_preference}

    Assign:
    - risk_level: Conservative, Moderate, or Aggressive
    - risk_score: integer from 1 to 10
    - explanation: concise reasoning
    """

    structured_llm = llm.with_structured_output(RiskOutput)

    response = structured_llm.invoke(prompt)

    state["risk"] = response
    state["risk_profile"] = response.explanation

    return state