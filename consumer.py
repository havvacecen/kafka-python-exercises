from confluent_kafka import Consumer, KafkaException
from config import config

def set_consumer_configs():
    config['group.id'] = 'region_group'
    config['auto.offset.reset'] = 'earliest'
    config['enable.auto.commit'] = False

def assignment_callback(consumer, partitions):
    for p in partitions:
        print(f'Assigned to {p.topic}, partition {p.partition}')

if __name__ == '__main__':
    set_consumer_configs()
    consumer = Consumer(config)
    consumer.subscribe(['regions'], on_assign=assignment_callback)

    try:
        while True:
            event = consumer.poll(1.0)
            if event is None:
                continue
            if event.error():
                raise KafkaException(event.error())
            else:
                key = event.key().decode('utf8') if event.key() else None
                val = event.value().decode('utf8')
                partition = event.partition()
                timestamp = event.timestamp()[1] # index 1 timestamp verir -0 type-
                print(f'Key: {key}, Value: {val}, Partition: {partition}, Timestamp: {timestamp} ')
                # consumer.commit(event)
    except KeyboardInterrupt:
        print('Canceled by user.')
    finally:
        consumer.close()
