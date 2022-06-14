
import sys
from kafka import KafkaConsumer, OffsetAndMetadata
import json

"""
An at-most-once consumer will commit offsets to kafka as early as possible to avoid reprocessing of the same messages.
This will sometimes result in missed messages.

This consumer will pull a batch of messages and immediately commit the offsets, then proceed to iterate over 
process them. This will ensure that messages are never processed more than once. It will however mean that if a consumer 
unexpectedly exits after comitting but before finishing processing every message in a batch, the unprocessed messages 
will be lost.

docker-compose -f dc-kafka-cluster.yml exec kafka-broker kafka-console-consumer --bootstrap-server kafka-broker:9092 --topic test-topic --from-beginning --max-messages 100

"""

RUNNING = True
TOPIC = "kafka-python-json-topic"
MIN_COMMIT_COUNT = 10
key_deserializer = lambda k: k.decode("utf-8")
value_deserializer = lambda v: json.loads(v.decode("utf-8"))

consumer = KafkaConsumer(
    bootstrap_servers='kafka-broker:9092',
    client_id='kafka_python_most_once_consumer-client',
    group_id='kafka_python_most_once_consumer-cg',
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
        consumer.commit()

        for topic_partition, partition_batch in message_batch.items():
            for message in partition_batch:
                # do processing of message
                msg_process(message)



if __name__ == '__main__':
    consume_messages()
    shutdown()
