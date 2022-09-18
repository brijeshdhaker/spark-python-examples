#!/usr/bin/env python
# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
#
# =============================================================================
import base64
import random
import json
import hashlib
from time import sleep

from kafka import KafkaProducer

def key_partitioner(key, all_partitions, available):

    """
    Customer Kafka partitioner to get the partition corresponding to key
    :param key: partitioning key
    :param all_partitions: list of all partitions sorted by partition ID
    :param available: list of available partitions in no particular order
    :return: one of the values from all_partitions or available
    """

    numPartitions = len(all_partitions)
    sp = abs(numPartitions*0.3)
    p = 0

    if key is None:
        if available:
            return random.choice(available)
        return random.choice(all_partitions)

    if key == "TESS":
        p = int(hashlib.sha1(key).hexdigest(), 16) % sp
    else:
        p = int(hashlib.sha1(key).hexdigest(), 16) % (numPartitions - sp) + sp

    print("Key = " + str(key) + " Partition = " + str(p))
    return all_partitions[p]


def hash_partitioner(key, all_partitions, available):
    """
    Customer Kafka partitioner to get the partition corresponding to key
    :param key: partitioning key
    :param all_partitions: list of all partitions sorted by partition ID
    :param available: list of available partitions in no particular order
    :return: one of the values from all_partitions or available
    """

    if key is None:
        if available:
            return random.choice(available)
        return random.choice(all_partitions)

    idx = int(hashlib.sha1(key).hexdigest(), 16) % (10 ** 8)
    idx &= 0x7fffffff
    idx %= len(all_partitions)
    return all_partitions[idx]

#
#
#
TOPIC = "kafka-python-partitioned-topic"
key_serializer = lambda k: k.encode('utf-8')
value_serializer = lambda v: json.dumps(v).encode('utf-8')

# Create Producer instance
producer = KafkaProducer(
    bootstrap_servers='kafka-broker:9092',
    client_id='python-kafka-client',
    key_serializer=key_serializer,
    value_serializer=value_serializer,
    partitioner=hash_partitioner,
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
    log.error('I am an errback', exc_info=excp) # handle exception

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
        delivered_records += 1
        COUNTRIES = ["IN", "USA", "UK", "JP"]
        record_key = random.choice(COUNTRIES)
        record_value = json.dumps({'key': record_key, 'index': delivered_records})
        produce_message({"key": record_key, "value": record_value})
        #
        sleep(1)

    print("{} messages were produced to topic {}!".format(delivered_records, TOPIC))

