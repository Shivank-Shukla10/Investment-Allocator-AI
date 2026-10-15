from langgraph.graph import StateGraph, START, END

from .agents.profile_agent import profile_analyzer
from .agents.risk_agent import risk_model
from .agents.allocation_agent import asset_allocator
from .agents.etf_agent import investment_suggestion, fetch_etf_prices
from .agents.summary_agent import final_summary

from .models.state import InvestmentState


graph = StateGraph(InvestmentState)

graph.add_node("profile_analyzer", profile_analyzer)
graph.add_node("risk_model", risk_model)
graph.add_node("asset_allocator", asset_allocator)
graph.add_node("investment_suggestion", investment_suggestion)
graph.add_node("fetch_etf_prices", fetch_etf_prices)
graph.add_node("final_summary", final_summary)


graph.add_edge(START, "profile_analyzer")
graph.add_edge("profile_analyzer", "risk_model")
graph.add_edge("risk_model", "asset_allocator")
graph.add_edge("asset_allocator", "investment_suggestion")
graph.add_edge("investment_suggestion", "fetch_etf_prices")
graph.add_edge("fetch_etf_prices", "final_summary")
graph.add_edge("final_summary", END)


investment_graph = graph.compile()