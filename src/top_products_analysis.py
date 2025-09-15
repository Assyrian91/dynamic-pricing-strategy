import pandas as pd

# Load recommendations with predicted quantities
df = pd.read_csv("data/recommendations/daily_price_recommendation.csv", parse_dates=['order_date'])

# Load mapping to get product names
mapping_df = pd.read_csv("data/product_mapping.csv")

# Merge to add product_name
df = df.merge(mapping_df, on='product_id', how='left')

# Ensure product_name exists
if 'product_name' not in df.columns:
    df['product_name'] = df['product_id'].astype(str)

# Calculate total revenue per product
df['revenue'] = df['recommended_price'] * df['predicted_quantity']

# Top 5 products by revenue
top_products = df.groupby('product_name')['revenue'].sum().sort_values(ascending=False).head(5).reset_index()
top_products.rename(columns={'revenue': 'total_revenue'}, inplace=True)

print("Top 5 Products by Revenue:")
print(top_products)
