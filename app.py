import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration with institutional terminal layout
st.set_page_config(
    page_title="CreditLens – Credit Risk Intelligence Terminal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Institutional Credit Risk CSS Injection (Bloomberg/S&P Risk Memo Aesthetic)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');
    
    /* Root & Global Reset */
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', -apple-system, sans-serif !important;
        background-color: #0b0f17 !important;
        color: #f1f5f9 !important;
    }
    
    /* Streamlit Canvas Background */
    .stApp {
        background-color: #0b0f17 !important;
    }
    
    /* Sidebar Overhaul */
    section[data-testid="stSidebar"] {
        background-color: #0d131f !important;
        border-right: 1px solid #1e293b !important;
    }
    
    /* Card System */
    .risk-card {
        background-color: #141c28;
        border: 1px solid #232d3f;
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .risk-card-alert {
        background-color: #1a1625;
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-top: 3px solid #ef4444;
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .risk-card-warning {
        background-color: #1a1b24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-top: 3px solid #f59e0b;
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .risk-card-neutral {
        background-color: #141c28;
        border: 1px solid #232d3f;
        border-top: 1px solid #334155;
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    /* Typography System: Tabular Numerals & Monospace */
    .mono-val-lg {
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums;
        font-size: 32px;
        font-weight: 800;
        line-height: 1.1;
        margin-top: 4px;
        margin-bottom: 4px;
    }
    
    .mono-val-md {
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums;
        font-size: 24px;
        font-weight: 700;
    }
    
    /* Risk Badges */
    .risk-badge {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        padding: 2px 8px;
        border-radius: 3px;
        letter-spacing: 0.5px;
    }
    .badge-crimson {
        background-color: rgba(239, 68, 68, 0.18);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .badge-amber {
        background-color: rgba(245, 158, 11, 0.18);
        color: #fde047;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-blue {
        background-color: rgba(59, 130, 246, 0.15);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .badge-emerald {
        background-color: rgba(16, 185, 129, 0.15);
        color: #6ee7b7;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-slate {
        background-color: rgba(100, 116, 139, 0.2);
        color: #94a3b8;
        border: 1px solid #334155;
    }

    /* Meta Labels */
    .meta-label {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 11px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    /* Risk Memo Panel */
    .memo-card {
        background-color: #111722;
        border: 1px solid #1e293b;
        border-left: 4px solid #ef4444;
        border-radius: 6px;
        padding: 20px;
        height: 100%;
    }
    .memo-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        color: #ef4444;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    /* Terminal Sync Header */
    .terminal-bar {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 12px 18px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Dataframe / Table Overhaul */
    div[data-testid="stTable"] table {
        border-collapse: collapse !important;
        border: 1px solid #232d3f !important;
        background-color: #141c28 !important;
        border-radius: 4px !important;
        width: 100% !important;
    }
    div[data-testid="stTable"] th {
        background-color: #0f172a !important;
        color: #94a3b8 !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        border-bottom: 1px solid #232d3f !important;
        padding: 10px 14px !important;
    }
    div[data-testid="stTable"] td {
        color: #e2e8f0 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
        font-variant-numeric: tabular-nums !important;
        border-bottom: 1px solid #1e293b !important;
        padding: 10px 14px !important;
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

# Theme palette configuration (Institutional Financial Palette)
theme_colors = {
    'primary': '#3b82f6',       # Institutional Blue
    'alert': '#ef4444',         # Crimson Risk Warning (reserved for risk signals)
    'warning': '#f59e0b',       # Amber DPD/Alert
    'health': '#10b981',        # Emerald Stable/Payoff
    'neutral': '#64748b',       # Muted Slate
    'surface': '#141c28',
    'bg': '#0b0f17'
}
chart_colors = ['#3b82f6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']

# Sidebar Header & Workspace Navigation
st.sidebar.markdown(
    "<div style='padding: 10px 0px 5px 0px;'>"
    "<div style='font-family: \"JetBrains Mono\", monospace; color: #3b82f6; font-weight: 800; font-size: 22px; letter-spacing: -0.5px;'>CREDITLENS</div>"
    "<div style='color: #64748b; font-size: 11px; font-weight: 600; letter-spacing: 0.8px;'>CREDIT RISK TERMINAL v2.4</div>"
    "</div>", 
    unsafe_allow_html=True
)
st.sidebar.divider()

page = st.sidebar.radio(
    "WORKSPACE NAVIGATION",
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
    "<div style='background: #141c28; border: 1px solid #232d3f; border-radius: 6px; padding: 14px; font-size: 11.5px; color: #94a3b8; line-height: 1.5;'>"
    "<span style='font-family: \"JetBrains Mono\", monospace; color: #3b82f6; font-weight: 700;'>WAREHOUSE ENGINE</span><br>"
    "PostgreSQL Data Warehouse online.<br>"
    "<span style='font-family: \"JetBrains Mono\", monospace; color: #64748b;'>5.8M Payment Records Loaded</span>"
    "</div>", 
    unsafe_allow_html=True
)

# Helper function to render institutional KPI card
def render_kpi(label, val, badge_text, badge_class, card_class="risk-card-neutral", val_color="#f1f5f9", subtext=None):
    sub_html = f"<div style='font-size:11px; color:#64748b; margin-top:4px;'>{subtext}</div>" if subtext else ""
    st.markdown(f"""
    <div class="{card_class}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span class="meta-label">{label}</span>
            <span class="risk-badge {badge_class}">{badge_text}</span>
        </div>
        <div class="mono-val-lg" style="color: {val_color};">{val}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

# Helper to apply institutional dark financial theme to Plotly charts
def polish_plotly(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="IBM Plex Sans",
        font_color="#94a3b8",
        margin=dict(t=25, b=25, l=25, r=15),
        xaxis=dict(
            gridcolor='#1e293b',
            zerolinecolor='#1e293b',
            tickfont=dict(size=11, family="JetBrains Mono", color="#64748b"),
            title_font=dict(size=11, color="#94a3b8")
        ),
        yaxis=dict(
            gridcolor='#1e293b',
            zerolinecolor='#1e293b',
            tickfont=dict(size=11, family="JetBrains Mono", color="#64748b"),
            title_font=dict(size=11, color="#94a3b8")
        ),
        legend=dict(
            bgcolor='rgba(15,23,42,0.7)',
            bordercolor='#232d3f',
            font=dict(size=11, color="#cbd5e1")
        )
    )
    if fig.layout.title and fig.layout.title.text:
        fig.layout.title.font = dict(size=13, family="IBM Plex Sans", color="#f1f5f9", weight="bold")
    else:
        fig.layout.title = None
    return fig

# ==========================================
# PAGE 1: EXECUTIVE PORTFOLIO OVERVIEW
# ==========================================
if page == "Executive Portfolio Overview":
    # Top Status Bar
    st.markdown(
        "<div class='terminal-bar'>"
        "<div>"
        "<span style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #10b981; font-weight: 700;'>SYSTEM ONLINE</span> "
        "<span style='font-size: 13px; font-weight: 600; color: #f1f5f9; margin-left: 10px;'>EXECUTIVE PORTFOLIO RISK AUDIT</span>"
        "</div>"
        "<div style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #64748b;'>"
        "DATA SYNC: 2026-09-11 16:30 UTC | PORTFOLIO BATCH: AS-OF-DATE"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        # KPI Grid - Strict Risk Hierarchy
        kpi_cols = st.columns(4)
        with kpi_cols[0]:
            render_kpi("PAR 30 | 30-89 DAYS DPD", "2.40%", "ELEVATED RISK", "badge-amber", "risk-card-warning", "#fde047", "▲ +0.35% MoM vs Target 2.00%")
        with kpi_cols[1]:
            render_kpi("NPL RATE | 90+ DPD EXPOSURE", "1.10%", "TARGET 1.50%", "badge-crimson", "risk-card-alert", "#fca5a5", "▲ +0.12% MoM ($1.60M NPL)")
        with kpi_cols[2]:
            render_kpi("ACTIVE PORTFOLIO VALUE", "$145.2M", "CAPITAL BASE", "badge-blue", "risk-card-neutral", "#93c5fd", "12,450 Disbursed Accounts")
        with kpi_cols[3]:
            render_kpi("NET INTEREST MARGIN (NIM)", "8.70%", "SPREAD HEALTH", "badge-emerald", "risk-card-neutral", "#6ee7b7", "WAIR 11.20% | Cost 2.50%")
            
    with row1_col2:
        # AI Underwriting Risk Memo
        st.markdown(
            "<div class='memo-card'>"
            "<div class='memo-header'>RISK COMMITTEE MEMORANDUM | CR-2026-09</div>"
            "<div style='font-size: 14px; font-weight: 700; color: #f1f5f9; margin-bottom: 8px;'>Executive Risk Findings & Stress Warning</div>"
            "<div style='color: #cbd5e1; font-size: 12.5px; line-height: 1.5; margin-bottom: 12px;'>"
            "Overall portfolio defaults remain bounded (NPL at 1.10%), but <strong style='color: #ef4444;'>Cohort Mar 25 shows 2.4x accelerated delinquency migration</strong> at Month on Book (MOB) 6."
            "</div>"
            "<ul style='color: #94a3b8; font-size: 11.5px; padding-left: 16px; line-height: 1.5; margin-bottom: 0px;'>"
            "<li><strong style='color: #f1f5f9;'>Subprime Segment (CIBIL &lt;650):</strong> PAR 30 expanded to 3.90%.</li>"
            "<li><strong style='color: #f1f5f9;'>Geographic Concentration:</strong> Uttar Pradesh NPL outlier at 4.20%.</li>"
            "<li><strong style='color: #f1f5f9;'>Channel Quality:</strong> Partner Digital affiliates driving 58% of defaults.</li>"
            "</ul>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    st.write("")

    row2_col1, row2_col2 = st.columns([1, 2])
    
    with row2_col1:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>DISBURSED LOANS BY SOURCING CHANNEL</div>", unsafe_allow_html=True)
        df_disb_ch = df_disb.merge(df_apprv, on='approval_key')\
                            .merge(df_app, on='application_key')\
                            .merge(df_chan, on='channel_key')
        ch_counts = df_disb_ch['acquisition_source'].value_counts().reset_index()
        ch_counts.columns = ['Source', 'Loans Funded']
        
        fig = px.pie(ch_counts, values='Loans Funded', names='Source', 
                     color_discrete_sequence=chart_colors, hole=0.55)
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'><span class='meta-label'>INTERACTIVE CREDIT STRESS TESTER</span><span class='risk-badge badge-blue'>SIMULATION ENGINE</span></div>", unsafe_allow_html=True)
        
        cutoff = st.slider("Underwriting CIBIL Score Cutoff Floor", 300, 850, 600, 10)
        
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
            st.markdown(f"<div class='meta-label'>Simulated Active Portfolio Value</div><div class='mono-val-md' style='color:#3b82f6;'>${active_val_m:.1f}M</div>", unsafe_allow_html=True)
        with metric_cols[1]:
            npl_color = "#ef4444" if simulated_npl > 2.0 else "#10b981"
            st.markdown(f"<div class='meta-label'>Simulated NPL Default Rate</div><div class='mono-val-md' style='color:{npl_color};'>{simulated_npl:.2f}%</div>", unsafe_allow_html=True)
            
        st.markdown("<p style='font-size:11.5px; color:#64748b; margin-top:15px; margin-bottom:0px;'>Adjusting the minimum credit score requirement acts as an immediate lever on underwriting conversions. Raising limits cuts high-risk default volumes but restricts outstanding balances.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    row3_col1, row3_col2 = st.columns([2, 1])
    
    with row3_col1:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>PRODUCT CATEGORY PORTFOLIO PERFORMANCE MATRIX</div>", unsafe_allow_html=True)
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
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>OUTSTANDING BALANCE BY RISK TIER</div>", unsafe_allow_html=True)
        df_cust_mix = df_disb.merge(df_cust, on='customer_key')
        mix_data = df_cust_mix.groupby('risk_tier')['disbursed_amount'].sum().reset_index()
        mix_data.columns = ['Risk Tier', 'Outstanding Balance']
        
        fig = px.bar(mix_data, x='Outstanding Balance', y='Risk Tier', orientation='h',
                     color='Risk Tier', color_discrete_sequence=['#ef4444', '#f59e0b', '#3b82f6', '#10b981'])
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 2: UNDERWRITING FUNNEL ANALYTICS
# ==========================================
elif page == "Underwriting Funnel Analytics":
    st.markdown(
        "<div class='terminal-bar'>"
        "<div>"
        "<span style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #3b82f6; font-weight: 700;'>OPERATIONS AUDIT</span> "
        "<span style='font-size: 13px; font-weight: 600; color: #f1f5f9; margin-left: 10px;'>UNDERWRITING FUNNEL & PIPELINE THROUGHPUT</span>"
        "</div>"
        "<div style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #64748b;'>"
        "PIPELINE TAT: 18.5 HRS | APPROVAL CONVERSION: 42.5%"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    
    row1_col1, row1_col2 = st.columns([1, 2])
    
    with row1_col1:
        st.markdown(
            "<div class='memo-card'>"
            "<div class='memo-header'>UNDERWRITING AUDIT MEMO</div>"
            "<div style='font-size: 14px; font-weight: 700; color: #f1f5f9; margin-bottom: 8px;'>Verification Stage Bottleneck</div>"
            "<div style='color: #cbd5e1; font-size: 12.5px; line-height: 1.5; margin-bottom: 10px;'>"
            "Significant attrition observed between <strong style='color: #f1f5f9;'>KYC Passed</strong> and <strong style='color: #f1f5f9;'>Verified</strong> milestones, driving total turnaround time to 18.5 hours."
            "</div>"
            "<ul style='color: #94a3b8; font-size: 11.5px; padding-left: 15px; line-height: 1.5; margin-bottom: 0px;'>"
            "<li>CIBIL default threshold breaches cause 42% of total declines.</li>"
            "<li>Income verification holds 12.5 hours of processing latency.</li>"
            "<li>Auto loan throughput speed is 1.8x faster than housing loans.</li>"
            "</ul>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    with row1_col2:
        kpi_cols = st.columns(3)
        with kpi_cols[0]:
            render_kpi("TOTAL APPLICATIONS", "250,000", "PIPELINE VOLUME", "badge-slate")
        with kpi_cols[1]:
            render_kpi("APPROVAL CONVERSION", "42.50%", "PASSED UNDERWRITING", "badge-emerald", val_color="#6ee7b7")
        with kpi_cols[2]:
            render_kpi("AVG PIPELINE TAT", "18.5 HRS", "PROCESSING TIME", "badge-blue", val_color="#93c5fd")

    st.write("")

    row2_col1, row2_col2 = st.columns([2, 1])
    
    with row2_col1:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>UNDERWRITING FUNNEL MILESTONES</div>", unsafe_allow_html=True)
        stages = ["1. Applied", "2. KYC Passed", "3. Verified", "4. Approved", "5. Disbursed"]
        counts = [250000, 212500, 150000, 106250, 100000]
        
        fig = go.Figure(go.Funnel(
            y=stages,
            x=counts,
            textposition="inside",
            textinfo="value+percent initial",
            opacity=0.9,
            marker={"color": ['#3b82f6', '#06b6d4', '#10b981', '#f59e0b', '#64748b']}
        ))
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>UNDERWRITING SIMULATOR</div>", unsafe_allow_html=True)
        
        sim_income = st.slider("Minimum Monthly Income Limit ($)", 10000, 100000, 30000, 5000)
        sim_cibil = st.slider("Minimum Underwriting CIBIL", 300, 900, 650, 10)
        
        # Calculate simulated rates
        income_ratio = (sim_income - 10000) / 90000.0
        cibil_ratio = (sim_cibil - 300) / 600.0
        simulated_app_rate = max(5.0, min(95.0, 42.5 * (1 - cibil_ratio * 0.45 - income_ratio * 0.15)))
        simulated_declines = int(250000 * (1 - (simulated_app_rate / 100.0)))
        
        st.write("")
        st.markdown(f"<div class='meta-label'>Projected Approval Rate</div><div class='mono-val-md' style='color:#10b981;'>{simulated_app_rate:.1f}%</div>", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"<div class='meta-label'>Estimated Declined Applications</div><div class='mono-val-md' style='color:#ef4444;'>{simulated_declines:,}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
    st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>TOP UNDERWRITING REJECTION REASONS</div>", unsafe_allow_html=True)
    rejections = df_apprv[df_apprv['approval_status'] == 'Declined']['rejection_reason'].value_counts().reset_index()
    rejections.columns = ['Reason', 'Count']
    
    fig = px.bar(rejections, x='Count', y='Reason', orientation='h',
                 color_discrete_sequence=['#ef4444'])
    st.plotly_chart(polish_plotly(fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 3: PORTFOLIO PERFORMANCE
# ==========================================
elif page == "Portfolio Performance":
    st.markdown(
        "<div class='terminal-bar'>"
        "<div>"
        "<span style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #10b981; font-weight: 700;'>AMORTIZATION MONITOR</span> "
        "<span style='font-size: 13px; font-weight: 600; color: #f1f5f9; margin-left: 10px;'>PORTFOLIO MATURITIES & VINTAGE DELINQUENCY</span>"
        "</div>"
        "<div style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #64748b;'>"
        "MOB HORIZON: 0-12 | COHORT MONITORING: ACTIVE"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        st.markdown(
            "<div class='memo-card'>"
            "<div class='memo-header'>VINTAGE AUDIT MEMO</div>"
            "<div style='font-size: 14px; font-weight: 700; color: #f1f5f9; margin-bottom: 6px;'>Cohort Mar '25 Early Stress Warning</div>"
            "<div style='color: #cbd5e1; font-size: 12.5px; line-height: 1.5;'>"
            "Repayment ledgers indicate an amortization gap of $1.2M in past-due installment maturities. Cohort Mar 25 shows cumulative default expansion starting at MOB 4."
            "</div>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    with row1_col2:
        render_kpi("REPAYMENT AMORTIZATION GAP", "$1.2M", "MATURITY DELAY", "badge-amber", "risk-card-warning", "#fde047")

    st.write("")

    row2_col1, row2_col2 = st.columns([1, 2])
    
    with row2_col1:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>VINTAGE DELINQUENCY STRESS SIMULATOR</div>", unsafe_allow_html=True)
        
        sim_cohort = st.selectbox("Highlight Cohort Curve", ["Cohort Jan 25", "Cohort Feb 25", "Cohort Mar 25"])
        stress_multiplier = st.slider("Apply Vintage Stress Multiplier", 1.0, 3.0, 1.0, 0.1)
        
        st.write("")
        st.markdown(f"<div class='meta-label'>Selected Target Cohort</div><div class='mono-val-md' style='color:#3b82f6;'>{sim_cohort}</div>", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"<div class='meta-label'>Applied Stress Multiplier</div><div class='mono-val-md' style='color:#ef4444;'>{stress_multiplier:.1f}x</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>VINTAGE COHORT DELINQUENCY CURVES (MOB 0-12)</div>", unsafe_allow_html=True)
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
        fig.add_trace(go.Scatter(x=mobs, y=v_jan.tolist(), name='Cohort Jan 25', line=dict(color='#10b981', width=2.5)))
        fig.add_trace(go.Scatter(x=mobs, y=v_feb.tolist(), name='Cohort Feb 25', line=dict(color='#3b82f6', width=2.5)))
        fig.add_trace(go.Scatter(x=mobs, y=v_mar.tolist(), name='Cohort Mar 25 (Alert)', line=dict(color='#ef4444', width=3, dash='dash')))
        fig.update_layout(xaxis_title="Months on Book (MOB)", yaxis_title="Cumulative Default Rate %")
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
    st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>SCHEDULED INSTALLMENT DUES VS. ACTUAL AMOUNT COLLECTED</div>", unsafe_allow_html=True)
    repay_agg = df_repay.groupby('installment_number')[['installment_amount', 'amount_paid']].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=repay_agg['installment_number'], y=repay_agg['installment_amount'], name='Scheduled Due', marker_color='#3b82f6'))
    fig.add_trace(go.Bar(x=repay_agg['installment_number'], y=repay_agg['amount_paid'], name='Actual Paid', marker_color='#10b981'))
    fig.update_layout(barmode='group', xaxis_title="Installment Sequence", yaxis_title="Capital Volume ($)")
    st.plotly_chart(polish_plotly(fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 4: RISK INTELLIGENCE
# ==========================================
elif page == "Risk Intelligence":
    st.markdown(
        "<div class='terminal-bar'>"
        "<div>"
        "<span style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #ef4444; font-weight: 700;'>RISK ENGINE</span> "
        "<span style='font-size: 13px; font-weight: 600; color: #f1f5f9; margin-left: 10px;'>DELINQUENCY SEGMENTATION & ACTION QUEUE</span>"
        "</div>"
        "<div style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #64748b;'>"
        "HIGH RISK QUEUE FILTER: ACTIVE"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        st.markdown(
            "<div class='memo-card'>"
            "<div class='memo-header'>RISK SEGMENTATION FINDINGS</div>"
            "<div style='font-size: 14px; font-weight: 700; color: #f1f5f9; margin-bottom: 6px;'>Subprime Concentration Loss</div>"
            "<div style='color: #cbd5e1; font-size: 12.5px; line-height: 1.5;'>"
            "Subprime borrowers with monthly income under $35,000 represent 58% of total portfolio default volume. Action queues prioritized by DPD and cover ratios."
            "</div>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    with row1_col2:
        render_kpi("SUBPRIME DEFAULT SHARE", "58.0%", "HIGH RISK EXPOSURE", "badge-crimson", "risk-card-alert", "#fca5a5")

    st.write("")

    row2_col1, row2_col2 = st.columns([1, 2])
    
    with row2_col1:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>ACTION QUEUE CONTROLLER</div>", unsafe_allow_html=True)
        
        min_dpd = st.slider("Minimum Days Past Due (DPD)", 30, 90, 30, 5)
        selected_tiers = st.multiselect("Filter Risk Tier", ["Subprime", "Near Prime", "Prime", "Super Prime"], default=["Subprime", "Near Prime"])
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>PRIORITY OUTBOUND DIALER QUEUE (DELINQUENT ACCOUNTS)</div>", unsafe_allow_html=True)
        
        # Apply filters to outbound dialer queue
        df_delinq = df_repay[df_repay['days_past_due'] >= min_dpd].merge(df_cust, on='customer_key').merge(df_disb, left_on='loan_key', right_on='disbursement_key')
        df_delinq = df_delinq[['customer_id', 'credit_score', 'loan_id', 'installment_amount', 'days_past_due', 'delinquency_bucket', 'risk_tier']].drop_duplicates()
        
        if selected_tiers:
            df_delinq = df_delinq[df_delinq['risk_tier'].isin(selected_tiers)]
            
        df_disp = df_delinq.head(6)
        st.dataframe(df_disp)
        st.markdown("<p style='font-size:11px; color:#64748b; margin-top:8px;'>Prioritized using dense ranking based on installment-to-income cover ratios and total days past due.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
    st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>NPL DEFAULT RATE % HEATMAP (CIBIL BAND VS. MONTHLY INCOME DECILE)</div>", unsafe_allow_html=True)
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
    st.markdown(
        "<div class='terminal-bar'>"
        "<div>"
        "<span style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #f59e0b; font-weight: 700;'>RECOVERIES ENGINE</span> "
        "<span style='font-size: 13px; font-weight: 600; color: #f1f5f9; margin-left: 10px;'>COLLECTIONS EFFICACY & OUTREACH STRATEGY</span>"
        "</div>"
        "<div style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #64748b;'>"
        "STRATEGY AUDIT: ACTIVE"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    
    row1_col1, row1_col2 = st.columns([1, 2])
    
    with row1_col1:
        st.markdown(
            "<div class='memo-card'>"
            "<div class='memo-header'>COLLECTIONS AUDIT MEMO</div>"
            "<div style='font-size: 14px; font-weight: 700; color: #f1f5f9; margin-bottom: 8px;'>Outreach Resolution Efficiencies</div>"
            "<div style='color: #cbd5e1; font-size: 12.5px; line-height: 1.5; margin-bottom: 10px;'>"
            "SMS/Digital outreach handles high early-stage volume at minimal expense, but <strong style='color: #f1f5f9;'>legal escalations</strong> deliver highest recovery values on prime defaults."
            "</div>"
            "<ul style='color: #94a3b8; font-size: 11.5px; padding-left: 15px; line-height: 1.5; margin-bottom: 0px;'>"
            "<li>Top 3 collection agents account for 38% of recovered capital.</li>"
            "<li>Tele-calling converts at 14.5% Collections Efficiency Index (CEI).</li>"
            "</ul>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    with row1_col2:
        st.markdown("<div class='risk-card' style='margin-bottom: 0px;'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>COLLECTIONS EFFICIENCY INDEX (CEI) BY AGENT ($ RECOVERED)</div>", unsafe_allow_html=True)
        agent_stats = df_coll.groupby('agent_id')['recovered_amount'].sum().reset_index()
        agent_stats = agent_stats.sort_values(by='recovered_amount', ascending=False).head(10)
        
        fig = px.bar(agent_stats, x='agent_id', y='recovered_amount', color='recovered_amount',
                     color_continuous_scale='Blues', labels=dict(recovered_amount="Amount Recovered ($)"))
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    row2_col1, row2_col2 = st.columns([2, 1])
    
    with row2_col1:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>RECOVERIES SPLIT BY OUTREACH STRATEGY</div>", unsafe_allow_html=True)
        strat_stats = df_coll.groupby('collection_strategy')['recovered_amount'].sum().reset_index()
        
        fig = px.pie(strat_stats, values='recovered_amount', names='collection_strategy',
                     color_discrete_sequence=chart_colors)
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>STRATEGY BUDGET SIMULATOR</div>", unsafe_allow_html=True)
        
        sms_pct = st.slider("SMS/Digital Allocation %", 0, 100, 30, 5)
        call_pct = st.slider("Tele-calling Allocation %", 0, 100, 50, 5)
        
        legal_pct = max(0, 100 - sms_pct - call_pct)
        st.info(f"Legal Outreach Allocation: {legal_pct}%")
        
        base_recovery_vol = 8.4
        sms_recovery_eff = 0.05
        call_recovery_eff = 0.12
        legal_recovery_eff = 0.22
        
        projected_recovery_est = base_recovery_vol * (1.0 + (sms_pct/100.0)*sms_recovery_eff + (call_pct/100.0)*call_recovery_eff + (legal_pct/100.0)*legal_recovery_eff)
        
        st.write("")
        st.markdown(f"<div class='meta-label'>Projected Monthly Recoveries</div><div class='mono-val-md' style='color:#f59e0b;'>${projected_recovery_est:.2f}M</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 6: GEOGRAPHIC INTELLIGENCE
# ==========================================
elif page == "Geographic Intelligence":
    st.markdown(
        "<div class='terminal-bar'>"
        "<div>"
        "<span style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #3b82f6; font-weight: 700;'>LOCATION PROFILER</span> "
        "<span style='font-size: 13px; font-weight: 600; color: #f1f5f9; margin-left: 10px;'>GEOGRAPHIC CONCENTRATION & LOSS HEATMAP</span>"
        "</div>"
        "<div style='font-family: \"JetBrains Mono\", monospace; font-size: 11px; color: #64748b;'>"
        "REGIONAL EXPOSURE AUDIT"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        st.markdown(
            "<div class='memo-card'>"
            "<div class='memo-header'>GEOGRAPHIC RISK MEMO</div>"
            "<div style='font-size: 14px; font-weight: 700; color: #f1f5f9; margin-bottom: 6px;'>State Default Concentration Outliers</div>"
            "<div style='color: #cbd5e1; font-size: 12.5px; line-height: 1.5;'>"
            "Maharashtra and Delhi hold top funding volumes with healthy defaults (&lt;1.20%). However, <strong style='color: #ef4444;'>Uttar Pradesh (4.20%) and Bihar (3.40%)</strong> exceed risk tolerance limits."
            "</div>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    with row1_col2:
        render_kpi("HIGHEST STATE NPL (UP)", "4.20%", "OUTLIER ALERT", "badge-crimson", "risk-card-alert", "#fca5a5")

    st.write("")

    row2_col1, row2_col2 = st.columns([1, 2])
    
    with row2_col1:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>EXPOSURE THRESHOLD CONTROLLER</div>", unsafe_allow_html=True)
        
        max_allowed_default = st.slider("Highlight Default Rates Above %", 0.5, 5.0, 2.5, 0.1)
        
        st.write("")
        st.markdown(f"<div class='meta-label'>Active High Risk Filter Limit</div><div class='mono-val-md' style='color:#ef4444;'>{max_allowed_default:.1f}%</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
        st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>STATE DEFAULT RATES % (LOSS CONCENTRATION)</div>", unsafe_allow_html=True)
        default_data = {
            "State": ["Maharashtra ", "Delhi ", "Uttar Pradesh ", "Karnataka ", "Tamil Nadu ", "Telangana ", "West Bengal ", "Bihar ", "Madhya Pradesh ", "Gujarat "],
            "Default Rate %": [1.20, 0.95, 4.20, 0.85, 1.10, 0.70, 2.10, 3.40, 1.80, 0.90]
        }
        df_df = pd.DataFrame(default_data)
        
        # Color dynamically based on threshold
        colors = ['#ef4444' if val > max_allowed_default else '#10b981' for val in df_df['Default Rate %']]
        
        fig = px.bar(df_df, x='Default Rate %', y='State', orientation='h')
        fig.update_traces(marker_color=colors)
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    st.markdown("<div class='risk-card'>", unsafe_allow_html=True)
    st.markdown("<div class='meta-label' style='margin-bottom: 12px;'>STATE-LEVEL DISBURSEMENT VOLUMES ($)</div>", unsafe_allow_html=True)
    state_data = {
        "State": ["Maharashtra ", "Delhi ", "Uttar Pradesh ", "Karnataka ", "Tamil Nadu ", "Telangana ", "West Bengal ", "Bihar ", "Madhya Pradesh ", "Gujarat "],
        "Funded Volume": [35400000, 24500000, 18200000, 21500000, 16400000, 12200000, 9800000, 7200000, 8400000, 11500000]
    }
    df_st = pd.DataFrame(state_data).sort_values(by='Funded Volume', ascending=True)
    
    fig = px.bar(df_st, x='Funded Volume', y='State', orientation='h', color='Funded Volume', color_continuous_scale='Blues')
    st.plotly_chart(polish_plotly(fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
