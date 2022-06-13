#!/usr/bin/env python

import base64
import io

import avro.schema
import fastavro
from avro.io import DatumReader, BinaryDecoder
from confluent_kafka import Consumer
from confluent_kafka.avro import SerializerError
import random
import json
from confluent_kafka import Producer, KafkaError
from random import randint
from time import sleep
from com.example.models.Transaction import Transaction

from com.example.utils.load_avro_schema_from_file import load_avro_schema_as_schema, load_avro_schema_as_str
import random
import json
import hashlib

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
        p = numPartitions % sp
    else:
        p = int(hashlib.sha1(key.encode()).hexdigest(), 16) % (numPartitions - sp) + sp

    #print("Key = " + str(key) + " Partition = " + str(p))
    return all_partitions[int(p)]



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

    idx = int(hashlib.sha1(key.encode()).hexdigest(), 16) % (10 ** 8)
    idx &= 0x7fffffff
    idx %= len(all_partitions)
    return all_partitions[idx]

if __name__ == '__main__':

    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    print("Key = " + str("TESS") + " Partition = " + str(hash_partitioner("TESS", list, list)))
    print("Key = " + str("ABC") + " Partition = " + str(hash_partitioner("TESS", list, list)))
    print("Key = " + str("XYZ") + " Partition = " + str(hash_partitioner("TESS", list, list)))
    print("Key = " + str("TESS") + " Partition = " + str(hash_partitioner("TESS", list, list)))
    print("Key = " + str("PQR") + " Partition = " + str(hash_partitioner("TESS", list, list)))

    print("Hello")
