# 📊 Dynamic Pricing Strategy – End-to-End Data Science Project

## 🔹 Overview

This project implements a **Dynamic Pricing System** inspired by Uber’s surge pricing model.
The system predicts product demand using **Machine Learning (XGBoost)** and recommends optimal prices that maximize revenue while keeping customer demand in balance.

The project includes:

- ✅ Data preprocessing & feature engineering
- ✅ Demand prediction model (XGBoost)
- ✅ Dynamic pricing recommendations
- ✅ Interactive Dashboard (Dash) for visualization
- ✅ FastAPI endpoint for real-time predictions

---

## 🔹 Project Workflow

### 1. Data Collection & Cleaning
- Historical sales data:
  - `event_date`
  - `stock_code`
  - `product_name`
  - `daily_quantity`
  - `daily_revenue`
  - `avg_price`
- Handling missing values and outliers

### 2. Feature Engineering
- Lag features:
  - `qty_lag_1`
  - `price_lag_1`
- Rolling averages:
  - `qty_7d_ma`
  - `qty_30d_ma`
- Date features:
  - `day_of_week`
  - `month`
  - `quarter`

### 3. Model Training
**Model:** XGBoost Regressor

**Evaluation Metrics**
- RMSE ≈ 0.33
- MAE ≈ 0.13
- R² ≈ 0.95

### 4. Dynamic Pricing Recommendation
- Predict demand for each product
- Suggest optimal prices to balance quantity and revenue

### 5. Visualization (Dash Dashboard)
- 📈 Line Chart → Daily revenue per product
- 🎯 Scatter Plot → Price vs Predicted Demand
- 🍩 Pie/Donut Chart → Revenue share by product
- 📊 Bar Chart → Top products by revenue

### 6. FastAPI Deployment
**Endpoint:** `/predict_price`

Returns:
- Predicted demand
- Recommended price

---

## 🔹 Project Structure

```text
dynamic-pricing-strategy/
│
├── airflow/
│   └── dags/
│       └── dynamic_pricing_dag.py
│
├── data/
│   └── processed/
│       ├── cleaned_retail.csv
│       ├── daily_product_sales.csv
│       ├── final_features.csv
│
├── recommendations/
│   ├── bar_chart_data.csv
│   ├── dot_chart_data.csv
│   ├── line_chart_data.csv
│   ├── pie_chart_data.csv
│   ├── scatter_chart_data.csv
│   ├── top_products.csv
│   ├── product_mapping.csv
│   ├── test_data.csv
│   └── train_data.csv
│
├── models/
│   ├── xgb_demand_model.joblib
│   ├── price_optimizer.py
│   ├── train_model.py
│   ├── data_preprocessing.py
│   ├── dynamic_pricing_model.py
│   └── dynamic_pricing_recommendation.py
│
├── src/
│   ├── api/
│   │   └── app.py
│   ├── dashboard/
│   │   └── dashboard_app_v.py
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

## 🔹 How to Run

### 1. Clone Repository

```bash
git clone https://github.com/Assyrian91/dynamic_pricing.git
cd dynamic_pricing
```

### 2. Create Virtual Environment & Install Dependencies

**Linux / macOS**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Train the Model

```bash
python src/models/train_model.py
```

### 4. Generate Recommendations

```bash
python src/dynamic_pricing_recommendation.py
```

### 5. Run Dashboard

```bash
python src/dashboard/dashboard_app.py
```

Open:

`http://127.0.0.1:8050`

### 6. Run FastAPI

```bash
uvicorn src.api.app:app --reload
```

Swagger Docs:

`http://127.0.0.1:8000/docs`

---

## 🔹 Example Screenshots

### 📌 Dashboard (Dash)

> Insert dashboard screenshots here after running the application.

### 📌 FastAPI Documentation

> Insert screenshot of the `/docs` endpoint here.

---

## 🔹 Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Plotly Dash
- FastAPI
- Joblib
- PostgreSQL
- Apache Airflow

---

## 🔹 Results & Insights

- Achieved high-accuracy demand prediction (**R² = 0.95**)
- Built a dynamic pricing engine that adapts prices based on demand signals
- Created an interactive dashboard to monitor revenue, demand, and product performance
- Exposed model predictions through a FastAPI endpoint for integration with external systems

---

## 🔹 Future Improvements

- Add real-time streaming data using Kafka or Spark Streaming
- Integrate directly with SQL databases for production workloads
- Deploy to AWS, Azure, or Google Cloud Platform
- Extend to multi-store and multi-region pricing optimization
- Incorporate competitor pricing and external market signals

---

## 🔹 Author

**Khoshaba Odeesho**

📍 Melbourne, Australia

- GitHub: https://github.com/Assyrian91
- LinkedIn: Add your LinkedIn profile link here

---

⭐ If you found this project useful, consider giving the repository a star.
