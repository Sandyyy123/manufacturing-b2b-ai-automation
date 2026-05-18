import os

TIER_MULTIPLIERS = {"premium": 0.92, "standard": 1.0, "spot": 1.08}
VOLUME_BREAKS = [(1, 99, 1.0), (100, 499, 0.93), (500, 1999, 0.87), (2000, float("inf"), 0.81)]


class PricingIntelligence:
    def __init__(self):
        self.margin_floor = float(os.getenv("MARGIN_FLOOR", "0.18"))
        self.target_margin = float(os.getenv("TARGET_MARGIN", "0.28"))

    def score(self, data: dict) -> dict:
        volume = data["volume"]
        proposed = data["proposed_price"]
        tier = data.get("customer_tier", "standard")

        volume_discount = next(d for lo, hi, d in VOLUME_BREAKS if lo <= volume <= hi)
        tier_adj = TIER_MULTIPLIERS.get(tier, 1.0)
        estimated_cogs = proposed * 0.68 * volume_discount * tier_adj
        margin = (proposed - estimated_cogs) / proposed if proposed > 0 else 0
        competitiveness = "competitive" if margin <= self.target_margin + 0.05 else "high"

        return {
            "product_id": data["product_id"],
            "proposed_price": proposed,
            "estimated_margin": round(margin, 3),
            "margin_status": "ok" if margin >= self.margin_floor else "below_floor",
            "competitiveness": competitiveness,
            "volume_discount_applied": round((1 - volume_discount) * 100, 1),
            "recommendation": self._recommend(margin),
            "confidence": 0.84
        }

    def _recommend(self, margin: float) -> str:
        if margin < self.margin_floor:
            return f"Price too low - increase by {round((self.margin_floor - margin) * 100, 1)}% minimum"
        elif margin > self.target_margin + 0.08:
            return "Consider discounting to improve win probability"
        return "Price within target range - proceed"
