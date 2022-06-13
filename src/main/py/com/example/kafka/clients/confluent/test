#!/usr/bin/env python
#
# Copyright 2020 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# =============================================================================
#
# Consume messages from Confluent Cloud
# Using Confluent Python Client for Apache Kafka
# Reads Avro data, integration with Confluent Cloud Schema Registry
#
# =============================================================================
import base64
import io

import avro.schema
import fastavro
from avro.io import DatumReader, BinaryDecoder
from confluent_kafka import Consumer
from confluent_kafka.avro import SerializerError

from com.example.utils.load_avro_schema_from_file import load_avro_schema_as_schema, load_avro_schema_as_str

if __name__ == '__main__':

    # Read arguments and configurations and initialize
    topic = "users-topic"
    BASE_DIR = "/home/brijeshdhaker/PycharmProjects/spark-python-examples/"
    key_schema, value_schema = load_avro_schema_as_schema(BASE_DIR + 'resources/avro/user-record.avsc')
    key_schema_str, value_schema_str = load_avro_schema_as_str(BASE_DIR + 'resources/avro/user-record.avsc')

    schema = avro.schema.parse(open(BASE_DIR + 'resources/avro/user-record.avsc').read())

    reader = DatumReader(schema)
    def avro_decode(raw_bytes):
        bytes_reader = io.BytesIO(raw_bytes)
        bytes_reader.seek(5)
        decoder = BinaryDecoder(bytes_reader)
        event_dict = reader.read(decoder)
        return event_dict

    def fastavro_decode(raw_bytes):
        bytes_reader = io.BytesIO(raw_bytes)
        # bytes_reader.seek(5)
        event = {}
        for record in fastavro.reader(bytes_reader):
            event = record
            #print("{}".format(record['id']))
        return event

    # Report malformed record, discard results, continue polling
    avro_consumer = Consumer({
        'bootstrap.servers': 'thinkpad:9092',
        'group.id': 'python-avro-cg',
        'auto.offset.reset': 'earliest'
    })

    avro_consumer.subscribe(["users-topic"])

    # Process messages
    total_count = 0
    while True:
        try:
            msg = avro_consumer.poll(1.0)
            if msg is None:
                # No message available within timeout.
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print('error: {}'.format(msg.error()))
            else:
                key_object = msg.key()
                #
                # raw_bytes = base64.b64decode(msg.value())
                raw_bytes = msg.value()
                user_object = avro_decode(raw_bytes)
                # user_object = fastavro_decode(raw_bytes)

                #
                print("Consumed Avro Record: {}".format(user_object))
        except KeyboardInterrupt:
            break
        except SerializerError as e:
            # Report malformed record, discard results, continue polling
            print("Message deserialization failed {}".format(e))
            pass

    # Leave group and commit final offsets
    avro_consumer.close()
