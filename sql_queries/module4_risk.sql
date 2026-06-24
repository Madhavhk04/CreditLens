-- MODULE 4: RISK SEGMENTATION

-- Query 11: Delinquency Rate by Credit Score Range
-- Analyzes defaults across typical bureau score groupings.
WITH customer_scorecard AS (
    SELECT 
        CASE 
            WHEN credit_score >= 800 THEN '800-900 (Excellent)'
            WHEN credit_score BETWEEN 740 AND 799 THEN '740-799 (Very Good)'
            WHEN credit_score BETWEEN 670 AND 739 THEN '670-739 (Good)'
            WHEN credit_score BETWEEN 580 AND 669 THEN '580-669 (Fair)'
            ELSE '300-579 (Poor/Subprime)'
        END AS credit_score_band,
        fd.disbursement_key,
        CASE WHEN fr.default_flag = TRUE THEN 1 ELSE 0 END AS is_defaulted
    FROM fact_disbursement fd
    JOIN dim_customer dc ON fd.customer_key = dc.customer_key
    LEFT JOIN fact_repayment fr ON fd.disbursement_key = fr.loan_key
)
SELECT 
    credit_score_band,
    COUNT(DISTINCT disbursement_key) AS loans_funded,
    SUM(is_defaulted) AS defaulted_loans,
    ROUND((SUM(is_defaulted)::numeric / COUNT(DISTINCT disbursement_key)) * 100, 2) AS default_rate_pct
FROM customer_scorecard
GROUP BY credit_score_band
ORDER BY credit_score_band;


-- Query 12: NTILE Portfolio Score Quartile Risk Profiling
-- Distributes originations into score quartiles to monitor losses vs. interest.
WITH ranked_loans AS (
    SELECT 
        fd.disbursement_key,
        dc.credit_score,
        fd.disbursed_amount,
        COALESCE(SUM(fr.interest_paid), 0) AS interest_paid,
        MAX(CASE WHEN fr.default_flag = TRUE THEN 1 ELSE 0 END) AS defaulted,
        NTILE(4) OVER (ORDER BY dc.credit_score ASC) AS credit_quartile
    FROM fact_disbursement fd
    JOIN dim_customer dc ON fd.customer_key = dc.customer_key
    LEFT JOIN fact_repayment fr ON fd.disbursement_key = fr.loan_key
    GROUP BY fd.disbursement_key, dc.credit_score, fd.disbursed_amount
)
SELECT 
    credit_quartile,
    MIN(credit_score) AS min_score_in_quartile,
    MAX(credit_score) AS max_score_in_quartile,
    COUNT(disbursement_key) AS total_loans,
    ROUND(SUM(disbursed_amount), 2) AS total_disbursed,
    ROUND(SUM(interest_paid), 2) AS interest_collected,
    SUM(defaulted) AS defaults,
    ROUND((SUM(defaulted)::numeric / COUNT(disbursement_key)) * 100, 2) AS default_rate_pct
FROM ranked_loans
GROUP BY credit_quartile
ORDER BY credit_quartile;


-- Query 13: High-Exposure Delinquent Borrowers (Debt Cover Ranking)
-- Isolates and prioritizes collections based on monthly installment relative to income.
WITH delinquent_exposure AS (
    SELECT 
        dc.customer_id,
        dc.monthly_income,
        fd.loan_id,
        fr.installment_amount,
        fr.days_past_due,
        fr.delinquency_bucket,
        ROUND((fr.installment_amount / dc.monthly_income) * 100, 2) AS installment_to_income_pct
    FROM fact_repayment fr
    JOIN fact_disbursement fd ON fr.loan_key = fd.disbursement_key
    JOIN dim_customer dc ON fr.customer_key = dc.customer_key
    WHERE fr.days_past_due > 30
)
SELECT 
    customer_id,
    monthly_income,
    loan_id,
    installment_amount,
    days_past_due,
    delinquency_bucket,
    installment_to_income_pct,
    DENSE_RANK() OVER (
        PARTITION BY delinquency_bucket 
        ORDER BY installment_to_income_pct DESC, days_past_due DESC
    ) AS priority_rank
FROM delinquent_exposure
ORDER BY delinquency_bucket, priority_rank;
