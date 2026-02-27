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

def generate_explanation(state, commodity, best_market):
    return (
        f"For {commodity} in {state}, the system evaluated multiple markets "
        f"and ranked them based on predicted profit. "
        f"The market '{best_market}' offers the highest expected return "
        f"considering regional trends and seasonal price variations."
    )

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

    results = []

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

            results.append({
                "market": market,
                "predicted_price": round(predicted_price, 2),
                "expected_profit": round(profit, 2)
            })

        except:
            continue

    if not results:
        return {"error": "Prediction failed."}

    # Sort by profit descending
    results = sorted(results, key=lambda x: x["expected_profit"], reverse=True)

    top_3 = results[:3]

    explanation = generate_explanation(
        state,
        commodity,
        top_3[0]["market"]
    )

    return {
        "best_market": top_3[0],
        "top_3_markets": top_3,
        "ai_explanation": explanation
    }