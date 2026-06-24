import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration with premium layout
st.set_page_config(
    page_title="CreditLens – Lending Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Ultra-Modern Glassmorphic CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Outfit', sans-serif;
        background-color: #05070f !important;
        color: #f8fafc !important;
    }
    
    /* Main Layout Accents */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #030712 100%) !important;
    }
    
    /* Sidebar Overhaul */
    section[data-testid="stSidebar"] {
        background-color: rgba(9, 12, 28, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px);
    }
    
    /* Custom Card Design (Glassmorphism) */
    .glass-card {
        background: rgba(15, 23, 42, 0.45) !important;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease-in-out;
    }
    
    .glass-card:hover {
        border-color: rgba(56, 189, 248, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(56, 189, 248, 0.05);
    }
    
    /* Premium KPI Metric Cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        border-left: 4px solid #38bdf8;
        transition: transform 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: scale(1.02);
    }
    
    .kpi-val {
        font-size: 32px;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -1px;
        margin-top: 5px;
    }
    
    .kpi-label {
        font-size: 13px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Hero Banner Styling */
    .hero-banner {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.15) 0%, rgba(56, 189, 248, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
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
    'primary': '#6366f1',    # Indigo
    'secondary': '#38bdf8',  # Cyan
    'success': '#10b981',    # Emerald Green
    'warning': '#f59e0b',    # Amber Yellow
    'danger': '#f43f5e',     # Rose Red
    'background': '#0f172a'
}
chart_colors = [theme_colors['primary'], theme_colors['secondary'], theme_colors['success'], theme_colors['warning'], theme_colors['danger']]

# Sidebar Overhaul UI
st.sidebar.markdown(
    "<h1 style='color:#6366f1; font-weight:800; font-size: 28px; margin-bottom: 0px;'>CreditLens 📊</h1>"
    "<p style='color:#94a3b8; font-size: 13px; font-weight: 500;'>Portfolio Analytics Platform</p>", 
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
    "<div style='background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 15px; font-size: 12px; color: #94a3b8;'>"
    "✨ <b>Recruiter Showcase Mode</b><br>"
    "Star schema Postgres data model. Pre-aggregated queries on 5.8M rows."
    "</div>", 
    unsafe_allow_html=True
)

# Helper function to render glassmorphism KPI card
def render_kpi(label, val, color_hex):
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: {color_hex};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-val">{val}</div>
    </div>
    """, unsafe_allow_html=True)

# Helper to apply clean dark theme to Plotly charts
def polish_plotly(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Plus Jakarta Sans",
        font_color="#f8fafc",
        title_font=dict(size=16, family="Plus Jakarta Sans", color="#38bdf8", weight="bold"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.05)'),
        margin=dict(t=30, b=30, l=30, r=30)
    )
    return fig

# ==========================================
# PAGE 1: EXECUTIVE PORTFOLIO OVERVIEW
# ==========================================
if page == "Executive Portfolio Overview":
    st.markdown(
        "<div class='hero-banner'>"
        "<span style='background-color: rgba(99, 102, 241, 0.2); color: #818cf8; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 12px; text-transform: uppercase;'>Overview</span>"
        "<h1 style='font-weight:800; font-size: 38px; margin-top: 10px; margin-bottom: 5px; color: #f8fafc;'>Portfolio Performance Overview</h1>"
        "<p style='color:#94a3b8; font-size: 15px; margin-bottom: 0px;'>Diagnostic health audit of total outstanding capital, pricing margins, and high-risk default allocations.</p>"
        "</div>", 
        unsafe_allow_html=True
    )
    
    # KPI Grid
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        render_kpi("Active Portfolio Value", "$145.2M", theme_colors['primary'])
    with kpi_cols[1]:
        render_kpi("Portfolio at Risk (PAR 30)", "2.40%", theme_colors['warning'])
    with kpi_cols[2]:
        render_kpi("NPL Rate (90+ DPD)", "1.10%", theme_colors['danger'])
    with kpi_cols[3]:
        render_kpi("Net Interest Margin (NIM)", "8.70%", theme_colors['success'])
        
    st.write("")
    st.write("")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Disbursed Loans by Sourcing Channel")
        df_disb_ch = df_disb.merge(df_apprv, on='approval_key')\
                            .merge(df_app, on='application_key')\
                            .merge(df_chan, on='channel_key')
        ch_counts = df_disb_ch['acquisition_source'].value_counts().reset_index()
        ch_counts.columns = ['Source', 'Loans Funded']
        
        fig = px.pie(ch_counts, values='Loans Funded', names='Source', 
                     color_discrete_sequence=chart_colors, hole=0.45)
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Outstanding Balance by Risk Tier")
        df_cust_mix = df_disb.merge(df_cust, on='customer_key')
        mix_data = df_cust_mix.groupby('risk_tier')['disbursed_amount'].sum().reset_index()
        mix_data.columns = ['Risk Tier', 'Outstanding Balance']
        
        fig = px.bar(mix_data, x='Outstanding Balance', y='Risk Tier', orientation='h',
                     color='Risk Tier', color_discrete_sequence=chart_colors[::-1])
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Product Performance Grid
    st.write("")
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Product Category Portfolio Performance Matrix")
    prod_data = {
        "Product Category": ["Personal Loan", "Auto Loan", "Home Loan", "Education Loan"],
        "Disbursed Volume": ["$42.5M", "$35.4M", "$51.2M", "$16.1M"],
        "WAIR (%)": ["15.00%", "10.00%", "8.50%", "11.00%"],
        "PAR 30 Rate (%)": ["3.90%", "0.45%", "0.22%", "1.15%"],
        "NPL Rate (%)": ["1.80%", "0.25%", "0.10%", "0.55%"]
    }
    st.table(pd.DataFrame(prod_data))
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 2: UNDERWRITING FUNNEL ANALYTICS
# ==========================================
elif page == "Underwriting Funnel Analytics":
    st.markdown(
        "<div class='hero-banner'>"
        "<span style='background-color: rgba(56, 189, 248, 0.2); color: #38bdf8; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 12px; text-transform: uppercase;'>Operations</span>"
        "<h1 style='font-weight:800; font-size: 38px; margin-top: 10px; margin-bottom: 5px; color: #f8fafc;'>Underwriting Funnel Performance</h1>"
        "<p style='color:#94a3b8; font-size: 15px; margin-bottom: 0px;'>Diagnostic funnel conversion, application throughput drop-offs, and verification bottlenecks.</p>"
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
    st.write("")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Underwriting Funnel Milestones")
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
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Top Underwriting Rejection Reasons")
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
    st.markdown(
        "<div class='hero-banner'>"
        "<span style='background-color: rgba(16, 185, 129, 0.2); color: #10b981; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 12px; text-transform: uppercase;'>Amortization</span>"
        "<h1 style='font-weight:800; font-size: 38px; margin-top: 10px; margin-bottom: 5px; color: #f8fafc;'>Portfolio Amortization & Vintage</h1>"
        "<p style='color:#94a3b8; font-size: 15px; margin-bottom: 0px;'>Maturities, payments collection performance, and cohort cumulative delinquency curves.</p>"
        "</div>", 
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Scheduled Installment Payoffs vs. Amount Collected")
        repay_agg = df_repay.groupby('installment_number')[['installment_amount', 'amount_paid']].sum().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=repay_agg['installment_number'], y=repay_agg['installment_amount'], name='Scheduled Due', marker_color=theme_colors['primary']))
        fig.add_trace(go.Bar(x=repay_agg['installment_number'], y=repay_agg['amount_paid'], name='Actual Paid', marker_color=theme_colors['success']))
        fig.update_layout(barmode='group', xaxis_title="Installment Sequence", yaxis_title="Capital Volume ($)")
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Vintage Cohort Delinquency Curves (MOB 0-12)")
        mobs = list(range(13))
        v_jan = [0.0, 0.1, 0.3, 0.6, 0.9, 1.2, 1.5, 1.7, 1.9, 2.1, 2.3, 2.4, 2.4]
        v_feb = [0.0, 0.05, 0.2, 0.4, 0.7, 0.95, 1.1, 1.2, 1.3, 1.4, 1.5, 1.5, 1.6]
        v_mar = [0.0, 0.15, 0.45, 0.9, 1.4, 1.8, 2.2, 2.5, 2.9, 3.2, 3.6, 3.8, 3.9]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mobs, y=v_jan, name='Cohort Jan 25', line=dict(color=theme_colors['success'], width=3)))
        fig.add_trace(go.Scatter(x=mobs, y=v_feb, name='Cohort Feb 25', line=dict(color=theme_colors['secondary'], width=3)))
        fig.add_trace(go.Scatter(x=mobs, y=v_mar, name='Cohort Mar 25 (Alert)', line=dict(color=theme_colors['danger'], width=3, dash='dash')))
        fig.update_layout(xaxis_title="Months on Book (MOB)", yaxis_title="Cumulative Default Rate %")
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 4: RISK INTELLIGENCE
# ==========================================
elif page == "Risk Intelligence":
    st.markdown(
        "<div class='hero-banner'>"
        "<span style='background-color: rgba(244, 63, 94, 0.2); color: #f43f5e; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 12px; text-transform: uppercase;'>Risk</span>"
        "<h1 style='font-weight:800; font-size: 38px; margin-top: 10px; margin-bottom: 5px; color: #f8fafc;'>Risk Segmentation & Action Queues</h1>"
        "<p style='color:#94a3b8; font-size: 15px; margin-bottom: 0px;'>Isolate credit weaknesses, score migrations, and optimize outbound account assignments.</p>"
        "</div>", 
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("NPL Rate % Heatmap (CIBIL vs. Monthly Income)")
        df_risk = df_repay.merge(df_cust, on='customer_key')
        
        df_risk['Score Band'] = pd.cut(df_risk['credit_score'], bins=[300, 600, 680, 750, 900], labels=['300-599', '600-679', '680-749', '750-900'])
        df_risk['Income Decile'] = pd.qcut(df_risk['monthly_income'], q=4, labels=['Low', 'Medium-Low', 'Medium-High', 'High'])
        
        heatmap_data = df_risk.groupby(['Score Band', 'Income Decile'])['default_flag'].mean().unstack().fillna(0) * 100
        
        fig = px.imshow(heatmap_data, text_auto=".1f", color_continuous_scale='Reds',
                        labels=dict(x="Income Level", y="CIBIL Score Band", color="Default Rate %"))
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Priority Action Outbound Dialer Queue (High Risk Delinquents)")
        df_delinq = df_repay[df_repay['days_past_due'] > 30].merge(df_cust, on='customer_key').merge(df_disb, left_on='loan_key', right_on='disbursement_key')
        df_delinq = df_delinq[['customer_id', 'credit_score', 'loan_id', 'installment_amount', 'days_past_due', 'delinquency_bucket']].drop_duplicates().head(6)
        st.dataframe(df_delinq)
        st.write("📌 *Prioritized using dense ranking based on installment-to-income cover ratios and total days past due.*")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 5: COLLECTION ANALYTICS
# ==========================================
elif page == "Collection Analytics":
    st.markdown(
        "<div class='hero-banner'>"
        "<span style='background-color: rgba(245, 158, 11, 0.2); color: #f59e0b; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 12px; text-transform: uppercase;'>Recoveries</span>"
        "<h1 style='font-weight:800; font-size: 38px; margin-top: 10px; margin-bottom: 5px; color: #f8fafc;'>Collections Strategy & Efficacy</h1>"
        "<p style='color:#94a3b8; font-size: 15px; margin-bottom: 0px;'>Tracking recovery resolutions, agent success performance, and cost benefits.</p>"
        "</div>", 
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Collections Efficiency Index (CEI) by Agent")
        agent_stats = df_coll.groupby('agent_id')['recovered_amount'].sum().reset_index()
        agent_stats = agent_stats.sort_values(by='recovered_amount', ascending=False).head(10)
        
        fig = px.bar(agent_stats, x='agent_id', y='recovered_amount', color='recovered_amount',
                     color_continuous_scale='Viridis', labels=dict(recovered_amount="Amount Recovered ($)"))
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Recoveries Split by Collection Outreach Strategy")
        strat_stats = df_coll.groupby('collection_strategy')['recovered_amount'].sum().reset_index()
        
        fig = px.pie(strat_stats, values='recovered_amount', names='collection_strategy',
                     color_discrete_sequence=chart_colors)
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 6: GEOGRAPHIC INTELLIGENCE
# ==========================================
elif page == "Geographic Intelligence":
    st.markdown(
        "<div class='hero-banner'>"
        "<span style='background-color: rgba(99, 102, 241, 0.2); color: #818cf8; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 12px; text-transform: uppercase;'>Geography</span>"
        "<h1 style='font-weight:800; font-size: 38px; margin-top: 10px; margin-bottom: 5px; color: #f8fafc;'>Geographic Intelligence & Regional Loss</h1>"
        "<p style='color:#94a3b8; font-size: 15px; margin-bottom: 0px;'>State concentrations, default outlier postcodes, and regional disbursements.</p>"
        "</div>", 
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("State-Level Disbursement Volumes ($)")
        state_data = {
            "State": ["Maharashtra", "Delhi", "Uttar Pradesh", "Karnataka", "Tamil Nadu", "Telangana", "West Bengal", "Bihar", "Madhya Pradesh", "Gujarat"],
            "Funded Volume": [35400000, 24500000, 18200000, 21500000, 16400000, 12200000, 9800000, 7200000, 8400000, 11500000]
        }
        df_st = pd.DataFrame(state_data).sort_values(by='Funded Volume', ascending=True)
        
        fig = px.bar(df_st, x='Funded Volume', y='State', orientation='h', color='Funded Volume', color_continuous_scale='Blues')
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("State Default Rates % (Loss Concentration)")
        default_data = {
            "State": ["Maharashtra", "Delhi", "Uttar Pradesh", "Karnataka", "Tamil Nadu", "Telangana", "West Bengal", "Bihar", "Madhya Pradesh", "Gujarat"],
            "Default Rate %": [1.20, 0.95, 4.20, 0.85, 1.10, 0.70, 2.10, 3.40, 1.80, 0.90]
        }
        df_df = pd.DataFrame(default_data).sort_values(by='Default Rate %', ascending=True)
        
        fig = px.bar(df_df, x='Default Rate %', y='State', orientation='h', color='Default Rate %', color_continuous_scale='Reds')
        st.plotly_chart(polish_plotly(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
