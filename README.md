📊 Dynamic Pricing Strategy – End-to-End Data Science Project

🔹 Overview

This project implements a Dynamic Pricing System inspired by Uber’s surge pricing model.
The system predicts product demand using Machine Learning (XGBoost) and recommends optimal prices that maximize revenue while keeping customer demand in balance.

The project includes:
✅ Data preprocessing & feature engineering
✅ Demand prediction model (XGBoost)
✅ Dynamic pricing recommendations
✅ Interactive Dashboard (Dash) for visualization
✅ FastAPI endpoint for real-time predictions

⸻

🔹 Project Workflow
	1.	Data Collection & Cleaning
	•	Historical sales data (event_date, stock_code, product_name, daily_quantity, daily_revenue, avg_price)
	•	Handling missing values & outliers
	2.	Feature Engineering
	•	Lag features (qty_lag_1, price_lag_1)
	•	Rolling averages (qty_7d_ma, qty_30d_ma)
	•	Date features (day_of_week, month, quarter)
	3.	Model Training
	•	Model: XGBoost Regressor
	•	Metrics: RMSE, MAE, R²
	•	Achieved:
	•	✅ RMSE ≈ 0.33
	•	✅ MAE ≈ 0.13
	•	✅ R² ≈ 0.95
	4.	Dynamic Pricing Recommendation
	•	Predict demand for each product
	•	Suggest optimal price to balance quantity & revenue
	5.	Visualization (Dash Dashboard)
	•	Line Chart → Daily revenue per product
	•	Scatter Plot → Price vs Predicted demand
	•	Pie/Donut → Revenue share by product
	•	Bar Chart → Top products by revenue
	6.	FastAPI Deployment
	•	Endpoint: /predict_price → Returns predicted demand & recommended price

⸻

🔹 Project Structure
dynamic-pricing-strategy/
│
├── airflow/
│   └── dags/
│       └── dynamic_pricing_dag.py       # DAG لأتمتة ETL والنمذجة
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

🔹 How to Run

	1. Clone repo
		git clone https://github.com/Assyrian91/dynamic_pricing.git
		cd dynamic_pricing

	2. Create virtual environment & install dependencies
		python -m venv .venv
		source .venv/bin/activate   # (Linux/Mac)
		.venv\Scripts\activate      # (Windows)

		pip install -r requirements.txt

	3. Train the model
		python src/models/train_model.py

	4. Generate recommendations
		python src/dynamic_pricing_recommendation.py

	5. Run Dashboard
		python src/dashboard/dashboard_app.py
		Open http://127.0.0.1:8050 in browser.

	6. Run FastAPI
		uvicorn src.api.app:app --reload
		Docs: http://127.0.0.1:8000/docs

⸻

🔹 Example Screenshots

📌 Dashboard (Dash)
(Insert screenshots here after running your app)

📌 FastAPI Docs
(Insert screenshot of /docs endpoint)

⸻

🔹 Tech Stack
	•	Python (Pandas, NumPy, Scikit-learn, XGBoost)
	•	Dash (Plotly) → Interactive dashboard
	•	FastAPI → API deployment
	•	Joblib → Model persistence

⸻

🔹 Results & Insights
	•	Achieved high accuracy demand prediction (R² = 0.95)
	•	Built dynamic pricing engine that adapts prices in real-time
	•	Created a dashboard to track revenue, demand, and product performance
	•	Deployed an API for integration with external systems

⸻

🔹 Future Improvements
	•	Add real-time streaming data (Kafka / Spark Streaming)
	•	Integrate with SQL database for storage
	•	Deploy on cloud (AWS / Azure / GCP)
	•	Extend to multi-store, multi-region pricing

⸻

🔹 Author

👤 Khoshaba Odeesho
📍 Melbourne, Australia
🔗 GitHub | LinkedIn
