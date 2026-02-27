"""Project entry point.

This file is intentionally lightweight: it wires together data loading,
model inference, and optimization.
"""

from __future__ import annotations

from pathlib import Path

from model import PriceModel
from optimizer import recommend_action


DATA_PATH = Path(__file__).parent / "data" / "mandi_sample.csv"


def main() -> None:
    model = PriceModel()
    rows = model.load_csv(DATA_PATH)
    prediction = model.predict_next_price(rows)
    decision = recommend_action(prediction)

    print(f"Predicted next price: {prediction}")
    print(f"Recommendation: {decision}")


if __name__ == "__main__":
    main()
