#!/usr/bin/env python
# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
# Writes Avro data, integration with Confluent Cloud Schema Registry
#
# =============================================================================

from confluent_kafka import SerializingProducer
from confluent_kafka import avro
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient, Schema, SchemaRegistryError
from confluent_kafka.schema_registry.avro import AvroSerializer
import kafka_utils as kfu
import json

BASE_DIR = "/home/brijeshdhaker/git-repos/spark-python-examples/"

if __name__ == '__main__':

    args = kfu.parse_args()
    conf = kfu.read_kafka_config(BASE_DIR+"resources/kafka_producer.properties")

    # Read arguments and configurations and initialize
    topic = "users-topic"

    # Create topic if needed
    kfu.create_topic(conf, topic)

    #
    # for full list of configurations, see:
    #  https://docs.confluent.io/platform/current/clients/confluent-kafka-python/#schemaregistryclient
    # Confluent Schema Registry
    #
    schema_registry_conf = {
        'url': 'http://localhost:8081',
        'basic.auth.user.info': '{}:{}'.format('userid', 'password')
    }
    users_schema=""
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    try:
        users_schema_response = schema_registry_client.get_latest_version("users-topic-value").schema
        users_schema = users_schema_response.schema_str
    except SchemaRegistryError as e:
        # Report malformed record, discard results, continue polling
        users_schema = open(BASE_DIR+'resources/avro/UserService-Schema.avsc', 'r').read()
        avro_schema = Schema(users_schema, 'AVRO')
        _schema_id = schema_registry_client.register_schema("users-topic-value", avro_schema)
        pass

    if users_schema:

        print(users_schema)

        key_str_serializer = StringSerializer('utf_8')
        user_avro_serializer = AvroSerializer(schema_registry_client=schema_registry_client, schema_str=users_schema)

        # for full list of configurations, see:
        #  https://docs.confluent.io/platform/current/clients/confluent-kafka-python/#serializingproducer
        producer_conf = {
            'bootstrap.servers': 'localhost:9092',
            'key.serializer': key_str_serializer,
            'value.serializer': user_avro_serializer
        }
        producer = SerializingProducer(producer_conf)
        delivered_records = 0

        # Optional per-message on_delivery handler (triggered by poll() or flush())
        # when a message has been successfully delivered or
        # permanently failed delivery (after retries).
        def acked(err, msg):
            global delivered_records
            """
            Delivery report handler called on
            successful or failed delivery of message
            """
            if err is not None:
                print("Failed to deliver message: {}".format(err))
            else:
                delivered_records += 1
                print("Produced record to topic {} partition [{}] @ offset {}"
                      .format(msg.topic(), msg.partition(), msg.offset()))

        user_object = {'id': None, 'uuid': '18e1a8aa-6dc6-4e3e-9212-42f32d9d8a49', 'name': 'Brijesh K Dhaker', 'emailAddr': 'brijeshdhaker@gmail.com', 'age': 38, 'dob': 1232, 'height': 5.60, 'roles': ['admin', 'Technology'], 'status': 'Active'}

        for n in range(10):
            user_object['id'] = n+1000
            #user_object['addTs'] = 11122324433242
            #user_object['updTs'] = 32133423431232
            print(f"Producing Avro Record: {user_object['uuid']}\t{user_object['name']}")
            producer.produce(topic=topic, value=user_object, on_delivery=acked)
            producer.poll(0)

        producer.flush()
        print("{} messages were produced to topic {}!".format(delivered_records, topic))

    else:
        print("Avro Schema Can not be Blank.")
