
import sys
from kafka import KafkaConsumer, OffsetAndMetadata
import json

"""
An at-least-once consumer commits the offsets to kafka only after finishing storing all of results of processing the 
message. This will result in occasional reprocessing of the same messages.

docker-compose -f dc-kafka-cluster.yml exec kafka-broker kafka-console-consumer --bootstrap-server kafka-broker:9092 --topic test-topic --from-beginning --max-messages 100

"""

RUNNING = True
TOPIC = "kafka-python-json-topic"
MIN_COMMIT_COUNT = 10
key_deserializer = lambda k: k.decode("utf-8")
value_deserializer = lambda v: json.loads(v.decode("utf-8"))

consumer = KafkaConsumer(
    bootstrap_servers='kafka-broker:9092',
    client_id='kafka_python_least_once_consumer-client',
    group_id='kafka_python_least_once_consumer-cg',
    key_deserializer=key_deserializer,
    value_deserializer=value_deserializer,
    enable_auto_commit=False
)
consumer.subscribe(TOPIC)

def shutdown():
    RUNNING = False

def msg_process(msg):
    m_value = msg.value
    print('Received message: {}'.format(m_value))


def consume_messages():
    while True:
        message_batch = consumer.poll()

        for topic_partition, partition_batch in message_batch.items():
            for message in partition_batch:
                # do processing of message
                print(message.value.decode('utf-8'))

                # commit once every two messages for each partition
                if message.offset % 2 == 0:
                    # pass the topic, partition and offset as a dict of TopicPartition: OffsetAndMetadata
                    consumer.commit({topic_partition: OffsetAndMetadata(message.offset, "no metadata")})


def least_once_consume_messages():
    while True:
        message_batch = consumer.poll()
        for partition_batch in message_batch.values():
            for message in partition_batch:
                # do processing of message
                msg_process(message)

        # commits the latest offsets returned by poll
        consumer.commit()

if __name__ == '__main__':
    least_once_consume_messages()
    shutdown()
