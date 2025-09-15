import pandas as pd
from sklearn.model_selection import train_test_split

# ===== Load cleaned daily data =====
csv_path = r"data/processed/cleaned_retail.csv"
df = pd.read_csv(csv_path, parse_dates=['order_date'])

# ===== Basic info =====
print(df.head())
print(df.info())

# ===== Time features =====
df['day_of_week'] = df['order_date'].dt.dayofweek  # 0 = Monday
df['month'] = df['order_date'].dt.month
df['quarter'] = df['order_date'].dt.quarter

# ===== Sort & rolling features =====
df = df.sort_values(['product_id', 'order_date'])

df['qty_7d_ma'] = df.groupby('product_id')['quantity'].transform(lambda x: x.rolling(7, min_periods=1).mean())
df['qty_30d_ma'] = df.groupby('product_id')['quantity'].transform(lambda x: x.rolling(30, min_periods=1).mean())

df['qty_lag_1'] = df.groupby('product_id')['quantity'].shift(1).fillna(0)

# ===== Price lag and avg price =====
df['avg_price'] = df.groupby('product_id')['price'].transform('mean')
df['price_lag_1'] = df.groupby('product_id')['price'].shift(1).fillna(df['avg_price'])

# ===== Features & Target =====
features = ['qty_7d_ma', 'qty_30d_ma', 'qty_lag_1', 'price_lag_1', 'day_of_week', 'month', 'quarter', 'avg_price']
target = 'quantity'

X = df[features]
y = df[target]

# ===== Train/Test Split =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# ===== Save CSVs =====
X_train.assign(target=y_train).to_csv(r"data/train_data.csv", index=False)
X_test.assign(target=y_test).to_csv(r"data/test_data.csv", index=False)

print("✅ Train/Test CSV saved successfully!")
print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)
