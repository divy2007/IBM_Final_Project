from datetime import datetime
import random
from backend.database import get_db, FOOD_CATALOG
from backend.agents.analytics_agent import AnalyticsAgent

class ProcurementAgent:
    """
    Autonomous Procurement & Portioning Agent (Indian Region):
    Formulates predictive recipe batch scaling, automated purchase orders, and mess portion alerts in INR (₹).
    """
    def __init__(self):
        self.agent_id = "AGENT-PROCUREMENT-03"
        self.analytics_agent = AnalyticsAgent()

    def run_procurement_optimization(self):
        trends = self.analytics_agent.analyze_waste_trends()
        top_dishes = trends.get("top_wasted_dishes", [])

        recommendations = []
        purchase_orders = []

        if top_dishes:
            for dish in top_dishes[:3]:
                dish_name = dish["dish_name"]
                tot_kg = dish["total_kg"]
                tot_cost = dish["total_cost"]

                # Calculate suggested reduction %
                reduction_pct = 18 if "Paneer" in dish["category"] or "Non-Veg" in dish["category"] else 25
                monthly_saving_inr = round(tot_cost * (reduction_pct / 100.0), 2)
                co2_saving = round(tot_kg * FOOD_CATALOG[dish_name]["co2_factor"] * (reduction_pct / 100.0), 1)

                recommendations.append({
                    "id": f"REC-IND-{random.randint(1000, 9999)}",
                    "dish_name": dish_name,
                    "category": dish["category"],
                    "action_type": "Recipe Portion Scale",
                    "recommendation": f"Scale back mess prep volume for '{dish_name}' by {reduction_pct}% during peak lunch shifts.",
                    "rationale": f"Identified as top-discarded mess item ({tot_kg} kg wasted). Scaling saves ₹{monthly_saving_inr:,.2f} per month.",
                    "monthly_savings_inr": monthly_saving_inr,
                    "co2_reduction_kg": co2_saving,
                    "status": "Recommended"
                })

                # Generate draft Purchase Order adjustment in INR
                purchase_orders.append({
                    "po_number": f"PO-IND-2026-{random.randint(1000, 9999)}",
                    "ingredient": dish_name,
                    "original_qty_kg": round(tot_kg * 1.5, 1),
                    "adjusted_qty_kg": round((tot_kg * 1.5) * (1.0 - (reduction_pct / 100.0)), 1),
                    "unit_price_inr": FOOD_CATALOG[dish_name]["cost_per_kg"],
                    "cost_reduction_inr": monthly_saving_inr,
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "approval_status": "Draft - Awaiting Mess Manager Confirmation"
                })

        return {
            "status": "success",
            "agent_id": self.agent_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": "Autonomous Indian mess procurement analysis complete. Generated 3 predictive PO adjustments in INR (₹).",
            "recommendations": recommendations,
            "draft_purchase_orders": purchase_orders
        }
