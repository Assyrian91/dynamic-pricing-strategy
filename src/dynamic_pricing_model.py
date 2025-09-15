import pandas as pd

train_df = pd.read_csv(r"data/train_data.csv")
test_df = pd.read_csv(r"data/test_data.csv")

features = ['qty_7d_ma', 'qty_30d_ma', 'qty_lag_1', 'price_lag_1', 'day_of_week', 'month', 'quarter', 'avg_price']
target = 'target'

X_train = train_df[features]
y_train = train_df[target]

X_test = test_df[features]
y_test = test_df[target]

print("Train Features head:\n", X_train.head())
print("Train Target head:\n", y_train.head())

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R2 Score: {r2:.2f}")

os.makedirs('models', exist_ok=True)
joblib.dump(model, r"models/dynamic_pricing_model.pkl")
print("Model saved successfully!")
