#!/usr/bin/env python
# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
#
# =============================================================================
import random
import json
from os.path import expanduser
from pathlib import Path
from time import sleep
from kafka import KafkaProducer
from com.example.utils.load_avro_schema_from_file import load_avro_schema_as_json
from fastavro import schemaless_writer, schemaless_reader, parse_schema
from io import BytesIO
from com.example.models.Transaction import Transaction



AVRO_PATH = Path(expanduser("~"), "IdeaProjects", "spark-python-examples", "resources", "avro",
                 "transaction-record.avsc")
key_schema, value_schema = load_avro_schema_as_json(AVRO_PATH)
#
#
#
TOPIC = "kafka-python-avro-topic"

def avroValueSerializer(raw_value):
    rb = BytesIO()
    schemaless_writer(rb, parse_schema(value_schema), raw_value)
    raw_bytes = rb.getvalue()
    return raw_bytes


key_serializer = lambda k: k.encode('utf-8')
value_serializer = lambda v: json.dumps(v).encode('utf-8')

# Create Producer instance
producer = KafkaProducer(
    bootstrap_servers='kafka-broker:9092',
    client_id='kafka_python_avro_producer-client',
    key_serializer=key_serializer,
    value_serializer=avroValueSerializer,
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
        transaction = Transaction.random()
        record_key = str(transaction.uuid)
        produce_message({"key": record_key, "value": transaction.to_dict()})
        sleep(1)

    print("{} messages were produced to topic {}!".format(delivered_records, TOPIC))

