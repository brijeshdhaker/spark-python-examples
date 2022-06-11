
import sys
from kafka import KafkaConsumer
import json

"""
The simplest way to use the iterator API is to complete the processing and persisting of the result data of the message 
each iteration. This will give you at-least-once behaviour as the latest processed offset may or may not be committed to 
kafka before each iteration meaning that in the event of a failure the consumer will restart from the last comitted 
offset which may not be the latest message that was successfully processed.
"""

RUNNING = True
TOPIC = "test-topic"
MIN_COMMIT_COUNT = 10
key_deserializer = lambda k: k.decode("utf-8")
value_deserializer = lambda v: json.loads(v.decode("utf-8"))

consumer = KafkaConsumer(
    bootstrap_servers='kafka-broker:9092',
    client_id='kafka_python_simple_consumer-client',
    group_id='kafka_python_simple_consumer-cg',
    key_deserializer=key_deserializer,
    value_deserializer=value_deserializer
)
consumer.subscribe(TOPIC)

def shutdown():
    RUNNING = False

def msg_process(msg):
    m_value = msg.value
    print('Received message: {}'.format(m_value))

def consume_messages():
    for message in consumer:
        msg_process(message)

if __name__ == '__main__':
    consume_messages()
    shutdown()
