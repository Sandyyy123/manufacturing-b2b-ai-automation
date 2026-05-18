import os
from datetime import datetime, timedelta
from typing import Optional, List

MOCK_ORDER_HISTORY = [
    {"order_id": "ORD-2024-0441", "customer_id": "C001", "product": "CF-Panel-A2", "volume": 200,
     "interval_days": 45, "last_order": "2026-04-01", "confidence": 0.93},
    {"order_id": "ORD-2024-0388", "customer_id": "C002", "product": "GRP-Tube-B8", "volume": 500,
     "interval_days": 30, "last_order": "2026-04-22", "confidence": 0.88},
    {"order_id": "ORD-2024-0312", "customer_id": "C001", "product": "Epoxy-Sheet-C1", "volume": 100,
     "interval_days": 90, "last_order": "2026-02-15", "confidence": 0.76},
]


class RepeatOrderWorkflow:
    def get_candidates(self, customer_id: Optional[str] = None, min_confidence: float = 0.7) -> List[dict]:
        orders = [o for o in MOCK_ORDER_HISTORY if o["confidence"] >= min_confidence]
        if customer_id:
            orders = [o for o in orders if o["customer_id"] == customer_id]

        results = []
        for order in orders:
            last = datetime.strptime(order["last_order"], "%Y-%m-%d")
            predicted_next = last + timedelta(days=order["interval_days"])
            days_until = (predicted_next - datetime.now()).days
            results.append({
                **order,
                "predicted_reorder_date": predicted_next.strftime("%Y-%m-%d"),
                "days_until_reorder": max(0, days_until),
                "action": "draft_po" if days_until <= 7 else "monitor"
            })

        return sorted(results, key=lambda x: x["days_until_reorder"])
