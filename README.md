# 📊 Dynamic Pricing Strategy — End-to-End Data Science Project

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-R²_0.95-EB5B25?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)

> **XGBoost demand prediction + dynamic pricing engine + FastAPI deployment + Airflow orchestration**  
> Built by **Khoshaba Odeesho** | [Assyrian AI](https://github.com/Assyrian91)

---

## 🎯 What This Project Does

Most pricing systems are static — set a price and leave it. This project builds a **dynamic pricing engine** that continuously predicts product demand using machine learning and automatically adjusts recommended prices to maximise revenue while maintaining demand balance.

Inspired by Uber's surge pricing model, applied to real e-commerce retail data.

---

## 📈 Key Results

| Metric | Value |
|---|---|
| **Model** | XGBoost Regressor |
| **R²** | **0.95** |
| **RMSE** | 0.33 |
| **MAE** | 0.13 |
| **Deployment** | FastAPI REST endpoint |
| **Orchestration** | Apache Airflow DAG |

---

## 🏗️ Architecture

```
Raw Retail Data (PostgreSQL)
        │
        ▼
ETL Pipeline (load_online_retail_to_postgres.py)
        │
        ▼
Data Preprocessing + Feature Engineering
  Lag features: qty_lag_1, price_lag_1
  Rolling averages: qty_7d_ma, qty_30d_ma
  Date features: day_of_week, month, quarter
        │
        ▼
XGBoost Demand Prediction Model (R² = 0.95)
        │
        ▼
Dynamic Pricing Engine
  Predict demand per product
  Optimise price to maximise revenue
        │
   ┌────┴────┐
   ▼         ▼
 Dash      FastAPI
Dashboard  /predict_price endpoint
(live viz) (real-time predictions)
        │
        ▼
Apache Airflow DAG
(scheduled pipeline orchestration)
```

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| ML Model | XGBoost |
| Feature Engineering | Python · Pandas · NumPy · Scikit-learn |
| Dashboard | Plotly Dash |
| API Deployment | FastAPI · Uvicorn |
| Orchestration | Apache Airflow |
| Database | PostgreSQL |
| Model Serialisation | Joblib |

---

## 📁 Project Structure

```
dynamic-pricing-strategy/
│
├── airflow/
│   └── dags/
│       └── dynamic_pricing_dag.py      ← Airflow orchestration
│
├── data/
│   └── processed/
│       ├── cleaned_retail.csv
│       ├── daily_product_sales.csv
│       └── final_features.csv
│
├── models/
│   ├── xgb_demand_model.joblib         ← Trained model
│   ├── train_model.py                  ← Model training script
│   ├── data_preprocessing.py
│   ├── dynamic_pricing_model.py
│   ├── dynamic_pricing_recommendation.py
│   └── price_optimizer.py
│
├── src/
│   ├── api/
│   │   └── app.py                      ← FastAPI endpoint
│   ├── dashboard/
│   │   └── dashboard_app_v.py          ← Dash dashboard
│   ├── etl/
│   │   └── load_online_retail_to_postgres.py
│   ├── feature_engineering.py
│   ├── price_elasticity.py
│   └── top_product_analysis.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

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
