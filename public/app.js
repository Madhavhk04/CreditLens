/* ==========================================================================
   CREDITLENS INSTITUTIONAL APPLICATION ENGINE (V3 REVISION)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  initStressTester();
  initUnderwritingSimulator();
  initVintageSimulator();
  initRiskQueueController();
  initCollectionsBudgetSimulator();
  initGeoThresholdController();
  
  // Render Chart.js visual engines with authored sweep animation
  renderChartsPage1();
  renderChartsPage2();
  renderChartsPage3();
  renderChartsPage4();
  renderChartsPage5();
  renderChartsPage6();
});

/* ==========================================================================
   1. ANIMATED NUMBER INTERPOLATION HELPER (RAF TWEEN)
   ========================================================================== */
function tweenNumber(element, startVal, endVal, durationMs, formatFn) {
  if (!element) return;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / durationMs, 1);
    
    // Easing: Ease Out Quad
    const easeProgress = 1 - (1 - progress) * (1 - progress);
    const currentVal = startVal + (endVal - startVal) * easeProgress;

    element.textContent = formatFn ? formatFn(currentVal) : currentVal.toFixed(2);

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

/* ==========================================================================
   2. TAB NAVIGATION SYSTEM
   ========================================================================== */
function initNavigation() {
  const navBtns = document.querySelectorAll(".nav-btn");
  const pages = document.querySelectorAll(".view-page");
  const viewTitle = document.getElementById("active-view-title");

  const titles = {
    overview: "Executive Portfolio Overview",
    funnel: "Underwriting Funnel & Pipeline Throughput",
    portfolio: "Portfolio Maturities & Vintage Delinquency",
    risk: "Delinquency Segmentation & Action Queue",
    collections: "Collections Efficacy & Outreach Strategy",
    geography: "Geographic Concentration & Loss Heatmap"
  };

  navBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const pageId = btn.getAttribute("data-page");

      navBtns.forEach(b => {
        b.classList.remove("active");
        b.removeAttribute("aria-current");
      });
      btn.classList.add("active");
      btn.setAttribute("aria-current", "page");

      pages.forEach(p => p.classList.remove("active"));
      const targetPage = document.getElementById(`page-${pageId}`);
      if (targetPage) {
        targetPage.classList.add("active");
      }

      if (viewTitle && titles[pageId]) {
        viewTitle.textContent = titles[pageId];
      }
    });
  });
}

/* ==========================================================================
   3. INTERACTIVE CREDIT STRESS TESTER (LIVE DRAGGING RAF INTERPOLATION)
   ========================================================================== */
let currentSimVal = 145.2;
let currentSimNpl = 1.10;

function initStressTester() {
  const slider = document.getElementById("slider-cibil");
  const lblCutoff = document.getElementById("val-cibil-cutoff");
  const elPortfolioVal = document.getElementById("sim-portfolio-val");
  const elNplRate = document.getElementById("sim-npl-rate");

  if (!slider) return;

  function updateValues(cutoff) {
    lblCutoff.textContent = cutoff;

    // Calculate dynamic values
    const targetVal = Math.max(85.0, 145.2 - ((cutoff - 600) / 250.0) * 45.0);
    let targetNpl = 1.10;
    if (cutoff > 600) {
      targetNpl = Math.max(0.15, 1.10 - ((cutoff - 600) / 250.0) * 0.95);
    } else {
      targetNpl = Math.min(4.50, 1.10 + ((600 - cutoff) / 300.0) * 3.4);
    }

    // Live continuous RAF tween
    tweenNumber(elPortfolioVal, currentSimVal, targetVal, 150, (v) => `$${v.toFixed(1)}M`);
    currentSimVal = targetVal;

    tweenNumber(elNplRate, currentSimNpl, targetNpl, 150, (v) => `${v.toFixed(2)}%`);
    currentSimNpl = targetNpl;

    // Toggle Alert Color
    if (targetNpl > 2.0) {
      elNplRate.className = "mono-val-md color-alert";
    } else {
      elNplRate.className = "mono-val-md color-health";
    }
  }

  slider.addEventListener("input", (e) => {
    updateValues(parseInt(e.target.value, 10));
  });
}

/* ==========================================================================
   4. UNDERWRITING SIMULATOR
   ========================================================================== */
function initUnderwritingSimulator() {
  const sliderInc = document.getElementById("slider-income");
  const sliderCibil = document.getElementById("slider-funnel-cibil");
  const lblInc = document.getElementById("val-income");
  const lblCibil = document.getElementById("val-funnel-cibil");
  const elAppRate = document.getElementById("sim-app-rate");
  const elDeclines = document.getElementById("sim-declines");

  if (!sliderInc || !sliderCibil) return;

  function update() {
    const inc = parseInt(sliderInc.value, 10);
    const cibil = parseInt(sliderCibil.value, 10);
    lblInc.textContent = inc.toLocaleString();
    lblCibil.textContent = cibil;

    const incRatio = (inc - 10000) / 90000.0;
    const cibilRatio = (cibil - 300) / 600.0;
    const appRate = Math.max(5.0, Math.min(95.0, 42.5 * (1 - cibilRatio * 0.45 - incRatio * 0.15)));
    const declines = Math.round(250000 * (1 - (appRate / 100.0)));

    elAppRate.textContent = `${appRate.toFixed(1)}%`;
    elDeclines.textContent = declines.toLocaleString();
  }

  sliderInc.addEventListener("input", update);
  sliderCibil.addEventListener("input", update);
}

/* ==========================================================================
   5. VINTAGE STRESS SIMULATOR
   ========================================================================== */
let vintageChartInstance = null;

function initVintageSimulator() {
  const selectCohort = document.getElementById("select-cohort");
  const sliderStress = document.getElementById("slider-stress-mult");
  const lblStress = document.getElementById("val-stress-mult");

  if (!sliderStress || !selectCohort) return;

  function update() {
    const mult = parseFloat(sliderStress.value);
    lblStress.textContent = `${mult.toFixed(1)}x`;

    if (vintageChartInstance) {
      const cohort = selectCohort.value;
      let v_jan = [0.0, 0.1, 0.3, 0.6, 0.9, 1.2, 1.5, 1.7, 1.9, 2.1, 2.3, 2.4, 2.4];
      let v_feb = [0.0, 0.05, 0.2, 0.4, 0.7, 0.95, 1.1, 1.2, 1.3, 1.4, 1.5, 1.5, 1.6];
      let v_mar = [0.0, 0.15, 0.45, 0.9, 1.4, 1.8, 2.2, 2.5, 2.9, 3.2, 3.6, 3.8, 3.9];

      if (cohort === "Cohort Jan 25") v_jan = v_jan.map(v => v * mult);
      if (cohort === "Cohort Feb 25") v_feb = v_feb.map(v => v * mult);
      if (cohort === "Cohort Mar 25") v_mar = v_mar.map(v => v * mult);

      vintageChartInstance.data.datasets[0].data = v_jan;
      vintageChartInstance.data.datasets[1].data = v_feb;
      vintageChartInstance.data.datasets[2].data = v_mar;
      vintageChartInstance.update();
    }
  }

  sliderStress.addEventListener("input", update);
  selectCohort.addEventListener("change", update);
}

/* ==========================================================================
   6. RISK QUEUE CONTROLLER
   ========================================================================== */
const sampleQueueData = [
  { custId: "CUST-8821", cibil: 540, loanId: "LN-9012", inst: "$1,450", dpd: 65, tier: "Subprime" },
  { custId: "CUST-7743", cibil: 580, loanId: "LN-8834", inst: "$2,100", dpd: 45, tier: "Subprime" },
  { custId: "CUST-6612", cibil: 610, loanId: "LN-7721", inst: "$980", dpd: 35, tier: "Near Prime" },
  { custId: "CUST-5541", cibil: 520, loanId: "LN-6643", inst: "$3,400", dpd: 85, tier: "Subprime" },
  { custId: "CUST-4439", cibil: 630, loanId: "LN-5512", inst: "$1,850", dpd: 40, tier: "Near Prime" },
  { custId: "CUST-3310", cibil: 590, loanId: "LN-4489", inst: "$1,200", dpd: 75, tier: "Subprime" }
];

function initRiskQueueController() {
  const sliderDpd = document.getElementById("slider-min-dpd");
  const lblDpd = document.getElementById("val-min-dpd");
  const tableBody = document.querySelector("#table-queue tbody");

  if (!sliderDpd || !tableBody) return;

  function renderTable(minDpd) {
    tableBody.innerHTML = "";
    const filtered = sampleQueueData.filter(item => item.dpd >= minDpd);
    filtered.forEach(row => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="font-medium">${row.custId}</td>
        <td>${row.cibil}</td>
        <td>${row.loanId}</td>
        <td>${row.inst}</td>
        <td class="color-alert font-bold">${row.dpd} DPD</td>
        <td><span class="risk-badge ${row.tier === 'Subprime' ? 'badge-crimson' : 'badge-amber'}">${row.tier}</span></td>
      `;
      tableBody.appendChild(tr);
    });
  }

  sliderDpd.addEventListener("input", (e) => {
    const val = parseInt(e.target.value, 10);
    lblDpd.textContent = val;
    renderTable(val);
  });

  renderTable(30);
}

/* ==========================================================================
   7. COLLECTIONS BUDGET SIMULATOR
   ========================================================================== */
function initCollectionsBudgetSimulator() {
  const sliderSms = document.getElementById("slider-sms");
  const sliderCall = document.getElementById("slider-call");
  const lblSms = document.getElementById("val-sms");
  const lblCall = document.getElementById("val-call");
  const lblLegal = document.getElementById("val-legal");
  const elRec = document.getElementById("sim-recoveries");

  if (!sliderSms || !sliderCall) return;

  function update() {
    const sms = parseInt(sliderSms.value, 10);
    const call = parseInt(sliderCall.value, 10);
    const legal = Math.max(0, 100 - sms - call);

    lblSms.textContent = `${sms}%`;
    lblCall.textContent = `${call}%`;
    lblLegal.textContent = `${legal}%`;

    const base = 8.4;
    const est = base * (1.0 + (sms / 100.0) * 0.05 + (call / 100.0) * 0.12 + (legal / 100.0) * 0.22);
    elRec.textContent = `$${est.toFixed(2)}M`;
  }

  sliderSms.addEventListener("input", update);
  sliderCall.addEventListener("input", update);
}

/* ==========================================================================
   8. GEOGRAPHIC THRESHOLD CONTROLLER
   ========================================================================== */
let geoChartInstance = null;

function initGeoThresholdController() {
  const sliderGeo = document.getElementById("slider-geo-thresh");
  const lblGeo = document.getElementById("val-geo-thresh");

  if (!sliderGeo) return;

  sliderGeo.addEventListener("input", (e) => {
    const thresh = parseFloat(e.target.value);
    lblGeo.textContent = `${thresh.toFixed(1)}%`;

    if (geoChartInstance) {
      const dataVals = geoChartInstance.data.datasets[0].data;
      const colors = dataVals.map(v => v > thresh ? "#dc2626" : "#059669");
      geoChartInstance.data.datasets[0].backgroundColor = colors;
      geoChartInstance.update();
    }
  });
}

/* ==========================================================================
   CHART.JS CONFIGURATION & RENDERING ENGINES
   ========================================================================== */
const commonChartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: "#cbd5e1",
        font: { family: "IBM Plex Sans", size: 11 }
      }
    }
  },
  scales: {
    x: {
      grid: { color: "#1e293b" },
      ticks: { color: "#64748b", font: { family: "JetBrains Mono", size: 10.5 } }
    },
    y: {
      grid: { color: "#1e293b" },
      ticks: { color: "#64748b", font: { family: "JetBrains Mono", size: 10.5 } }
    }
  }
};

// Page 1 Charts
function renderChartsPage1() {
  const ctxChannel = document.getElementById("chart-channel")?.getContext("2d");
  if (ctxChannel) {
    new Chart(ctxChannel, {
      type: "doughnut",
      data: {
        labels: ["Organic Search", "Direct Branch", "Partner Digital", "Referral"],
        datasets: [{
          data: [4200, 3100, 2400, 1800],
          backgroundColor: ["#2563eb", "#06b6d4", "#f59e0b", "#059669"],
          borderWidth: 1,
          borderColor: "#121824"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "68%",
        animation: {
          animateRotate: true,
          animateScale: true,
          duration: 900
        },
        plugins: {
          legend: { position: "right", labels: { color: "#cbd5e1", font: { family: "IBM Plex Sans", size: 11 } } }
        }
      }
    });
  }

  const ctxRiskTier = document.getElementById("chart-risktier")?.getContext("2d");
  if (ctxRiskTier) {
    new Chart(ctxRiskTier, {
      type: "bar",
      data: {
        labels: ["Subprime", "Near Prime", "Prime", "Super Prime"],
        datasets: [{
          label: "Outstanding Balance ($M)",
          data: [28.4, 45.2, 51.0, 20.6],
          backgroundColor: ["#dc2626", "#f59e0b", "#2563eb", "#059669"],
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: "y",
        ...commonChartDefaults
      }
    });
  }
}

// Page 2 Charts
function renderChartsPage2() {
  const ctxFunnel = document.getElementById("chart-funnel")?.getContext("2d");
  if (ctxFunnel) {
    new Chart(ctxFunnel, {
      type: "bar",
      data: {
        labels: ["1. Applied", "2. KYC Passed", "3. Verified", "4. Approved", "5. Disbursed"],
        datasets: [{
          label: "Applications Count",
          data: [250000, 212500, 150000, 106250, 100000],
          backgroundColor: ["#2563eb", "#06b6d4", "#059669", "#f59e0b", "#64748b"],
          borderRadius: 4
        }]
      },
      options: commonChartDefaults
    });
  }

  const ctxRejections = document.getElementById("chart-rejections")?.getContext("2d");
  if (ctxRejections) {
    new Chart(ctxRejections, {
      type: "bar",
      data: {
        labels: ["CIBIL Below Threshold", "High Debt Cover Ratio", "Unverified Income", "Employer Fail", "Doc Mismatch"],
        datasets: [{
          label: "Declines",
          data: [60500, 38200, 24100, 14200, 6750],
          backgroundColor: "#dc2626",
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: "y",
        ...commonChartDefaults
      }
    });
  }
}

// Page 3 Charts
function renderChartsPage3() {
  const ctxVintage = document.getElementById("chart-vintage")?.getContext("2d");
  if (ctxVintage) {
    vintageChartInstance = new Chart(ctxVintage, {
      type: "line",
      data: {
        labels: ["MOB 0", "MOB 1", "MOB 2", "MOB 3", "MOB 4", "MOB 5", "MOB 6", "MOB 7", "MOB 8", "MOB 9", "MOB 10", "MOB 11", "MOB 12"],
        datasets: [
          { label: "Cohort Jan 25", data: [0.0, 0.1, 0.3, 0.6, 0.9, 1.2, 1.5, 1.7, 1.9, 2.1, 2.3, 2.4, 2.4], borderColor: "#059669", tension: 0.3 },
          { label: "Cohort Feb 25", data: [0.0, 0.05, 0.2, 0.4, 0.7, 0.95, 1.1, 1.2, 1.3, 1.4, 1.5, 1.5, 1.6], borderColor: "#2563eb", tension: 0.3 },
          { label: "Cohort Mar 25 (Alert)", data: [0.0, 0.15, 0.45, 0.9, 1.4, 1.8, 2.2, 2.5, 2.9, 3.2, 3.6, 3.8, 3.9], borderColor: "#dc2626", borderDash: [5, 5], tension: 0.3 }
        ]
      },
      options: commonChartDefaults
    });
  }

  const ctxRepay = document.getElementById("chart-repay")?.getContext("2d");
  if (ctxRepay) {
    new Chart(ctxRepay, {
      type: "bar",
      data: {
        labels: ["Inst 1", "Inst 2", "Inst 3", "Inst 4", "Inst 5", "Inst 6", "Inst 7", "Inst 8", "Inst 9", "Inst 10", "Inst 11", "Inst 12"],
        datasets: [
          { label: "Scheduled Dues ($M)", data: [12.4, 12.4, 12.4, 12.4, 12.4, 12.4, 12.4, 12.4, 12.4, 12.4, 12.4, 12.4], backgroundColor: "#2563eb" },
          { label: "Actual Collected ($M)", data: [12.2, 12.1, 11.9, 11.7, 11.5, 11.2, 11.1, 10.9, 10.8, 10.7, 10.5, 10.4], backgroundColor: "#059669" }
        ]
      },
      options: commonChartDefaults
    });
  }
}

// Page 4 Charts
function renderChartsPage4() {
  const ctxHeatmap = document.getElementById("chart-heatmap")?.getContext("2d");
  if (ctxHeatmap) {
    new Chart(ctxHeatmap, {
      type: "bar",
      data: {
        labels: ["Subprime (300-599)", "Near Prime (600-679)", "Prime (680-749)", "Super Prime (750+)"],
        datasets: [
          { label: "Low Income", data: [6.8, 4.2, 1.8, 0.4], backgroundColor: "#dc2626" },
          { label: "Mid Income", data: [4.5, 2.8, 1.1, 0.2], backgroundColor: "#f59e0b" },
          { label: "High Income", data: [2.9, 1.5, 0.5, 0.1], backgroundColor: "#2563eb" }
        ]
      },
      options: commonChartDefaults
    });
  }
}

// Page 5 Charts
function renderChartsPage5() {
  const ctxAgents = document.getElementById("chart-agents")?.getContext("2d");
  if (ctxAgents) {
    new Chart(ctxAgents, {
      type: "bar",
      data: {
        labels: ["Agent-101", "Agent-104", "Agent-108", "Agent-112", "Agent-115", "Agent-120"],
        datasets: [{
          label: "Amount Recovered ($k)",
          data: [840, 720, 680, 540, 490, 410],
          backgroundColor: "#2563eb",
          borderRadius: 4
        }]
      },
      options: commonChartDefaults
    });
  }

  const ctxStrat = document.getElementById("chart-strategies")?.getContext("2d");
  if (ctxStrat) {
    new Chart(ctxStrat, {
      type: "pie",
      data: {
        labels: ["SMS / Digital", "Tele-calling", "Field Visits", "Legal Escalation"],
        datasets: [{
          data: [35, 45, 12, 8],
          backgroundColor: ["#2563eb", "#06b6d4", "#f59e0b", "#dc2626"]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          animateRotate: true,
          animateScale: true,
          duration: 900
        },
        plugins: {
          legend: { position: "right", labels: { color: "#cbd5e1", font: { family: "IBM Plex Sans", size: 11 } } }
        }
      }
    });
  }
}

// Page 6 Charts
function renderChartsPage6() {
  const ctxGeoDefaults = document.getElementById("chart-geodefaults")?.getContext("2d");
  if (ctxGeoDefaults) {
    const states = ["Maharashtra", "Delhi", "Uttar Pradesh", "Karnataka", "Tamil Nadu", "Telangana", "West Bengal", "Bihar", "Madhya Pradesh", "Gujarat"];
    const defaults = [1.20, 0.95, 4.20, 0.85, 1.10, 0.70, 2.10, 3.40, 1.80, 0.90];
    const colors = defaults.map(v => v > 2.5 ? "#dc2626" : "#059669");

    geoChartInstance = new Chart(ctxGeoDefaults, {
      type: "bar",
      data: {
        labels: states,
        datasets: [{
          label: "Default Rate %",
          data: defaults,
          backgroundColor: colors,
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: "y",
        ...commonChartDefaults
      }
    });
  }

  const ctxGeoVol = document.getElementById("chart-geovolumes")?.getContext("2d");
  if (ctxGeoVol) {
    new Chart(ctxGeoVol, {
      type: "bar",
      data: {
        labels: ["Maharashtra", "Delhi", "Karnataka", "Uttar Pradesh", "Tamil Nadu", "Telangana", "Gujarat", "West Bengal", "Madhya Pradesh", "Bihar"],
        datasets: [{
          label: "Disbursed Volume ($M)",
          data: [35.4, 24.5, 21.5, 18.2, 16.4, 12.2, 11.5, 9.8, 8.4, 7.2],
          backgroundColor: "#2563eb",
          borderRadius: 4
        }]
      },
      options: commonChartDefaults
    });
  }
}
