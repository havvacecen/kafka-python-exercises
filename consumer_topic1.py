from confluent_kafka import Consumer, KafkaException
from config import config
import os

def set_consumer_configs():
    config['group.id'] = 'iris_group'
    config['auto.offset.reset'] = 'earliest'
    config['enable.auto.commit'] = False

# dosyaların bulunacağı dizin
OUT_DIR = "/tmp/kafka_out"
os.makedirs(OUT_DIR, exist_ok=True)

if __name__ == '__main__':
    set_consumer_configs()
    consumer = Consumer(config)
    consumer.subscribe(['topic1'])

    try:
        while True:
            event = consumer.poll(1.0)
            if event is None:
                continue
            if event.error():
                raise KafkaException(event.error())

            topic = event.topic()
            partition = event.partition()
            offset = event.offset()
            val = event.value().decode('utf-8')
            val = val.replace(',', '|')

            # dosyayı belirleme
            species = val.split(',')[-1].strip().lower()
            if 'setosa' in species:
                out_path = f"{OUT_DIR}/setosa_out.txt"
            elif 'versicolor' in species:
                out_path = f"{OUT_DIR}/versicolor_out.txt"
            elif 'virginica' in species:
                out_path = f"{OUT_DIR}/virginica_out.txt"
            else:
                out_path = f"{OUT_DIR}/other_out.txt"

            # Dosyaya yazma
            with open(out_path, "a") as f:
                f.write(f"{topic}|{partition}|{offset}|{val}\n")

            print(f"Written to {out_path}: {val}")

            # consumer.commit(event)

    except KeyboardInterrupt:
        print('Canceled by user.')
    finally:
        consumer.close()
