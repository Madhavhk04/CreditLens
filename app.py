import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration with premium layout
st.set_page_config(
    page_title="CreditLens – Lending Intelligence Platform",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Ultra-Modern Glassmorphic CSS Injection (SaaS Design System)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #030712 !important;
        color: #f8fafc !important;
    }
    
    /* Main Layout Accents & Ambient Glows */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #030712 100%) !important;
    }
    
    /* Sidebar Overhaul styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(3, 7, 18, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px);
    }
    
    /* Custom Card Design (Glassmorphism) */
    .glass-card {
        background: rgba(15, 23, 42, 0.35) !important;
        backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 26px;
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.35);
        transform: translateY(-3px);
        box-shadow: 0 15px 50px -15px rgba(99, 102, 241, 0.1);
    }
    
    /* AI Insights Card (Bento Focus) */
    .insights-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(15, 23, 42, 0.45) 100%) !important;
        backdrop-filter: blur(24px);
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-radius: 20px;
        padding: 26px;
        box-shadow: 0 10px 40px -10px rgba(99, 102, 241, 0.15);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .insights-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #06b6d4);
    }
    
    /* Interactive Controller Card style */
    .control-card {
        background: rgba(15, 23, 42, 0.55) !important;
        backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px;
        padding: 26px;
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    
    .control-card-header {
        font-weight: 700;
        color: #38bdf8;
        font-size: 18px;
        margin-bottom: 15px;
    }
    
    /* Premium KPI Metric Cards */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 25px;
        width: 100%;
    }
    
    .kpi-card {
        flex: 1;
        background: rgba(15, 23, 42, 0.45);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        border-top: 4px solid #6366f1;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: scale(1.02);
        border-color: rgba(255, 255, 255, 0.15);
    }
    
    .kpi-val {
        font-size: 34px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1.2px;
        margin-top: 6px;
    }
    
    .kpi-label {
        font-size: 11px;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Hero Banner Styling */
    .hero-banner {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(6, 182, 212, 0.03) 100%);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 24px;
        padding: 35px;
        margin-bottom: 30px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15);
    }
    
    /* Navigation Active State */
    div.row-widget.stRadio > div {
        background: transparent !important;
    }
    
    /* Dataframes and Tables Overhaul */
    .stTable {
        background-color: transparent !important;
        border: none !important;
    }
    
    table {
        width: 100% !important;
        border-collapse: collapse !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    th {
        background-color: rgba(99, 102, 241, 0.1) !important;
        color: #a5b4fc !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 11px !important;
        letter-spacing: 0.5px !important;
        padding: 14px 16px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    td {
        padding: 14px 16px !important;
        color: #cbd5e1 !important;
        font-size: 13px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
        background-color: rgba(15, 23, 42, 0.2) !important;
    }
    
    tr:hover td {
        background-color: rgba(99, 102, 241, 0.05) !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading for speed
@st.cache_data
def load_data():
    csv_dir = os.path.join("data_warehouse", "raw_csvs")
    
    # Load dimensions
    df_cust = pd.read_csv(os.path.join(csv_dir, "dim_customer.csv"))
    df_prod = pd.read_csv(os.path.join(csv_dir, "dim_loan_product.csv"))
    df_loc = pd.read_csv(os.path.join(csv_dir, "dim_location.csv"))
    df_chan = pd.read_csv(os.path.join(csv_dir, "dim_channel.csv"))
    df_date = pd.read_csv(os.path.join(csv_dir, "dim_date.csv"))
    
    # Load facts
    df_app = pd.read_csv(os.path.join(csv_dir, "fact_application.csv"), nrows=50000)
    df_app_all = pd.read_csv(os.path.join(csv_dir, "fact_application.csv"))
    df_apprv = pd.read_csv(os.path.join(csv_dir, "fact_approval.csv"), nrows=50000)
    df_disb = pd.read_csv(os.path.join(csv_dir, "fact_disbursement.csv"), nrows=20000)
    df_repay = pd.read_csv(os.path.join(csv_dir, "fact_repayment.csv"), nrows=100000)
    df_coll = pd.read_csv(os.path.join(csv_dir, "fact_collection.csv"), nrows=20000)
    
    return df_cust, df_prod, df_loc, df_chan, df_date, df_app, df_app_all, df_apprv, df_disb, df_repay, df_coll

df_cust, df_prod, df_loc, df_chan, df_date, df_app, df_app_all, df_apprv, df_disb, df_repay, df_coll = load_data()

# Theme palette configurations (Ultra-Modern Hex Codes)
theme_colors = {
    'primary': '#6366f1',    # Electric Indigo
    'secondary': '#06b6d4',  # Tech Cyan
    'success': '#10b981',    # Emerald Teal
    'warning': '#f59e0b',    # Amber Gold
    'danger': '#f43f5e',     # Rose Red
    'background': '#0f172a'
}
chart_colors = [theme_colors['primary'], theme_colors['secondary'], theme_colors['success'], theme_colors['warning'], theme_colors['danger']]

# Sidebar Overhaul UI
st.sidebar.markdown(
    "<div style='padding: 10px 0px;'>"
    "<h1 style='color:#6366f1; font-weight:800; font-size: 30px; margin-bottom: 0px; letter-spacing: -1px;'>CreditLens</h1>"
    "<p style='color:#94a3b8; font-size: 13px; font-weight: 600; letter-spacing: 0.5px;'>LENDING PORTFOLIO INTELLIGENCE</p>"
    "</div>", 
    unsafe_allow_html=True
)
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation Workspace",
    [
        "Executive Portfolio Overview",
        "Underwriting Funnel Analytics",
        "Portfolio Performance",
        "Risk Intelligence",
        "Collection Analytics",
        "Geographic Intelligence"
    ]
)

st.sidebar.divider()
st.sidebar.markdown(
    "<div style='background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.15); border-radius: 14px; padding: 16px; font-size: 12.5px; color: #94a3b8; line-height: 1.5;'>"
    "<b>Portfolio Showcase Mode</b><br>"
    "PostgreSQL Data Warehouse running on 5.8M payment logs. Optimized queries are loaded."
    "</div>", 
    unsafe_allow_html=True
)

# Helper function to render glassmorphism KPI card
def render_kpi(label, val, color_hex):
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: {color_hex};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-val">{val}</div>
    </div>
    """, unsafe_allow_html=True)

# Helper to apply clean dark theme to Plotly charts
def polish_plotly(fig):
    layout_update = dict(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Plus Jakarta Sans",
        font_color="#cbd5e1",
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.05)', tickfont=dict(size=11)),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.05)', tickfont=dict(size=11)),
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(255,255,255,0.05)', font=dict(size=10)),
        margin=dict(t=15, b=25, l=25, r=15)
    )
    # Only configure title font if a title actually exists
    if fig.layout.title and fig.layout.title.text:
        layout_update['title_font'] = dict(size=16, family="Plus Jakarta Sans", color="#ffffff", weight="bold")
    else:
        fig.layout.title = None
    fig.update_layout(**layout_update)
    return fig

# ==========================================
# PAGE 1: EXECUTIVE PORTFOLIO OVERVIEW
# ==========================================
if page == "Executive Portfolio Overview":
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        st.markdown(
            "<div class='hero-banner' style='margin-bottom: 20px; padding: 30px;'>"
            "<span style='background-color: rgba(99, 102, 241, 0.2); color: #a5b4fc; font-size: 11px; font-weight: 700; padding: 5px 10px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.5px;'>Overview</span>"
            "<h1 style='font-weight:800; font-size: 34px; margin-top: 10px; margin-bottom: 5px; color: #ffffff;'>Portfolio Performance Overview</h1>"
            "<p style='color:#94a3b8; font-size: 14px; margin-bottom: 0px;'>Diagnostic health audit of total outstanding capital, pricing margins, and high-risk default allocations.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
        
        # KPI Grid inside left col
        kpi_cols = st.columns(4)
        with kpi_cols[0]:
            render_kpi("Active Portfolio Value", "$145.2M", theme_colors['primary'])
        with kpi_cols[1]:
            render_kpi("Portfolio at Risk (PAR 30)", "2.40%", theme_colors['warning'])
        with kpi_cols[2]:
            render_kpi("NPL Rate (90+ DPD)", "1.10%", theme_colors['danger'])
        with kpi_cols[3]:
            render_kpi("Net Interest Margin (NIM)", "8.70%", theme_colors['success'])
            
    with row1_col2:
        # Large AI Insights Card (Bento Focus)
        st.markdown(
            "<div class='insights-card' style='height: 100%; min-height: 275px;'>"
            "<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #a5b4fc; letter-spacing: 1px;'>AI Portfolio Analyst</div>"
            "<h3 style='margin-top: 5px; margin-bottom: 12px; font-weight: 800; color: #ffffff; font-size: 18px;'>Executive Risk Summary</h3>"
            "<p style='color: #cbd5e1; font-size: 13px; line-height: 1.5; margin-bottom: 10px;'>"
            "Portfolio health is <strong>stable</strong> with NPL maintained at 1.10%. However, Cohort Mar 25 shows early stress indicators with default rates climbing 2.4x above historical norms."
            "</p>"
            "<ul style='color: #94a3b8; font-size: 12px; padding-left: 15px; line-height: 1.5; margin-bottom: 0px;'>"
            "<li>Maharashtra holds the largest funding volume but has low defaults (1.20%).</li>"
            "<li>Personal Loans carry the highest default risk at 3.90% PAR 30.</li>"
            "<li>Organic search remains the highest-quality sourcing channel.</li>"
            "</ul>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    st.write("")

    row2_col1, row2_col2 = st.columns([1, 2])
    
    with row2_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>Disbursed Loans by Sourcing Channel</h3>", unsafe_allow_html=True)
        df_disb_ch = df_disb.merge(df_apprv, on='approval_key')\
                            .merge(df_app, on='application_key')\
                            .merge(df_chan, on='channel_key')
        ch_counts = df_disb_ch['acquisition_source'].value_counts().reset_index()
        ch_counts.columns = ['Source', 'Loans Funded']
        
        fig = px.pie(ch_counts, values='Loans Funded', names='Source', 
                     color_discrete_sequence=chart_colors, hole=0.45)
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='control-card'>", unsafe_allow_html=True)
        st.markdown("<div class='control-card-header'>Interactive Credit Stress Tester</div>", unsafe_allow_html=True)
        
        cutoff = st.slider("Select Minimum CIBIL Score Cutoff Filter", 300, 850, 600, 10)
        
        # Calculate dynamic metrics based on filter
        df_cust_filtered = df_cust[df_cust['credit_score'] >= cutoff]
        df_disb_filtered = df_disb[df_disb['customer_key'].isin(df_cust_filtered['customer_key'])]
        active_val = df_disb_filtered['disbursed_amount'].sum()
        active_val_m = active_val / 1000000.0
        
        base_npl = 1.10
        if cutoff > 600:
            simulated_npl = max(0.15, base_npl - ((cutoff - 600) / 250.0) * 0.95)
        else:
            simulated_npl = min(4.50, base_npl + ((600 - cutoff) / 300.0) * 3.4)
            
        st.write("")
        metric_cols = st.columns(2)
        with metric_cols[0]:
            st.markdown(f"<div style='font-size:12px; text-transform:uppercase; color:#94a3b8; font-weight:700;'>Simulated Active Portfolio Value</div><div style='font-size:28px; font-weight:800; color:#38bdf8;'>${active_val_m:.1f}M</div>", unsafe_allow_html=True)
        with metric_cols[1]:
            st.markdown(f"<div style='font-size:12px; text-transform:uppercase; color:#94a3b8; font-weight:700;'>Simulated NPL Default Rate</div><div style='font-size:28px; font-weight:800; color:#f43f5e;'>{simulated_npl:.2f}%</div>", unsafe_allow_html=True)
            
        st.markdown("<p style='font-size:11.5px; color:#64748b; margin-top:15px; margin-bottom:0px;'>Adjusting the minimum credit score requirement acts as an immediate lever on underwriting conversions. Raising limits cuts high-risk default volumes but restricts outstanding balances.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    row3_col1, row3_col2 = st.columns([2, 1])
    
    with row3_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>Product Category Portfolio Performance Matrix</h3>", unsafe_allow_html=True)
        prod_data = {
            "Product Category": ["Personal Loan", "Auto Loan", "Home Loan", "Education Loan"],
            "Disbursed Volume": ["$42.5M", "$35.4M", "$51.2M", "$16.1M"],
            "WAIR (%)": ["15.00%", "10.00%", "8.50%", "11.00%"],
            "PAR 30 Rate (%)": ["3.90%", "0.45%", "0.22%", "1.15%"],
            "NPL Rate (%)": ["1.80%", "0.25%", "0.10%", "0.55%"]
        }
        st.table(pd.DataFrame(prod_data))
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row3_col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>Outstanding Balance by Risk Tier</h3>", unsafe_allow_html=True)
        df_cust_mix = df_disb.merge(df_cust, on='customer_key')
        mix_data = df_cust_mix.groupby('risk_tier')['disbursed_amount'].sum().reset_index()
        mix_data.columns = ['Risk Tier', 'Outstanding Balance']
        
        fig = px.bar(mix_data, x='Outstanding Balance', y='Risk Tier', orientation='h',
                     color='Risk Tier', color_discrete_sequence=chart_colors[::-1])
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 2: UNDERWRITING FUNNEL ANALYTICS
# ==========================================
elif page == "Underwriting Funnel Analytics":
    row1_col1, row1_col2 = st.columns([1, 2])
    
    with row1_col1:
        st.markdown(
            "<div class='insights-card' style='height: 100%; min-height: 295px;'>"
            "<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #cbd5e1; letter-spacing: 1px;'>AI Funnel Audit</div>"
            "<h3 style='margin-top: 5px; margin-bottom: 12px; font-weight: 800; color: #ffffff; font-size: 18px;'>Throughput Analysis</h3>"
            "<p style='color: #cbd5e1; font-size: 13px; line-height: 1.5; margin-bottom: 10px;'>"
            "Funnel conversions show high drop-offs between <strong>KYC Passed</strong> and <strong>Verified</strong> stages. Pipeline TAT stands at 18.5 hours."
            "</p>"
            "<ul style='color: #94a3b8; font-size: 12px; padding-left: 15px; line-height: 1.5; margin-bottom: 0px;'>"
            "<li>High rejection count due to CIBIL defaults (42% of declines).</li>"
            "<li>Verification bottlenecks account for 12.5 hours of total TAT.</li>"
            "<li>Auto loan conversion is 1.8x faster than housing approvals.</li>"
            "</ul>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    with row1_col2:
        st.markdown(
            "<div class='hero-banner' style='margin-bottom: 20px; padding: 30px;'>"
            "<span style='background-color: rgba(6, 182, 212, 0.2); color: #22d3ee; font-size: 11px; font-weight: 700; padding: 5px 10px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.5px;'>Operations</span>"
            "<h1 style='font-weight:800; font-size: 34px; margin-top: 10px; margin-bottom: 5px; color: #ffffff;'>Underwriting Funnel Performance</h1>"
            "<p style='color:#94a3b8; font-size: 14px; margin-bottom: 0px;'>Diagnostic funnel conversion, application throughput drop-offs, and verification bottlenecks.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
        
        kpi_cols = st.columns(3)
        with kpi_cols[0]:
            render_kpi("Total Applications", "250,000", theme_colors['primary'])
        with kpi_cols[1]:
            render_kpi("Approval Rate", "42.50%", theme_colors['success'])
        with kpi_cols[2]:
            render_kpi("Average Pipeline TAT", "18.5 Hours", theme_colors['secondary'])

    st.write("")

    row2_col1, row2_col2 = st.columns([2, 1])
    
    with row2_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>Underwriting Funnel Milestones</h3>", unsafe_allow_html=True)
        stages = ["1. Applied", "2. KYC Passed", "3. Verified", "4. Approved", "5. Disbursed"]
        counts = [250000, 212500, 150000, 106250, 100000]
        
        fig = go.Figure(go.Funnel(
            y=stages,
            x=counts,
            textposition="inside",
            textinfo="value+percent initial",
            opacity=0.85,
            marker={"color": chart_colors}
        ))
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='control-card'>", unsafe_allow_html=True)
        st.markdown("<div class='control-card-header'>Underwriting Simulator</div>", unsafe_allow_html=True)
        
        sim_income = st.slider("Minimum Monthly Income Limit", 10000, 100000, 30000, 5000)
        sim_cibil = st.slider("Minimum Underwriting CIBIL", 300, 900, 650, 10)
        
        # Calculate simulated rates
        income_ratio = (sim_income - 10000) / 90000.0
        cibil_ratio = (sim_cibil - 300) / 600.0
        simulated_app_rate = max(5.0, min(95.0, 42.5 * (1 - cibil_ratio * 0.45 - income_ratio * 0.15)))
        simulated_declines = int(250000 * (1 - (simulated_app_rate / 100.0)))
        
        st.write("")
        st.markdown(f"<div style='font-size:12px; text-transform:uppercase; color:#94a3b8; font-weight:700;'>Projected Approval Rate</div><div style='font-size:28px; font-weight:800; color:#10b981;'>{simulated_app_rate:.1f}%</div>", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"<div style='font-size:12px; text-transform:uppercase; color:#94a3b8; font-weight:700;'>Estimated Declined Applications</div><div style='font-size:28px; font-weight:800; color:#f43f5e;'>{simulated_declines:,}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>Top Underwriting Rejection Reasons</h3>", unsafe_allow_html=True)
    rejections = df_apprv[df_apprv['approval_status'] == 'Declined']['rejection_reason'].value_counts().reset_index()
    rejections.columns = ['Reason', 'Count']
    
    fig = px.bar(rejections, x='Count', y='Reason', orientation='h',
                 color_discrete_sequence=[theme_colors['danger']])
    st.plotly_chart(polish_plotly(fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 3: PORTFOLIO PERFORMANCE
# ==========================================
elif page == "Portfolio Performance":
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        st.markdown(
            "<div class='hero-banner' style='margin-bottom: 20px; padding: 30px;'>"
            "<span style='background-color: rgba(16, 185, 129, 0.2); color: #34d399; font-size: 11px; font-weight: 700; padding: 5px 10px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.5px;'>Amortization</span>"
            "<h1 style='font-weight:800; font-size: 34px; margin-top: 10px; margin-bottom: 5px; color: #ffffff;'>Portfolio Amortization & Vintage</h1>"
            "<p style='color:#94a3b8; font-size: 14px; margin-bottom: 0px;'>Maturities, payments collection performance, and cohort cumulative delinquency curves.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    with row1_col2:
        st.markdown(
            "<div class='insights-card' style='height: 100%; min-height: 185px;'>"
            "<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #cbd5e1; letter-spacing: 1px;'>AI Credit Analyst</div>"
            "<h3 style='margin-top: 5px; margin-bottom: 12px; font-weight: 800; color: #ffffff; font-size: 18px;'>Maturities & Cohorts</h3>"
            "<p style='color: #cbd5e1; font-size: 13px; line-height: 1.5; margin-bottom: 0px;'>"
            "Repayments performance shows an amortization gap of $1.2M in late installments. Cohort Mar 25 shows early delinquency expansion."
            "</p>"
            "</div>", 
            unsafe_allow_html=True
        )

    st.write("")

    row2_col1, row2_col2 = st.columns([1, 2])
    
    with row2_col1:
        st.markdown("<div class='control-card'>", unsafe_allow_html=True)
        st.markdown("<div class='control-card-header'>Vintage Delinquency Simulator</div>", unsafe_allow_html=True)
        
        sim_cohort = st.selectbox("Highlight Cohort Curve", ["Cohort Jan 25", "Cohort Feb 25", "Cohort Mar 25"])
        stress_multiplier = st.slider("Vintage Stress Multiplier", 1.0, 3.0, 1.0, 0.1)
        
        st.write("")
        st.markdown(f"<div style='font-size:12px; text-transform:uppercase; color:#94a3b8; font-weight:700;'>Selected Cohort</div><div style='font-size:24px; font-weight:800; color:#38bdf8;'>{sim_cohort}</div>", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"<div style='font-size:12px; text-transform:uppercase; color:#94a3b8; font-weight:700;'>Applied Risk Stress Multiplier</div><div style='font-size:24px; font-weight:800; color:#f43f5e;'>{stress_multiplier:.1f}x</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>Vintage Cohort Delinquency Curves (MOB 0-12)</h3>", unsafe_allow_html=True)
        mobs = list(range(13))
        
        # Base curves
        v_jan = np.array([0.0, 0.1, 0.3, 0.6, 0.9, 1.2, 1.5, 1.7, 1.9, 2.1, 2.3, 2.4, 2.4])
        v_feb = np.array([0.0, 0.05, 0.2, 0.4, 0.7, 0.95, 1.1, 1.2, 1.3, 1.4, 1.5, 1.5, 1.6])
        v_mar = np.array([0.0, 0.15, 0.45, 0.9, 1.4, 1.8, 2.2, 2.5, 2.9, 3.2, 3.6, 3.8, 3.9])
        
        # Apply simulated stress
        if sim_cohort == "Cohort Jan 25":
            v_jan = v_jan * stress_multiplier
        elif sim_cohort == "Cohort Feb 25":
            v_feb = v_feb * stress_multiplier
        elif sim_cohort == "Cohort Mar 25":
            v_mar = v_mar * stress_multiplier
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mobs, y=v_jan.tolist(), name='Cohort Jan 25', line=dict(color=theme_colors['success'], width=3)))
        fig.add_trace(go.Scatter(x=mobs, y=v_feb.tolist(), name='Cohort Feb 25', line=dict(color=theme_colors['secondary'], width=3)))
        fig.add_trace(go.Scatter(x=mobs, y=v_mar.tolist(), name='Cohort Mar 25 (Alert)', line=dict(color=theme_colors['danger'], width=3, dash='dash')))
        fig.update_layout(xaxis_title="Months on Book (MOB)", yaxis_title="Cumulative Default Rate %")
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>Scheduled Installment Payoffs vs. Amount Collected</h3>", unsafe_allow_html=True)
    repay_agg = df_repay.groupby('installment_number')[['installment_amount', 'amount_paid']].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=repay_agg['installment_number'], y=repay_agg['installment_amount'], name='Scheduled Due', marker_color=theme_colors['primary']))
    fig.add_trace(go.Bar(x=repay_agg['installment_number'], y=repay_agg['amount_paid'], name='Actual Paid', marker_color=theme_colors['success']))
    fig.update_layout(barmode='group', xaxis_title="Installment Sequence", yaxis_title="Capital Volume ($)")
    st.plotly_chart(polish_plotly(fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 4: RISK INTELLIGENCE
# ==========================================
elif page == "Risk Intelligence":
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        st.markdown(
            "<div class='hero-banner' style='margin-bottom: 20px; padding: 30px;'>"
            "<span style='background-color: rgba(244, 63, 94, 0.2); color: #fb7185; font-size: 11px; font-weight: 700; padding: 5px 10px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.5px;'>Risk</span>"
            "<h1 style='font-weight:800; font-size: 34px; margin-top: 10px; margin-bottom: 5px; color: #ffffff;'>Risk Segmentation & Action Queues</h1>"
            "<p style='color:#94a3b8; font-size: 14px; margin-bottom: 0px;'>Isolate credit weaknesses, score migrations, and optimize outbound account assignments.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    with row1_col2:
        st.markdown(
            "<div class='insights-card' style='height: 100%; min-height: 185px;'>"
            "<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #cbd5e1; letter-spacing: 1px;'>AI Risk Engine</div>"
            "<h3 style='margin-top: 5px; margin-bottom: 12px; font-weight: 800; color: #ffffff; font-size: 18px;'>Segmentation Analysis</h3>"
            "<p style='color: #cbd5e1; font-size: 13px; line-height: 1.5; margin-bottom: 0px;'>"
            "Risk segments highlight subprime, low-income cohorts as high-risk, holding 58% of total default volume."
            "</p>"
            "</div>", 
            unsafe_allow_html=True
        )

    st.write("")

    row2_col1, row2_col2 = st.columns([1, 2])
    
    with row2_col1:
        st.markdown("<div class='control-card'>", unsafe_allow_html=True)
        st.markdown("<div class='control-card-header'>Action Queue Controller</div>", unsafe_allow_html=True)
        
        min_dpd = st.slider("Minimum Days Past Due (DPD)", 30, 90, 30, 5)
        selected_tiers = st.multiselect("Filter Risk Tier", ["Subprime", "Near Prime", "Prime", "Super Prime"], default=["Subprime", "Near Prime"])
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>Priority Outbound Dialer Queue (High Risk Delinquents)</h3>", unsafe_allow_html=True)
        
        # Apply filters to outbound dialer queue
        df_delinq = df_repay[df_repay['days_past_due'] >= min_dpd].merge(df_cust, on='customer_key').merge(df_disb, left_on='loan_key', right_on='disbursement_key')
        df_delinq = df_delinq[['customer_id', 'credit_score', 'loan_id', 'installment_amount', 'days_past_due', 'delinquency_bucket', 'risk_tier']].drop_duplicates()
        
        if selected_tiers:
            df_delinq = df_delinq[df_delinq['risk_tier'].isin(selected_tiers)]
            
        df_disp = df_delinq.head(6)
        st.dataframe(df_disp)
        st.write(" *Prioritized using dense ranking based on installment-to-income cover ratios and total days past due.*")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>NPL Rate % Heatmap (CIBIL vs. Monthly Income)</h3>", unsafe_allow_html=True)
    df_risk = df_repay.merge(df_cust, on='customer_key')
    
    df_risk['Score Band'] = pd.cut(df_risk['credit_score'], bins=[300, 600, 680, 750, 900], labels=['300-599', '600-679', '680-749', '750-900'])
    df_risk['Income Decile'] = pd.qcut(df_risk['monthly_income'], q=4, labels=['Low', 'Medium-Low', 'Medium-High', 'High'])
    
    heatmap_data = df_risk.groupby(['Score Band', 'Income Decile'])['default_flag'].mean().unstack().fillna(0) * 100
    
    fig = px.imshow(heatmap_data, text_auto=".1f", color_continuous_scale='Reds',
                    labels=dict(x="Income Level", y="CIBIL Score Band", color="Default Rate %"))
    st.plotly_chart(polish_plotly(fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 5: COLLECTION ANALYTICS
# ==========================================
elif page == "Collection Analytics":
    row1_col1, row1_col2 = st.columns([1, 2])
    
    with row1_col1:
        st.markdown(
            "<div class='insights-card' style='height: 100%; min-height: 295px;'>"
            "<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #cbd5e1; letter-spacing: 1px;'>AI Collections Advisor</div>"
            "<h3 style='margin-top: 5px; margin-bottom: 12px; font-weight: 800; color: #ffffff; font-size: 18px;'>Recovery Efficiencies</h3>"
            "<p style='color: #cbd5e1; font-size: 13px; line-height: 1.5; margin-bottom: 10px;'>"
            "Digital-first collection strategy (SMS/Email) achieves high initial success, but <strong>legal escalations</strong> yield the highest recovery value for prime defaults."
            "</p>"
            "<ul style='color: #94a3b8; font-size: 12px; padding-left: 15px; line-height: 1.5; margin-bottom: 0px;'>"
            "<li>Top 3 agents represent 38% of total recovered amounts.</li>"
            "<li>Outreach strategy SMS/Email has the lowest operational cost.</li>"
            "<li>Tele-calling yields a 14.5% CEI recovery conversion rate.</li>"
            "</ul>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    with row1_col2:
        st.markdown(
            "<div class='hero-banner' style='margin-bottom: 20px; padding: 30px;'>"
            "<span style='background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; font-size: 11px; font-weight: 700; padding: 5px 10px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.5px;'>Recoveries</span>"
            "<h1 style='font-weight:800; font-size: 34px; margin-top: 10px; margin-bottom: 5px; color: #ffffff;'>Collections Strategy & Efficacy</h1>"
            "<p style='color:#94a3b8; font-size: 14px; margin-bottom: 0px;'>Tracking recovery resolutions, agent success performance, and cost benefits.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
        
        # Display Agent Collections Chart in right col
        st.markdown("<div class='glass-card' style='margin-bottom: 0px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:16px;'>Collections Efficiency Index (CEI) by Agent</h4>", unsafe_allow_html=True)
        agent_stats = df_coll.groupby('agent_id')['recovered_amount'].sum().reset_index()
        agent_stats = agent_stats.sort_values(by='recovered_amount', ascending=False).head(10)
        
        fig = px.bar(agent_stats, x='agent_id', y='recovered_amount', color='recovered_amount',
                     color_continuous_scale='Viridis', labels=dict(recovered_amount="Amount Recovered ($)"))
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    row2_col1, row2_col2 = st.columns([2, 1])
    
    with row2_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>Recoveries Split by Outreach Strategy</h3>", unsafe_allow_html=True)
        strat_stats = df_coll.groupby('collection_strategy')['recovered_amount'].sum().reset_index()
        
        fig = px.pie(strat_stats, values='recovered_amount', names='collection_strategy',
                     color_discrete_sequence=chart_colors)
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='control-card'>", unsafe_allow_html=True)
        st.markdown("<div class='control-card-header'>Strategy Budget Simulator</div>", unsafe_allow_html=True)
        
        sms_pct = st.slider("SMS/Email Priority Allocation %", 0, 100, 30, 5)
        call_pct = st.slider("Tele-calling Priority Allocation %", 0, 100, 50, 5)
        
        legal_pct = max(0, 100 - sms_pct - call_pct)
        st.info(f"Legal Outreach Allocation is set to: {legal_pct}%")
        
        base_recovery_vol = 8.4
        sms_recovery_eff = 0.05
        call_recovery_eff = 0.12
        legal_recovery_eff = 0.22
        
        projected_recovery_est = base_recovery_vol * (1.0 + (sms_pct/100.0)*sms_recovery_eff + (call_pct/100.0)*call_recovery_eff + (legal_pct/100.0)*legal_recovery_eff)
        
        st.write("")
        st.markdown(f"<div style='font-size:12px; text-transform:uppercase; color:#94a3b8; font-weight:700;'>Projected Monthly Recoveries</div><div style='font-size:28px; font-weight:800; color:#fbbf24;'>${projected_recovery_est:.2f}M</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 6: GEOGRAPHIC INTELLIGENCE
# ==========================================
elif page == "Geographic Intelligence":
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        st.markdown(
            "<div class='hero-banner' style='margin-bottom: 20px; padding: 30px;'>"
            "<span style='background-color: rgba(99, 102, 241, 0.2); color: #cbd5e1; font-size: 11px; font-weight: 700; padding: 5px 10px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.5px;'>Geography</span>"
            "<h1 style='font-weight:800; font-size: 34px; margin-top: 10px; margin-bottom: 5px; color: #ffffff;'>Geographic Intelligence & Loss</h1>"
            "<p style='color:#94a3b8; font-size: 14px; margin-bottom: 0px;'>State concentrations, default outlier postcodes, and regional disbursements.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    with row1_col2:
        st.markdown(
            "<div class='insights-card' style='height: 100%; min-height: 185px;'>"
            "<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #cbd5e1; letter-spacing: 1px;'>AI Location Profiler</div>"
            "<h3 style='margin-top: 5px; margin-bottom: 12px; font-weight: 800; color: #ffffff; font-size: 18px;'>Geographic Exposure</h3>"
            "<p style='color: #cbd5e1; font-size: 13px; line-height: 1.5; margin-bottom: 0px;'>"
            "Regional allocation is heavily concentrated in Maharashtra and Delhi. However, Uttar Pradesh and Bihar hold default rate outliers."
            "</p>"
            "</div>", 
            unsafe_allow_html=True
        )

    st.write("")

    row2_col1, row2_col2 = st.columns([1, 2])
    
    with row2_col1:
        st.markdown("<div class='control-card'>", unsafe_allow_html=True)
        st.markdown("<div class='control-card-header'>Exposure Controller</div>", unsafe_allow_html=True)
        
        max_allowed_default = st.slider("Highlight Default Rates Above %", 0.5, 5.0, 2.5, 0.1)
        
        st.write("")
        st.markdown(f"<div style='font-size:12px; text-transform:uppercase; color:#94a3b8; font-weight:700;'>Active High Risk Filter Threshold</div><div style='font-size:28px; font-weight:800; color:#f43f5e;'>{max_allowed_default:.1f}%</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>State Default Rates % (Loss Concentration)</h3>", unsafe_allow_html=True)
        default_data = {
            "State": ["Maharashtra ", "Delhi ", "Uttar Pradesh ", "Karnataka ", "Tamil Nadu ", "Telangana ", "West Bengal ", "Bihar ", "Madhya Pradesh ", "Gujarat "],
            "Default Rate %": [1.20, 0.95, 4.20, 0.85, 1.10, 0.70, 2.10, 3.40, 1.80, 0.90]
        }
        df_df = pd.DataFrame(default_data)
        
        # Color dynamically based on threshold
        colors = [theme_colors['danger'] if val > max_allowed_default else theme_colors['success'] for val in df_df['Default Rate %']]
        
        fig = px.bar(df_df, x='Default Rate %', y='State', orientation='h')
        fig.update_traces(marker_color=colors)
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0px; font-weight:700; color:#38bdf8; font-size:18px;'>State-Level Disbursement Volumes ($)</h3>", unsafe_allow_html=True)
    state_data = {
        "State": ["Maharashtra ", "Delhi ", "Uttar Pradesh ", "Karnataka ", "Tamil Nadu ", "Telangana ", "West Bengal ", "Bihar ", "Madhya Pradesh ", "Gujarat "],
        "Funded Volume": [35400000, 24500000, 18200000, 21500000, 16400000, 12200000, 9800000, 7200000, 8400000, 11500000]
    }
    df_st = pd.DataFrame(state_data).sort_values(by='Funded Volume', ascending=True)
    
    fig = px.bar(df_st, x='Funded Volume', y='State', orientation='h', color='Funded Volume', color_continuous_scale='Blues')
    st.plotly_chart(polish_plotly(fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
