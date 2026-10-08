import random
from datetime import datetime
from backend.database import get_db, FOOD_CATALOG

class VisionAgent:
    """
    Edge Vision Agent: Simulates YOLOv8 Object Detection & Spatial Depth Volume Estimation fine-tuned on Indian cuisine.
    Mounted overhead on dining mess disposal stations.
    """
    def __init__(self, station_id="MESS-BIN-EDGE-01"):
        self.station_id = station_id
        self.model_version = "YOLOv8x-IndianCuisineWaste-v3.1"

    def scan_disposal_frame(self, selected_dish=None, custom_weight=None):
        if not selected_dish or selected_dish not in FOOD_CATALOG:
            selected_dish = random.choice(list(FOOD_CATALOG.keys()))
            
        catalog_info = FOOD_CATALOG[selected_dish]
        
        if custom_weight:
            weight_g = float(custom_weight)
        else:
            weight_g = round(random.uniform(150, 600), 1)
            
        cost_inr = round((weight_g / 1000.0) * catalog_info["cost_per_kg"], 2)
        co2_kg = round((weight_g / 1000.0) * catalog_info["co2_factor"], 3)
        confidence = round(random.uniform(0.925, 0.988), 3)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save event to DB
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO waste_events (timestamp, dish_name, category, weight_grams, cost_inr, co2_kg, confidence_score, station_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, selected_dish, catalog_info["category"], weight_g, cost_inr, co2_kg, confidence, self.station_id))
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()

        bbox = {
            "x": random.randint(120, 320),
            "y": random.randint(100, 240),
            "width": random.randint(140, 220),
            "height": random.randint(120, 190)
        }

        return {
            "status": "success",
            "event_id": event_id,
            "timestamp": timestamp,
            "station_id": self.station_id,
            "model_version": self.model_version,
            "detection": {
                "dish_name": selected_dish,
                "category": catalog_info["category"],
                "confidence_score": confidence,
                "weight_grams": weight_g,
                "cost_inr": cost_inr,
                "co2_kg": co2_kg,
                "bounding_box": bbox
            }
        }
