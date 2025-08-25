from kafka.admin import KafkaAdminClient, NewTopic
from dotenv import load_dotenv
import os

load_dotenv()

IP = os.getenv("IP")

admin_client = KafkaAdminClient(
    bootstrap_servers=f"{IP}:9092", 
    client_id='test'
)

weather_topic = NewTopic(name="weather-topic", 
                      num_partitions=2, 
                      replication_factor=2)

airplane_topic  = NewTopic(name="airplane-topic", 
                      num_partitions=2, 
                      replication_factor=2)

admin_client.create_topics(new_topics=[weather_topic, airplane_topic], validate_only=False)