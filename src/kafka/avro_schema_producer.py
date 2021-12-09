#!/usr/bin/env python
# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
# Writes Avro data, integration with Confluent Cloud Schema Registry
#
# =============================================================================
import base64
import io
import json
import random
from datetime import datetime
from uuid import uuid4

import fastavro
from avro.io import DatumWriter, BinaryEncoder
from confluent_kafka import Producer
from confluent_kafka.avro import AvroProducer

from src.utils.load_avro_schema_from_file import load_avro_schema_from_file, load_avro_schema_as_str

if __name__ == '__main__':

    # args = kfu.parse_args()

    # Read arguments and configurations and initialize
    topic = "users-topic-avro"

    # Create Producer instance
    producer_conf = {
        'bootstrap.servers': 'thinkpad:9092',
    }
    producer = Producer(producer_conf)

    # Report malformed record, discard results, continue polling
    BASE_DIR = "/home/brijeshdhaker/PycharmProjects/spark-python-examples/"
    key_schema, value_schema = load_avro_schema_from_file(BASE_DIR + 'resources/avro/user-record.avsc')
    key_schema_str, value_schema_str = load_avro_schema_as_str(BASE_DIR + 'resources/avro/user-record.avsc')

    epoch = datetime.utcfromtimestamp(0)
    def unix_time_millis(dt):
        return (dt - epoch).total_seconds() * 1000.0

    writer = DatumWriter(value_schema)
    def avro_encode(msg_value):
        bytes_writer = io.BytesIO()
        encoder = BinaryEncoder(bytes_writer)
        writer.write(msg_value, encoder)
        raw_bytes = bytes_writer.getvalue()
        bytes_writer.flush()
        # print(len(raw_bytes) + ", " + type(raw_bytes))
        return raw_bytes

    # using json.loads()
    # convert dictionary string to dictionary
    value_schema_dict = json.loads(value_schema_str)
    def fastavro_encode(msg_value):
        bytes_writer = io.BytesIO()
        fastavro.writer(bytes_writer, fastavro.parse_schema(value_schema_dict), [msg_value])
        raw_bytes = bytes_writer.getvalue()
        bytes_writer.flush()
        # print(len(raw_bytes) + ", " + type(raw_bytes))
        # return base64.b64encode(raw_bytes)
        return raw_bytes

    delivered_records = 0
    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or
    # permanently failed delivery (after retries).
    def delivery_report(err, msg):
        global delivered_records
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            delivered_records += 1
            print("Produced record to topic {} partition [{}] @ offset {}".format(msg.topic(), msg.partition(), msg.offset()))

    if value_schema:

        u_names = ["Brijesh K", "Neeta K", "Keshvi K", "Tejas K"]


        while True:
            #

            user_object = {'id': random.randint(1000, 5000), 'uuid': str(uuid4()), 'name': random.choice(u_names),
                           'emailAddr': "abc@gmail.com", 'age': random.randint(18, 70),
                           'dob': random.randint(18, 70), 'height': round(random.uniform(5.0, 7.0)),
                           'roles': ['admin', 'Technology'], 'status': 'Active'}

            event_datetime = datetime.now()
            d_in_ms = int(event_datetime.strftime("%s")) * 1000
            # int(time.timestamp() * 1000)

            user_object['addTs'] = d_in_ms
            user_object['updTs'] = d_in_ms
            key = user_object['uuid']

            #
            # value = avro_encode(user_object)

            #
            value = fastavro_encode(user_object)
            producer.produce(topic, key=key, value=value, on_delivery=delivery_report)
            # p.poll() serves delivery reports (on_delivery)
            # from previous produce() calls.
            producer.poll(0)
    else:
        print("Avro Schema Can not be Blank.")

    #
    producer.flush()

