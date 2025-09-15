import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

# Load pre-trained model
model = joblib.load("models/xgb_demand_model.joblib")

app = FastAPI(title="Dynamic Pricing API")

# Input schema
class PredictionInput(BaseModel):
    avg_price: float
    daily_quantity: int
    event_date: str  # "YYYY-MM-DD"

@app.post("/predict_price")
def predict_price(data: PredictionInput):
    # Convert input to DataFrame
    df = pd.DataFrame([data.dict()])
    df['event_date'] = pd.to_datetime(df['event_date'])
    
    # Feature engineering (as used in training)
    df['day_of_week'] = df['event_date'].dt.dayofweek
    df['month'] = df['event_date'].dt.month
    df['quarter'] = df['event_date'].dt.quarter
    df['qty_lag_1'] = df['daily_quantity']      # تبسيط
    df['qty_7d_ma'] = df['daily_quantity']      # تبسيط
    df['qty_30d_ma'] = df['daily_quantity']     # تبسيط
    df['price_lag_1'] = df['avg_price']         # تبسيط

    features = [
        'qty_7d_ma', 'qty_30d_ma', 'qty_lag_1', 'price_lag_1',
        'day_of_week', 'month', 'quarter', 'avg_price'
    ]

    # Prediction
    predicted_quantity = model.predict(df[features])[0]
    recommended_price = df['avg_price'][0] * (1 + 0.05)  # مثال: زيادة 5%

    return {
        "predicted_quantity": float(predicted_quantity),
        "recommended_price": float(recommended_price)
    }

@app.get("/top_products")
def top_products(limit: int = 10):
    # تحميل ملف top products
    top_products_path = "data/recommendations/top_products.csv"
    df = pd.read_csv(top_products_path)
    return df.head(limit).to_dict(orient="records")
