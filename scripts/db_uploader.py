import os
import psycopg2

# Database Connection Settings (Configure as needed)
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "postgres_password"  # Update with your password
DB_NAME = "postgres"                # Update with target database name

def upload_data():
    csv_dir = os.path.join("data_warehouse", "raw_csvs")
    
    # Tables in order of foreign key dependency
    tables_to_upload = [
        ("dim_customer", "dim_customer.csv"),
        ("dim_date", "dim_date.csv"),
        ("dim_loan_product", "dim_loan_product.csv"),
        ("dim_location", "dim_location.csv"),
        ("dim_channel", "dim_channel.csv"),
        ("fact_application", "fact_application.csv"),
        ("fact_approval", "fact_approval.csv"),
        ("fact_disbursement", "fact_disbursement.csv"),
        ("fact_repayment", "fact_repayment.csv"),
        ("fact_collection", "fact_collection.csv")
    ]

    print(f"Connecting to database {DB_NAME} on {DB_HOST}:{DB_PORT}...")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        print("Connection successful! Beginning data upload...")

        for table_name, csv_filename in tables_to_upload:
            csv_path = os.path.join(csv_dir, csv_filename)
            if not os.path.exists(csv_path):
                print(f"CSV file not found: {csv_path}. Skipping table {table_name}.")
                continue

            print(f"Uploading {csv_filename} to table {table_name}...")
            
            # Truncate table first to prevent duplicate key errors
            cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE;")
            
            # Fast COPY command in PostgreSQL
            with open(csv_path, 'r', encoding='utf-8') as f:
                # Read header to construct clean copy expert sql
                header = f.readline().strip()
                copy_sql = f"COPY {table_name} ({header}) FROM STDIN WITH CSV HEADER;"
                f.seek(0)
                cursor.copy_expert(copy_sql, f)
            
            conn.commit()
            print(f"Table {table_name} uploaded successfully.")

        cursor.close()
        conn.close()
        print("Database upload completed successfully!")
    except Exception as e:
        print(f"An error occurred during database upload: {e}")

if __name__ == "__main__":
    upload_data()
