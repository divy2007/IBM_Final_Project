import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.pdf_generator import SimplePDFBuilder
from backend.pptx_generator import build_pptx

def generate_all_submission_files():
    print("============================================================")
    print("  Generating IBM SkillsBuild Masterclass 5 Submission Files ")
    print("============================================================")

    # 1. BUILD LEAN CANVAS PDF
    pdf_lc = SimplePDFBuilder("1_Lean_Canvas.pdf")
    pdf_lc.add_title("EcoPlate AI: Food Waste Intelligence Agent")
    pdf_lc.add_subtitle("Deliverable 1: Complete Lean Canvas (India Region - INR Currency)")
    pdf_lc.add_heading("1. Problem & Existing Alternatives")
    pdf_lc.add_bullet("High Food Waste in Indian Messes: Universities (IITs, NITs) & IT Parks discard 25-35% food daily.")
    pdf_lc.add_bullet("Lack of Itemized Disposal Telemetry: Wardens log total weight without tracking specific dishes.")
    pdf_lc.add_bullet("Financial & Environmental Toll: High procurement spend and rotting methane emissions violating FSSAI & SEBI BRSR.")
    pdf_lc.add_bullet("Existing Alternatives: Manual registers, basic weighing scales lacking dish vision classification.")

    pdf_lc.add_heading("2. Customer Segments & Early Adopters")
    pdf_lc.add_bullet("Target Customers: University Dining Messes, Corporate IT Cafeterias, Hospital Messes, Large Buffet Operators.")
    pdf_lc.add_bullet("Key Stakeholders: Mess Committee Leads, Catering Contractors (Sodexo India, Compass Group India), CSR Heads.")
    pdf_lc.add_bullet("Early Adopters: Top Higher Ed Campuses with Zero-Waste targets, Fortune 500 Corporate Hubs.")

    pdf_lc.add_heading("3. Unique Value Proposition (UVP)")
    pdf_lc.add_bullet("Zero-Touch Food Waste Intelligence: Autonomous multi-agent AI that sees what Indian kitchens waste, predicts what they need, and cuts procurement costs by up to 25-30% while advancing UN SDG 12 & FSSAI compliance.")

    pdf_lc.add_heading("4. Solution & Top Features")
    pdf_lc.add_bullet("Edge AI Vision Analysis: Overhead camera with fine-tuned YOLOv8 model for real-time dish recognition.")
    pdf_lc.add_bullet("Autonomous Predictive Procurement Agent: Multi-agent system analyzing historical waste, weather, and exam schedules.")
    pdf_lc.add_bullet("Automated Executive & Kitchen Reporting: FastAPI backend & React dashboard pushing portion alerts directly to mess chefs.")

    pdf_lc.add_heading("5. Channels & Revenue Streams")
    pdf_lc.add_bullet("Channels: Direct sales to Sodexo India/Compass Group India, IBM Ecosystem showcases, Higher Ed Summits.")
    pdf_lc.add_bullet("B2B SaaS Subscription: INR 25,000 - INR 60,000 / mess / month.")
    pdf_lc.add_bullet("Hardware & Setup Fee: INR 85,000 - INR 1,80,000 upfront per smart bin installation.")

    pdf_lc.add_heading("6. Cost Structure & Key Metrics")
    pdf_lc.add_bullet("Costs: Edge devices (Raspberry Pi 5/NVIDIA Jetson), Serverless cloud hosting, R&D for Indian regional datasets.")
    pdf_lc.add_bullet("Key Metrics: Kg Waste Prevented, Monthly Procurement Savings (INR 1.5L - 4.5L/mo), Vision Accuracy (>94%), CO2e Avoided.")
    pdf_lc.save()

    # 2. BUILD CONCEPT NOTE PDF
    pdf_cn = SimplePDFBuilder("2_Concept_Note.pdf")
    pdf_cn.add_title("EcoPlate AI: Project Concept Note")
    pdf_cn.add_subtitle("Deliverable 2: Concept Note (India Region & UN SDG 12 Target 12.3)")
    pdf_cn.add_heading("1. Executive Summary & Background")
    pdf_cn.add_paragraph("Institutional kitchens in India—such as university hostel messes (IITs, NITs) and corporate IT cafeterias in Bengaluru, Hyderabad, and Pune—prepare thousands of meals daily, yet 25-35% of prepared food ends up wasted. This inefficiency stems from an information void at disposal stations. Mess wardens log total waste weight without tracking specific dishes (Paneer Butter Masala, Basmati Rice, Dal Tadka). Consequently, kitchens over-purchase ingredients, incurring severe financial losses (INR 2 Lakh to INR 5 Lakh monthly per campus) and generating landfill methane emissions.")
    pdf_cn.add_paragraph("EcoPlate AI addresses this challenge by deploying an autonomous multi-agent AI framework powered by edge computer vision fine-tuned on regional Indian cuisine. Positioned above disposal bins, EcoPlate AI classifies and quantifies food waste in real time, translating telemetry into automated predictive supply chain adjustments.")

    pdf_cn.add_heading("2. System Architecture & Core AI Technologies")
    pdf_cn.add_bullet("Edge Computer Vision: Low-cost edge hardware (Raspberry Pi 5 / NVIDIA Jetson) running YOLOv8 fine-tuned on Indian cuisine for sub-100ms dish classification and spatial depth volume estimation.")
    pdf_cn.add_bullet("FastAPI Asynchronous Backend: High-performance Python backend processing vision telemetry, mapping volume to financial cost in INR, and calculating CO2e avoided.")
    pdf_cn.add_bullet("React Web Dashboard: Responsive interface presenting real-time financial loss counters in INR, waste category heatmaps, and downloadable ESG compliance reports.")

    pdf_cn.add_heading("3. Autonomous Multi-Agent Workflow (Zero Human Intervention)")
    pdf_cn.add_bullet("Step 1 (Vision Agent): Scans disposal frames, tags Indian dish categories, calculates mass and monetary loss in INR.")
    pdf_cn.add_bullet("Step 2 (Analytics Agent): Correlates waste streams against 30-day historical trends, weather, and exam schedules.")
    pdf_cn.add_bullet("Step 3 (Procurement Agent): Calculates recipe batch size reductions and auto-drafts Purchase Orders (POs) in INR.")

    pdf_cn.add_heading("4. Measurable Impact on UN SDG 12 & FSSAI / SEBI BRSR")
    pdf_cn.add_bullet("Waste Volume: 40% reduction in organic waste (~140 kg saved daily per mess, 50 Metric Tons/year).")
    pdf_cn.add_bullet("Financial Savings: INR 1,50,000 - INR 4,50,000 saved per month in procurement spend.")
    pdf_cn.add_bullet("Decarbonization: ~120 Metric Tons of CO2e avoided annually per mess.")
    pdf_cn.add_bullet("Compliance: 100% digital audit readiness for FSSAI Save Food Share Food & SEBI BRSR ESG disclosures.")
    pdf_cn.save()

    # 3. BUILD PITCH DECK OUTLINE PDF
    pdf_pd = SimplePDFBuilder("3_Pitch_Deck_Outline.pdf")
    pdf_pd.add_title("EcoPlate AI: Pitch Deck Outline & Speaker Script")
    pdf_pd.add_subtitle("Deliverable 3: PowerPoint Presentation Outline (12 Slides)")
    
    slides_summary = [
        ("Slide 1: Title Slide", "EcoPlate AI: Zero-Touch Food Waste Intelligence for Indian Messes (SDG 12 & FSSAI)."),
        ("Slide 2: The Problem Scale", "68M Tons food waste in India; 25-35% mess waste due to itemized data blindspot."),
        ("Slide 3: The EcoPlate Solution", "Overhead edge YOLOv8 camera + FastAPI backend + Autonomous Procurement Agent in INR."),
        ("Slide 4: Technical Architecture", "Raspberry Pi 5 edge vision, async Python backend, React frontend, TimescaleDB store."),
        ("Slide 5: Autonomous Agent Flow", "Vision Agent -> Analytics Agent -> Procurement Agent (Auto POs & WhatsApp alerts)."),
        ("Slide 6: Business Model (Lean Canvas)", "B2B SaaS (INR 25k-60k/mo) + Hardware Setup (INR 85k-1.8L) + Enterprise Integrations."),
        ("Slide 7: Unfair Advantage Matrix", "100% hands-free vision vs manual scales; proprietary Indian regional thali dataset."),
        ("Slide 8: Environmental & ESG Impact", "50 Tons waste saved/yr, 120 Tons CO2e avoided/yr, SEBI BRSR ESG audit compliance."),
        ("Slide 9: Market Opportunity & GTM", "TAM: INR 35,000 Cr; GTM via Sodexo India, Compass Group India, higher ed pilots."),
        ("Slide 10: Product Roadmap", "Q1 Prototype -> Q2 Campus Pilots -> Q3 SAP/Tally Connectors -> Q4 50 Commercial Messes."),
        ("Slide 11: Team & IBM Synergy", "Computer vision & full-stack expertise built with IBM Agentic AI principles."),
        ("Slide 12: Call to Action", "Join us in halving institutional food waste in India by 2030!")
    ]
    
    for title, desc in slides_summary:
        pdf_pd.add_heading(title)
        pdf_pd.add_paragraph(desc)
    pdf_pd.save()

    # 4. BUILD RICH 2-COLUMN PPTX PRESENTATION WITH SPEAKER NOTES
    pptx_slides = [
        {
            "title": "EcoPlate AI: Food Waste Intelligence Agent",
            "subtitle": "Autonomous Edge Vision & Multi-Agent Supply Chain Optimization for Indian Kitchens",
            "badge": "TITLE SLIDE",
            "left_points": [
                "Project Name: EcoPlate AI (India Region)",
                "Aligned UN SDG: SDG 12 - Responsible Consumption & Production (Target 12.3)",
                "National Compliance: FSSAI Save Food Share Food Initiative & SEBI BRSR Framework",
                "Program: IBM SkillsBuild For Academia Masterclass 5"
            ],
            "right_points": [
                "Transforming Mess Waste Bins into Supply Chain Feedback Loops",
                "Edge YOLOv8 Vision Dish Recognition (<100ms)",
                "Autonomous Procurement Agent & Auto PO Generator",
                "25-30% Reduction in Procurement Expenses"
            ],
            "script": "Good day everyone. Did you know that across higher education messes and corporate IT parks in India, nearly 30% of prepared food is discarded daily? Today, I am excited to introduce EcoPlate AI: an autonomous multi-agent AI platform powered by edge computer vision that turns food waste bins into real-time supply chain intelligence."
        },
        {
            "title": "The Problem: Institutional Waste Scale in India",
            "subtitle": "The Invisible Crisis in Indian Campus Dining Halls & Corporate Cafeterias",
            "badge": "PROBLEM SCALE",
            "left_points": [
                "68 Million Tons: Annual organic food waste generated across India",
                "25% - 35%: Daily prepared food discarded in university messes & IT parks",
                "INR 1.5 Lakh Crore: Annual financial loss due to institutional food over-preparation"
            ],
            "right_points": [
                "The Data Blindspot: Mess wardens log total weight without tracking WHICH dishes are wasted",
                "Recurrent Over-Purchasing: Kitchens re-order ingredients (Paneer, Rice, Proteins) rejected by diners",
                "Existing Alternatives Fail: Manual registers are tedious; standard scales lack dish vision"
            ],
            "script": "Institutional messes in India serve thousands of meals daily. However, mess managers face a major blindspot: they know how much total weight is thrown away, but they have no idea whether that weight was expensive Paneer Butter Masala, Steamed Basmati Rice, or Dal. Without itemized data, catering contractors re-order ingredients that students consistently reject."
        },
        {
            "title": "The Solution: Zero-Touch Food Waste Intelligence",
            "subtitle": "Automating Waste Detection and Supply Chain Action",
            "badge": "SOLUTION OVERVIEW",
            "left_points": [
                "Overhead Edge Vision: Compact camera running YOLOv8 fine-tuned on regional Indian cuisine",
                "Sub-100ms Inference: Instantly classifies dish types, estimates mass, and maps monetary loss in INR",
                "100% Hands-Free: Kitchen staff change nothing about their daily dish scraping routine"
            ],
            "right_points": [
                "Autonomous Multi-Agent Engine: Correlates waste with weather, attendance, and exam schedules",
                "Predictive Recipe Scaling: Recommends precise batch reductions for upcoming meal shifts",
                "Automated PO Generation: Drafts purchase order adjustments directly in INR (₹)"
            ],
            "script": "EcoPlate AI replaces guess-work with an automated intelligence loop. A low-cost edge camera unit mounted above mess disposal bins captures items as trays are scraped. Using YOLOv8 computer vision fine-tuned on Indian cuisine, our system classifies dish types and estimates volume in real time, delivering actionable procurement reports directly to the catering manager's phone."
        },
        {
            "title": "System Architecture & AI Tech Stack",
            "subtitle": "Enterprise-Grade Architecture for Speed, Privacy, and Scalability",
            "badge": "ARCHITECTURE",
            "left_points": [
                "Edge Vision Layer: Raspberry Pi 5 / NVIDIA Jetson + HD Optical Sensor running YOLOv8",
                "Backend API Core: Asynchronous FastAPI (Python 3.11) handling telemetry streams",
                "Database Engine: TimescaleDB / SQLite time-series store for disposal event records"
            ],
            "right_points": [
                "Privacy First: Video frames processed locally at the edge node without leaving campus",
                "Multi-Agent Orchestration: Vision Agent -> Analytics Agent -> Procurement Agent",
                "Responsive React Dashboard: Glassmorphic UI presenting financial loss tickers and ESG exports"
            ],
            "script": "Architecturally, EcoPlate AI is built for speed, privacy, and scalability. Edge micro-processors execute localized YOLOv8 inference so video feeds never leave the campus, maintaining strict privacy and sub-second speed. Data telemetry feeds into a lightweight FastAPI backend that translates image pixels into Rupee amounts and carbon footprint metrics."
        },
        {
            "title": "Autonomous Multi-Agent Workflow in Action",
            "subtitle": "Closed-Loop Automation from Bin Scraping to Purchase Order Draft",
            "badge": "AGENT WORKFLOW",
            "left_points": [
                "Step 1 (Vision Agent): Detects 350g discarded Paneer Butter Masala; calculates INR 126 loss",
                "Step 2 (Analytics Agent): Identifies pattern—Paneer waste up 38% on Thursday lunch shifts",
                "Step 3 (Procurement Agent): Calculates -18% recipe prep scaling factor for upcoming shifts"
            ],
            "right_points": [
                "Step 4 (Auto PO Draft): Auto-drafts updated ingredient purchasing order in INR (₹)",
                "Step 5 (WhatsApp Push Alert): Sends one-click approval prompt to executive chef's mobile",
                "Zero Human Data Entry: 100% automated feedback loop"
            ],
            "script": "Let's walk through our autonomous agent pipeline. When a plate is scraped, our Vision Agent tags the specific Indian dish and logs its mass and monetary loss in Rupees. The Analytics Agent aggregates these entries against historical trends, weather, and university exam schedules. Finally, our Procurement Agent calculates exact batch reductions and auto-drafts purchasing orders in INR."
        },
        {
            "title": "Business Model & Lean Canvas Summary",
            "subtitle": "Attractive Enterprise B2B SaaS Model with Rapid Payback",
            "badge": "BUSINESS MODEL",
            "left_points": [
                "B2B SaaS Subscription: INR 25,000 - INR 60,000 / mess / month for AI intelligence engine",
                "Hardware Installation Fee: INR 85,000 - INR 1,80,000 upfront per smart bin node",
                "Enterprise ERP Integration: INR 3,50,000+ for SAP / Tally Enterprise connectors"
            ],
            "right_points": [
                "Rapid Payback Period: Messes achieve 100% ROI within 45 - 60 days",
                "Substantial Customer Savings: Saves INR 1.5 Lakh - INR 4.5 Lakh monthly per campus",
                "Target Customers: University Messes, IT Cafeterias, Hospital Messes, Food Contractors"
            ],
            "script": "Our business model pairs an initial hardware installation fee per mess bin unit with a recurring SaaS subscription per mess for our AI intelligence engine. Indian campus messes achieve ROI within 60 days by saving lakhs of rupees in monthly food procurement expenses."
        },
        {
            "title": "Unfair Advantage & Competitive Landscape",
            "subtitle": "Outperforming Manual Registers & Standard Weighing Scales",
            "badge": "COMPETITIVE MATRIX",
            "left_points": [
                "100% Hands-Free Edge Vision: Zero button presses required by busy kitchen staff",
                "Proprietary Vision Dataset: Fine-tuned on North & South Indian thalis, gravies & breads",
                "Closed-Loop Multi-Agent Action: Connects waste vision directly to purchasing POs"
            ],
            "right_points": [
                "Manual Registers: High friction, inaccurate, tedious during rush cleanup hours",
                "Smart Weigh Scales (Winnow/Leanpath): Require manual screen button selection per dish",
                "Static Inventory Systems: Lack real-time disposal telemetry & predictive feedback loops"
            ],
            "script": "Unlike standard smart scales that require kitchen staff to manually press screen buttons to log food items—creating friction during fast-paced mess cleanup—EcoPlate AI is completely hands-free. Our unfair advantage lies in our proprietary vision dataset fine-tuned on North and South Indian thalis and gravies."
        },
        {
            "title": "Environmental Impact & SDG 12 Alignment",
            "subtitle": "Driving UN SDG Target 12.3 and National Sustainability Commitments",
            "badge": "SDG 12 & ESG",
            "left_points": [
                "UN SDG Target 12.3: Directly driving the goal to halve global per capita food waste by 2030",
                "50 Metric Tons/Year: Organic waste prevented per institutional mess site",
                "120 Metric Tons CO2e: Methane emissions avoided per campus mess annually"
            ],
            "right_points": [
                "National Compliance: Aligned with FSSAI Save Food Share Food Initiative",
                "SEBI BRSR Reporting: Generates auditable ESG data reports for corporate disclosures",
                "Water Conservation: Saves ~4.2 Million Liters of embedded agricultural water annually"
            ],
            "script": "EcoPlate AI is directly aligned with UN Sustainable Development Goal 12.3 and FSSAI directives. On average, a single campus mess equipped with EcoPlate AI prevents 50 metric tons of food waste per year, directly avoiding 120 metric tons of CO2 equivalent emissions while generating auditable SEBI BRSR ESG reports."
        },
        {
            "title": "Market Opportunity in India & GTM Strategy",
            "subtitle": "Capturing the Rapidly Growing Institutional Catering Market",
            "badge": "MARKET & GTM",
            "left_points": [
                "TAM: INR 35,000 Cr Commercial Mess & Kitchen Management Market in India",
                "SAM: INR 3,200 Cr Institutional Mess Analytics Market in Tier-1 & Tier-2 Cities",
                "SOM: INR 85 Cr Higher Ed & IT Park Cafeterias in key hubs (Bengaluru, Hyderabad, NCR)"
            ],
            "right_points": [
                "Enterprise Distribution: Direct partnerships with catering giants (Sodexo India, Compass Group)",
                "Campus Green Initiatives: University Mess Committee referral pilots",
                "IBM Ecosystem Acceleration: Showcased via IBM Sustainability & SkillsBuild networks"
            ],
            "script": "The market opportunity in India is expanding rapidly due to rising food inflation and corporate ESG mandates. Our serviceable market includes over 25,000 university messes and corporate cafeterias. Our go-to-market strategy focuses on partnering directly with major foodservice management contractors like Sodexo India and Compass Group India."
        },
        {
            "title": "Product Roadmap & Scalability Milestones",
            "subtitle": "Clear Execution Path from Masterclass Prototype to Commercial Scale",
            "badge": "ROADMAP",
            "left_points": [
                "Q1 (Current Phase): Core YOLOv8 Indian dataset & Multi-Agent prototype (IBM Masterclass 5)",
                "Q2 (Pilot Deployment): Launch 3 live campus mess pilots in higher ed dining halls",
                "Q3 (Enterprise Integration): Bidirectional ERP connectors for SAP and Tally Enterprise"
            ],
            "right_points": [
                "Q4 (Market Scaling): Commercial SaaS rollout across 50 mess accounts in Bengaluru & NCR",
                "Continuous AI Fine-Tuning: Expanding dataset coverage to regional South/East Indian dishes",
                "Hardware Optimization: Low-cost turnkey camera kit for plug-and-play installation"
            ],
            "script": "Having built our core prototype during the IBM SkillsBuild Masterclass, our next step is deploying live pilot stations across three university messes in Q2. In Q3, we will launch bidirectional ERP connectors for Tally Enterprise and SAP, scaling to 50 commercial mess accounts by Q4."
        },
        {
            "title": "Team Credentials & IBM Ecosystem Synergy",
            "subtitle": "Building Enterprise-Grade AI Solutions with Proven Frameworks",
            "badge": "TEAM & IBM SYNERGY",
            "left_points": [
                "Core Team Expertise: Computer Vision, Full-Stack Engineering & Sustainability Operations",
                "Built on IBM Principles: Designed following IBM Agentic AI Architecture guidelines",
                "Domain Focus: Tailored specifically for Indian institutional food service operational needs"
            ],
            "right_points": [
                "Serverless Backend: Async Python architecture ensuring high concurrency & reliability",
                "Mentorship & Guidance: Developed through IBM SkillsBuild Masterclass 5 program",
                "Ecosystem Ready: Prepared for integration with enterprise cloud platforms"
            ],
            "script": "Our team combines technical expertise in computer vision and full-stack software development with a passion for sustainability. Developing EcoPlate AI through the IBM SkillsBuild Masterclass has allowed us to implement enterprise agentic design patterns tailored for the Indian market."
        },
        {
            "title": "Conclusion & Pilot Call to Action",
            "subtitle": "Partner with EcoPlate AI to Eliminate Institutional Food Waste",
            "badge": "CALL TO ACTION",
            "left_points": [
                "Food Waste is a Solvable Data Problem: EcoPlate AI eliminates waste at the source",
                "Our 2030 Vision: Preventing 100,000+ Tons of food waste across Indian messes",
                "Financial Impact: Saving Indian institutions INR 500 Cr+ in cumulative procurement spend"
            ],
            "right_points": [
                "Now Accepting Pilot Partners: Deploy EcoPlate AI in your campus mess or corporate cafeteria",
                "Web Platform Live: http://127.0.0.1:8000",
                "Contact Email: pilots@ecoplate.ai | Website: www.ecoplate.ai"
            ],
            "script": "Food waste in Indian messes is not an inevitable loss—it is a solvable data problem. EcoPlate AI provides the real-time vision, intelligence, and autonomous workflows necessary to eliminate waste at the source. We invite pilot partners, university mess committees, and mentors to join us in bringing EcoPlate AI to kitchens across India. Thank you!"
        }
    ]
    build_pptx("PowerPoint_Presentation.pptx", pptx_slides)

    # 5. BUILD PRINTABLE HTML FILES FOR INSTANT PDF BROWSER PRINTING
    create_printable_html_files()

    print("============================================================")
    print("  ALL SUBMISSION FILES GENERATED SUCCESSFULLY!")
    print("============================================================")

def create_printable_html_files():
    lc_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Lean Canvas - EcoPlate AI</title>
<style>
body { font-family: Arial, sans-serif; padding: 20px; background: #fff; color: #111; }
h1 { color: #059669; text-align: center; margin-bottom: 5px; }
.sub { text-align: center; font-size: 14px; color: #666; margin-bottom: 20px; }
.canvas-grid { display: grid; grid-template-columns: repeat(5, 1fr); border: 2px solid #111; gap: 0; }
.box { border: 1px solid #111; padding: 10px; font-size: 11px; }
.box h4 { margin: 0 0 5px 0; font-size: 12px; color: #059669; text-transform: uppercase; }
.box ul { padding-left: 15px; margin: 0; }
</style>
</head>
<body>
<h1>EcoPlate AI: Food Waste Intelligence Agent</h1>
<div class="sub">Deliverable 1: Lean Canvas (India Region - INR Currency) | UN SDG 12</div>
<div class="canvas-grid">
  <div class="box" style="grid-row: span 2;">
    <h4>1. Problem</h4>
    <p><strong>Top Problems:</strong></p>
    <ul>
      <li>High Food Waste in Indian Messes (25-35% daily waste).</li>
      <li>Lack of Itemized Disposal Data (no dish-level tracking).</li>
      <li>Financial loss (INR 2L-5L/mo) & landfill methane.</li>
    </ul>
    <p><strong>Alternatives:</strong> Paper registers, basic scales.</p>
  </div>
  <div class="box">
    <h4>4. Solution</h4>
    <ul>
      <li>Edge YOLOv8 Vision Dish Classification.</li>
      <li>Autonomous Predictive Procurement Agent.</li>
      <li>Automated Kitchen & ESG Reports.</li>
    </ul>
  </div>
  <div class="box" style="grid-row: span 2;">
    <h4>3. Unique Value Prop</h4>
    <p><strong>Zero-Touch Food Waste Intelligence:</strong> Autonomous multi-agent AI that sees what Indian messes waste, predicts what they need, and cuts procurement costs by 25-30% while advancing UN SDG 12 & FSSAI compliance.</p>
  </div>
  <div class="box">
    <h4>9. Unfair Advantage</h4>
    <ul>
      <li>Proprietary Indian regional thali vision dataset.</li>
      <li>Closed-loop disposal-to-PO multi-agent feedback.</li>
    </ul>
  </div>
  <div class="box" style="grid-row: span 2;">
    <h4>2. Customer Segments</h4>
    <ul>
      <li>Indian University Messes.</li>
      <li>Corporate IT Parks.</li>
      <li>Hospital Messes.</li>
    </ul>
    <p><strong>Early Adopters:</strong> Top campuses with Zero-Waste goals, corporate BRSR reporting.</p>
  </div>
  <div class="box">
    <h4>8. Key Metrics</h4>
    <ul>
      <li>Kg Organic Waste Saved.</li>
      <li>Monthly INR Savings (INR 1.5L-4.5L).</li>
      <li>Vision Accuracy (>94%).</li>
    </ul>
  </div>
  <div class="box">
    <h4>5. Channels</h4>
    <ul>
      <li>Enterprise Sales (Sodexo/Compass).</li>
      <li>IBM Ecosystem.</li>
      <li>Higher Ed Summits.</li>
    </ul>
  </div>
  <div class="box" style="grid-column: span 2;">
    <h4>7. Cost Structure</h4>
    <ul>
      <li>Edge Devices (INR 15k-25k/unit).</li>
      <li>Serverless Cloud Hosting & LLM APIs.</li>
      <li>Dataset R&D & Field Operations.</li>
    </ul>
  </div>
  <div class="box" style="grid-column: span 3;">
    <h4>6. Revenue Streams</h4>
    <ul>
      <li>B2B SaaS Subscription: INR 25,000 - INR 60,000 / mess / month.</li>
      <li>Hardware & Setup Fee: INR 85,000 - INR 1,80,000 upfront per smart bin.</li>
      <li>Enterprise Integration Fee: INR 3,50,000+ (SAP/Tally).</li>
    </ul>
  </div>
</div>
</body>
</html>"""
    with open("1_Lean_Canvas_Printable.html", "w", encoding="utf-8") as f:
        f.write(lc_html)

if __name__ == '__main__':
    generate_all_submission_files()
