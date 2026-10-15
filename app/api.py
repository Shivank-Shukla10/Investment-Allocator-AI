from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.graph import investment_graph


app = FastAPI(
    title="Investment Allocator AI",
    description="Agentic AI investment allocation application",
    version="1.0.0"
)


# Serve frontend static files
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


@app.get("/")
def root():
    return FileResponse("frontend/index.html")


class InvestmentRequest(BaseModel):
    age: int
    goal: str
    horizon: int
    income: float
    risk: str


@app.post("/api/invest")
def invest(request: InvestmentRequest):

    user_input = {
        "age": request.age,
        "goal": request.goal,
        "horizon": request.horizon,
        "income": request.income,
        "risk": request.risk
    }

    initial_state = {
        "user_input": user_input
    }

    result = investment_graph.invoke(initial_state)

    summary = result["final_summary"]

    return {
        "profile": {
            "age": result["profile"].age,
            "goal": result["profile"].goal,
            "horizon": result["profile"].investment_horizon,
            "income": result["profile"].income,
            "risk_preference": result["profile"].risk_preference
        },

        "risk": {
            "level": result["risk"].risk_level,
            "score": result["risk"].risk_score,
            "explanation": result["risk"].explanation
        },

        "allocation": {
            "stocks": result["allocation"].stocks,
            "bonds": result["allocation"].bonds,
            "gold": result["allocation"].gold,
            "cash": result["allocation"].cash
        },

        "etfs": [
            {
                "ticker": etf.ticker,
                "name": etf.name,
                "asset_class": etf.asset_class,
                "reason": etf.reason
            }
            for etf in result["etf_recommendations"].recommendations
        ],

        "market_data": result["etf_prices"],

        "summary": {
            "investor": summary.investor_summary,
            "risk": summary.risk_summary,
            "allocation": summary.allocation_summary,
            "etfs": summary.etf_summary,
            "market_data": summary.market_data_summary,
            "disclaimer": summary.disclaimer
        }
    }