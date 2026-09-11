# CreditLens – Lending Portfolio Intelligence (V4)

**🚀 Live Demo: [https://credit-lens-5hms.vercel.app/](https://credit-lens-5hms.vercel.app/)**

<p align="center">
  <img src="https://img.shields.io/badge/Frontend-React_18-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/Build-Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/Motion-Framer_Motion-0055FF?style=for-the-badge&logo=framer&logoColor=white" alt="Framer Motion">
  <img src="https://img.shields.io/badge/Charts-Recharts_%7C_D3-FF6384?style=for-the-badge" alt="Recharts">
  <img src="https://img.shields.io/badge/Warehouse-PostgreSQL-336791?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
</p>

---

## Overview

**CreditLens V4** is an industry-grade, end-to-end data analytics and business intelligence platform built for credit risk officers, underwriters, and lending portfolio managers. 

Moving away from standard "SaaS dashboard" templates, V4 introduces a **Premium Financial Glass** aesthetic—a high-density, precision-focused interface designed for rapid scanning of complex risk metrics like PAR30, NPL migrations, and vintage delinquency stress.

## Features & Dashboards

The application is split into 6 core analytical domains:

1. **Executive Portfolio Overview:** High-level pulse on portfolio health, tracking active portfolio value, net interest margin, and core risk thresholds (PAR 30).
2. **Underwriting Funnel Analytics:** Pipeline visualization tracking conversion bottlenecks, TAT (Turnaround Time), and automated CIBIL/Income decline drivers.
3. **Portfolio Performance (Vintage):** Cohort-based asset behaviors mapping delinquency curves (MOB 0-12) and repayment amortization gaps.
4. **Risk Intelligence:** Actionable priority queues for the collections dialer based on DPD (Days Past Due) and income-decile risk heatmaps.
5. **Collection Analytics:** Agent efficacy tracking and a strategic budget simulator balancing SMS, Tele-calling, and Legal escalation recoveries.
6. **Geographic Intelligence:** State-level funding volumes and NPL concentration outliers.

---

## Technology Stack

### Frontend Application
- **Framework:** React 18 powered by Vite for instant HMR.
- **Styling:** Custom CSS Design System featuring hardware-accelerated glassmorphism, ambient glows, and a curated deep violet/amber palette.
- **Animation:** Framer Motion for highly polished interactions (number tweening, layout morphs, staggered entry reveals, and interactive slider simulations).
- **Visualization:** Recharts for complex data plotting (funnels, vintage curves) and D3.js (Shape & Interpolate) for custom SVG generation like the radial gauge.
- **Icons:** `lucide-react` for clean, monochrome iconography.

### Data Warehouse Architecture
Behind the frontend sits a theoretical star-schema PostgreSQL warehouse processing ~5.8M synthetic payment logs:
- **Dimensions:** `dim_customer`, `dim_date`, `dim_loan_product`, `dim_location`, `dim_channel`
- **Facts:** `fact_application`, `fact_approval`, `fact_disbursement`, `fact_repayment`, `fact_collection`

*(Note: The current V4 React build runs on static embedded data for immediate Vercel deployment, but is architected to plug directly into this backend warehouse via JSON APIs).*

---

## Local Development (React Frontend)

To run the React application locally:

### Prerequisites
- Node.js (v18+)
- npm or yarn

### Installation

1. **Clone the repository and install dependencies:**
   ```bash
   npm install
   ```

2. **Start the Vite development server:**
   ```bash
   npm run dev
   ```

3. **View the app:**
   Open your browser to `http://localhost:5173`

---

## Vercel Deployment

CreditLens V4 is configured as a fully static Single Page Application (SPA), making it trivial to host on Vercel:

1. Push your code to GitHub.
2. Import the repository into your Vercel account.
3. Vercel will automatically detect **Vite**.
4. Leave the default build commands (`npm run build`) and output directory (`dist`).
5. Click **Deploy**.

---

## Legacy Backend Tools

If you wish to interact with the original synthetic data generator and PostgreSQL backend:

1. Setup the Python environment: `pip install -r requirements.txt`
2. Create DB schema: `psql -h localhost -U postgres -d postgres -f data_warehouse/ddl/create_schema.sql`
3. Generate data: `python scripts/data_generator.py`
4. Upload to Postgres: `python scripts/db_uploader.py`
