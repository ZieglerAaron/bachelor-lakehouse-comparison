from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'spark_example_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

run_spark_job = SparkSubmitOperator(
    task_id='run_spark_job',
    application='/opt/spark-apps/csv_to_delta.py',
    conn_id='spark_delta',
    dag=dag,
) 