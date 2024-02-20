
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
TOPIC = "kafka-python-simple-topic"
MIN_COMMIT_COUNT = 10
key_deserializer = lambda k: k.decode("utf-8")
value_deserializer = lambda v: v.decode("utf-8")

consumer = KafkaConsumer(
    bootstrap_servers='kafkabroker.sandbox.net:9092',
    client_id='kafka_python_simple_consumer-client',
    group_id='kafka_python_simple_consumer-cg',
    key_deserializer=key_deserializer,
    value_deserializer=value_deserializer,
    auto_offset_reset='earliest',
    enable_auto_commit=False
)
""" 
Partitions will be dynamically assigned via a group coordinator. 
Topic subscriptions are not incremental: this list will replace the current assignment (if there is one).
"""
consumer.subscribe(TOPIC)

def shutdown():
    RUNNING = False

def msg_process(msg):
    m_value = msg.value
    print('Received message: {}'.format(m_value))

def consume_messages():
    for m in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print ("%s:%d:%d: key=%s value=%s" % (m.topic, m.partition, m.offset, m.key, m.value))
        msg_process(m)

if __name__ == '__main__':
    consume_messages()
    shutdown()
