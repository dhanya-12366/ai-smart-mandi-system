from fastapi import FastAPI
from pydantic import BaseModel
from optimizer import recommend_market

app = FastAPI(title="AI Smart Mandi System")

class FarmerInput(BaseModel):
    state: str
    commodity: str
    quantity: int

@app.post("/recommend")
def get_recommendation(data: FarmerInput):
    result = recommend_market(
        data.state,
        data.commodity,
        data.quantity
    )
    return result