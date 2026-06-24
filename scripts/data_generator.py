import os
import random
import datetime
import numpy as np
import pandas as pd
from faker import Faker

def run_generator():
    print("Initializing CreditLens Synthetic Data Generator...")
    fake = Faker('en_IN') # Localized for Indian city/state names
    random.seed(42)
    np.random.seed(42)

    output_dir = os.path.join("data_warehouse", "raw_csvs")
    os.makedirs(output_dir, exist_ok=True)

    # ==========================================
    # 1. GENERATE DIM_DATE
    # ==========================================
    print("Generating Date Dimension...")
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2026, 6, 30)
    delta = end_date - start_date

    date_records = []
    for i in range(delta.days + 1):
        d = start_date + datetime.timedelta(days=i)
        date_records.append({
            'date_key': int(d.strftime("%Y%m%d")),
            'full_date': d,
            'day_of_month': d.day,
            'month_number': d.month,
            'month_name': d.strftime("%B"),
            'quarter': (d.month - 1) // 3 + 1,
            'year': d.year,
            'is_weekend': d.weekday() in (5, 6)
        })
    df_date = pd.DataFrame(date_records)
    df_date.to_csv(os.path.join(output_dir, "dim_date.csv"), index=False)

    # ==========================================
    # 2. GENERATE DIM_CUSTOMER
    # ==========================================
    print("Generating Customer Dimension (100,000+)...")
    num_customers = 105000
    employment_types = ['Salaried', 'Self-Employed', 'Freelancer', 'Unemployed']
    emp_probs = [0.60, 0.25, 0.10, 0.05]

    # Generate correlated incomes and credit scores
    credit_scores = np.random.normal(loc=710, scale=75, size=num_customers)
    credit_scores = np.clip(credit_scores, 300, 900).astype(int)

    customer_records = []
    for i in range(num_customers):
        c_id = f"CUST-{i+1:06d}"
        emp = np.random.choice(employment_types, p=emp_probs)
        
        # Correlate income with employment type
        if emp == 'Salaried':
            income = np.random.lognormal(mean=10.5, sigma=0.4)
        elif emp == 'Self-Employed':
            income = np.random.lognormal(mean=10.8, sigma=0.6)
        elif emp == 'Freelancer':
            income = np.random.lognormal(mean=10.2, sigma=0.5)
        else: # Unemployed
            income = np.random.lognormal(mean=9.5, sigma=0.3)
        
        income = round(income, 2)
        score = credit_scores[i]

        # Map credit score to risk tier
        if score >= 750:
            tier = 'Super Prime'
        elif score >= 700:
            tier = 'Prime'
        elif score >= 650:
            tier = 'Near Prime'
        else:
            tier = 'Subprime'

        customer_records.append({
            'customer_key': i + 1,
            'customer_id': c_id,
            'employment_type': emp,
            'monthly_income': income,
            'credit_score': score,
            'risk_tier': tier
        })
    df_customer = pd.DataFrame(customer_records)
    df_customer.to_csv(os.path.join(output_dir, "dim_customer.csv"), index=False)

    # ==========================================
    # 3. GENERATE DIM_LOAN_PRODUCT
    # ==========================================
    print("Generating Loan Product Dimension...")
    products = [
        {'product_key': 1, 'product_id': 'PROD-PL', 'loan_type': 'Personal Loan', 'interest_rate': 15.00, 'tenure_months': 12},
        {'product_key': 2, 'product_id': 'PROD-AL', 'loan_type': 'Auto Loan', 'interest_rate': 10.00, 'tenure_months': 36},
        {'product_key': 3, 'product_id': 'PROD-HL', 'loan_type': 'Home Loan', 'interest_rate': 8.50, 'tenure_months': 120},
        {'product_key': 4, 'product_id': 'PROD-EL', 'loan_type': 'Education Loan', 'interest_rate': 11.00, 'tenure_months': 60}
    ]
    df_product = pd.DataFrame(products)
    df_product.to_csv(os.path.join(output_dir, "dim_loan_product.csv"), index=False)

    # ==========================================
    # 4. GENERATE DIM_LOCATION
    # ==========================================
    print("Generating Location Dimension...")
    locations = [
        {'location_key': 1, 'city': 'Mumbai', 'state': 'Maharashtra', 'region': 'West'},
        {'location_key': 2, 'Pune': 'Pune', 'city': 'Pune', 'state': 'Maharashtra', 'region': 'West'},
        {'location_key': 3, 'city': 'Nagpur', 'state': 'Maharashtra', 'region': 'West'},
        {'location_key': 4, 'city': 'Delhi', 'state': 'Delhi', 'region': 'North'},
        {'location_key': 5, 'city': 'Noida', 'state': 'Uttar Pradesh', 'region': 'North'},
        {'location_key': 6, 'city': 'Lucknow', 'state': 'Uttar Pradesh', 'region': 'North'},
        {'location_key': 7, 'city': 'Kanpur', 'state': 'Uttar Pradesh', 'region': 'North'},
        {'location_key': 8, 'city': 'Bengaluru', 'state': 'Karnataka', 'region': 'South'},
        {'location_key': 9, 'city': 'Mysore', 'state': 'Karnataka', 'region': 'South'},
        {'location_key': 10, 'city': 'Chennai', 'state': 'Tamil Nadu', 'region': 'South'},
        {'location_key': 11, 'city': 'Coimbatore', 'state': 'Tamil Nadu', 'region': 'South'},
        {'location_key': 12, 'city': 'Hyderabad', 'state': 'Telangana', 'region': 'South'},
        {'location_key': 13, 'city': 'Kolkata', 'state': 'West Bengal', 'region': 'East'},
        {'location_key': 14, 'city': 'Patna', 'state': 'Bihar', 'region': 'East'},
        {'location_key': 15, 'city': 'Bhopal', 'state': 'Madhya Pradesh', 'region': 'Central'},
        {'location_key': 16, 'city': 'Indore', 'state': 'Madhya Pradesh', 'region': 'Central'},
        {'location_key': 17, 'city': 'Ahmedabad', 'state': 'Gujarat', 'region': 'West'},
        {'location_key': 18, 'city': 'Jaipur', 'state': 'Rajasthan', 'region': 'West'},
        {'location_key': 19, 'city': 'Guwahati', 'state': 'Assam', 'region': 'East'},
        {'location_key': 20, 'city': 'Chandigarh', 'state': 'Punjab', 'region': 'North'}
    ]
    # Clean location data structures
    for loc in locations:
        if 'Pune' in loc and loc['Pune'] == 'Pune':
            del loc['Pune']
    df_location = pd.DataFrame(locations)
    df_location.to_csv(os.path.join(output_dir, "dim_location.csv"), index=False)

    # ==========================================
    # 5. GENERATE DIM_CHANNEL
    # ==========================================
    print("Generating Channel Dimension...")
    channels = [
        {'channel_key': 1, 'acquisition_source': 'Google Ads', 'campaign_name': 'festive_cash_pl'},
        {'channel_key': 2, 'acquisition_source': 'Google Ads', 'campaign_name': 'brand_search_generic'},
        {'channel_key': 3, 'acquisition_source': 'Meta Ads', 'campaign_name': 'social_stories_auto'},
        {'channel_key': 4, 'acquisition_source': 'Organic Search', 'campaign_name': 'organic_seo_loans'},
        {'channel_key': 5, 'acquisition_source': 'Referral', 'campaign_name': 'customer_invite_program'},
        {'channel_key': 6, 'acquisition_source': 'Partners', 'campaign_name': 'aggregator_policy_bazaar'}
    ]
    df_channel = pd.DataFrame(channels)
    df_channel.to_csv(os.path.join(output_dir, "dim_channel.csv"), index=False)

    # ==========================================
    # 6. GENERATE FACT_APPLICATION (250,000)
    # ==========================================
    print("Generating Application Fact Table...")
    num_applications = 260000
    app_records = []
    
    # Assign date ranges
    app_dates = df_date['date_key'].values
    location_keys = df_location['location_key'].values
    channel_keys = df_channel['channel_key'].values
    product_keys = df_product['product_key'].values

    for i in range(num_applications):
        app_id = f"APP-{i+1:06d}"
        cust_key = random.randint(1, num_customers)
        loc_key = random.choice(location_keys)
        ch_key = random.choice(channel_keys)
        prod_key = random.choice(product_keys)
        app_date = random.choice(app_dates)
        
        # Correlate requested amount to income
        income = df_customer.at[cust_key - 1, 'monthly_income']
        req_amount = round(income * random.uniform(2, 6), 2)
        
        # Risk Tier probabilistic states
        tier = df_customer.at[cust_key - 1, 'risk_tier']
        if tier == 'Super Prime':
            kyc = np.random.choice(['Passed', 'Failed'], p=[0.98, 0.02])
            ver = np.random.choice(['Verified', 'Rejected'], p=[0.97, 0.03])
        elif tier == 'Prime':
            kyc = np.random.choice(['Passed', 'Failed'], p=[0.95, 0.05])
            ver = np.random.choice(['Verified', 'Rejected'], p=[0.92, 0.08])
        elif tier == 'Near Prime':
            kyc = np.random.choice(['Passed', 'Failed'], p=[0.88, 0.12])
            ver = np.random.choice(['Verified', 'Rejected'], p=[0.82, 0.18])
        else: # Subprime
            kyc = np.random.choice(['Passed', 'Failed'], p=[0.70, 0.30])
            ver = np.random.choice(['Verified', 'Rejected'], p=[0.60, 0.40])

        app_records.append({
            'application_key': i + 1,
            'application_id': app_id,
            'customer_key': cust_key,
            'location_key': loc_key,
            'channel_key': ch_key,
            'product_key': prod_key,
            'application_date_key': app_date,
            'requested_amount': req_amount,
            'kyc_status': kyc,
            'verification_status': ver
        })
    df_app = pd.DataFrame(app_records)
    df_app.to_csv(os.path.join(output_dir, "fact_application.csv"), index=False)

    # ==========================================
    # 7. GENERATE FACT_APPROVAL
    # ==========================================
    print("Generating Approval Fact Table...")
    approval_records = []
    app_counter = 1

    for row in df_app.itertuples():
        kyc = row.kyc_status
        ver = row.verification_status
        cust_key = row.customer_key
        tier = df_customer.at[cust_key - 1, 'risk_tier']

        # Determine decision states
        if kyc == 'Passed' and ver == 'Verified':
            if tier == 'Super Prime':
                decision = np.random.choice(['Approved', 'Declined'], p=[0.95, 0.05])
            elif tier == 'Prime':
                decision = np.random.choice(['Approved', 'Declined'], p=[0.85, 0.15])
            elif tier == 'Near Prime':
                decision = np.random.choice(['Approved', 'Declined'], p=[0.65, 0.35])
            else: # Subprime
                decision = np.random.choice(['Approved', 'Declined'], p=[0.35, 0.65])
        else:
            decision = 'Declined'

        if decision == 'Approved':
            approved_amt = round(row.requested_amount * random.uniform(0.9, 1.0), 2)
            reason = None
        else:
            approved_amt = 0.0
            reasons = ['Low Credit Score', 'Insufficient Income', 'Verification Discrepancy', 'KYC Fail']
            reason = random.choice(reasons) if kyc != 'Passed' or ver != 'Verified' else 'Credit Policy Decline'

        approval_records.append({
            'approval_key': app_counter,
            'application_key': row.application_key,
            'customer_key': cust_key,
            'product_key': row.product_key,
            'approval_date_key': row.application_date_key + 2, # Decided 2 days later
            'approved_amount': approved_amt,
            'approval_status': decision,
            'rejection_reason': reason
        })
        app_counter += 1

    df_approval = pd.DataFrame(approval_records)
    df_approval.to_csv(os.path.join(output_dir, "fact_approval.csv"), index=False)

    # ==========================================
    # 8. GENERATE FACT_DISBURSEMENT (100,000)
    # ==========================================
    print("Generating Disbursement Fact Table (100,000)...")
    disb_records = []
    disb_counter = 1

    df_approved_only = df_approval[df_approval['approval_status'] == 'Approved']
    
    # Cap funded disbursements to 100k
    df_approved_only = df_approved_only.head(102000)

    for row in df_approved_only.itertuples():
        loan_id = f"LN-{disb_counter:06d}"
        
        # Funded date (approx 3 days after approval date)
        funding_date_key = row.approval_date_key + 3
        
        # Limit payment date format errors
        first_pay_key = funding_date_key + 100 # Approx next month in YYYYMMDD key format

        disb_records.append({
            'disbursement_key': disb_counter,
            'loan_id': loan_id,
            'approval_key': row.approval_key,
            'customer_key': row.customer_key,
            'product_key': row.product_key,
            'disbursement_date_key': funding_date_key,
            'disbursed_amount': row.approved_amount,
            'first_payment_date_key': first_pay_key
        })
        disb_counter += 1

    df_disb = pd.DataFrame(disb_records)
    df_disb.to_csv(os.path.join(output_dir, "fact_disbursement.csv"), index=False)

    # ==========================================
    # 9. GENERATE FACT_REPAYMENT & COLLECTION
    # ==========================================
    print("Generating Amortization Repayments & Collections (1,000,000+)...")
    repay_records = []
    collection_records = []
    
    repay_counter = 1
    collection_counter = 1
    
    # Pre-load dates dictionary to resolve date formats
    dates_dict = df_date.set_index('date_key')['full_date'].to_dict()
    dates_list = sorted(list(dates_dict.keys()))

    # Process first 100,000 disbursed loans
    for loan in df_disb.itertuples():
        cust_key = loan.customer_key
        tier = df_customer.at[cust_key - 1, 'risk_tier']
        
        prod_key = loan.product_key
        interest_rate = df_product.at[prod_key - 1, 'interest_rate']
        tenure = df_product.at[prod_key - 1, 'tenure_months']
        
        p = loan.disbursed_amount
        r_monthly = (interest_rate / 100) / 12
        
        # Installment amount using standard Amortization calculation
        if r_monthly > 0:
            installment = p * (r_monthly * (1 + r_monthly)**tenure) / ((1 + r_monthly)**tenure - 1)
        else:
            installment = p / tenure
        
        installment = round(installment, 2)
        outstanding = p
        
        start_date_idx = dates_list.index(loan.disbursement_date_key) if loan.disbursement_date_key in dates_list else 0

        # Amortize over installments
        for inst_num in range(1, tenure + 1):
            # Calculate due date (approx 30 days per installment)
            due_idx = min(start_date_idx + (inst_num * 30), len(dates_list) - 1)
            due_date_key = dates_list[due_idx]
            
            # Determine payment states (delinquency probability correlates with risk tier)
            rand_val = random.random()
            
            if tier == 'Super Prime':
                is_on_time = rand_val < 0.995
                dpd = 0 if is_on_time else random.randint(1, 15)
            elif tier == 'Prime':
                is_on_time = rand_val < 0.97
                dpd = 0 if is_on_time else random.randint(1, 45)
            elif tier == 'Near Prime':
                is_on_time = rand_val < 0.88
                dpd = 0 if is_on_time else random.randint(1, 95)
            else: # Subprime
                is_on_time = rand_val < 0.70
                dpd = 0 if is_on_time else random.randint(1, 120)

            # Map delinquency buckets
            if dpd == 0:
                bucket = 'Current'
                pay_date_key = due_date_key
                default_f = False
            elif dpd <= 30:
                bucket = '1-30 DPD'
                pay_idx = min(due_idx + dpd, len(dates_list) - 1)
                pay_date_key = dates_list[pay_idx]
                default_f = False
            elif dpd <= 60:
                bucket = '31-60 DPD'
                pay_idx = min(due_idx + dpd, len(dates_list) - 1)
                pay_date_key = dates_list[pay_idx]
                default_f = False
            elif dpd <= 90:
                bucket = '61-90 DPD'
                pay_idx = min(due_idx + dpd, len(dates_list) - 1)
                pay_date_key = dates_list[pay_idx]
                default_f = False
            else:
                bucket = '90+ DPD'
                pay_date_key = np.nan # Unpaid / write-off state
                default_f = True

            # Standard interest vs principal calculations
            interest_portion = round(outstanding * r_monthly, 2)
            principal_portion = round(installment - interest_portion, 2)
            
            if default_f:
                amt_paid = 0.0
                principal_portion = 0.0
                interest_portion = 0.0
            else:
                amt_paid = installment

            outstanding = max(round(outstanding - principal_portion, 2), 0.0)

            repay_records.append({
                'repayment_key': repay_counter,
                'loan_key': loan.disbursement_key,
                'customer_key': cust_key,
                'due_date_key': due_date_key,
                'payment_date_key': pay_date_key if not pd.isna(pay_date_key) else None,
                'installment_number': inst_num,
                'installment_amount': installment,
                'principal_paid': principal_portion,
                'interest_paid': interest_portion,
                'amount_paid': amt_paid,
                'days_past_due': dpd,
                'delinquency_bucket': bucket,
                'default_flag': default_f,
                'outstanding_balance': outstanding
            })

            # Create collection record if past due by 30+ days
            if dpd > 30:
                assigned_date_key = due_date_key + 30
                action_date_key = assigned_date_key + random.randint(1, 10)
                
                status = 'Paid' if not default_f else random.choice(['Contacted', 'Promised to Pay', 'Unreachable'])
                strategy = 'SMS' if dpd <= 60 else ('Agent Call' if dpd <= 90 else 'Field Visit')
                rec_amount = round(installment * random.uniform(0.1, 0.8), 2) if status != 'Paid' else installment

                collection_records.append({
                    'collection_key': collection_counter,
                    'repayment_key': repay_counter,
                    'customer_key': cust_key,
                    'assigned_date_key': assigned_date_key,
                    'action_date_key': action_date_key,
                    'collection_status': status,
                    'collection_strategy': strategy,
                    'recovered_amount': rec_amount,
                    'agent_id': f"AGN-{random.randint(1, 20):03d}"
                })
                collection_counter += 1

            repay_counter += 1

    df_repay = pd.DataFrame(repay_records)
    df_repay.to_csv(os.path.join(output_dir, "fact_repayment.csv"), index=False)

    df_collection = pd.DataFrame(collection_records)
    df_collection.to_csv(os.path.join(output_dir, "fact_collection.csv"), index=False)

    print(f"Generation Complete! Outputs saved in: {output_dir}")
    print(f"Generated Rows: Customers: {len(df_customer)}, Applications: {len(df_app)}, Disbursements: {len(df_disb)}, Repayments: {len(df_repay)}, Collections: {len(df_collection)}")

if __name__ == "__main__":
    run_generator()
