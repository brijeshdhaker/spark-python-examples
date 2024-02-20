#!/usr/bin/env python
# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
#
# =============================================================================
import random
from time import sleep
from kafka import KafkaProducer


#
#
#
TOPIC = "kafka-python-simple-topic"

#
# Create Producer instance
#
key_serializer = lambda k: k.encode('utf-8')
value_serializer = lambda v: v.encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers='kafkabroker.sandbox.net:9092',
    client_id='kafka_python_simple_producer',
    key_serializer=key_serializer,
    value_serializer=value_serializer,
    acks=1
)

#
#
#
def on_send_success(record_metadata):
    print("topic [{}] partition [{}]  offset [{}]".format(record_metadata.topic, record_metadata.partition, record_metadata.offset))

#
#
#
def on_send_error(excp):
    # handle exception
    print('There is an error {}'.format(excp))

#
#
#
def produce_message(event):
    #
    future = producer.send(TOPIC, value=event["value"], key=event["key"]).add_callback(on_send_success).add_errback(on_send_error)
    result = future.get(timeout=60)
    # flush the message buffer to force message delivery to broker on each iteration
    producer.flush()


#
#
#
if __name__ == '__main__':

    produced_records = 0
    while True:
        #
        produced_records += 1
        #
        KEYS = ["A", "B", "C", "D"]
        record_key = random.choice(KEYS)
        record_value = "This is test event {} of type {}".format(produced_records, record_key)
        produce_message({"key": record_key, "value": record_value})
        sleep(1)

    print("{} messages were produced to topic {}!".format(delivered_records, TOPIC))

