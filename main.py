from fastapi import FastAPI
from pydantic import BaseModel
from optimizer import recommend_market

app = FastAPI(title="AI Smart Mandi System")

@app.get("/")
def home():
    return {"message": "AI Smart Mandi API is running"}

class FarmerInput(BaseModel):
    state: str
    commodity: str
    quantity: int

@app.post("/recommend")
def get_recommendation(data: FarmerInput):
    return recommend_market(
        data.state,
        data.commodity,
        data.quantity
    )

# ============================
# SMS SIMULATION ENDPOINT
# ============================

@app.get("/sms")
def sms_simulation(message: str):
    """
    Format expected:
    WHEAT MAHARASHTRA 1000
    """

    try:
        parts = message.split()

        if len(parts) != 3:
            return {"error": "Format must be: CROP STATE QUANTITY"}

        commodity = parts[0].capitalize()
        state = parts[1].capitalize()
        quantity = int(parts[2])

        result = recommend_market(state, commodity, quantity)

        if "error" in result:
            return result

        best = result["best_market"]
        top3 = result["top_3_markets"]

        sms_response = (
            f"Best Market: {best['market']}\n"
            f"Price: ₹{best['predicted_price']}\n"
            f"Profit: ₹{best['expected_profit']}\n"
            f"Top 3: {top3[0]['market']}, "
            f"{top3[1]['market']}, "
            f"{top3[2]['market']}"
        )

        return {"sms_reply": sms_response}

    except Exception as e:
        return {"error": str(e)}