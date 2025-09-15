import pandas as pd
import os

def preprocess_data():
    input_path = "data/online_retail.csv"
    output_cleaned = "data/processed/cleaned_retail.csv"
    output_daily = "data/processed/daily_product_sales.csv"

    print("Loading dataset...")
    df = pd.read_csv(input_path, parse_dates=['order_date'])

    print("Cleaning dataset...")
    df.drop_duplicates(inplace=True)
    df.dropna(subset=['customer_id', 'product_id', 'quantity', 'price'], inplace=True)
    df = df[(df['quantity'] > 0) & (df['price'] > 0)]

    print("Adding time features...")
    df['day_of_week'] = df['order_date'].dt.dayofweek
    df['month'] = df['order_date'].dt.month
    df['quarter'] = df['order_date'].dt.quarter
    df['total_price'] = df['quantity'] * df['price']

    # Save cleaned retail
    os.makedirs(os.path.dirname(output_cleaned), exist_ok=True)
    df.to_csv(output_cleaned, index=False)
    print(f"✅ Cleaned dataset saved to {output_cleaned}")

    print("Aggregating daily sales...")
    daily_sales = df.groupby(['order_date', 'product_id', 'product_name']) \
                    .agg(daily_quantity=('quantity', 'sum'),
                         daily_revenue=('total_price', 'sum'),
                         avg_price=('price', 'mean')) \
                    .reset_index()

    # Rename order_date to event_date for consistency with dashboard
    daily_sales.rename(columns={'order_date': 'event_date', 'product_id': 'stock_code'}, inplace=True)

    os.makedirs(os.path.dirname(output_daily), exist_ok=True)
    daily_sales.to_csv(output_daily, index=False)
    print(f"✅ Daily product sales saved to {output_daily}")

if __name__ == "__main__":
    preprocess_data()
