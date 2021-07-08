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

from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer

if __name__ == '__main__':

    # Read arguments and configurations and initialize
    topic = "users-topic"

    schema_registry_conf = {
        'url': 'http://dockerhost:8081',
        'basic.auth.user.info': '{}:{}'.format('userid', 'password')
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    users_schema_response = schema_registry_client.get_latest_version("users-topic-value").schema
    users_schema = users_schema_response.schema_str

    key_str_deserializer = StringDeserializer()
    user_avro_deserializer = AvroDeserializer(schema_registry_client = schema_registry_client, schema_str =  users_schema)

    # for full list of configurations, see:
    #   https://docs.confluent.io/platform/current/clients/confluent-kafka-python/#deserializingconsumer
    consumer_conf = {
        'bootstrap.servers': 'dockerhost:9092',
        'value.deserializer': user_avro_deserializer,
        'group.id': 'py_avro_consumer',
        'auto.offset.reset': 'earliest'
    }
    # consumer_conf['key.deserializer'] = name_avro_deserializer
    consumer = DeserializingConsumer(consumer_conf)

    # Subscribe to topic
    consumer.subscribe([topic])

    # Process messages
    total_count = 0
    while True:
        try:
            msg = consumer.poll(1.0)
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
                user_object = msg.value()
                print(f"Consumed Avro Record : {user_object['uuid']}\t{user_object['name']}")
        except KeyboardInterrupt:
            break
        except SerializerError as e:
            # Report malformed record, discard results, continue polling
            print("Message deserialization failed {}".format(e))
            pass

    # Leave group and commit final offsets
    consumer.close()