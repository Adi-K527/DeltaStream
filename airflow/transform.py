from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
import requests


def transform_data_bronze():
    pass


def transform_data_silver():
    pass


def transform_data_gold():
    pass