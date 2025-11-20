# Kafka Python Exercises

This repository contains practical exercises for learning Kafka with Python using confluent-kafka library.
It includes producer and consumer examples for topics with structured data.

## 📁 Repository Structure

kafka_play/

├── config.py                # Helper: Kafka cluster configuration

├── admin.py                # Main: Topic creation helper and example

├── producer.py             # Main: Produces Turkey's regions to 'regions' topic

├── consumer.py             # Main: Consumes messages from 'regions' topic

├── consumer_topic1.py      # Main: Consumes messages from 'topic1' (iris.csv) and writes to files

├── README.md               # This file

├── .gitignore

└── LICENSE

## 🛠️ Technologies Used

- Docker & Docker Compose
- Python 3.x
- Confluent Kafka Python library:
   ```
   docker exec -it kafka1 python3 -m pip install pip --upgrade
   docker exec -it kafka1 python3 -m pip install confluent-kafka

   ```
- Sample CSV for exercise 2: https://github.com/erkansirin78/data-generator/blob/master/input/iris.csv

## 📝 Exercises

### 1. Produce and Consume Turkey's Geographical Regions

#### Goal: 
Produce a topic regions with keys and names of Turkey's geographical regions, then consume and display messages with partition and timestamp.

#### Files:
- config.py – Helper, defines Kafka bootstrap server and client ID.
- admin.py – Main helper for topic creation (regions).
- producer.py – Main, produces region names with keys.
- consumer.py – Main, consumes messages and prints: Key, Value, Partition, Timestamp.

#### Steps:

I) Create Kafka topic regions if it doesn't exist:
   ```
   docker exec -it kafka1 python3 admin.py
   
   ```

II) Verify topic creation:
   ```
   docker exec -it kafka1 kafka/bin/kafka-topics.sh --bootstrap-server kafka1:9092 --list
   
   ```

III) Produce regions to topic:
   ```
   docker exec -it kafka1 python3 producer.py
   ```

IV) Run consumer in separate terminals:
   ```
   docker exec -it kafka1 python3 consumer.py

   ```
   
  ##### Example Output:
  
  Key: 1, Value: Marmara, Partition: 0, Timestamp: 1613224639352
  
  Key: 4, Value: İç Anadolu, Partition: 1, Timestamp: 1613224654849


### 2. Truncate topic1 and Consume Iris Dataset

#### Goal: 
Send iris.csv data to Kafka and consume it into separate files per flower type.

#### Steps:
I) Truncate topic1:
   ```
   docker exec -it kafka1 /kafka/bin/kafka-topics.sh --bootstrap-server kafka1:9092 --delete --topic topic1
   docker exec -it kafka1 /kafka/bin/kafka-topics.sh --bootstrap-server kafka1:9092 --create --topic topic1 --partitions 3 --replication-factor 1
  ```

II) Produce iris.csv to topic1 using data-generator:
   ```
   docker exec -it kafka1 python3 dataframe_to_kafka.py -t topic1 -ks '|' -b kafka1:9092 kafka2:9092 kafka3:9092 --input /iris.csv
  ```

III) Run consumer to write flower types to files:
   ```
   docker exec -it kafka1 python3 /consumer_topic1.py
   ```

  ##### Example Output:
  
  topic1|2|0|0|5.1|3.5|1.4|0.2|Iris-setosa
  
  topic1|2|1|2|4.7|3.2|1.3|0.2|Iris-setosa


### 3. Create a Topic if Not Exists (Helper Function)

Usage: Creates a topic only if it does not exist yet.

#### File:
admin.py

#### Function:
```
def create_a_new_topic_if_not_exists(admin_client, topic_name="example-topic", num_partitions=1, replication_factor=1):
    if not topic_exists(admin_client, topic_name):
        new_topic = NewTopic(topic_name, num_partitions, replication_factor)
        result_dict = admin_client.create_topics([new_topic])
        for topic, future in result_dict.items():
            try:
                future.result()  
                print(f"Topic '{topic_name}' created successfully.")
            except Exception as e:
                print(f"Failed to create topic '{topic_name}': {e}")

```


## 🛠️ Notes

- config.py is shared across all scripts for Kafka connection.
- admin.py contains helper logic for creating topics.
- producer.py, consumer.py, and consumer_topic1.py are main scripts meant to be executed.
- Consumers can run in multiple terminals simultaneously to observe message distribution across partitions.
- consumer_topic1.py writes messages to separate files by species.

## 🧾 References

- Confluent Kafka Python Docs: https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html
- Irıs Dataset CSV: https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html

- ## Tips

- Use docker exec -it kafka1 bash to explore container files (/tmp/kafka_out).
- Use docker cp to copy .py files into Kafka container.
- Use Ctrl+C to stop consumers gracefully.

