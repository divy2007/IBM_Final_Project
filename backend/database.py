import sqlite3
import random
from datetime import datetime, timedelta

# Menu Item Catalog with Indian Regional Cuisine, cost per kg in INR (₹), and carbon footprint factor (kg CO2e per kg)
FOOD_CATALOG = {
    "Paneer Butter Masala": {"category": "Paneer / Protein", "cost_per_kg": 360.00, "co2_factor": 5.20},
    "Steamed Basmati Rice": {"category": "Rice / Carbs", "cost_per_kg": 75.00, "co2_factor": 2.70},
    "Hyderabadi Chicken Biryani": {"category": "Non-Veg Protein", "cost_per_kg": 290.00, "co2_factor": 7.40},
    "Dal Tadka & Rajma": {"category": "Pulses / Lentils", "cost_per_kg": 95.00, "co2_factor": 1.80},
    "Vegetable Pulao": {"category": "Rice / Carbs", "cost_per_kg": 125.00, "co2_factor": 2.10},
    "Butter Naan & Roti": {"category": "Breads", "cost_per_kg": 110.00, "co2_factor": 1.40},
    "Green Salad & Cucumber": {"category": "Salad / Veggies", "cost_per_kg": 55.00, "co2_factor": 0.90},
    "Mixed Veg Subzi": {"category": "Vegetables", "cost_per_kg": 140.00, "co2_factor": 1.50},
}

DB_PATH = "ecoplate.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Drop existing tables if re-initializing schema for Indian currency
    cursor.execute("DROP TABLE IF EXISTS waste_events")
    cursor.execute("DROP TABLE IF EXISTS agent_actions")

    # Waste events table
    cursor.execute("""
    CREATE TABLE waste_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        dish_name TEXT,
        category TEXT,
        weight_grams REAL,
        cost_inr REAL,
        co2_kg REAL,
        confidence_score REAL,
        station_id TEXT
    )
    """)
    
    # Agent actions table
    cursor.execute("""
    CREATE TABLE agent_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        agent_name TEXT,
        action_type TEXT,
        details TEXT,
        savings_inr REAL,
        co2_reduction_kg REAL,
        status TEXT
    )
    """)
    
    seed_historical_data(cursor)
    conn.commit()
    conn.close()

def seed_historical_data(cursor):
    now = datetime.now()
    dish_list = list(FOOD_CATALOG.keys())
    
    # Generate 30 days of synthetic disposal logs for an Indian campus dining hall
    for day_offset in range(30, 0, -1):
        day_time = now - timedelta(days=day_offset)
        # Simulate 20-35 waste events per day
        num_events = random.randint(20, 35)
        for _ in range(num_events):
            event_time = day_time + timedelta(hours=random.randint(11, 21), minutes=random.randint(0, 59))
            dish = random.choice(dish_list)
            catalog_info = FOOD_CATALOG[dish]
            
            # Rice, Dal, and Salad are discarded in higher volumes
            weight = random.uniform(250, 750) if "Rice" in dish or "Dal" in dish else random.uniform(100, 400)
            cost_inr = (weight / 1000.0) * catalog_info["cost_per_kg"]
            co2 = (weight / 1000.0) * catalog_info["co2_factor"]
            confidence = round(random.uniform(0.91, 0.985), 3)
            
            cursor.execute("""
                INSERT INTO waste_events (timestamp, dish_name, category, weight_grams, cost_inr, co2_kg, confidence_score, station_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (event_time.strftime("%Y-%m-%d %H:%M:%S"), dish, catalog_info["category"], round(weight, 1), round(cost_inr, 2), round(co2, 3), confidence, "MESS-BIN-EDGE-01"))

    # Initial seed for agent recommendations in INR ₹
    cursor.execute("""
        INSERT INTO agent_actions (timestamp, agent_name, action_type, details, savings_inr, co2_reduction_kg, status)
        VALUES 
        (?, 'Procurement Agent', 'Recipe Portion Scale', 'Reduce Steamed Basmati Rice prep volume by 20% during Thursday lunch service to prevent recurrent mess waste.', 18500.00, 142.5, 'Active'),
        (?, 'Procurement Agent', 'Purchase Order Draft', 'Auto-generated PO #PO-IND-809: Reduced Paneer order by 15kg based on historical 14-day plate waste metrics.', 32400.00, 210.0, 'Pending Approval'),
        (?, 'Analytics Agent', 'Anomaly Detected', 'Dal Tadka discard volume spiked +38% during Wednesday dinner shift.', 0.0, 0.0, 'Resolved')
    """, (now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
