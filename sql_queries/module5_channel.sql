-- MODULE 5: CHANNEL ANALYTICS

-- Query 14: Acquisition Channel ROI & Unit Economics
-- Maps channels by comparing CAC costs vs interest collected and credit write-offs.
WITH channel_unit_econ AS (
    SELECT 
        dc.acquisition_source,
        COUNT(DISTINCT fd.disbursement_key) AS loans_funded,
        SUM(fd.disbursed_amount) AS total_disbursed,
        SUM(COALESCE(fr.interest_paid, 0)) AS total_interest_earned,
        SUM(CASE WHEN fr.default_flag = TRUE THEN fr.outstanding_balance ELSE 0 END) AS written_off_principal,
        CASE 
            WHEN dc.acquisition_source = 'Google Ads' THEN 1200
            WHEN dc.acquisition_source = 'Meta Ads' THEN 950
            WHEN dc.acquisition_source = 'Referral' THEN 400
            WHEN dc.acquisition_source = 'Partners' THEN 1500
            ELSE 50
        END AS CAC_per_loan
    FROM dim_channel dc
    LEFT JOIN fact_application fa ON dc.channel_key = fa.channel_key
    LEFT JOIN fact_approval fap ON fa.application_key = fap.application_key
    LEFT JOIN fact_disbursement fd ON fap.approval_key = fd.approval_key
    LEFT JOIN fact_repayment fr ON fd.disbursement_key = fr.loan_key
    GROUP BY dc.acquisition_source
)
SELECT 
    acquisition_source,
    loans_funded,
    ROUND(total_disbursed, 2) AS total_disbursed,
    ROUND(total_interest_earned, 2) AS interest_revenue,
    ROUND(written_off_principal, 2) AS default_losses,
    ROUND((loans_funded * CAC_per_loan), 2) AS total_channel_cac,
    ROUND((total_interest_earned - written_off_principal - (loans_funded * CAC_per_loan)), 2) AS net_profit_contribution,
    ROUND(
        ((total_interest_earned - written_off_principal) / NULLIF(loans_funded * CAC_per_loan, 0)) * 100, 
        2
    ) AS channel_roi_pct
FROM channel_unit_econ
ORDER BY net_profit_contribution DESC;


-- Query 15: Campaign-Level Risk Scorecard
-- Maps borrower quality down to specific marketing campaigns.
WITH campaign_performance AS (
    SELECT 
        dc.acquisition_source,
        dc.campaign_name,
        COUNT(DISTINCT fd.disbursement_key) AS disbursed_count,
        AVG(dcus.credit_score) AS avg_credit_score,
        COUNT(CASE WHEN fr.default_flag = TRUE THEN 1 END) AS default_count
    FROM dim_channel dc
    JOIN fact_application fa ON dc.channel_key = fa.channel_key
    JOIN dim_customer dcus ON fa.customer_key = dcus.customer_key
    JOIN fact_approval fap ON fa.application_key = fap.application_key
    JOIN fact_disbursement fd ON fap.approval_key = fd.approval_key
    LEFT JOIN fact_repayment fr ON fd.disbursement_key = fr.loan_key
    GROUP BY dc.acquisition_source, dc.campaign_name
)
SELECT 
    acquisition_source,
    campaign_name,
    disbursed_count,
    ROUND(average_borrower_credit_score, 0) AS avg_score,
    default_count,
    ROUND((default_count::numeric / NULLIF(disbursed_count, 0)) * 100, 2) AS default_rate_pct,
    ROW_NUMBER() OVER (ORDER BY (default_count::numeric / NULLIF(disbursed_count, 0)) DESC) AS risk_rank
FROM campaign_performance
WHERE disbursed_count >= 100
ORDER BY default_rate_pct DESC;
