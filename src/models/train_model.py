import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import os
import numpy as np

DATA_PATH = "data/processed/daily_product_sales.csv"  
MODEL_PATH = "models/xgb_demand_model.joblib"

def main():
    # Load dataset
    df = pd.read_csv(DATA_PATH, parse_dates=['event_date'])  
    print("Columns available:", df.columns.tolist())

    # Features
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
    y = df['daily_quantity']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # هنا أخذنا الجذر التربيعي للـ MSE
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"✅ Validation RMSE: {rmse:.2f}")
    print(f"✅ Validation MAE: {mae:.2f}")
    print(f"✅ Validation R²: {r2:.3f}")

    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    main()
