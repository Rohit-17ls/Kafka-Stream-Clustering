import time
import random
import numpy as np
import pandas as pd
import json
from kafka import KafkaProducer
from faker import Faker
    
def clamp(val, min_val, max_val):
    return min(max(min_val, val), max_val)

def generate_data(fake, mock_df):
    global ind

    data = {
        'instance_id': fake.uuid4(),
        'cpu_usage_percent': clamp(mock_df.iloc[ind]['CPU Utilization'] + random.uniform(-5, 5), 0, 100),
        'memory_usage_percent': clamp(mock_df.iloc[ind]['Memory Usage'] + random.uniform(-5, 5), 0, 100),
        'disk_usage_percent': clamp(mock_df.iloc[ind]['Disk IO'] + random.uniform(-5, 5), 0, 100),
        'network_latency' : clamp(mock_df.iloc[ind]['Network Latency'] + random.uniform(-3, 3), 0, 80)
    }
    
    ind = (ind + 1) % len(mock_df)

    return data



DATA_PATH = "./mock_data.csv"
mock_df = pd.read_csv(DATA_PATH)
mock_df = mock_df.drop("Load", axis = 1)
ind = 0

fake = Faker()
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'mock_stream'



while True:

    data = generate_data(fake, mock_df)
    producer.send(topic, value=json.dumps(data).encode('utf-8'))
    time.sleep(random.random() * 0.1)
    