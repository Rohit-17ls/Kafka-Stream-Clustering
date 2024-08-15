import time
import random
import numpy as np
import json
from kafka import KafkaProducer
from faker import Faker

def get_frac():
    return np.random.choice(np.arange(4, 10)/10, 1, p = [0.1, 0.1, 0.1, 0.3, 0.2, 0.2])[0]

def clamp(val, min_val, max_val):
    return min(max(min_val, val), max_val)

def generate_data(fake):
    instance_id = fake.uuid4()
    
    # Generate CPU usage as a base metric
    cpu_usage_percent = (np.random.choice(np.arange(0, 10)/10, 1, p = [0, 0.15, 0.2, 0, 0.1, 0.2, 0, 0.2, 0.15, 0])[0] + random.random() * 0.15) * 100
    
    # Add more randomness to disk usage while keeping a loose positive correlation with CPU usage
    disk_usage_percent = clamp(cpu_usage_percent * get_frac() + random.uniform(0, 30), 0, 100)
    
    # Add randomness to memory usage but maintain a positive correlation with CPU usage
    memory_usage_mb = cpu_usage_percent * get_frac() * random.uniform(1800, 2200)
    
    # Disk IOPS loosely based on disk usage, but with additional randomness
    disk_iops = disk_usage_percent * random.uniform(160, 200) + random.uniform(0, 50)

    data = {
        'instance_id': instance_id,
        'cpu_usage_percent': round(cpu_usage_percent, 2),
        'disk_usage_percent': round(disk_usage_percent, 2),
        'memory_usage_mb': round(memory_usage_mb, 2),
        'disk_iops': round(disk_iops, 2)
    }

    return data


fake = Faker()
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'mock_stream'

while True:

    data = generate_data(fake)
    producer.send(topic, value=json.dumps(data).encode('utf-8'))
    time.sleep(random.random() * 0.1)
    