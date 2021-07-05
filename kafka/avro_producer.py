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
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
# Writes Avro data, integration with Confluent Cloud Schema Registry
#
# =============================================================================
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

import json

if __name__ == '__main__':

    # Read arguments and configurations and initialize
    topic = "users-topic"

    #
    # for full list of configurations, see:
    #  https://docs.confluent.io/platform/current/clients/confluent-kafka-python/#schemaregistryclient
    # Confluent Schema Registry
    #
    schema_registry_conf = {
        'url': 'http://dockerhost:8081',
        'basic.auth.user.info': '{}:{}'.format('userid', 'password')
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    users_schema_response = schema_registry_client.get_latest_version("users-topic-value").schema
    users_schema = users_schema_response.schema_str

    user_avro_serializer = AvroSerializer(schema_registry_client = schema_registry_client, schema_str =  users_schema)

    # for full list of configurations, see:
    #  https://docs.confluent.io/platform/current/clients/confluent-kafka-python/#serializingproducer
    producer_conf = {
        'bootstrap.servers': 'dockerhost:9092',
        'value.serializer' : user_avro_serializer
    }
    # producer_conf['key.serializer'] = StringSerializer
    producer = SerializingProducer(producer_conf)
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

    user_object = {'id': None, 'uuid': '18e1a8aa-6dc6-4e3e-9212-42f32d9d8a49', 'name': 'Brijesh K Dhaker', 'emailAddr': 'brijeshdhaker@gmail.com', 'age': 38, 'dob': 1232, 'height': 5.599999904632568, 'roles': ['admin', 'Technology'], 'status': 'Active', 'addTs': None, 'updTs': None}

    for n in range(10):
        print(f"Producing Avro Record: {user_object['uuid']}\t{user_object['name']}")
        producer.produce(topic=topic, value=user_object, on_delivery=acked)
        producer.poll(0)

    producer.flush()

    print("{} messages were produced to topic {}!".format(delivered_records, topic))