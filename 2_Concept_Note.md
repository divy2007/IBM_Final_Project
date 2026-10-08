# Concept Note: EcoPlate AI (India Region)
## Autonomous Food Waste Intelligence & Predictive Procurement Agent

**Project Title:** EcoPlate AI: Food Waste Intelligence Agent  
**Domain:** AI for Sustainability & Agentic Workflows  
**Target Region:** India (Higher Education Messes & Corporate IT Cafeterias)  
**Aligned UN Sustainable Development Goal:** SDG 12: Responsible Consumption & Production (Target 12.3)  
**National Alignment:** FSSAI Save Food Share Food Initiative & SEBI BRSR ESG Framework  
**Program:** IBM SkillsBuild Masterclass 5  

---

### 1. Executive Summary & Project Background

Institutional kitchens in India—such as those in university hostel messes (IITs, NITs, Central Universities) and corporate cafeterias across Bengaluru, Hyderabad, Pune, and NCR—prepare thousands of meals daily. Despite advances in catering operations, institutional dining in India suffers from an inherent inefficiency: **up to 25–35% of prepared food is discarded daily**. This systemic waste stems from a critical information gap: mess catering managers lack real-time, item-specific data on what is actually scraped into waste bins at disposal stations.

Traditional approaches rely on manual paper registers or basic weighing scales that register total mass without context. A mess warden or catering manager might know that 150 kilograms of waste was discarded after lunch, but cannot determine whether it comprised expensive Paneer Butter Masala, untouched Steamed Basmati Rice, Dal Tadka, or Roti. Consequently, kitchens consistently over-purchase ingredients, incurring massive financial losses (**₹2,00,000 to ₹5,00,000+ monthly per campus**) and generating landfill methane emissions.

**EcoPlate AI** addresses this challenge by deploying an autonomous, multi-agent AI framework powered by edge computer vision fine-tuned on regional Indian cuisine. Positioned above waste disposal bins, EcoPlate AI continuously classifies, quantifies, and values food waste in real time. Crucially, it translates disposal data into **predictive supply chain action**, enabling mess managers to optimize procurement, adjust recipe batch sizes, and eliminate food waste before it occurs.

---

### 2. System Architecture & Core AI Technologies

EcoPlate AI integrates edge computer vision, a high-performance backend, a modern React interface, and an autonomous multi-agent core into a unified ecosystem tailored for Indian dining halls.

```
       +-------------------------------------------------------+
       |             EDGE MESS DISPOSAL STATION                |
       |  Overhead Camera + YOLOv8 Edge Vision (Raspberry Pi 5) |
       +---------------------------+---------------------------+
                                   | Real-Time JSON Stream
                                   v
       +-------------------------------------------------------+
       |                  FASTAPI BACKEND SERVICE              |
       |  Ingestion, Data Normalization, Cost (₹) & CO2 Calc   |
       +---------------------------+---------------------------+
                                   | Orchestrates
                                   v
       +-------------------------------------------------------+
       |               MULTI-AGENT INTELLIGENCE ENGINE         |
       |  - Vision Agent (Classifies Indian Dishes & Volume)   |
       |  - Analytics Agent (Correlates Trends & Anomalies)    |
       |  - Procurement Agent (Generates Predictive POs in ₹)  |
       +---------------------------+---------------------------+
                                   | Automated Reports & Alerts
                                   v
       +-------------------------------------------------------+
       |                 REACT MANAGEMENT DASHBOARD            |
       |    Chefs & Mess Committee Leads (Live Alerts & KPI)   |
       +-------------------------------------------------------+
```

#### A. Edge Computer Vision (YOLOv8 & Spatial Depth Maps)
* **Model:** A customized **YOLOv8** object detection model fine-tuned on regional Indian cuisine items (North/South Indian thalis, paneer gravies, biryani, dal, subzi, rice, and flatbreads).
* **Functionality:** Mounted above mess disposal stations, the vision system captures video frames as plates or trays are emptied into the bin. It identifies dish types, tracks bounding boxes, and estimates volume using spatial depth maps.
* **Edge Execution:** Inference runs locally on low-cost edge hardware (e.g., Raspberry Pi 5 / NVIDIA Jetson) to protect privacy, reduce bandwidth requirements, and maintain sub-100ms latency.

#### B. FastAPI High-Performance Backend
* **Asynchronous Data Pipeline:** Built with **FastAPI** (Python 3.11+), providing ultra-low latency API endpoints to receive edge vision telemetry.
* **Financial & Environmental Engine:** Automatically translates food volume metrics into financial cost in **Indian Rupees (₹)** using ingredient master market prices and carbon footprint metrics (kg CO2e avoided).

#### C. React Web Dashboard (Frontend)
* **User Interface:** A responsive dashboard built with **React** and custom CSS design tokens featuring live telemetry, financial loss counters in INR (₹), portion adjustment advisories, and downloadable ESG compliance reports.

---

### 3. Autonomous Multi-Agent Workflow (Zero Human Intervention)

EcoPlate AI operates beyond passive monitoring; it utilizes an **autonomous multi-agent workflow** that connects disposal data directly to inventory procurement without manual human intervention.

1. **Step 1: Ingestion & Vision Agent Processing**  
   As food is scraped into the mess disposal bin, the *Vision Agent* captures image frames, identifies discarded Indian food items (e.g., 350g Paneer Butter Masala), computes estimated mass and monetary loss in ₹, and transmits structured JSON events to the backend.

2. **Step 2: Analytics Agent Pattern Correlation**  
   The *Data Analytics Agent* evaluates incoming waste streams against historical data, day-of-week mess attendance, exam/holiday calendars, and weather conditions. It detects systemic anomalies (e.g., "Steamed Basmati Rice waste increased by 40% on Thursdays when served alongside specific curries").

3. **Step 3: Autonomous Procurement & Portioning Agent**  
   The *Procurement Agent* synthesizes insights from the Analytics Agent and calculates optimal recipe scaling factors. Without manual prompts, the agent:
   * Formulates revised mess prep quantities for upcoming shifts.
   * Generates draft Purchase Orders (POs) in INR (₹) calibrated to actual consumption rates.
   * Sends automated push notifications (via WhatsApp/Slack/Email) to mess managers (e.g., *"Reduce rice prep by 20 kg tomorrow; recommendation saves ₹1,850 and 54 kg CO2e"*).

---

### 4. Measurable Impact & Alignment with UN SDG 12 & Indian Frameworks

| Impact Dimension | Baseline (Traditional Indian Mess) | With EcoPlate AI | Tangible Benefit |
| :--- | :--- | :--- | :--- |
| **Food Waste Volume** | ~350 kg / campus mess / day | ~210 kg / campus mess / day | **40% Reduction in Organic Waste** |
| **Financial Savings** | High over-purchasing loss | Optimized purchasing | **₹1,50,000 – ₹4,50,000 Saved / Month** |
| **Carbon Footprint** | ~850 kg CO2e / day landfill impact | ~510 kg CO2e / day | **~120 Metric Tons CO2e Avoided / Year** |
| **FSSAI & SEBI Compliance**| Unverified manual records | Auditable digital telemetry | **100% BRSR ESG Audit Readiness** |

---

### 5. Conclusion

EcoPlate AI transforms Indian institutional food waste from an ignored operational loss into a quantifiable data stream. By combining edge computer vision with autonomous agentic intelligence, EcoPlate AI empowers Indian universities and corporate IT parks to operate efficiently, preserve financial resources, and drive meaningful progress toward global sustainability goals.
