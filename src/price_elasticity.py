# price_elasticity.py
import pandas as pd
import numpy as np

df = pd.read_csv("data/recommendations/daily_price_recommendation.csv", parse_dates=['event_date'])

try:
    mapping_df = pd.read_csv("data/product_mapping.csv")
    df = df.merge(mapping_df, on='stock_code', how='left')
except FileNotFoundError:
    df['product_name'] = df['stock_code'].astype(str)

elasticity_results = []

for product in df['product_name'].unique():
    product_df = df[df['product_name'] == product]
    product_df = product_df[product_df['predicted_quantity'] > 0]
    if len(product_df) < 2:
        continue
    X = np.log(product_df['recommended_price'])
    y = np.log(product_df['predicted_quantity'])
    coef = np.polyfit(X, y, 1)[0]  # slope = elasticity
    elasticity_results.append({'product_name': product, 'price_elasticity': coef})

elasticity_df = pd.DataFrame(elasticity_results)

if not elasticity_df.empty:
    print("Price Elasticity per Product:")
    print(elasticity_df.sort_values(by='price_elasticity'))
else:
    print("No products have enough data to calculate price elasticity.")
