from airflow import DAG
from airflow.providers.trino.operators.trino import TrinoOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'trino_example_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

run_trino_query = TrinoOperator(
    task_id='run_trino_query',
    trino_conn_id='trino_iceberg',
    sql="SELECT * FROM example.iceberg.sample_table LIMIT 10",
    dag=dag,
) 