import pandas as pd
from datetime import datetime
from model import predict_price

# Load dataset
data = pd.read_csv("data/real_mandi_data.csv")

data = data.rename(columns={
    "STATE": "state",
    "District Name": "district",
    "Market Name": "market",
    "Commodity": "commodity",
    "Modal_Price": "price",
    "Price Date": "date"
})

data["date"] = pd.to_datetime(data["date"], errors="coerce")
data = data.dropna()

def generate_explanation(state, commodity, market, price, profit):
    explanation = (
        f"For {commodity} in {state}, the market '{market}' "
        f"is recommended because it has the highest predicted price "
        f"of ₹{round(price,2)} per unit. "
        f"This results in an expected profit of ₹{round(profit,2)} "
        f"after accounting for transport cost. "
        f"The recommendation considers regional trends and seasonal patterns."
    )
    return explanation

def recommend_market(state, commodity, quantity):

    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day

    filtered = data[
        (data["state"] == state) &
        (data["commodity"] == commodity)
    ]

    if filtered.empty:
        return {"error": "No matching state/commodity found."}

    markets = filtered["market"].unique()

    best_market = None
    best_profit = float("-inf")
    best_price = None

    for market in markets:
        try:
            district = filtered[filtered["market"] == market]["district"].iloc[0]

            predicted_price = predict_price(
                state,
                district,
                market,
                commodity,
                year,
                month,
                day
            )

            transport_cost = 1000
            profit = (predicted_price * quantity) - transport_cost

            if profit > best_profit:
                best_profit = profit
                best_market = market
                best_price = predicted_price

        except:
            continue

    if best_market is None:
        return {"error": "Prediction failed."}

    explanation = generate_explanation(
        state,
        commodity,
        best_market,
        best_price,
        best_profit
    )

    return {
        "recommended_market": best_market,
        "predicted_price_per_unit": round(best_price, 2),
        "expected_profit": round(best_profit, 2),
        "ai_explanation": explanation
    }