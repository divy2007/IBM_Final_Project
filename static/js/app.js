// EcoPlate AI Enterprise Platform JavaScript
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initCanvas();
    fetchDashboardStats();
    fetchProcurementRecommendations();
    initRoiCalculator();

    // Event Listeners
    document.getElementById('scanBtn')?.addEventListener('click', triggerVisionScan);
    document.getElementById('runAgentsBtn')?.addEventListener('click', runMultiAgentCycle);
    document.getElementById('fetchEsgBtn')?.addEventListener('click', fetchESGReport);
});

// Tab Navigation
function initNavigation() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPages = document.querySelectorAll('.tab-page');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            tabBtns.forEach(b => b.classList.remove('active'));
            tabPages.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetTab)?.classList.add('active');

            if (targetTab === 'vision-sim') {
                drawCameraFrame();
            }
        });
    });
}

// Global Canvas State
let canvas, ctx;
let currentDetection = null;

// Standalone Indian Catalog Fallback
const MOCK_CATALOG = {
    "Paneer Butter Masala": { category: "Paneer / Protein", cost_per_kg: 360.00, co2_factor: 5.20 },
    "Steamed Basmati Rice": { category: "Rice / Carbs", cost_per_kg: 75.00, co2_factor: 2.70 },
    "Hyderabadi Chicken Biryani": { category: "Non-Veg Protein", cost_per_kg: 290.00, co2_factor: 7.40 },
    "Dal Tadka & Rajma": { category: "Pulses / Lentils", cost_per_kg: 95.00, co2_factor: 1.80 },
    "Vegetable Pulao": { category: "Rice / Carbs", cost_per_kg: 125.00, co2_factor: 2.10 }
};

let mockStats = {
    kpis: {
        total_events: 840,
        total_waste_kg: 2140.5,
        total_financial_loss: 285400.00,
        total_co2_kg: 4850.2,
        avg_vision_accuracy: 95.2,
        estimated_monthly_savings: 99890.00,
        estimated_co2_prevented: 1697.5
    },
    top_wasted_dishes: [
        { dish_name: "Steamed Basmati Rice", category: "Rice / Carbs", frequency: 240, total_kg: 680.5, total_cost: 51037.50 },
        { dish_name: "Paneer Butter Masala", category: "Paneer / Protein", frequency: 135, total_kg: 410.0, total_cost: 147600.00 },
        { dish_name: "Dal Tadka & Rajma", category: "Pulses / Lentils", frequency: 210, total_kg: 490.2, total_cost: 46569.00 },
        { dish_name: "Hyderabadi Chicken Biryani", category: "Non-Veg Protein", frequency: 95, total_kg: 280.0, total_cost: 81200.00 },
        { dish_name: "Vegetable Pulao", category: "Rice / Carbs", frequency: 160, total_kg: 279.8, total_cost: 34975.00 }
    ],
    category_breakdown: [
        { category: "Paneer / Protein", total_kg: 690.0, total_cost: 228800.00 },
        { category: "Rice / Carbs", total_kg: 960.3, total_cost: 86012.50 },
        { category: "Pulses / Lentils", total_kg: 490.2, total_cost: 46569.00 }
    ]
};

function initCanvas() {
    canvas = document.getElementById('visionCanvas');
    if (canvas) {
        ctx = canvas.getContext('2d');
        canvas.width = 640;
        canvas.height = 360;
        drawCameraFrame();
    }
}

// Draw simulated edge camera frame
function drawCameraFrame(detection = null) {
    if (!ctx) return;

    // Dark bin background
    ctx.fillStyle = '#0f141d';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Bin circular boundary
    ctx.beginPath();
    ctx.arc(320, 180, 150, 0, 2 * Math.PI);
    ctx.fillStyle = '#18202e';
    ctx.fill();
    ctx.strokeStyle = '#2d3748';
    ctx.lineWidth = 4;
    ctx.stroke();

    // Grid lines for edge vision sensor
    ctx.strokeStyle = 'rgba(16, 185, 129, 0.12)';
    ctx.lineWidth = 1;
    for (let x = 0; x < canvas.width; x += 40) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 40) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }

    // Default static food graphics
    drawFoodGraphic(280, 150, 70, '#d97706'); // Paneer / Curry
    drawFoodGraphic(330, 190, 50, '#fef08a'); // Rice

    // Render Detection Bounding Box if scan active
    if (detection) {
        const bbox = detection.bounding_box;
        ctx.strokeStyle = '#10b981';
        ctx.lineWidth = 2;
        ctx.strokeRect(bbox.x, bbox.y, bbox.width, bbox.height);

        // Corner accents
        const cornerSize = 12;
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(bbox.x, bbox.y + cornerSize);
        ctx.lineTo(bbox.x, bbox.y);
        ctx.lineTo(bbox.x + cornerSize, bbox.y);
        ctx.stroke();

        // Label box
        ctx.fillStyle = 'rgba(16, 185, 129, 0.9)';
        ctx.fillRect(bbox.x, bbox.y - 26, bbox.width, 24);

        ctx.fillStyle = '#000000';
        ctx.font = 'bold 12px Inter, sans-serif';
        ctx.fillText(`${detection.dish_name} [${(detection.confidence_score * 100).toFixed(1)}%]`, bbox.x + 6, bbox.y - 8);
    }
}

function drawFoodGraphic(x, y, r, color) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.strokeStyle = 'rgba(0,0,0,0.3)';
    ctx.stroke();
}

// Fetch API Statistics
async function fetchDashboardStats() {
    try {
        const res = await fetch('/api/dashboard/stats');
        const data = await res.json();
        if (data.status === 'success') {
            updateKPIs(data.kpis);
            renderDishesList(data.top_wasted_dishes);
            renderCategoryBreakdown(data.category_breakdown);
            return;
        }
    } catch (e) {}

    updateKPIs(mockStats.kpis);
    renderDishesList(mockStats.top_wasted_dishes);
    renderCategoryBreakdown(mockStats.category_breakdown);
}

function updateKPIs(kpis) {
    const lossVal = kpis.total_financial_loss || 0;
    const savVal = kpis.estimated_monthly_savings || 0;
    document.getElementById('statWeight').innerText = `${kpis.total_waste_kg} kg`;
    document.getElementById('statLoss').innerText = `₹${lossVal.toLocaleString('en-IN')}`;
    document.getElementById('statCo2').innerText = `${kpis.total_co2_kg} kg`;
    document.getElementById('statAccuracy').innerText = `${kpis.avg_vision_accuracy}%`;
    document.getElementById('statSavings').innerText = `₹${savVal.toLocaleString('en-IN')}`;
}

function renderDishesList(dishes) {
    const tbody = document.getElementById('dishesTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    dishes.forEach((d, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>#${idx + 1} ${d.dish_name}</td>
            <td><span class="badge-tag">${d.category}</span></td>
            <td>${d.total_kg} kg</td>
            <td>₹${d.total_cost.toLocaleString('en-IN')}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderCategoryBreakdown(categories) {
    const container = document.getElementById('categoryBreakdown');
    if (!container) return;
    container.innerHTML = '';
    categories.forEach(c => {
        const item = document.createElement('div');
        item.style.marginBottom = '0.8rem';
        item.innerHTML = `
            <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:0.25rem;">
                <span>${c.category}</span>
                <span style="color:var(--color-emerald); font-weight:600;">${c.total_kg} kg (₹${c.total_cost.toLocaleString('en-IN')})</span>
            </div>
            <div style="background:rgba(255,255,255,0.08); height:6px; border-radius:3px; overflow:hidden;">
                <div style="background:linear-gradient(90deg, var(--color-emerald), var(--color-cyan)); height:100%; width:${Math.min(c.total_kg * 0.1, 100)}%;"></div>
            </div>
        `;
        container.appendChild(item);
    });
}

// Trigger Live Bin Vision Scan
async function triggerVisionScan() {
    const dishSelect = document.getElementById('scanDishSelect');
    let selectedDish = dishSelect ? dishSelect.value : null;
    if (!selectedDish) {
        const keys = Object.keys(MOCK_CATALOG);
        selectedDish = keys[Math.floor(Math.random() * keys.length)];
    }

    const logBox = document.getElementById('scanLogBox');
    if (logBox) {
        logBox.innerHTML = `<div class="terminal-line"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> Edge Camera capturing mess disposal frame...</div>`;
    }

    try {
        const res = await fetch('/api/waste/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dish_name: selectedDish })
        });
        const data = await res.json();

        if (data.status === 'success') {
            const det = data.detection;
            currentDetection = det;
            drawCameraFrame(det);
            renderLog(logBox, det);
            fetchDashboardStats();
            return;
        }
    } catch (e) {}

    const info = MOCK_CATALOG[selectedDish];
    const weight = Math.round(150 + Math.random() * 450);
    const cost = Math.round((weight / 1000.0) * info.cost_per_kg * 100) / 100;
    const co2 = Math.round((weight / 1000.0) * info.co2_factor * 100) / 100;
    const conf = Math.round((0.92 + Math.random() * 0.07) * 1000) / 1000;

    const det = {
        dish_name: selectedDish,
        category: info.category,
        confidence_score: conf,
        weight_grams: weight,
        cost_inr: cost,
        co2_kg: co2,
        bounding_box: { x: 140 + Math.random() * 150, y: 120 + Math.random() * 80, width: 180, height: 140 }
    };

    drawCameraFrame(det);
    renderLog(logBox, det);

    mockStats.kpis.total_waste_kg = Math.round((mockStats.kpis.total_waste_kg + weight / 1000) * 10) / 10;
    mockStats.kpis.total_financial_loss = Math.round((mockStats.kpis.total_financial_loss + cost) * 100) / 100;
    updateKPIs(mockStats.kpis);
}

function renderLog(logBox, det) {
    if (!logBox) return;
    const costVal = det.cost_inr !== undefined ? det.cost_inr : det.cost_dollars;
    logBox.innerHTML += `
        <div class="terminal-line"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> YOLOv8 Indian Cuisine Classification: <strong>${det.dish_name}</strong></div>
        <div class="terminal-line"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> Mass Estimate: <strong>${det.weight_grams} g</strong> | Financial Impact: <strong>₹${costVal}</strong></div>
        <div class="terminal-line"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> Carbon Footprint: <strong>${det.co2_kg} kg CO2e</strong></div>
        <div class="terminal-line" style="color:var(--color-emerald)"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> Event logged to database successfully.</div>
    `;
}

// Run Multi-Agent Cycle
async function runMultiAgentCycle() {
    const term = document.getElementById('agentTerminal');
    if (!term) return;

    term.innerHTML = `<div class="terminal-line"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> Initiating Multi-Agent Synchronization for Mess Operations...</div>`;

    setTimeout(async () => {
        term.innerHTML += `<div class="terminal-line"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> 👁️ <strong>Vision Agent:</strong> Verified active telemetry streams from MESS-BIN-EDGE-01.</div>`;

        setTimeout(async () => {
            term.innerHTML += `<div class="terminal-line"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> 📊 <strong>Analytics Agent:</strong> Correlating 30-day temporal disposal patterns against weather & mess schedules.</div>`;

            setTimeout(async () => {
                term.innerHTML += `<div class="terminal-line"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> 🤖 <strong>Procurement Agent:</strong> Formulating predictive batch size scaling factors in INR (₹)...</div>`;

                try {
                    const res = await fetch('/api/agents/procurement', { method: 'POST' });
                    const data = await res.json();
                    if (data.status === 'success') {
                        term.innerHTML += `<div class="terminal-line" style="color:var(--color-emerald);"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> Multi-Agent cycle completed. Generated ${data.recommendations.length} predictive action cards in INR!</div>`;
                        renderProcurementCards(data.recommendations);
                        return;
                    }
                } catch (e) {}

                const mockRecs = [
                    { id: "REC-IND-1042", dish_name: "Steamed Basmati Rice", category: "Rice / Carbs", action_type: "Recipe Portion Scale", recommendation: "Scale back mess prep volume for 'Steamed Basmati Rice' by 20% during Thursday lunch service.", rationale: "Identified as top-discarded mess item. Scaling saves ₹18,500.00/mo.", monthly_savings_inr: 18500.00, co2_reduction_kg: 142.5 },
                    { id: "REC-IND-1043", dish_name: "Paneer Butter Masala", category: "Paneer / Protein", action_type: "Purchase Order Draft", recommendation: "Auto-generated PO #PO-IND-809: Reduced Paneer order by 15kg based on 14-day plate waste metrics.", rationale: "Prevents high monetary paneer losses during weekend mess shifts.", monthly_savings_inr: 32400.00, co2_reduction_kg: 210.0 },
                    { id: "REC-IND-1044", dish_name: "Dal Tadka & Rajma", category: "Pulses / Lentils", action_type: "Batch Prep Shift", recommendation: "Transition from single morning prep to twice-daily batch prep for Dal Tadka.", rationale: "Reduces afternoon waste by 30%.", monthly_savings_inr: 12800.00, co2_reduction_kg: 95.0 }
                ];
                term.innerHTML += `<div class="terminal-line" style="color:var(--color-emerald);"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> Multi-Agent cycle completed. Generated 3 predictive action cards in INR!</div>`;
                renderProcurementCards(mockRecs);
            }, 600);
        }, 600);
    }, 500);
}

// Fetch Procurement Recommendations
async function fetchProcurementRecommendations() {
    try {
        const res = await fetch('/api/agents/procurement', { method: 'POST' });
        const data = await res.json();
        if (data.status === 'success') {
            renderProcurementCards(data.recommendations);
            return;
        }
    } catch (e) {}

    renderProcurementCards([
        { id: "REC-IND-1042", dish_name: "Steamed Basmati Rice", category: "Rice / Carbs", action_type: "Recipe Portion Scale", recommendation: "Scale back mess prep volume for 'Steamed Basmati Rice' by 20% during Thursday lunch service.", rationale: "Identified as top-discarded mess item. Scaling saves ₹18,500.00/mo.", monthly_savings_inr: 18500.00, co2_reduction_kg: 142.5 },
        { id: "REC-IND-1043", dish_name: "Paneer Butter Masala", category: "Paneer / Protein", action_type: "Purchase Order Draft", recommendation: "Auto-generated PO #PO-IND-809: Reduced Paneer order by 15kg based on 14-day plate waste metrics.", rationale: "Prevents high monetary paneer losses during weekend mess shifts.", monthly_savings_inr: 32400.00, co2_reduction_kg: 210.0 }
    ]);
}

function renderProcurementCards(recs) {
    const container = document.getElementById('recommendationsContainer');
    if (!container) return;
    container.innerHTML = '';

    recs.forEach(r => {
        const savVal = r.monthly_savings_inr !== undefined ? r.monthly_savings_inr : r.monthly_savings_dollars;
        const card = document.createElement('div');
        card.className = 'action-card';
        card.innerHTML = `
            <div class="action-card-header">
                <div>
                    <span class="badge-tag">${r.action_type}</span>
                    <strong style="margin-left:0.5rem; font-size:1rem;">${r.dish_name}</strong>
                </div>
                <span style="color:var(--color-emerald); font-weight:700;">Save ₹${savVal.toLocaleString('en-IN')}/mo</span>
            </div>
            <p style="font-size:0.88rem; color:var(--color-text-main); margin-bottom:0.5rem;">${r.recommendation}</p>
            <p style="font-size:0.8rem; color:var(--color-text-muted);">${r.rationale}</p>
            <div style="margin-top:0.75rem; display:flex; gap:0.5rem;">
                <button class="btn-primary" style="padding:0.4rem 0.8rem; font-size:0.8rem;" onclick="approveRec('${r.id}')">Approve PO Adjustment</button>
            </div>
        `;
        container.appendChild(card);
    });
}

function approveRec(id) {
    alert(`Recommendation ${id} approved! Purchase order updated in INR.`);
}

// Fetch ESG Report
async function fetchESGReport() {
    try {
        const res = await fetch('/api/esg/report');
        const data = await res.json();
        renderESGDisplay(data);
        return;
    } catch (e) {}

    renderESGDisplay({
        report_title: "EcoPlate AI - ESG Sustainability & SDG 12 Compliance Audit (India Region)",
        audit_date: "October 08, 2026",
        framework_alignment: { un_sdg: "SDG 12: Responsible Consumption & Production", indian_compliance: "FSSAI Save Food Share Food & SEBI BRSR" },
        metrics: {
            co2_emissions_avoided_metric_tons: 1.697,
            financial_savings_inr: "₹99,890.00",
            water_footprint_saved_liters: 636500
        },
        auditor_signature: "EcoPlate Multi-Agent ESG Telemetry Engine (India Reg. Hash: #IN-8F90A-SDG12)"
    });
}

function renderESGDisplay(data) {
    const display = document.getElementById('esgReportDisplay');
    if (display) {
        const savText = data.metrics.financial_savings_inr ? data.metrics.financial_savings_inr : `₹${data.metrics.financial_savings_dollars}`;
        display.innerHTML = `
            <div class="glass-panel" style="padding:1.5rem; border-color:var(--border-glow);">
                <h3 style="color:var(--color-emerald); font-family:var(--font-heading); margin-bottom:0.5rem;">${data.report_title}</h3>
                <p style="font-size:0.85rem; color:var(--color-text-muted); margin-bottom:1rem;">Audit Date: ${data.audit_date} | ${data.framework_alignment.un_sdg}</p>
                <p style="font-size:0.8rem; color:var(--color-cyan); margin-bottom:1rem;">Framework: ${data.framework_alignment.indian_compliance || 'FSSAI & SEBI BRSR'}</p>
                
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1rem; margin-bottom:1.5rem;">
                    <div style="background:rgba(255,255,255,0.04); padding:1rem; border-radius:8px;">
                        <div style="font-size:0.75rem; color:var(--color-text-muted);">CO2e Emissions Avoided</div>
                        <div style="font-size:1.4rem; font-weight:700; color:var(--color-emerald);">${data.metrics.co2_emissions_avoided_metric_tons} Metric Tons</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.04); padding:1rem; border-radius:8px;">
                        <div style="font-size:0.75rem; color:var(--color-text-muted);">Projected Financial Savings</div>
                        <div style="font-size:1.4rem; font-weight:700; color:var(--color-cyan);">${savText}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.04); padding:1rem; border-radius:8px;">
                        <div style="font-size:0.75rem; color:var(--color-text-muted);">Embedded Water Saved</div>
                        <div style="font-size:1.4rem; font-weight:700; color:var(--color-gold);">${data.metrics.water_footprint_saved_liters.toLocaleString('en-IN')} Liters</div>
                    </div>
                </div>
                
                <div style="font-size:0.8rem; color:var(--color-text-muted); font-family:monospace;">
                    ${data.auditor_signature}
                </div>
            </div>
        `;
    }
}

// Interactive ROI Calculator Logic
function initRoiCalculator() {
    const rangeInput = document.getElementById('roiMealsRange');
    const mealsValDisplay = document.getElementById('roiMealsVal');
    const savingsValDisplay = document.getElementById('roiSavingsVal');

    if (!rangeInput || !mealsValDisplay || !savingsValDisplay) return;

    rangeInput.addEventListener('input', (e) => {
        const meals = parseInt(e.target.value);
        mealsValDisplay.innerText = `${meals.toLocaleString('en-IN')} meals/day`;

        // Calculate estimated savings: Average ₹3.50 saved per meal via food waste reduction
        const monthlySavings = Math.round(meals * 3.50 * 30);
        savingsValDisplay.innerText = `₹${monthlySavings.toLocaleString('en-IN')}`;
    });
}
