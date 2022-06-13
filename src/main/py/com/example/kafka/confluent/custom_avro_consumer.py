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
import io

from avro.io import DatumReader, BinaryDecoder
from confluent_kafka import Consumer
from confluent_kafka.avro import SerializerError

from com.example.utils.load_avro_schema_from_file import load_avro_schema_as_schema

if __name__ == '__main__':

    # Read arguments and configurations and initialize
    topic = "users-topic-avro"
    BASE_DIR = "/home/brijeshdhaker/IdeaProjects/spark-bigdata-examples/"
    key_schema, value_schema = load_avro_schema_as_schema(BASE_DIR + 'resources/avro/user-record.avsc')

    reader = DatumReader(value_schema)
    def decode(msg_value):
        message_bytes = io.BytesIO(msg_value)
        message_bytes.seek(5)
        decoder = BinaryDecoder(message_bytes)
        event_dict = reader.read(decoder)
        return event_dict


    # Report malformed record, discard results, continue polling
    avro_consumer = Consumer({
        'bootstrap.servers': 'kafka-broker:9092',
        'group.id': 'python-custom-cg',
        'auto.offset.reset': 'earliest'
    })

    avro_consumer.subscribe([topic])

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
                continue
            elif msg.error():
                print('error: {}'.format(msg.error()))
            else:
                key_object = msg.key()
                user_object = decode(msg.value())
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
