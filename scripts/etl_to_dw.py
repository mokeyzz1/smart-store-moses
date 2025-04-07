import pandas as pd
import sqlite3
import pathlib
import sys

# Add project root to system path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Paths
DW_DIR = pathlib.Path("data") / "dw"
DW_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DW_DIR / "smart_sales.db"
PREPARED_DATA_DIR = pathlib.Path("data") / "prepared"

# --- SCHEMA SETUP --- #
def create_schema(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            join_date TEXT,
            loyalty_points INTEGER,
            customer_segment TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
            sale_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            sale_amount REAL,
            sale_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
            FOREIGN KEY (product_id) REFERENCES product (product_id)
        )
    """)

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sale")

# --- INSERT FUNCTIONS --- #
def insert_customers(df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    print("📥 Inserting customers...")
    df = df.rename(columns={
        "CustomerID": "customer_id",
        "Name": "name",
        "Region": "region",
        "JoinDate": "join_date",
        "LoyaltyPoints": "loyalty_points",
        "CustomerSegment": "customer_segment"
    })
    df = df[["customer_id", "name", "region", "join_date", "loyalty_points", "customer_segment"]]
    df.to_sql("customer", cursor.connection, if_exists="append", index=False)
    print("✅ Customers inserted.")

def insert_products(df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    print("📥 Inserting products...")
    df = df.rename(columns={
        "productid": "product_id",
        "productname": "product_name",
        "category": "category"
    })
    df = df[["product_id", "product_name", "category"]]
    df.to_sql("product", cursor.connection, if_exists="append", index=False)
    print("✅ Products inserted.")

def insert_sales(df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    print("📥 Inserting sales...")
    df = df.rename(columns={
        "transactionid": "sale_id",
        "customerid": "customer_id",
        "productid": "product_id",
        "saleamount": "sale_amount",
        "saledate": "sale_date"
    })
    df = df[["sale_id", "customer_id", "product_id", "sale_amount", "sale_date"]]
    df.to_sql("sale", cursor.connection, if_exists="append", index=False)
    print("✅ Sales inserted.")

# --- MAIN FUNCTION --- #
def load_data_to_db() -> None:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("🔧 Creating schema...")
        create_schema(cursor)

        print("🧹 Deleting existing records...")
        delete_existing_records(cursor)

        # Load prepared data
        customers_df = pd.read_csv(PREPARED_DATA_DIR / "customers_data_prepared.csv")
        products_df = pd.read_csv(PREPARED_DATA_DIR / "products_data_prepared.csv")
        sales_df = pd.read_csv(PREPARED_DATA_DIR / "sales_data_prepared.csv")

        # Insert into DW
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
        print("🎉 Data warehouse load successful.")

    except Exception as e:
        print(f"❌ ETL Error: {e}")

    finally:
        if conn:
            conn.close()

# --- RUN SCRIPT --- #
if __name__ == "__main__":
    load_data_to_db()
