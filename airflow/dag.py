from airflow import DAG
from airflow import PythonOperator
from airflow.utils.task_group import TaskGroup
import requests
from extract import extract_airplane_data, extract_weather_data
from transform import transform_data_bronze, transform_data_silver, transform_data_gold
from load import load_data_to_postgres


with DAG(dag_id='etl_dag', schedule_interval='@daily') as dag:

    with TaskGroup("extract") as extract_group:
        extract_airplane_data_task = PythonOperator(
            task_id='extract_airplane_data',
            python_callable=extract_airplane_data
        )

        extract_weather_data_task = PythonOperator(
            task_id='extract_weather_data',
            python_callable=extract_weather_data
        )


    with TaskGroup("transform") as transform_group:
        transform_data_bronze_task = PythonOperator(
            task_id='transform_data_bronze',
            python_callable=transform_data_bronze
        )

        transform_data_silver_task = PythonOperator(
            task_id='transform_data_silver',
            python_callable=transform_data_silver
        )

        transform_data_gold_task = PythonOperator(
            task_id='transform_data_gold',
            python_callable=transform_data_gold
        )

        transform_data_bronze_task >> transform_data_silver_task >> transform_data_gold_task


    with TaskGroup("load") as load_group:
        load_data_to_postgres_task = PythonOperator(
            task_id='load_data_to_postgres',
            python_callable=load_data_to_postgres
        )


    extract_group >> transform_group >> load_group