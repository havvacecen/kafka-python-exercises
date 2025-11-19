from confluent_kafka.admin import (AdminClient, NewTopic, 
                                   ConfigResource)
from config import config
# return True if topic exists and False if not
def topic_exists(admin, topic):
    metadata = admin.list_topics()
    for t in iter(metadata.topics.values()):
        if t.topic == topic:
            return True
    return False

# create new topic and return results dictionary
def create_topic(admin, topic):
    new_topic = NewTopic(topic, num_partitions=3, replication_factor=1) 
    result_dict = admin.create_topics([new_topic])
    for topic, future in result_dict.items():
        try:
            future.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))

if __name__ == '__main__':
    # Create Admin client
    admin = AdminClient(config)
    topic_name = 'regions'

    # Create topic if it doesn't exist
    if not topic_exists(admin, topic_name):
        create_topic(admin, topic_name)
