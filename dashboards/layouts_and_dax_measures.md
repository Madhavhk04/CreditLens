# CreditLens – Power BI Visual Specifications

This document defines the report page layouts, visual elements, slicers, and copy-pasteable DAX measures required to create the 6-page interactive CreditLens Power BI report.

---

## 1. Enterprise DAX Measures Library

Add these core metrics in your Power BI model.

```dax
// 1. Total Originations (Funded Volume)
Total Originations = SUM(fact_disbursement[disbursed_amount])

// 2. Active Portfolio Balance (Outstanding Principal)
Active Portfolio Balance = 
CALCULATE(
    SUM(fact_repayment[outstanding_balance]),
    LASTDATE(dim_date[full_date])
)

// 3. Application Approval Rate %
Approval Rate = 
DIVIDE(
    CALCULATE(COUNT(fact_approval[approval_key]), fact_approval[approval_status] = "Approved"),
    COUNT(fact_application[application_key]),
    0
)

// 4. Portfolio at Risk (PAR 30 %)
PAR 30 Rate = 
DIVIDE(
    CALCULATE(
        SUM(fact_repayment[outstanding_balance]), 
        fact_repayment[days_past_due] > 30
    ),
    [Active Portfolio Balance],
    0
)

// 5. Non-Performing Loan (NPL %)
NPL Rate = 
DIVIDE(
    CALCULATE(
        SUM(fact_repayment[outstanding_balance]), 
        fact_repayment[default_flag] = TRUE
    ),
    [Active Portfolio Balance],
    0
)

// 6. Collections Efficiency Index (CEI %)
Collections Efficiency Index = 
DIVIDE(
    SUM(fact_collection[recovered_amount]),
    CALCULATE(
        SUM(fact_repayment[installment_amount]),
        fact_repayment[days_past_due] > 30
    ),
    0
)

// 7. Weighted Average Interest Rate (WAIR %)
WAIR = 
DIVIDE(
    SUMX(
        fact_disbursement,
        fact_disbursement[disbursed_amount] * RELATED(dim_loan_product[interest_rate])
    ),
    [Total Originations],
    0
)
```

---

## 2. Dashboard Pages Wireframe Guide

### Page 1: Executive Portfolio Overview
*   **KPI cards:** Active Portfolio ($145.2M), PAR 30 % (2.40%), NPL % (1.10%), WAIR (12.35%), CEI % (88.50%), Yield (9.80%).
*   **Visual 1 (Line & Column Chart):** Monthly Disbursements vs. Net Profit.
*   **Visual 2 (Horizontal Stacked Bar):** Outstanding Portfolio Mix by Customer Risk Tier.
*   **Visual 3 (Donut Chart):** Sourcing Channel Distribution (Active Funded Loan Counts).
*   **Visual 4 (Table Visual):** Product Category Performance Grid (columns: Loan Type, Total Originations, WAIR, PAR 30 %, NPL %).

### Page 2: Underwriting Funnel Analytics
*   **KPI cards:** App Submissions (250k), Approval Rate (42.50%), Average Decision TAT (18.5 Hours).
*   **Visual 1 (Funnel Chart):** Application Lifecycle conversion stages (Applied -> KYC Passed -> Verification -> Approved).
*   **Visual 2 (Stacked Column Chart):** Count of Rejection reasons (e.g. Low Bureau Score, Insufficient Debt Coverage).
*   **Visual 3 (Line Chart):** Turnaround Time Trend (monthly average in hours).
*   **Visual 4 (Scatter Plot):** Average Credit Score (X) vs. Approval Rate (Y) by employment classification.

### Page 3: Portfolio Analytics
*   **KPI cards:** Total Active Loans (100k), Cumulative Principal Collected ($32M).
*   **Visual 1 (Line Chart):** Amortization forecast (Scheduled Payment Due vs. Actual Amount Paid monthly).
*   **Visual 2 (Matrix Visual):** Vintage default cohort loss heatmap (Rows: Disbursement Month, Columns: MOB 1-12, Values: Default Rate %).
*   **Visual 3 (Treemap):** Active Balance Concentration by State.
*   **Visual 4 (Clustered Bar Chart):** Outstanding Balance by Product Tenure.

### Page 4: Risk Intelligence
*   **KPI cards:** Gross Loss Amount ($1.6M), Average Portfolio CIBIL Score (712).
*   **Visual 1 (Matrix Visual):** Default Heatmap (Rows: FICO Score Band, Columns: Monthly Income Bracket, Values: Default Rate %).
*   **Visual 2 (Clustered Column Chart):** Transition Roll Rates from 30 DPD to 90 DPD.
*   **Visual 3 (Bar Chart):** Delinquent Balances by Employment Category.
*   **Visual 4 (Scatter Plot):** Days Past Due (X) vs. Outstanding Balance (Y) by borrower.

### Page 5: Collection Analytics
*   **KPI cards:** Total Delinquent Assigned ($8.5M), Total Recovered ($7.2M), Recovery Rate (84.7%).
*   **Visual 1 (Column Chart):** Collections Efficiency Index (CEI) sorted by Agent ID.
*   **Visual 2 (Donut Chart):** Collections Recoveries split by outreach strategy (SMS vs. Calls vs. Letters).
*   **Visual 3 (Line Chart):** Average days to recover past-due installments monthly.
*   **Visual 4 (Table Visual):** strategy cost-benefit analysis grid (attempts, conversions, yield).

### Page 6: Geographic Intelligence
*   **KPI cards:** Highest Loss State (Uttar Pradesh - 4.2% NPL), Highest volume State (Maharashtra - $35.4M).
*   **Visual 1 (Filled Map):** State-wise portfolio outstanding balance distribution (shaded green to red by NPL %).
*   **Visual 2 (Matrix Visual):** Regional drilldown grid (Region -> State -> City; showing Disbursements, PAR 30, and recovery %).
*   **Visual 3 (Treemap):** Region volume share (North, South, East, West, Central).
