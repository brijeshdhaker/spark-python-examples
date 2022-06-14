#!/usr/bin/env python
# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
#
# =============================================================================
import random
import json
from time import sleep
from kafka import KafkaProducer


#
#
#
TOPIC = "kafka-python-json-topic"
key_serializer = lambda k: k.encode('utf-8')
value_serializer = lambda v: v.encode('utf-8')

# Create Producer instance
producer = KafkaProducer(
    bootstrap_servers='kafka-broker:9092',
    client_id='python-kafka-client',
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
def produce_message(message):
    #
    producer.send(TOPIC, value=message["value"], key=message["key"]).add_callback(on_send_success).add_errback(on_send_error)
    # flush the message buffer to force message delivery to broker on each iteration
    producer.flush()


#
#
#
if __name__ == '__main__':

    delivered_records = 0
    while True:
        #
        delivered_records = delivered_records+1
        #
        KEYS = ["A", "B", "C", "D"]
        record_key = random.choice(KEYS)
        record_value = json.dumps({'key': record_key, 'index': delivered_records})
        produce_message({"key": record_key, "value": record_value})
        sleep(1)

    print("{} messages were produced to topic {}!".format(delivered_records, TOPIC))

