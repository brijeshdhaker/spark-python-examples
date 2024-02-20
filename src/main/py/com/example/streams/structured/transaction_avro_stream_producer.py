#!/usr/bin/python2

import random
import json
import os
from confluent_kafka import Producer, KafkaError
from random import randint
from time import sleep
from os.path import expanduser
from pathlib import Path
from com.example.models.Transaction import Transaction
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from com.example.utils.load_avro_schema_from_file import load_avro_schema_as_schema, load_avro_schema_as_str


def txn_to_dict(user, ctx):
    # User._address must not be serialized; omit from dict
    return dict(
        id=user.id,
        uuid=user.uuid,
        cardtype=user.cardType,
        website=user.website,
        product=user.product,
        amount=user.amount,
        city=user.city,
        country=user.country,
        addts=user.addts
    )


if __name__ == '__main__':

    # Read arguments and configurations and initialize
    topic = 'txn-avro-stream-topic'
    AVRO_PATH = Path(expanduser("~"), "IdeaProjects", "spark-python-examples", "resources", "avro",
                     "transaction-record.avsc")
    key_schema, value_schema = load_avro_schema_as_schema(AVRO_PATH)

    schema_registry_conf = {'url': 'http://schema-registry:8081'}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    avro_serializer = AvroSerializer(schema_registry_client, str(value_schema), txn_to_dict)

    # Create Producer instance
    producer_conf = {'bootstrap.servers': 'kafkabroker.sandbox.net:9092',
                     'key.serializer': StringSerializer('utf_8'),
                     'value.serializer': avro_serializer}

    producer = SerializingProducer(producer_conf)

    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or
    # permanently failed delivery (after retries).
    delivered_records = 0
    def acked(err, msg):
        global delivered_records
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            delivered_records += 1
            print("Produced record to topic {} partition [{}] @ offset {}".format(msg.topic(), msg.partition(),
                                                                                  msg.offset()))

    while True:
        # Serve on_delivery callbacks from previous calls to produce()
        producer.poll(0.0)
        try:

            transaction = Transaction.random()
            record_key = str(transaction.uuid)

            print("Producing record: {}\t{}".format(record_key, transaction.to_dict()))
            producer.produce(topic, key=record_key, value=transaction, on_delivery=acked)
            sleep(1)

        except KeyboardInterrupt:
            break
        except ValueError:
            print("Invalid input, discarding record...")
            continue

    producer.flush()

    print("{} messages were produced to topic {}!".format(delivered_records, topic))
