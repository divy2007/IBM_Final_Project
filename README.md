# EcoPlate AI: Food Waste Intelligence Agent
### IBM SkillsBuild Masterclass 5 - Project Submission
**Aligned with UN Sustainable Development Goal 12: Responsible Consumption and Production (Target 12.3)**

---

## 🌟 Project Overview
**EcoPlate AI** is an autonomous multi-agent AI system powered by edge computer vision designed for institutional kitchens (universities, corporate cafeterias, hospitals). Mounted above food waste disposal bins, EcoPlate AI continuously classifies, quantifies, and values discarded food in real time using YOLOv8 object detection. 

Crucially, EcoPlate AI translates disposal telemetry into **predictive supply chain action**, enabling kitchen managers to optimize ingredient procurement, adjust portion sizes, and eliminate food waste before it reaches the bin.

---

## 🚀 Key Deliverables Included
This repository contains the complete 100% project deliverables required for submission:

1. 📄 **[1_Lean_Canvas.md](1_Lean_Canvas.md)**: Complete 9-Block Lean Canvas detailing UVP, Customer Segments, Revenue Streams, Cost Structure, and Unfair Advantage.
2. 📜 **[2_Concept_Note.md](2_Concept_Note.md)**: 2-Page Executive Concept Note covering system architecture, Edge Vision (YOLOv8), FastAPI backend, React UI, zero-human-intervention multi-agent workflow, and SDG 12 impact.
3. 📊 **[3_Pitch_Deck_Outline.md](3_Pitch_Deck_Outline.md)**: 12-Slide Pitch Deck outline with slide visual layouts, key points, and detailed scripted speaker talking points.

---

## 🖥️ Interactive Web Application & Multi-Agent Simulator
In addition to full documentation, this project includes a **100% functional, zero-dependency web dashboard & multi-agent simulator**!

### Key Application Features:
* 👁️ **Edge Vision Bin Simulator**: Live canvas camera feed displaying simulated overhead YOLOv8 food detection bounding boxes, confidence tags, and instant item mass/cost calculations.
* 🤖 **Multi-Agent Command Center**: Visualizing the 3 autonomous agents (**Vision Agent**, **Analytics Agent**, **Procurement Agent**) with step-by-step reasoning terminal logs.
* 📊 **Live Analytics & KPIs**: Interactive financial loss tracker, organic waste mass prevented (kg), carbon footprint (CO2e), and dish breakdown charts.
* 🌿 **SDG 12 ESG Audit Generator**: Generate auditable ESG compliance certificates and carbon offset reports.
* 📄 **Deliverables Hub**: View and copy all 3 Masterclass submission deliverables right from the web app interface.

---

## ⚡ How to Run the Application

Run the server with Python 3:
```bash
python run.py
```

Then open your browser and navigate to:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🛠️ Tech Stack & Architecture
* **Backend Core**: Python (Zero-dependency HTTP & REST API server + SQLite persistence)
* **Edge Vision Simulation**: YOLOv8 dish classification & depth volume estimation model architecture
* **Multi-Agent Engine**: Vision Agent, Analytics Agent, Procurement & Portioning Agent
* **Frontend Dashboard**: Glassmorphic UI (HTML5, CSS3 Custom Tokens, Vanilla JS Canvas)
