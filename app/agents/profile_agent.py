from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from ..models.schemas import ProfileOutput


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="qwen/qwen3.8-27b",
    temperature=0.3
)


def profile_analyzer(state):
    user_input = state["user_input"]

    prompt = f"""
    Analyze the following investor profile:

    Age: {user_input["age"]}
    Goal: {user_input["goal"]}
    Investment Horizon: {user_input["horizon"]} years
    Income: {user_input["income"]}
    Risk Preference: {user_input["risk"]}

    Provide a concise analysis of the investor profile.
    """

    structured_llm = llm.with_structured_output(ProfileOutput)

    response = structured_llm.invoke(prompt)

    state["profile"] = response
    state["profile_summary"] = response.profile_summary

    return state