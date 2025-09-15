# src/airflow/dags/dynamic_pricing_dag.py
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import timedelta
import subprocess

default_args = {"retries":1, "retry_delay": timedelta(minutes=5)}

@dag(dag_id="dynamic_pricing_pipeline", schedule_interval="@daily", start_date=days_ago(1), default_args=default_args, catchup=False)
def pipeline():
    @task()
    def etl_load():
        subprocess.run(["python","/opt/airflow/dags/scripts/load_online_retail_to_postgres.py"], check=True)
    @task()
    def refresh_mv():
        # run psql command to REFRESH MATERIALIZED VIEW
        subprocess.run(["psql","-U","postgres","-d","dynamic_pricing","-c","REFRESH MATERIALIZED VIEW CONCURRENTLY mv_agg_sales_daily;"], check=True)
    @task()
    def train_model():
        subprocess.run(["python","/opt/airflow/dags/scripts/train_model.py"], check=True)

    etl = etl_load()
    mv = refresh_mv()
    tr = train_model()
    etl >> mv >> tr

dag = pipeline()
