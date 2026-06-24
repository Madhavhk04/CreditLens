-- PostgreSQL DDL Script for CreditLens Star Schema

-- ==========================================
-- 1. DIMENSION TABLES
-- ==========================================

-- Customer Dimension
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    employment_type VARCHAR(50) NOT NULL CHECK (employment_type IN ('Salaried', 'Self-Employed', 'Freelancer', 'Unemployed')),
    monthly_income NUMERIC(15, 2) NOT NULL CHECK (monthly_income >= 0),
    credit_score INT NOT NULL CHECK (credit_score BETWEEN 300 AND 900),
    risk_tier VARCHAR(20) NOT NULL CHECK (risk_tier IN ('Super Prime', 'Prime', 'Near Prime', 'Subprime')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Date Dimension
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY, -- YYYYMMDD
    full_date DATE UNIQUE NOT NULL,
    day_of_month INT NOT NULL CHECK (day_of_month BETWEEN 1 AND 31),
    month_number INT NOT NULL CHECK (month_number BETWEEN 1 AND 12),
    month_name VARCHAR(15) NOT NULL,
    quarter INT NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    year INT NOT NULL CHECK (year >= 2000),
    is_weekend BOOLEAN NOT NULL
);

-- Loan Product Dimension
CREATE TABLE dim_loan_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    loan_type VARCHAR(50) NOT NULL CHECK (loan_type IN ('Personal Loan', 'Auto Loan', 'Home Loan', 'Education Loan')),
    interest_rate NUMERIC(5, 2) NOT NULL CHECK (interest_rate >= 0),
    tenure_months INT NOT NULL CHECK (tenure_months > 0)
);

-- Location Dimension
CREATE TABLE dim_location (
    location_key SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL CHECK (region IN ('North', 'South', 'East', 'West', 'Central'))
);

-- Channel Dimension
CREATE TABLE dim_channel (
    channel_key SERIAL PRIMARY KEY,
    acquisition_source VARCHAR(100) NOT NULL CHECK (acquisition_source IN ('Google Ads', 'Meta Ads', 'Organic Search', 'Referral', 'Partners')),
    campaign_name VARCHAR(150) NOT NULL
);

-- ==========================================
-- 2. FACT TABLES
-- ==========================================

-- Application Fact
CREATE TABLE fact_application (
    application_key SERIAL PRIMARY KEY,
    application_id VARCHAR(50) UNIQUE NOT NULL,
    customer_key INT NOT NULL REFERENCES dim_customer(customer_key),
    location_key INT NOT NULL REFERENCES dim_location(location_key),
    channel_key INT NOT NULL REFERENCES dim_channel(channel_key),
    product_key INT NOT NULL REFERENCES dim_loan_product(product_key),
    application_date_key INT NOT NULL REFERENCES dim_date(date_key),
    requested_amount NUMERIC(15, 2) NOT NULL CHECK (requested_amount > 0),
    kyc_status VARCHAR(20) NOT NULL CHECK (kyc_status IN ('Pending', 'Passed', 'Failed')),
    verification_status VARCHAR(20) NOT NULL CHECK (verification_status IN ('Pending', 'Verified', 'Rejected'))
);

-- Approval Fact
CREATE TABLE fact_approval (
    approval_key SERIAL PRIMARY KEY,
    application_key INT NOT NULL REFERENCES fact_application(application_key),
    customer_key INT NOT NULL REFERENCES dim_customer(customer_key),
    product_key INT NOT NULL REFERENCES dim_loan_product(product_key),
    approval_date_key INT NOT NULL REFERENCES dim_date(date_key),
    approved_amount NUMERIC(15, 2) NOT NULL CHECK (approved_amount >= 0),
    approval_status VARCHAR(20) NOT NULL CHECK (approval_status IN ('Approved', 'Declined')),
    rejection_reason VARCHAR(255)
);

-- Disbursement Fact
CREATE TABLE fact_disbursement (
    disbursement_key SERIAL PRIMARY KEY,
    loan_id VARCHAR(50) UNIQUE NOT NULL,
    approval_key INT NOT NULL REFERENCES fact_approval(approval_key),
    customer_key INT NOT NULL REFERENCES dim_customer(customer_key),
    product_key INT NOT NULL REFERENCES dim_loan_product(product_key),
    disbursement_date_key INT NOT NULL REFERENCES dim_date(date_key),
    disbursed_amount NUMERIC(15, 2) NOT NULL CHECK (disbursed_amount > 0),
    first_payment_date_key INT NOT NULL REFERENCES dim_date(date_key)
);

-- Repayment Fact
CREATE TABLE fact_repayment (
    repayment_key SERIAL PRIMARY KEY,
    loan_key INT NOT NULL REFERENCES fact_disbursement(disbursement_key),
    customer_key INT NOT NULL REFERENCES dim_customer(customer_key),
    due_date_key INT NOT NULL REFERENCES dim_date(date_key),
    payment_date_key INT REFERENCES dim_date(date_key), -- Can be NULL if unpaid
    installment_number INT NOT NULL CHECK (installment_number > 0),
    installment_amount NUMERIC(15, 2) NOT NULL CHECK (installment_amount > 0),
    principal_paid NUMERIC(15, 2) DEFAULT 0 CHECK (principal_paid >= 0),
    interest_paid NUMERIC(15, 2) DEFAULT 0 CHECK (interest_paid >= 0),
    amount_paid NUMERIC(15, 2) DEFAULT 0 CHECK (amount_paid >= 0),
    days_past_due INT DEFAULT 0 CHECK (days_past_due >= 0),
    delinquency_bucket VARCHAR(20) NOT NULL DEFAULT 'Current' 
        CHECK (delinquency_bucket IN ('Current', '1-30 DPD', '31-60 DPD', '61-90 DPD', '90+ DPD')),
    default_flag BOOLEAN DEFAULT FALSE,
    outstanding_balance NUMERIC(15, 2) NOT NULL CHECK (outstanding_balance >= 0)
);

-- Collection Fact
CREATE TABLE fact_collection (
    collection_key SERIAL PRIMARY KEY,
    repayment_key INT NOT NULL REFERENCES fact_repayment(repayment_key),
    customer_key INT NOT NULL REFERENCES dim_customer(customer_key),
    assigned_date_key INT NOT NULL REFERENCES dim_date(date_key),
    action_date_key INT REFERENCES dim_date(date_key), -- Date action took place (can be NULL initially)
    collection_status VARCHAR(50) NOT NULL CHECK (collection_status IN ('Assigned', 'Contacted', 'Promised to Pay', 'Paid', 'Unreachable')),
    collection_strategy VARCHAR(50) NOT NULL CHECK (collection_strategy IN ('SMS', 'Automated Call', 'Email', 'Agent Call', 'Field Visit')),
    recovered_amount NUMERIC(15, 2) DEFAULT 0 CHECK (recovered_amount >= 0),
    agent_id VARCHAR(50) NOT NULL
);

-- ==========================================
-- 3. ANALYTICAL PERFORMANCE INDEXES
-- ==========================================

-- Application Date and Location Index for Channel/Geographic performance
CREATE INDEX idx_fact_app_analytics ON fact_application (application_date_key, location_key, channel_key);

-- Disbursement Date and Customer Key for Portfolio Vintage modeling
CREATE INDEX idx_fact_disb_vintage ON fact_disbursement (disbursement_date_key, customer_key, product_key);

-- Repayment Delinquency and Default tracking indexes
CREATE INDEX idx_fact_repay_status ON fact_repayment (loan_key, due_date_key, default_flag, delinquency_bucket);
CREATE INDEX idx_fact_repay_customer ON fact_repayment (customer_key);

-- Collections Strategy index for performance evaluations
CREATE INDEX idx_fact_coll_eval ON fact_collection (assigned_date_key, collection_strategy, collection_status);
