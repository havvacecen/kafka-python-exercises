from confluent_kafka import Producer
from config import config

def callback(err, event):
    if err:
        print(f'Produce to topic {event.topic()} failed for event: {event.key()}')
    else:
        val = event.value().decode('utf8')
        print(f'{val} sent to partition {event.partition()}.')

if __name__ == '__main__':
    producer = Producer(config)

    regions = {'1': 'Marmara', '2': 'Ege', '3': 'Akdeniz', '4': 'İç Anadolu',
               '5': 'Doğu Anadolu', '6': 'Karadeniz', '7': 'Güneydoğu Anadolu'}

    for key, value in regions.items():
        producer.produce(topic='regions', key=key, value=value, on_delivery=callback)

    producer.flush()
