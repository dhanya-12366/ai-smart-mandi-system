import pandas as pd
from datetime import datetime
from model import predict_price

# Load dataset
data = pd.read_csv("data/real_mandi_data.csv")

# Rename columns
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

def recommend_market(state, commodity, quantity):

    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day

    # Filter valid rows
    filtered = data[
        (data["state"] == state) &
        (data["commodity"] == commodity)
    ]

    if filtered.empty:
        return {
            "error": "No matching state/commodity found. Check exact spelling."
        }

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

            if isinstance(predicted_price, str):
                continue

            transport_cost = 1000
            profit = (predicted_price * quantity) - transport_cost

            if profit > best_profit:
                best_profit = profit
                best_market = market
                best_price = predicted_price

        except Exception:
            continue

    if best_market is None:
        return {
            "error": "Prediction failed for available markets."
        }

    return {
        "recommended_market": best_market,
        "predicted_price_per_unit": round(best_price, 2),
        "expected_profit": round(best_profit, 2)
    }