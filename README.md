## Stream Clustering

### 0. Installing Kafka
Follow the steps in this video : https://www.youtube.com/watch?v=LX5LKBYHmyU
(Note : Kafka requires that you have Java installed)

### 1. Start zookeeper and kafka servers
Navigate to kafka installation's directory and run the following two commands (on separate terminals):

#### Linux:
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

#### Windows:
```bash
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

### 2. Create a kafka topic that producers can publish to
Navigate to kafka installation's directory and run the following command:

**Note :** If a kafka stream with the name `mock_stream` already exists skip this step

#### Linux:
```bash
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic mock_stream 
```

#### Windows:
```bash
.\bin\windows\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic mock_stream
```

### 3. Create producer script `data_stream.py`
```python
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
```

### 4. Run the producer script `data_stream.py`
```bash
python data_stream.py
```

### 5. Run the cells in `Stream-Clustering.ipynb` to consume from the topic and perform clustering on the stream data periodically

