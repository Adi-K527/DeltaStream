from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
import requests


def extract_airplane_data():
    response = requests.get("https://opensky-network.org/api/states/all?lamin=32.55&lomin=96.50&lamax=33.05&lomax=97.20")
    data = response.json()
    return data


def extract_weather_data():
    response = requests.get("https://api.weather.gov/stations/KDFW/observations/latest")
    data = response.json()
    return data