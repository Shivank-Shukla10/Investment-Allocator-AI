# 💰 Investment Allocator AI

An Agentic AI-powered investment allocation system that analyzes an investor's profile, evaluates risk, generates a portfolio allocation, recommends ETFs, retrieves recent market data, and produces an AI-generated investment summary.

Built using **LangGraph, Groq, Qwen, FastAPI, Pydantic, and Yahoo Finance** with a lightweight HTML/CSS/JavaScript frontend.

> ⚠️ This project is for educational purposes only and does not provide financial advice or guarantee investment returns.

---

## 🚀 Project Overview

Investment Allocator AI demonstrates how multiple specialized AI agents can work together as an **Agentic AI workflow**.

Instead of asking one LLM to perform the entire task, the application divides the process into multiple stages:

```text
Investor Input
      ↓
Profile Analyzer
      ↓
Risk Assessment
      ↓
Asset Allocation
      ↓
ETF Recommendation
      ↓
Market Data
      ↓
Final AI Summary
```
