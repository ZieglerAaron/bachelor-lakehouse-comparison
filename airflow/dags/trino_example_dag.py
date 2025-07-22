from airflow import DAG
from airflow.providers.trino.operators.trino import TrinoOperator
from airflow.operators.bash import BashOperator
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

run_trino_query = BashOperator(
    task_id='run_trino_query',
    bash_command='curl -s -H "X-Trino-User: admin" http://controller:8080/v1/statement -X POST -H "Content-Type: application/json" -d \'{"query": "SHOW CATALOGS"}\'',
    dag=dag,
)

# Task zum Anlegen der Iceberg-Tabelle via CTAS
create_iceberg_table = BashOperator(
    task_id='create_iceberg_table',
    bash_command='''curl -s -H "X-Trino-User: admin" http://controller:8080/v1/statement -X POST -H "Content-Type: application/json" -d '{
      "query": "CREATE TABLE IF NOT EXISTS iceberg.default.testdaten WITH (format = \\"PARQUET\\", location = \\"s3a://wba/parquet/testdaten_table/\\") AS SELECT * FROM hive.default.\\"s3a://wba/parquet/Testdaten.parquet\\""
    }' ''',
    dag=dag,
)

# Task zum Preview der neu angelegten Tabelle
preview_iceberg_table = BashOperator(
    task_id='preview_iceberg_table',
    bash_command='curl -s -H "X-Trino-User: admin" http://controller:8080/v1/statement -X POST -H "Content-Type: application/json" -d \'{"query": "SELECT * FROM iceberg.default.testdaten LIMIT 10"}\'',
    dag=dag,
) 

# Abhängigkeiten
run_trino_query >> create_iceberg_table >> preview_iceberg_table 