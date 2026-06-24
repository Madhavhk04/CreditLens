-- MODULE 7: GEOGRAPHIC ANALYTICS

-- Query 19: State-Level Concentration & Loss Heatmap Data
-- Ranks and maps states based on exposure vs credit defaults.
WITH state_portfolio AS (
    SELECT 
        dloc.state,
        COUNT(DISTINCT fd.disbursement_key) AS active_loans,
        SUM(fd.disbursed_amount) AS total_disbursed,
        SUM(CASE WHEN fr.default_flag = TRUE THEN fr.outstanding_balance ELSE 0 END) AS outstanding_loss_exposure,
        COALESCE(SUM(fr.interest_paid), 0) AS interest_collected
    FROM dim_location dloc
    JOIN fact_application fa ON dloc.location_key = fa.location_key
    JOIN fact_approval fap ON fa.application_key = fap.application_key
    JOIN fact_disbursement fd ON fap.approval_key = fd.approval_key
    LEFT JOIN fact_repayment fr ON fd.disbursement_key = fr.loan_key
    GROUP BY dloc.state
)
SELECT 
    state,
    active_loans,
    ROUND(total_disbursed, 2) AS total_disbursed,
    ROUND(outstanding_loss_exposure, 2) AS defaulted_balance,
    ROUND((outstanding_loss_exposure / total_disbursed) * 100, 2) AS default_rate_pct,
    RANK() OVER (ORDER BY total_disbursed DESC) AS volume_rank,
    DENSE_RANK() OVER (ORDER BY (outstanding_loss_exposure / total_disbursed) DESC) AS risk_rank
FROM state_portfolio
ORDER BY default_rate_pct DESC;


-- Query 20: City-Level Default Outliers (Above State Average)
-- Finds outlier cities that significantly exceed their own state average.
WITH city_state_defaults AS (
    SELECT 
        dl.state,
        dl.city,
        COUNT(DISTINCT fd.disbursement_key) AS total_loans,
        COUNT(CASE WHEN fr.default_flag = TRUE THEN 1 END) AS default_loans,
        ROUND(
            (COUNT(CASE WHEN fr.default_flag = TRUE THEN 1 END)::numeric / 
             NULLIF(COUNT(DISTINCT fd.disbursement_key), 0)) * 100, 
            2
        ) AS city_default_rate_pct
    FROM dim_location dl
    JOIN fact_application fa ON dl.location_key = fa.location_key
    JOIN fact_approval fap ON fa.application_key = fap.application_key
    JOIN fact_disbursement fd ON fap.approval_key = fd.approval_key
    LEFT JOIN fact_repayment fr ON fd.disbursement_key = fr.loan_key
    GROUP BY dl.state, dl.city
),
state_baselines AS (
    SELECT 
        state,
        city,
        total_loans,
        city_default_rate_pct,
        ROUND(
            AVG(city_default_rate_pct) OVER (PARTITION BY state)::numeric, 
            2
        ) AS state_avg_default_rate
    FROM city_state_defaults
    WHERE total_loans >= 50
)
SELECT 
    state,
    city,
    total_loans,
    city_default_rate_pct,
    state_avg_default_rate,
    ROUND((city_default_rate_pct / NULLIF(state_avg_default_rate, 0)), 2) AS variance_ratio
FROM state_baselines
WHERE city_default_rate_pct > (state_avg_default_rate * 1.5)
ORDER BY variance_ratio DESC;
