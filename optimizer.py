"""Optimization / decision logic stub.

Given a predicted price, returns a basic action string.
"""

from __future__ import annotations


def recommend_action(predicted_price: float) -> str:
    if predicted_price <= 0:
        return "insufficient_data"

    # Simple heuristic placeholder.
    if predicted_price >= 2500:
        return "sell"
    if predicted_price <= 1800:
        return "buy"
    return "hold"
