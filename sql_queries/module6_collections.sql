-- MODULE 6: COLLECTIONS ANALYTICS

-- Query 16: Collections Efficiency Index (CEI) & Recoveries by Agent
-- Ranks recovery collections efficiency across agents.
WITH agent_collections AS (
    SELECT 
        fc.agent_id,
        COUNT(fc.collection_key) AS total_assigned_cases,
        SUM(fr.installment_amount) AS total_assigned_amount,
        SUM(fc.recovered_amount) AS total_recovered_amount
    FROM fact_collection fc
    JOIN fact_repayment fr ON fc.repayment_key = fr.repayment_key
    GROUP BY fc.agent_id
)
SELECT 
    agent_id,
    total_assigned_cases,
    ROUND(total_assigned_amount, 2) AS assigned_amt,
    ROUND(total_recovered_amount, 2) AS recovered_amt,
    ROUND((total_recovered_amount / total_assigned_amount) * 100, 2) AS collections_efficiency_index_pct,
    DENSE_RANK() OVER (ORDER BY (total_recovered_amount / total_assigned_amount) DESC) AS agent_performance_rank
FROM agent_collections
ORDER BY agent_performance_rank;


-- Query 17: Average Days to Recover Past-Due Installments
-- Analyzes speed of collections across geographical regions.
SELECT 
    dl.region,
    COUNT(fc.collection_key) AS recovered_accounts,
    ROUND(AVG(dd_pay.full_date - dd_due.full_date)::numeric, 1) AS avg_days_to_recover,
    ROUND(SUM(fc.recovered_amount), 2) AS total_recovered
FROM fact_collection fc
JOIN fact_repayment fr ON fc.repayment_key = fr.repayment_key
JOIN dim_date dd_due ON fr.due_date_key = dd_due.date_key
JOIN dim_date dd_pay ON fr.payment_date_key = dd_pay.date_key
JOIN dim_location dl ON fc.customer_key = (SELECT customer_key FROM dim_customer WHERE customer_key = fc.customer_key LIMIT 1)
WHERE fc.collection_status = 'Paid'
GROUP BY dl.region
ORDER BY avg_days_to_recover ASC;


-- Query 18: Collection Strategy Effectiveness Analysis
-- Compares resolution success rates of different outreach channels.
SELECT 
    fr.delinquency_bucket,
    fc.collection_strategy,
    COUNT(fc.collection_key) AS contact_attempts,
    SUM(CASE WHEN fc.collection_status = 'Paid' THEN 1 ELSE 0 END) AS success_counts,
    ROUND(
        (SUM(CASE WHEN fc.collection_status = 'Paid' THEN 1 ELSE 0 END)::numeric / COUNT(fc.collection_key)) * 100, 
        2
    ) AS resolution_rate_pct
FROM fact_collection fc
JOIN fact_repayment fr ON fc.repayment_key = fr.repayment_key
GROUP BY fr.delinquency_bucket, fc.collection_strategy
ORDER BY fr.delinquency_bucket, resolution_rate_pct DESC;
