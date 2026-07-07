---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Assyrian91/dynamic-pricing-strategy.git
cd dynamic-pricing-strategy
```

### 2. Create virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Train the model

```bash
python models/train_model.py
```

### 4. Generate pricing recommendations

```bash
python models/dynamic_pricing_recommendation.py
```

### 5. Run the Dash dashboard

```bash
python src/dashboard/dashboard_app_v.py
```

Open: `http://127.0.0.1:8050`

### 6. Run the FastAPI endpoint

```bash
uvicorn src.api.app:app --reload
```

Swagger docs: `http://127.0.0.1:8000/docs`

**Example API call:**

```bash
curl -X POST "http://127.0.0.1:8000/predict_price" \
  -H "Content-Type: application/json" \
  -d '{"stock_code": "85123A", "qty_lag_1": 6, "price_lag_1": 2.55, "day_of_week": 1, "month": 12}'
```

**Response:**
```json
{
  "predicted_demand": 8.3,
  "recommended_price": 2.89
}
```

### 7. Run Airflow DAG

```bash
airflow standalone
```

Then navigate to `http://localhost:8080` and trigger `dynamic_pricing_dag`.

---

## 📊 Dashboard Visualisations

| Chart | What It Shows |
|---|---|
| Line Chart | Daily revenue per product over time |
| Scatter Plot | Price vs Predicted Demand — elasticity curve |
| Donut Chart | Revenue share by product category |
| Bar Chart | Top products by total revenue |

---

## 💡 Key Insights

- **R² of 0.95** confirms XGBoost captures 95% of demand variance from price and time signals
- **Lag features** (previous day quantity and price) are the strongest demand predictors
- **Rolling 7-day average** smooths noise and improves forecast stability
- Products show **clear price elasticity** — small price increases cause measurable demand drops above threshold
- **Seasonal patterns** in month and day-of-week features confirm weekend and holiday demand spikes

---

## 🔮 Future Improvements

- Real-time streaming via Kafka or Spark Streaming
- Multi-store and multi-region pricing optimisation
- Competitor pricing integration via web scraping
- Deploy to AWS / Azure with Docker containerisation
- A/B testing framework for pricing experiments

---

## 👤 Author

**Khoshaba Odeesho**  
Data Scientist & AI Automation Engineer  
📍 Melbourne, Australia

[GitHub](https://github.com/Assyrian91) · [LinkedIn](https://www.linkedin.com/in/khoshaba-odeesho-17b5b92aa/)

---

*Part of a professional data science portfolio demonstrating end-to-end ML engineering — from raw data to deployed API.*
