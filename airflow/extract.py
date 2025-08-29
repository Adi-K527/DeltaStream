from kafka import KafkaProducer
import requests
import json
import os


IP = os.getenv("IP")
producer = KafkaProducer(bootstrap_servers=f'44.203.83.38:9092')


def extract_airplane_data():
    response = requests.get("https://opensky-network.org/api/states/all?lamin=32.6&lomin=-97.0&lamax=33.1&lomax=-96.4")
    data = response.json()
    
    for flight in data["states"]:
        producer.send('airplane-topic', json.dumps(flight).encode('utf-8'))
    producer.flush()


def extract_weather_data():
    response = requests.get("https://api.weather.gov/stations/KDFW/observations/latest")
    data = response.json()
    
    new_data = {
        "data": data["properties"]
    }

    producer.send('weather-topic', json.dumps(new_data).encode('utf-8'))
    producer.flush()