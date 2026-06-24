-- MODULE 2: VINTAGE ANALYTICS

-- Query 5: Vintage Loss Curves (Cumulative NPL by Months on Book)
-- Computes how default rates rise by cohort and months on book.
WITH loan_cohorts AS (
    SELECT 
        fd.disbursement_key,
        DATE_TRUNC('month', dd.full_date) AS cohort_month,
        fd.disbursed_amount
    FROM fact_disbursement fd
    JOIN dim_date dd ON fd.disbursement_date_key = dd.date_key
),
payment_months AS (
    SELECT 
        lc.cohort_month,
        lc.disbursed_amount,
        fr.loan_key,
        dd_due.year,
        dd_due.month_number,
        ((dd_due.year - EXTRACT(YEAR FROM lc.cohort_month)) * 12 + 
         (dd_due.month_number - EXTRACT(MONTH FROM lc.cohort_month))) AS mob,
        fr.default_flag,
        fr.installment_amount
    FROM fact_repayment fr
    JOIN loan_cohorts lc ON fr.loan_key = lc.disbursement_key
    JOIN dim_date dd_due ON fr.due_date_key = dd_due.date_key
),
cohort_totals AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT loan_key) AS loans_originated,
        SUM(disbursed_amount) AS total_disbursed_amount
    FROM loan_cohorts
    GROUP BY cohort_month
),
defaults_by_mob AS (
    SELECT 
        pm.cohort_month,
        pm.mob,
        COUNT(DISTINCT pm.loan_key) AS defaulted_loans,
        SUM(pm.installment_amount) AS defaulted_amount
    FROM payment_months pm
    WHERE pm.default_flag = TRUE
    GROUP BY pm.cohort_month, pm.mob
)
SELECT 
    ct.cohort_month,
    ct.loans_originated,
    ct.total_disbursed_amount,
    dbm.mob,
    COALESCE(dbm.defaulted_loans, 0) AS new_defaults_in_mob,
    SUM(COALESCE(dbm.defaulted_loans, 0)) OVER (
        PARTITION BY ct.cohort_month 
        ORDER BY dbm.mob
    ) AS cumulative_defaults,
    ROUND(
        (SUM(COALESCE(dbm.defaulted_loans, 0)) OVER (
            PARTITION BY ct.cohort_month 
            ORDER BY dbm.mob
        )::numeric / ct.loans_originated) * 100, 
        2
    ) AS cumulative_default_rate_pct
FROM cohort_totals ct
CROSS JOIN generate_series(0, 12) AS dbm(mob)
LEFT JOIN defaults_by_mob dbm ON ct.cohort_month = dbm.cohort_month AND dbm.mob = dbm.mob
ORDER BY ct.cohort_month, dbm.mob;


-- Query 6: Transition Matrix / Delinquency Roll Rates
-- Tracks the month-over-month roll rate probability of delinquent accounts.
WITH monthly_loan_status AS (
    SELECT 
        fr.loan_key,
        dd.month_number,
        dd.year,
        fr.delinquency_bucket,
        ROW_NUMBER() OVER (PARTITION BY fr.loan_key ORDER BY dd.year, dd.month_number) AS installment_seq
    FROM fact_repayment fr
    JOIN dim_date dd ON fr.due_date_key = dd.date_key
),
transitions AS (
    SELECT 
        curr.loan_key,
        curr.delinquency_bucket AS start_status,
        LEAD(curr.delinquency_bucket) OVER (PARTITION BY curr.loan_key ORDER BY curr.installment_seq) AS end_status
    FROM monthly_loan_status curr
)
SELECT 
    start_status,
    end_status,
    COUNT(*) AS transition_count,
    ROUND(
        (COUNT(*)::numeric / SUM(COUNT(*)) OVER (PARTITION BY start_status)) * 100, 
        2
    ) AS transition_probability_pct
FROM transitions
WHERE end_status IS NOT NULL
GROUP BY start_status, end_status
ORDER BY start_status, end_status;


-- Query 7: Post-Default Recovery Rate by Vintage Year
-- Evaluates recovery collection success percentages across annual vintages.
WITH defaulted_loans AS (
    SELECT 
        fd.loan_id,
        EXTRACT(YEAR FROM dd_disb.full_date) AS vintage_year,
        fd.disbursed_amount,
        SUM(fr.installment_amount) AS total_defaulted_principal
    FROM fact_repayment fr
    JOIN fact_disbursement fd ON fr.loan_key = fd.disbursement_key
    JOIN dim_date dd_disb ON fd.disbursement_date_key = dd_disb.date_key
    WHERE fr.default_flag = TRUE
    GROUP BY fd.loan_id, dd_disb.full_date, fd.disbursed_amount
),
recovery_totals AS (
    SELECT 
        dl.vintage_year,
        COUNT(DISTINCT dl.loan_id) AS total_defaulted_count,
        SUM(dl.total_defaulted_principal) AS default_exposure,
        SUM(fc.recovered_amount) AS total_recovered
    FROM defaulted_loans dl
    LEFT JOIN fact_repayment fr ON fr.loan_key = (SELECT disbursement_key FROM fact_disbursement WHERE loan_id = dl.loan_id LIMIT 1)
    LEFT JOIN fact_collection fc ON fr.repayment_key = fc.repayment_key
    GROUP BY dl.vintage_year
)
SELECT 
    vintage_year,
    total_defaulted_count,
    ROUND(default_exposure, 2) AS gross_loss_amount,
    ROUND(total_recovered, 2) AS recovered_amount,
    ROUND((total_recovered / NULLIF(default_exposure, 0)) * 100, 2) AS recovery_rate_pct,
    ROUND((default_exposure - total_recovered), 2) AS net_writeoff_loss
FROM recovery_totals
ORDER BY vintage_year;
