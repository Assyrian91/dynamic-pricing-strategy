import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/dynamic_pricing"
INPUT_PATH = r"data\Online_Retail.xlsx"

df = pd.read_excel(INPUT_PATH, engine='openpyxl')

# Cleaning
df = df.dropna(subset=["InvoiceNo", "StockCode", "InvoiceDate"])
df = df[df["Quantity"].notnull() & df["UnitPrice"].notnull()]
df = df[df["Quantity"] != 0]
df["Quantity"] = df["Quantity"].astype(int)
df["UnitPrice"] = df["UnitPrice"].astype(float)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df = df.rename(columns={
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Country": "country"
})

# Calculated columns
df["revenue"] = df["quantity"] * df["unit_price"]
df["event_date"] = df["invoice_date"].dt.date

# Load to Postgres
engine = create_engine(DB_URL)

with engine.begin() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS transactions (
        id BIGSERIAL PRIMARY KEY,
        invoice_no TEXT,
        stock_code TEXT,
        description TEXT,
        quantity INTEGER,
        invoice_date TIMESTAMPTZ,
        unit_price NUMERIC(12,2),
        customer_id TEXT,
        country TEXT,
        revenue NUMERIC(14,2),
        event_date DATE,
        created_at TIMESTAMPTZ DEFAULT now()
    );
    """))

df.to_sql("transactions", engine, if_exists="append", index=False, method='multi', chunksize=10000)
print(f"Loaded {len(df)} rows into transactions")
