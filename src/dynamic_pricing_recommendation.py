# dynamic_pricing_dashboard.py
import pandas as pd
import joblib
import os

# Paths
CSV_PATH = "data/processed/daily_product_sales.csv"
MODEL_PATH = "models/xgb_demand_model.joblib"
RECOMMENDATION_PATH = "data/recommendations/daily_price_recommendation.csv"
TOP_PRODUCTS_PATH = "data/recommendations/top_products.csv"

# Load dataset
df = pd.read_csv(CSV_PATH, parse_dates=['event_date'])
print("✅ Dataset loaded. Columns:", df.columns.tolist())

# Load trained model
model = joblib.load(MODEL_PATH)

# --- Feature Engineering ---
df['day_of_week'] = df['event_date'].dt.dayofweek
df['month'] = df['event_date'].dt.month
df['quarter'] = df['event_date'].dt.quarter

df = df.sort_values(['stock_code', 'event_date'])
df['qty_7d_ma'] = df.groupby('stock_code')['daily_quantity'].transform(lambda x: x.rolling(7, min_periods=1).mean())
df['qty_30d_ma'] = df.groupby('stock_code')['daily_quantity'].transform(lambda x: x.rolling(30, min_periods=1).mean())
df['qty_lag_1'] = df.groupby('stock_code')['daily_quantity'].shift(1).fillna(0)
df['price_lag_1'] = df.groupby('stock_code')['avg_price'].shift(1).fillna(df['avg_price'].mean())

features = ['qty_7d_ma', 'qty_30d_ma', 'qty_lag_1', 'price_lag_1', 'day_of_week', 'month', 'quarter', 'avg_price']
X = df[features]

# --- Predict Quantity ---
df['predicted_quantity'] = model.predict(X)

# --- Price Recommendation Logic ---
price_adjustments = [0.9, 1.0, 1.1]  # -10%, 0%, +10%
best_prices = []
for _, row in df.iterrows():
    best_rev = 0
    best_price = row['avg_price']
    for adj in price_adjustments:
        temp_price = row['avg_price'] * adj
        temp_revenue = temp_price * row['predicted_quantity']
        if temp_revenue > best_rev:
            best_rev = temp_revenue
            best_price = temp_price
    best_prices.append(best_price)
df['recommended_price'] = best_prices

# Save recommendations
os.makedirs(os.path.dirname(RECOMMENDATION_PATH), exist_ok=True)
df.to_csv(RECOMMENDATION_PATH, index=False)
print("✅ Dynamic pricing recommendations saved successfully!")

# --- Top Products Analysis ---
df['revenue'] = df['recommended_price'] * df['predicted_quantity']
top_products = df.groupby('product_name')['revenue'].sum().sort_values(ascending=False).head(10).reset_index()
top_products.rename(columns={'revenue': 'total_revenue'}, inplace=True)

os.makedirs(os.path.dirname(TOP_PRODUCTS_PATH), exist_ok=True)
top_products.to_csv(TOP_PRODUCTS_PATH, index=False)
print("✅ Top products by revenue saved successfully!")
print(top_products)

# --- Data ready for Dashboard Charts ---
# Line chart (daily revenue per product)
line_chart_data = df.groupby(['event_date', 'product_name'])['revenue'].sum().reset_index()
line_chart_data.to_csv("data/recommendations/line_chart_data.csv", index=False)

# Dot chart (predicted quantity)
dot_chart_data = df[['event_date', 'product_name', 'predicted_quantity']]
dot_chart_data.to_csv("data/recommendations/dot_chart_data.csv", index=False)

# Pie/Donut chart (total revenue share)
pie_chart_data = top_products.copy()
pie_chart_data.to_csv("data/recommendations/pie_chart_data.csv", index=False)

# Bar chart (top products)
bar_chart_data = top_products.copy()
bar_chart_data.to_csv("data/recommendations/bar_chart_data.csv", index=False)

# Scatter chart (price vs predicted quantity)
scatter_chart_data = df[['avg_price', 'predicted_quantity', 'product_name']]
scatter_chart_data.to_csv("data/recommendations/scatter_chart_data.csv", index=False)

print("✅ All chart data prepared for dashboard!")
