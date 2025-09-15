import pandas as pd
import os

# Load recommendations data
df = pd.read_csv("data/recommendations/daily_price_recommendation.csv")

# Extract unique product IDs
unique_ids = df['product_id'].unique()

# Generate readable product names
product_names = [f"Product {i+1}" for i in range(len(unique_ids))]

# Create mapping DataFrame
mapping_df = pd.DataFrame({
    'product_id': unique_ids,
    'product_name': product_names
})

# Ensure folder exists
os.makedirs('data', exist_ok=True)

# Save to CSV
mapping_df.to_csv("data/product_mapping.csv", index=False)
print("product_mapping.csv generated successfully!")
