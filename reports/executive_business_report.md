# CreditLens – Executive Insights & Business Report

**To:** Executive Committee  
**From:** Senior Data Analytics Lead & FinTech Analyst  
**Date:** June 24, 2026  
**Subject:** Loan Portfolio Intelligence, Underwriting Funnel Performance, & Loss Mitigation Review

---

## Executive Summary

This report evaluates our digital lending business's performance across **250,000+ applications**, **100,000+ active funded loans**, and **$145.2 Million in outstanding portfolio balance**. 

Through diagnostic analytical models, this report details our key revenue drivers, operational bottlenecks, credit risk leakage points, and provides actionable recommendations to optimize portfolio yield.

---

## Answers to the 10 Critical Management Questions

### 1. Which acquisition channels bring the most profitable borrowers?
*   **Findings:** The **Referral** and **Organic Search** channels yield the most profitable borrowers. Referral loans exhibit an average CIBIL score of 735, a low default rate (0.75%), and have a low Customer Acquisition Cost (CAC) of $400. 
*   **The Contrast:** While **Partners** and **Google Ads** drive 65% of our application volume, they are less profitable. Partners exhibit high default rates (3.80% NPL) and carry a high referral fee ($1,500 CAC), which severely depresses their Net Interest Margin (NIM).
*   **Business Recommendation:** Shift marketing budget away from high-cost digital paid search (Google/Meta Ads) and redirect capital to scale our organic growth programs and referral incentives.

### 2. Which customer segments default the most?
*   **Findings:** Delinquency is highly concentrated in the **Freelancer / Self-Employed** employment category and borrowers with **CIBIL scores below 650 (Subprime)**.
    *   Subprime borrowers make up only 10% of total originations but account for **45% of total defaulted balances**.
    *   Self-employed borrowers show a 2.8x higher default rate than Salaried corporate employees with identical credit scores, primarily due to monthly cash-flow volatility.
*   **Business Recommendation:** Credit risk policy should adjust the underwriting grid by introducing lower maximum loan size caps for self-employed individuals and requiring a higher CIBIL cutoff score for freelancers.

### 3. What is our overall approval funnel?
*   **Findings:** Out of 250,000 total application submissions:
    *   **212,500 (85%)** pass automated KYC verification.
    *   **150,000 (70% of KYC passed)** clear employment/risk verification.
    *   **106,250 (70.8% of verified)** are approved by the credit decision engine.
    *   **100,000 (94% of approved)** are funded, resulting in an end-to-end conversion rate of **40%**.
*   **Business Recommendation:** The overall funnel conversion is healthy, but we are losing high-quality applicants during manual review stages, which increases overall CAC.

### 4. Where are applicants dropping off in the funnel?
*   **Findings:** The primary drop-off bottleneck occurs during the **Risk/Employment Verification stage** (representing a 30% loss of the remaining pipeline). Drop-off analysis shows this is caused by:
    1.  Friction in manual bank statement uploads (40% of drop-offs at this stage).
    2.  Long manual verification wait times (Average of 36 hours queue time).
*   **Business Recommendation:** Integrate automated account aggregator APIs to verify income in real-time, eliminating manual PDF uploads and shortening turnaround time.

### 5. Which cities and states are generating the highest losses?
*   **Findings:** **Uttar Pradesh (UP)** generates our highest gross credit losses, with an NPL rate of **4.20%** (compared to our national portfolio average of 1.10%). 
    *   Specifically, city-level drill-downs identify Noida and Lucknow as high-risk outlier zones where default rates exceed UP's own average by 1.8x.
    *   **Maharashtra (MH)** represents our largest market by volume ($35.4M outstanding), but maintains a healthy NPL rate of **1.20%**.
*   **Business Recommendation:** Tighten lending limits for unsecured personal loans in UP and restrict new originations in Noida and Lucknow until local economic factors stabilize.

### 6. What is the current portfolio health?
*   **Findings:** The portfolio is in a stable condition but showing early signs of credit score migration.
    *   **Portfolio at Risk (PAR 30):** Currently sits at **2.40%** ($3.48M outstanding).
    *   **NPL Ratio (90+ DPD):** Stable at **1.10%** ($1.6M outstanding).
    *   **Score Drift:** The average credit score of newly acquired borrowers has drifted down from 718 in Q4 2024 to 702 in Q1 2026, indicating loose underwriting policies in recent months.
*   **Business Recommendation:** Initiate immediate scorecard calibration to prevent rising PAR 30 from converting into hard defaults over the next 60 days.

### 7. How much money is at risk?
*   **Findings:**
    *   Total past due balance (PAR > 0 DPD) is **$8.5 Million**.
    *   Total balance in critical delinquency (60+ DPD) is **$3.1 Million**.
    *   Total Non-Performing Loans (90+ DPD) ready for write-off exposure is **$1.6 Million**.
*   **Business Recommendation:** Increase our balance sheet provisioning reserves by **$1.8 Million** to cover projected write-offs under the CECL standard.

### 8. Which loan products perform best?
*   **Findings:**
    *   **Auto Loans** and **Home Loans** perform best from a risk perspective, showing default rates under **0.40%** due to asset collateralization.
    *   **Personal Loans** generate our highest yield (15% interest rate) but suffer from a **3.90% NPL rate**.
    *   **Net Yield Analysis:** Auto Loans produce the highest net financial yield (9.2% when adjusting for loss rates), whereas Personal Loans yield only 6.5% after writing off bad debts.
*   **Business Recommendation:** Shift capital allocation to grow our secured Auto Loan portfolio, while downsizing our exposure in unsecured Personal Loans.

### 9. Which collection strategies are most effective?
*   **Findings:**
    *   **Automated SMS/Robo-Call Funnels** are highly effective in the **1-30 DPD** bucket, achieving a **60% self-cure rate** at minimal operational cost.
    *   **Outbound Agent Calls** achieve the highest recovery rate (45%) in the **31-60 DPD** and **61-90 DPD** buckets.
    *   **Field Visits** are highly inefficient, resolving only 8% of cases and incurring high travel costs.
*   **Business Recommendation:** Eliminate routine field visits for balances under $5,000, and re-allocate field agents to focus exclusively on high-balance accounts in the 61-90 DPD bucket.

### 10. What actions should leadership take?
*   *See section below.*

---

## Strategic Recommendations for Leadership

### 1. Underwriting Strategy: Adjust Risk Scorecard Cutoffs
*   **Action Plan:** Raise the minimum CIBIL cutoff score for unsecured Personal Loans from 650 to 680. Introduce auto-decline filters for applicants who have open late payments on external accounts within the last 6 months.
*   **Expected Impact:** Reduce new default volumes by **18-20%**, stabilizing NPL rates below the 1.0% target.

### 2. Operational Efficiency: Automate verification for Super Prime applicants
*   **Action Plan:** Implement automated approval pathways for applicants with credit scores above 750. When scorecards indicate excellent credit histories, bypass manual bank statement checks and use auto-verification connections.
*   **Expected Impact:** Drop manual review volume by **30%**, reducing overall funnel Turnaround Time (TAT) from 18.5 hours to under 2 hours for our highest-quality leads.

### 3. Channel Management: Terminate / Restructure Unprofitable Partner Feeds
*   **Action Plan:** Renegotiate agreements with external sourcing partners who bring subprime borrowers. Restructure contracts to tie payouts to 90-day loan performance (clawback clauses) rather than simple application volumes.
*   **Expected Impact:** Protect the portfolio's Net Interest Margin (NIM) and reduce customer acquisition costs from partner channels.

### 4. Recovery Operations: Prioritize Outbound Collections by Balance-at-Risk
*   **Action Plan:** Calibrate the dialer schedule to prioritize outbound collections agents based on a composite score of outstanding balance and high DPD, rather than sorting cases chronologically by delinquent date.
*   **Expected Impact:** Increase Collections Efficiency Index (CEI) by **5-7%** within the next quarter, accelerating cash inflows.
