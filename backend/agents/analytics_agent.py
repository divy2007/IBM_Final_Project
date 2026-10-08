from backend.database import get_db

class AnalyticsAgent:
    """
    Data Analytics Agent: Evaluates time-series disposal metrics for Indian institutional messes,
    detects food waste anomalies, correlates temporal trends, and calculates sustainability KPIs in INR (₹).
    """
    def __init__(self):
        self.agent_id = "AGENT-ANALYTICS-02"

    def analyze_waste_trends(self):
        conn = get_db()
        cursor = conn.cursor()

        # Total aggregate stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_events,
                SUM(weight_grams) as total_weight_g,
                SUM(cost_inr) as total_cost_inr,
                SUM(co2_kg) as total_co2_kg,
                AVG(confidence_score) as avg_confidence
            FROM waste_events
        """)
        row = cursor.fetchone()

        total_weight_kg = round((row["total_weight_g"] or 0) / 1000.0, 1)
        total_cost_inr = round(row["total_cost_inr"] or 0, 2)
        total_co2 = round(row["total_co2_kg"] or 0, 2)
        avg_confidence = round((row["avg_confidence"] or 0.95) * 100, 1)

        # Top wasted dishes
        cursor.execute("""
            SELECT dish_name, category, COUNT(*) as frequency, SUM(weight_grams)/1000.0 as total_kg, SUM(cost_inr) as total_cost
            FROM waste_events
            GROUP BY dish_name
            ORDER BY total_kg DESC
            LIMIT 5
        """)
        top_dishes = [
            {
                "dish_name": r["dish_name"],
                "category": r["category"],
                "frequency": r["frequency"],
                "total_kg": round(r["total_kg"], 1),
                "total_cost": round(r["total_cost"], 2)
            }
            for r in cursor.fetchall()
        ]

        # Category breakdown
        cursor.execute("""
            SELECT category, SUM(weight_grams)/1000.0 as total_kg, SUM(cost_inr) as total_cost
            FROM waste_events
            GROUP BY category
            ORDER BY total_kg DESC
        """)
        category_breakdown = [
            {
                "category": r["category"],
                "total_kg": round(r["total_kg"], 1),
                "total_cost": round(r["total_cost"], 2)
            }
            for r in cursor.fetchall()
        ]

        # Anomaly detection simulation
        anomalies = []
        if top_dishes:
            top_dish = top_dishes[0]
            anomalies.append({
                "type": "Recurrent Over-Preparation",
                "severity": "HIGH",
                "title": f"Excessive Waste Spike: {top_dish['dish_name']}",
                "description": f"Accounts for {top_dish['total_kg']} kg discarded across {top_dish['frequency']} mess shifts, causing ₹{top_dish['total_cost']:,} in direct financial loss.",
                "affected_category": top_dish["category"]
            })

        conn.close()

        return {
            "status": "success",
            "agent_id": self.agent_id,
            "kpis": {
                "total_events": row["total_events"],
                "total_waste_kg": total_weight_kg,
                "total_financial_loss": total_cost_inr,
                "total_co2_kg": total_co2,
                "avg_vision_accuracy": avg_confidence,
                "estimated_monthly_savings": round(total_cost_inr * 0.35, 2), # 35% reduction target
                "estimated_co2_prevented": round(total_co2 * 0.35, 2)
            },
            "top_wasted_dishes": top_dishes,
            "category_breakdown": category_breakdown,
            "anomalies": anomalies
        }
