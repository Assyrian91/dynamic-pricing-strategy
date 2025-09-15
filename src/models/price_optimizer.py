# src/models/price_optimizer.py
import numpy as np
import pandas as pd
from joblib import load

MODEL_PATH = "models/xgb_demand_model.joblib"
DATA_PATH = "data/processed/daily_product_sales.csv"

# Load trained model
model = load(MODEL_PATH)

# Load preprocessed sales data
df = pd.read_csv(DATA_PATH, parse_dates=['order_date'])

# Get first available product_id as default
default_product_id = df['product_id'].iloc[0]

def find_optimal_price(product_id: int = None, price_min: float = 1.0, price_max: float = 50.0, steps: int = 200):
    global df, model
    
    # If no product_id specified, use default
    if product_id is None:
        product_id = default_product_id
    
    # Filter product
    product_data = df[df['product_id'] == product_id]
    if product_data.empty:
        raise ValueError(f"Product ID {product_id} not found in dataset")
    
    # Take average features
    avg_price = product_data['avg_price'].mean()
    day_of_week = int(product_data['order_date'].dt.dayofweek.mode()[0])
    is_weekend = int(day_of_week in [5,6])
    month = int(product_data['order_date'].dt.month.mode()[0])
    quarter = int(product_data['order_date'].dt.quarter.mode()[0])
    
    # Create dataframe for predictions
    prices = np.linspace(price_min, price_max, steps)
    base_features = pd.DataFrame({
        'avg_price': [avg_price] * steps,
        'price_lag_1': [avg_price] * steps,
        'day_of_week': [day_of_week] * steps,
        'is_weekend': [is_weekend] * steps,
        'month': [month] * steps,
        'quarter': [quarter] * steps
    })
    
    preds = model.predict(base_features)
    revenue = preds * prices
    best_idx = int(np.nanargmax(revenue))
    
    return {
        'product_id': product_id,
        'best_price': float(prices[best_idx]),
        'expected_qty': float(preds[best_idx]),
        'expected_revenue': float(revenue[best_idx])
    }

if __name__ == "__main__":
    result = find_optimal_price()
    print(result)
