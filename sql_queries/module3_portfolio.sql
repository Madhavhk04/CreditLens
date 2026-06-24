-- MODULE 3: PORTFOLIO ANALYTICS

-- Query 8: Monthly Active Portfolio Growth & Outstanding Principal
-- Measures active portfolio assets growth month-over-month.
WITH monthly_portfolio AS (
    SELECT 
        dd.year,
        dd.month_number,
        COUNT(DISTINCT fd.disbursement_key) AS loans_disbursed,
        SUM(fd.disbursed_amount) AS monthly_disbursed_volume,
        SUM(COALESCE(fr.interest_paid, 0)) AS interest_income_earned
    FROM dim_date dd
    LEFT JOIN fact_disbursement fd ON fd.disbursement_date_key = dd.date_key
    LEFT JOIN fact_repayment fr ON fd.disbursement_key = fr.loan_key
    GROUP BY dd.year, dd.month_number
)
SELECT 
    year,
    month_number,
    loans_disbursed,
    ROUND(monthly_disbursed_volume, 2) AS disbursed_volume,
    ROUND(interest_income_earned, 2) AS interest_income,
    ROUND(
        LAG(monthly_disbursed_volume) OVER (ORDER BY year, month_number), 
        2
    ) AS prev_month_disbursed,
    ROUND(
        ((monthly_disbursed_volume - LAG(monthly_disbursed_volume) OVER (ORDER BY year, month_number)) / 
        NULLIF(LAG(monthly_disbursed_volume) OVER (ORDER BY year, month_number), 0)) * 100, 
        2
    ) AS mom_growth_rate_pct
FROM monthly_portfolio
ORDER BY year, month_number;


-- Query 9: Weighted Average Interest Rate (WAIR) by Risk Tier
-- Evaluates the pricing/yield metrics we are charging across credit categories.
SELECT 
    dc.risk_tier,
    dlp.loan_type,
    COUNT(fd.disbursement_key) AS active_loans,
    SUM(fd.disbursed_amount) AS total_disbursed,
    ROUND(
        SUM(fd.disbursed_amount * dlp.interest_rate) / SUM(fd.disbursed_amount), 
        2
    ) AS weighted_average_interest_rate_pct,
    ROUND(
        AVG(dlp.interest_rate) OVER (PARTITION BY dc.risk_tier), 
        2
    ) AS avg_tier_interest_rate_pct
FROM fact_disbursement fd
JOIN dim_customer dc ON fd.customer_key = dc.customer_key
JOIN dim_loan_product dlp ON fd.product_key = dlp.product_key
GROUP BY dc.risk_tier, dlp.loan_type
ORDER BY dc.risk_tier, weighted_average_interest_rate_pct DESC;


-- Query 10: Product Performance Yield vs. Loss Matrix
-- Maps loan products to identify net yields when accounting for default write-offs.
WITH product_stats AS (
    SELECT 
        dlp.loan_type,
        SUM(fd.disbursed_amount) AS total_disbursed,
        SUM(COALESCE(fr.interest_paid, 0)) AS total_interest_earned,
        SUM(CASE WHEN fr.default_flag = TRUE THEN fr.outstanding_balance ELSE 0 END) AS total_defaulted_principal
    FROM dim_loan_product dlp
    JOIN fact_disbursement fd ON dlp.product_key = fd.product_key
    LEFT JOIN fact_repayment fr ON fd.disbursement_key = fr.loan_key
    GROUP BY dlp.loan_type
)
SELECT 
    loan_type,
    ROUND(total_disbursed, 2) AS total_disbursed,
    ROUND(total_interest_earned, 2) AS interest_earned,
    ROUND(total_defaulted_principal, 2) AS write_offs,
    ROUND((total_interest_earned - total_defaulted_principal), 2) AS net_financial_yield,
    ROUND(
        ((total_interest_earned - total_defaulted_principal) / total_disbursed) * 100, 
        2
    ) AS net_yield_percentage
FROM product_stats
ORDER BY net_yield_percentage DESC;
