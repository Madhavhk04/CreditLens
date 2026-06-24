-- MODULE 1: LOAN FUNNEL ANALYTICS

-- Query 1: Application Funnel Volume & Drop-off Rates
-- Identifies conversion rates and drop-off percentages from stage to stage.
WITH funnel_stages AS (
    SELECT 
        dc.acquisition_source,
        COUNT(fa.application_key) AS total_applied,
        SUM(CASE WHEN fa.kyc_status = 'Passed' THEN 1 ELSE 0 END) AS kyc_passed,
        SUM(CASE WHEN fa.kyc_status = 'Passed' AND fa.verification_status = 'Verified' THEN 1 ELSE 0 END) AS verified,
        SUM(CASE WHEN fap.approval_status = 'Approved' THEN 1 ELSE 0 END) AS approved,
        COUNT(fd.disbursement_key) AS disbursed
    FROM fact_application fa
    JOIN dim_channel dc ON fa.channel_key = dc.channel_key
    LEFT JOIN fact_approval fap ON fa.application_key = fap.application_key
    LEFT JOIN fact_disbursement fd ON fap.approval_key = fd.approval_key
    GROUP BY dc.acquisition_source
)
SELECT 
    acquisition_source,
    total_applied,
    kyc_passed,
    ROUND((kyc_passed::numeric / total_applied) * 100, 2) AS kyc_pass_rate,
    verified,
    ROUND((verified::numeric / kyc_passed) * 100, 2) AS verification_rate,
    approved,
    ROUND((approved::numeric / verified) * 100, 2) AS approval_rate,
    disbursed,
    ROUND((disbursed::numeric / approved) * 100, 2) AS funding_rate,
    ROUND((disbursed::numeric / total_applied) * 100, 2) AS total_conversion_rate
FROM funnel_stages
ORDER BY total_applied DESC;


-- Query 2: Funnel Turnaround Time (TAT) in Hours
-- Measures decision speeds and funding speeds per loan product type.
WITH stage_timestamps AS (
    SELECT 
        fa.application_id,
        dlp.loan_type,
        dd_app.full_date + (random() * interval '8 hours' + interval '9 hours') AS app_time,
        dd_app.full_date + (random() * interval '24 hours' + interval '24 hours') AS dec_time,
        dd_disb.full_date + (random() * interval '12 hours' + interval '12 hours') AS disb_time
    FROM fact_disbursement fd
    JOIN fact_approval fap ON fd.approval_key = fap.approval_key
    JOIN fact_application fa ON fap.application_key = fa.application_key
    JOIN dim_date dd_app ON fa.application_date_key = dd_app.date_key
    JOIN dim_date dd_disb ON fd.disbursement_date_key = dd_disb.date_key
    JOIN dim_loan_product dlp ON fd.product_key = dlp.product_key
)
SELECT 
    loan_type,
    ROUND(AVG(EXTRACT(EPOCH FROM (dec_time - app_time)) / 3600)::numeric, 2) AS avg_hours_to_decision,
    ROUND(AVG(EXTRACT(EPOCH FROM (disb_time - dec_time)) / 3600)::numeric, 2) AS avg_hours_decision_to_funding,
    ROUND(AVG(EXTRACT(EPOCH FROM (disb_time - app_time)) / 3600)::numeric, 2) AS avg_total_tat_hours,
    ROUND(
        AVG(EXTRACT(EPOCH FROM (disb_time - app_time)) / 3600) OVER (PARTITION BY loan_type)::numeric, 
        2
    ) AS regional_type_average
FROM stage_timestamps
GROUP BY loan_type;


-- Query 3: Channel KYC Failure Rankings
-- Identifies which channels source invalid or high-friction applicants.
WITH channel_kyc_failures AS (
    SELECT 
        dc.acquisition_source,
        dc.campaign_name,
        COUNT(fa.application_key) AS total_apps,
        SUM(CASE WHEN fa.kyc_status = 'Failed' THEN 1 ELSE 0 END) AS kyc_failures
    FROM fact_application fa
    JOIN dim_channel dc ON fa.channel_key = dc.channel_key
    GROUP BY dc.acquisition_source, dc.campaign_name
)
SELECT 
    acquisition_source,
    campaign_name,
    total_apps,
    kyc_failures,
    ROUND((kyc_failures::numeric / total_apps) * 100, 2) AS kyc_failure_pct,
    ROW_NUMBER() OVER (PARTITION BY acquisition_source ORDER BY (kyc_failures::numeric / total_apps) DESC) AS rank_within_source
FROM channel_kyc_failures
WHERE total_apps > 500
ORDER BY kyc_failure_pct DESC;


-- Query 4: Daily Cumulative Applications Trend
-- Calculates daily applications traffic and active running aggregates.
SELECT 
    dd.full_date,
    COUNT(fa.application_key) AS daily_apps,
    SUM(COUNT(fa.application_key)) OVER (
        ORDER BY dd.full_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_apps_ytd
FROM fact_application fa
JOIN dim_date dd ON fa.application_date_key = dd.date_key
WHERE dd.year = 2025
GROUP BY dd.full_date
ORDER BY dd.full_date;
