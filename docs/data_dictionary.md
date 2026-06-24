# CreditLens – Data Warehouse Data Dictionary

This document details the metadata and columns of the CreditLens Lending Analytics and Portfolio Intelligence star schema in PostgreSQL.

---

## 1. Dimension Tables

### Table: `dim_customer`
Stores historical attributes of borrowers at the time of credit evaluation.

| Column Name | Data Type | Nullable | Key | Constraints / Check | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `customer_key` | INT (SERIAL) | NO | PK | - | Surrogate primary key for customer dimension. |
| `customer_id` | VARCHAR(50) | NO | UK | UNIQUE | Business key representing unique customer identifier. |
| `employment_type` | VARCHAR(50) | NO | - | IN ('Salaried', 'Self-Employed', 'Freelancer', 'Unemployed') | Employment categorization of the borrower. |
| `monthly_income` | NUMERIC(15,2) | NO | - | >= 0 | Verified monthly income of the borrower. |
| `credit_score` | INT | NO | - | BETWEEN 300 AND 900 | Bureau score (CIBIL score in Indian market context). |
| `risk_tier` | VARCHAR(20) | NO | - | IN ('Super Prime', 'Prime', 'Near Prime', 'Subprime') | Derived risk categorization based on credit score. |
| `created_at` | TIMESTAMP | YES | - | DEFAULT CURRENT_TIMESTAMP | Date and time the customer record was created. |

### Table: `dim_date`
Enterprise date dimension supporting time-series aggregation.

| Column Name | Data Type | Nullable | Key | Constraints / Check | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `date_key` | INT | NO | PK | YYYYMMDD format | Integer date surrogate key. |
| `full_date` | DATE | NO | UK | UNIQUE | Standard Date format. |
| `day_of_month` | INT | NO | - | BETWEEN 1 AND 31 | Calendar day number. |
| `month_number` | INT | NO | - | BETWEEN 1 AND 12 | Calendar month number. |
| `month_name` | VARCHAR(15) | NO | - | - | Textual name of the month (e.g. 'January'). |
| `quarter` | INT | NO | - | BETWEEN 1 AND 4 | Calendar quarter of year. |
| `year` | INT | NO | - | >= 2000 | Year value. |
| `is_weekend` | BOOLEAN | NO | - | - | Indicator if date is Saturday or Sunday. |

### Table: `dim_loan_product`
Stores configurations for products offered by the lending company.

| Column Name | Data Type | Nullable | Key | Constraints / Check | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `product_key` | INT (SERIAL) | NO | PK | - | Surrogate primary key for loan product dimension. |
| `product_id` | VARCHAR(50) | NO | UK | UNIQUE | Unique loan product identifier. |
| `loan_type` | VARCHAR(50) | NO | - | IN ('Personal Loan', 'Auto Loan', 'Home Loan', 'Education Loan') | Classification of loan asset. |
| `interest_rate` | NUMERIC(5,2) | NO | - | >= 0 | Annual Interest Rate (APR) in percentage (e.g. 12.50 for 12.5%). |
| `tenure_months` | INT | NO | - | > 0 | Fixed amortization period in months. |

### Table: `dim_location`
Geographic dimension mapping borrower distributions.

| Column Name | Data Type | Nullable | Key | Constraints / Check | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `location_key` | INT (SERIAL) | NO | PK | - | Surrogate primary key for geographic location. |
| `city` | VARCHAR(100) | NO | - | - | Name of borrower city. |
| `state` | VARCHAR(100) | NO | - | - | Name of state. |
| `region` | VARCHAR(50) | NO | - | IN ('North', 'South', 'East', 'West', 'Central') | Geographic regional division. |

### Table: `dim_channel`
Funnels acquisition sources and marketing campaigns.

| Column Name | Data Type | Nullable | Key | Constraints / Check | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `channel_key` | INT (SERIAL) | NO | PK | - | Surrogate key for marketing acquisition channel. |
| `acquisition_source`| VARCHAR(100) | NO | - | IN ('Google Ads', 'Meta Ads', 'Organic Search', 'Referral', 'Partners') | Marketing source or channel. |
| `campaign_name` | VARCHAR(150) | NO | - | - | Advertising campaign name. |

---

## 2. Fact Tables

### Table: `fact_application`
Tracks initial loan request lifecycle stages and customer details.

| Column Name | Data Type | Nullable | Key | Constraints / Check | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `application_key` | INT (SERIAL) | NO | PK | - | Primary key for loan application. |
| `application_id` | VARCHAR(50) | NO | UK | UNIQUE | Business key representing unique application tracking ID. |
| `customer_key` | INT | NO | FK | REFERENCES dim_customer | Link to customer profile. |
| `location_key` | INT | NO | FK | REFERENCES dim_location | Link to applicant location. |
| `channel_key` | INT | NO | FK | REFERENCES dim_channel | Link to marketing funnel channel. |
| `product_key` | INT | NO | FK | REFERENCES dim_loan_product| Link to requested loan product configuration. |
| `application_date_key`| INT | NO | FK | REFERENCES dim_date | Date of application submission. |
| `requested_amount` | NUMERIC(15,2) | NO | - | > 0 | Financed amount requested by applicant. |
| `kyc_status` | VARCHAR(20) | NO | - | IN ('Pending', 'Passed', 'Failed') | Identity verification check status. |
| `verification_status`| VARCHAR(20) | NO | - | IN ('Pending', 'Verified', 'Rejected') | Risk/employment verification status. |

### Table: `fact_approval`
Stores decision records and manual or auto-decision outcomes.

| Column Name | Data Type | Nullable | Key | Constraints / Check | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `approval_key` | INT (SERIAL) | NO | PK | - | Primary key for loan approval transaction. |
| `application_key` | INT | NO | FK | REFERENCES fact_application | Link to originating application. |
| `customer_key` | INT | NO | FK | REFERENCES dim_customer | Link to customer profile. |
| `product_key` | INT | NO | FK | REFERENCES dim_loan_product| Link to loan product config. |
| `approval_date_key` | INT | NO | FK | REFERENCES dim_date | Date decision was reached. |
| `approved_amount` | NUMERIC(15,2) | NO | - | >= 0 | Authorized credit amount (0 if declined). |
| `approval_status` | VARCHAR(20) | NO | - | IN ('Approved', 'Declined') | Outright decision outcome. |
| `rejection_reason` | VARCHAR(255) | YES | - | - | Rejection reasons (e.g. 'Low Bureau Score'). |

### Table: `fact_disbursement`
Tracks funding events and represents active loan assets.

| Column Name | Data Type | Nullable | Key | Constraints / Check | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `disbursement_key` | INT (SERIAL) | NO | PK | - | Primary key for funded loan asset. |
| `loan_id` | VARCHAR(50) | NO | UK | UNIQUE | Primary customer-facing loan reference number. |
| `approval_key` | INT | NO | FK | REFERENCES fact_approval | Link to originating approval transaction. |
| `customer_key` | INT | NO | FK | REFERENCES dim_customer | Link to customer profile. |
| `product_key` | INT | NO | FK | REFERENCES dim_loan_product| Link to final loan product parameters. |
| `disbursement_date_key`| INT | NO | FK | REFERENCES dim_date | Date capital was sent to client. |
| `disbursed_amount` | NUMERIC(15,2) | NO | - | > 0 | Capital disbursed (funded principal). |
| `first_payment_date_key`| INT | NO | FK | REFERENCES dim_date | Due date of the first installment. |

### Table: `fact_repayment`
Tracks amortization transactions, installment statuses, and credit risk flags (DPD, defaults).

| Column Name | Data Type | Nullable | Key | Constraints / Check | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `repayment_key` | INT (SERIAL) | NO | PK | - | Primary key for repayment ledger. |
| `loan_key` | INT | NO | FK | REFERENCES fact_disbursement | Link to funded loan asset. |
| `customer_key` | INT | NO | FK | REFERENCES dim_customer | Link to customer profile. |
| `due_date_key` | INT | NO | FK | REFERENCES dim_date | Due date of installment. |
| `payment_date_key` | INT | YES | FK | REFERENCES dim_date | Actual date payment received. NULL if unpaid. |
| `installment_number`| INT | NO | - | > 0 | Order sequence of installment. |
| `installment_amount`| NUMERIC(15,2) | NO | - | > 0 | Calculated scheduled payment amount. |
| `principal_paid` | NUMERIC(15,2) | YES | - | DEFAULT 0, >= 0 | Portion of payment allocated to principal. |
| `interest_paid` | NUMERIC(15,2) | YES | - | DEFAULT 0, >= 0 | Portion of payment allocated to interest. |
| `amount_paid` | NUMERIC(15,2) | YES | - | DEFAULT 0, >= 0 | Total payment received (`principal` + `interest`). |
| `days_past_due` | INT | YES | - | DEFAULT 0, >= 0 | Days elapsed past due date without full payment. |
| `delinquency_bucket`| VARCHAR(20) | NO | - | Default 'Current'. IN ('Current', '1-30 DPD', '31-60 DPD', '61-90 DPD', '90+ DPD') | Aging categorization of unpaid balance. |
| `default_flag` | BOOLEAN | YES | - | DEFAULT FALSE | Trigger flag indicating loan default (if DPD >= 90). |
| `outstanding_balance`| NUMERIC(15,2) | NO | - | >= 0 | Remaining principal balance of the loan. |

### Table: `fact_collection`
Tracks efforts, costs, and recovery receipts on defaulted and past due accounts.

| Column Name | Data Type | Nullable | Key | Constraints / Check | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `collection_key` | INT (SERIAL) | NO | PK | - | Primary key for collection records. |
| `repayment_key` | INT | NO | FK | REFERENCES fact_repayment | Link to delinquent installment ledger. |
| `customer_key` | INT | NO | FK | REFERENCES dim_customer | Link to customer profile. |
| `assigned_date_key` | INT | NO | FK | REFERENCES dim_date | Date debt was referred to collections. |
| `action_date_key` | INT | YES | FK | REFERENCES dim_date | Date collection touchpoint occurred. |
| `collection_status` | VARCHAR(50) | NO | - | IN ('Assigned', 'Contacted', 'Promised to Pay', 'Paid', 'Unreachable') | Current status of recovery attempt. |
| `collection_strategy`| VARCHAR(50) | NO | - | IN ('SMS', 'Automated Call', 'Email', 'Agent Call', 'Field Visit') | Method used for the collection touchpoint. |
| `recovered_amount` | NUMERIC(15,2) | YES | - | DEFAULT 0, >= 0 | Recovered principal + fees collected. |
| `agent_id` | VARCHAR(50) | NO | - | - | Identifier of the collections team member. |
