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



if __name__ == '__main__':

    # Read arguments and configurations and initialize
    topic = "test-topic"

    key_serializer = lambda k: k.encode('utf-8')
    value_serializer = lambda v: json.dumps(v).encode('utf-8')

    # Create Producer instance
    producer_conf = {
        'bootstrap_servers': 'kafka-broker:9092',
        'client_id': 'python-kafka-client',
        'partitioner': hash_partitioner,
        'key_serializer': key_serializer,
        'value_serializer': value_serializer,
        'acks': 1
    }

    producer = KafkaProducer(
        bootstrap_servers='kafka-broker:9092',
        client_id='python-kafka-client',
        partitioner=hash_partitioner,
        key_serializer=key_serializer,
        value_serializer=value_serializer,
        acks=1
    )
    # Create topic if needed

    delivered_records = 0
    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or
    # permanently failed delivery (after retries).
    def acked(err, msg):
        global delivered_records
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            delivered_records += 1
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))


    def on_send_success(record_metadata):
        print("Produced record to topic {} partition [{}] @ offset {}".format(record_metadata.topic, record_metadata.partition, record_metadata.offset))

    def on_send_error(excp):
        log.error('I am an errback', exc_info=excp) # handle exception


    n = 0
    while True:

        record_key = "alice"
        record_value = json.dumps({'count': random.randint(1000, 5000)})
        print("Producing record: {}\t{}".format(record_key, record_value))

        producer.send(
            topic,
            value=record_value,
            key=record_key
        ).add_callback(on_send_success).add_errback(on_send_error)

        # result = future.get(timeout=60)

        # p.poll() serves delivery reports (on_delivery)
        # from previous produce() calls.
        # producer.poll(0)
        n = n+1
        if n > 1000:
            break

    producer.flush()

    print("{} messages were produced to topic {}!".format(delivered_records, topic))

