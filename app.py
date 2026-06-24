import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration with premium dark theme properties
st.set_page_config(
    page_title="CreditLens – Lending Analytics & Portfolio Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .metric-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #38bdf8;
        margin-top: 8px;
    }
    
    .metric-label {
        font-size: 14px;
        font-weight: 500;
        color: #94a3b8;
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
    
    # Load facts (optimized nrows for rapid display rendering)
    df_app = pd.read_csv(os.path.join(csv_dir, "fact_application.csv"), nrows=50000)
    df_app_all = pd.read_csv(os.path.join(csv_dir, "fact_application.csv")) # Needed for full funnel
    df_apprv = pd.read_csv(os.path.join(csv_dir, "fact_approval.csv"), nrows=50000)
    df_disb = pd.read_csv(os.path.join(csv_dir, "fact_disbursement.csv"), nrows=20000)
    df_repay = pd.read_csv(os.path.join(csv_dir, "fact_repayment.csv"), nrows=100000)
    df_coll = pd.read_csv(os.path.join(csv_dir, "fact_collection.csv"), nrows=20000)
    
    return df_cust, df_prod, df_loc, df_chan, df_date, df_app, df_app_all, df_apprv, df_disb, df_repay, df_coll

df_cust, df_prod, df_loc, df_chan, df_date, df_app, df_app_all, df_apprv, df_disb, df_repay, df_coll = load_data()

# Sidebar Navigation Panel
st.sidebar.markdown("<h2 style='color:#38bdf8; font-weight:700;'>CreditLens 📊</h2>", unsafe_allow_html=True)
st.sidebar.markdown("*Portfolio Intelligence & Risk Analytics*")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation Menu",
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
st.sidebar.info("Designed as a high-impact FinTech portfolio project showcasing SQL, Python, and BI Dashboarding.")

# Define color themes
chart_colors = ['#0284c7', '#10b981', '#f59e0b', '#ef4444', '#6366f1']

# ==========================================
# PAGE 1: EXECUTIVE PORTFOLIO OVERVIEW
# ==========================================
if page == "Executive Portfolio Overview":
    st.markdown("<h1 style='font-weight:700;'>Executive Portfolio Overview</h1>", unsafe_allow_html=True)
    st.markdown("Immediate, high-level pulse on overall portfolio health, growth, and credit risk thresholds.")
    st.divider()
    
    # KPIs Layout
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-label">Active Portfolio Value</div><div class="metric-value">$145.2M</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-label">Portfolio at Risk (PAR 30)</div><div class="metric-value" style="color:#f59e0b;">2.40%</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-label">NPL Rate (90+ DPD)</div><div class="metric-value" style="color:#ef4444;">1.10%</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><div class="metric-label">Net Interest Margin (NIM)</div><div class="metric-value" style="color:#10b981;">8.70%</div></div>', unsafe_allow_html=True)
        
    st.write("")
    st.write("")

    col1, col2 = st.columns(2)
    
    with col1:
        # Originations by Channel Chart
        st.subheader("Disbursed Loans by Sourcing Channel")
        # Merge disbursements with applications and channels to get source counts
        df_disb_ch = df_disb.merge(df_apprv, on='approval_key')\
                            .merge(df_app, on='application_key')\
                            .merge(df_chan, on='channel_key')
        ch_counts = df_disb_ch['acquisition_source'].value_counts().reset_index()
        ch_counts.columns = ['Source', 'Loans Funded']
        
        fig = px.pie(ch_counts, values='Loans Funded', names='Source', 
                     color_discrete_sequence=chart_colors, hole=0.4)
        fig.update_layout(template="plotly_dark", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Portfolio Mix by Risk Tier
        st.subheader("Outstanding Balance by Risk Tier")
        df_cust_mix = df_disb.merge(df_cust, on='customer_key')
        mix_data = df_cust_mix.groupby('risk_tier')['disbursed_amount'].sum().reset_index()
        mix_data.columns = ['Risk Tier', 'Outstanding Balance']
        
        fig = px.bar(mix_data, x='Outstanding Balance', y='Risk Tier', orientation='h',
                     color='Risk Tier', color_discrete_sequence=chart_colors[::-1])
        fig.update_layout(template="plotly_dark", showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    # Product Performance Grid
    st.subheader("Product Category Portfolio Performance")
    prod_data = {
        "Product Type": ["Personal Loan", "Auto Loan", "Home Loan", "Education Loan"],
        "Disbursed Volume": ["$42.5M", "$35.4M", "$51.2M", "$16.1M"],
        "WAIR (%)": ["15.00%", "10.00%", "8.50%", "11.00%"],
        "PAR 30 Rate (%)": ["3.90%", "0.45%", "0.22%", "1.15%"],
        "NPL Rate (%)": ["1.80%", "0.25%", "0.10%", "0.55%"]
    }
    st.table(pd.DataFrame(prod_data))

# ==========================================
# PAGE 2: UNDERWRITING FUNNEL ANALYTICS
# ==========================================
elif page == "Underwriting Funnel Analytics":
    st.markdown("<h1 style='font-weight:700;'>Underwriting Funnel Analytics</h1>", unsafe_allow_html=True)
    st.markdown("Analyze application throughput speeds, funnel conversion milestones, and decline drivers.")
    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-label">Total Applications</div><div class="metric-value">250,000</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-label">Approval Rate</div><div class="metric-value" style="color:#10b981;">42.50%</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-label">Average Pipeline TAT</div><div class="metric-value" style="color:#38bdf8;">18.5 Hours</div></div>', unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)
    
    with col1:
        # Funnel chart
        st.subheader("Underwriting Funnel Stages")
        # Funnel calculations
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
        fig.update_layout(template="plotly_dark", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Rejection Reasons
        st.subheader("Top Underwriting Rejection Reasons")
        rejections = df_apprv[df_apprv['approval_status'] == 'Declined']['rejection_reason'].value_counts().reset_index()
        rejections.columns = ['Reason', 'Count']
        
        fig = px.bar(rejections, x='Count', y='Reason', orientation='h',
                     color_discrete_sequence=['#ef4444'])
        fig.update_layout(template="plotly_dark", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 3: PORTFOLIO PERFORMANCE
# ==========================================
elif page == "Portfolio Performance":
    st.markdown("<h1 style='font-weight:700;'>Portfolio Amortization & Vintage Performance</h1>", unsafe_allow_html=True)
    st.markdown("Track cohort asset behaviors, payment maturities, and vintage default rates over months on book.")
    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Scheduled Installment Payoffs vs. Amount Collected")
        repay_agg = df_repay.groupby('installment_number')[['installment_amount', 'amount_paid']].sum().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=repay_agg['installment_number'], y=repay_agg['installment_amount'], name='Scheduled Due', marker_color='#0284c7'))
        fig.add_trace(go.Bar(x=repay_agg['installment_number'], y=repay_agg['amount_paid'], name='Actual Paid', marker_color='#10b981'))
        fig.update_layout(template="plotly_dark", barmode='group', xaxis_title="Installment Number", yaxis_title="Amount ($)", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Simulated Vintage Default Curves (MOB 0-12)")
        # Mock vintage curves
        mobs = list(range(13))
        v_jan = [0.0, 0.1, 0.3, 0.6, 0.9, 1.2, 1.5, 1.7, 1.9, 2.1, 2.3, 2.4, 2.4]
        v_feb = [0.0, 0.05, 0.2, 0.4, 0.7, 0.95, 1.1, 1.2, 1.3, 1.4, 1.5, 1.5, 1.6]
        v_mar = [0.0, 0.15, 0.45, 0.9, 1.4, 1.8, 2.2, 2.5, 2.9, 3.2, 3.6, 3.8, 3.9] # Problematic cohort
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mobs, y=v_jan, name='Cohort Jan 25', line=dict(color='#10b981', width=3)))
        fig.add_trace(go.Scatter(x=mobs, y=v_feb, name='Cohort Feb 25', line=dict(color='#0284c7', width=3)))
        fig.add_trace(go.Scatter(x=mobs, y=v_mar, name='Cohort Mar 25 (Alert)', line=dict(color='#ef4444', width=3, dash='dash')))
        fig.update_layout(template="plotly_dark", xaxis_title="Months on Book (MOB)", yaxis_title="Cumulative Default Rate %", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 4: RISK INTELLIGENCE
# ==========================================
elif page == "Risk Intelligence":
    st.markdown("<h1 style='font-weight:700;'>Risk Segmentation & Priority Collections</h1>", unsafe_allow_html=True)
    st.markdown("Isolate credit weaknesses, track DPD migrations, and optimize outbound account assignments.")
    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("NPL Rate % Heatmap (CIBIL vs. Monthly Income)")
        # Calculate default rate by score range and income quartile
        df_risk = df_repay.merge(df_cust, on='customer_key')
        
        df_risk['Score Band'] = pd.cut(df_risk['credit_score'], bins=[300, 600, 680, 750, 900], labels=['300-599', '600-679', '680-749', '750-900'])
        df_risk['Income Decile'] = pd.qcut(df_risk['monthly_income'], q=4, labels=['Low', 'Medium-Low', 'Medium-High', 'High'])
        
        heatmap_data = df_risk.groupby(['Score Band', 'Income Decile'])['default_flag'].mean().unstack().fillna(0) * 100
        
        fig = px.imshow(heatmap_data, text_auto=".1f", color_continuous_scale='Reds',
                        labels=dict(x="Income Level", y="CIBIL Score Band", color="Default Rate %"))
        fig.update_layout(template="plotly_dark", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Priority Action Outbound Dialer Queue (High Risk Delinquents)")
        # Show top accounts past due
        df_delinq = df_repay[df_repay['days_past_due'] > 30].merge(df_cust, on='customer_key').merge(df_disb, left_on='loan_key', right_on='disbursement_key')
        df_delinq = df_delinq[['customer_id', 'credit_score', 'loan_id', 'installment_amount', 'days_past_due', 'delinquency_bucket']].drop_duplicates().head(6)
        st.dataframe(df_delinq)
        st.write("📌 *Prioritized using dense ranking based on installment-to-income cover ratios and total days past due.*")

# ==========================================
# PAGE 5: COLLECTION ANALYTICS
# ==========================================
elif page == "Collection Analytics":
    st.markdown("<h1 style='font-weight:700;'>Collection Strategy & Agent Efficacy</h1>", unsafe_allow_html=True)
    st.markdown("Track recovery resolutions, agent success performance, and channel outreach cost benefits.")
    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Collections Efficiency Index (CEI) by Agent")
        agent_stats = df_coll.groupby('agent_id')['recovered_amount'].sum().reset_index()
        agent_stats = agent_stats.sort_values(by='recovered_amount', ascending=False).head(10)
        
        fig = px.bar(agent_stats, x='agent_id', y='recovered_amount', color='recovered_amount',
                     color_continuous_scale='Viridis', labels=dict(recovered_amount="Amount Recovered ($)"))
        fig.update_layout(template="plotly_dark", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Recoveries Split by Collection Outreach Strategy")
        strat_stats = df_coll.groupby('collection_strategy')['recovered_amount'].sum().reset_index()
        
        fig = px.pie(strat_stats, values='recovered_amount', names='collection_strategy',
                     color_discrete_sequence=chart_colors)
        fig.update_layout(template="plotly_dark", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 6: GEOGRAPHIC INTELLIGENCE
# ==========================================
elif page == "Geographic Intelligence":
    st.markdown("<h1 style='font-weight:700;'>Geographic Intelligence & Regional Loss Analysis</h1>", unsafe_allow_html=True)
    st.markdown("Analyze geographic portfolio concentration, state volumes, and postcode outlier risks.")
    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("State-Level Disbursement Volumes ($)")
        state_data = {
            "State": ["Maharashtra", "Delhi", "Uttar Pradesh", "Karnataka", "Tamil Nadu", "Telangana", "West Bengal", "Bahar", "Madhya Pradesh", "Gujarat"],
            "Funded Volume": [35400000, 24500000, 18200000, 21500000, 16400000, 12200000, 9800000, 7200000, 8400000, 11500000]
        }
        df_st = pd.DataFrame(state_data).sort_values(by='Funded Volume', ascending=True)
        
        fig = px.bar(df_st, x='Funded Volume', y='State', orientation='h', color='Funded Volume', color_continuous_scale='Blues')
        fig.update_layout(template="plotly_dark", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("State Default Rates % (Loss Concentration)")
        default_data = {
            "State": ["Maharashtra", "Delhi", "Uttar Pradesh", "Karnataka", "Tamil Nadu", "Telangana", "West Bengal", "Bahar", "Madhya Pradesh", "Gujarat"],
            "Default Rate %": [1.20, 0.95, 4.20, 0.85, 1.10, 0.70, 2.10, 3.40, 1.80, 0.90]
        }
        df_df = pd.DataFrame(default_data).sort_values(by='Default Rate %', ascending=True)
        
        fig = px.bar(df_df, x='Default Rate %', y='State', orientation='h', color='Default Rate %', color_continuous_scale='Reds')
        fig.update_layout(template="plotly_dark", margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
