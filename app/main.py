from graph import investment_graph


user_input = {
    "age": 30,
    "goal": "retirement",
    "horizon": 25,
    "income": 70000,
    "risk": "medium"
}


initial_state = {
    "user_input": user_input
}


result = investment_graph.invoke(initial_state)


print("\n" + "=" * 60)
print("INVESTMENT ALLOCATOR AI")
print("=" * 60)


print("\nPROFILE")
print("-" * 60)
print(result["profile_summary"])


print("\nRISK PROFILE")
print("-" * 60)
print(result["risk_profile"])


print("\nASSET ALLOCATION")
print("-" * 60)
print(result["allocation"])


print("\nETF RECOMMENDATIONS")
print("-" * 60)
print(result["etf_recommendations"])


print("\nETF MARKET DATA")
print("-" * 60)

for ticker, prices in result["etf_prices"].items():

    print(f"\n{ticker}")

    for date, price in prices.items():
        print(f"{date}: ${price}")


print("\n" + "=" * 60)

print("\nFINAL SUMMARY")
print("-" * 60)

summary = result["final_summary"]

print("\nInvestor:")
print(summary.investor_summary)

print("\nRisk:")
print(summary.risk_summary)

print("\nAllocation:")
print(summary.allocation_summary)

print("\nETFs:")
print(summary.etf_summary)

print("\nMarket Data:")
print(summary.market_data_summary)

print("\nDisclaimer:")
print(summary.disclaimer)

print("\n" + "=" * 60)