#!/usr/bin/env python
# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
# Writes Avro data, integration with Confluent Cloud Schema Registry
#
# =============================================================================
import random
from datetime import datetime
from uuid import uuid4
from time import sleep
from confluent_kafka.avro import AvroProducer

from com.example.utils.load_avro_schema_from_file import load_avro_schema_from_file

if __name__ == '__main__':

    # args = kfu.parse_args()

    # Read arguments and configurations and initialize
    topic = "users-topic-avro"

    # Report malformed record, discard results, continue polling
    BASE_DIR = "/home/brijeshdhaker/IdeaProjects/spark-bigdata-examples/"
    key_schema, value_schema = load_avro_schema_from_file(BASE_DIR + 'resources/avro/user-record.avsc')

    epoch = datetime.utcfromtimestamp(0)
    def unix_time_millis(dt):
        return (dt - epoch).total_seconds() * 1000.0


    if value_schema:

        delivered_records = 0

        # Optional per-message on_delivery handler (triggered by poll() or flush())
        # when a message has been successfully delivered or
        # permanently failed delivery (after retries).
        def delivery_report(err, msg):
            global delivered_records
            """
            Delivery report handler called on successful or failed delivery of message
            """
            if err is not None:
                print("Failed to deliver message: {}".format(err))
            else:
                delivered_records += 1
                print("Produced record to topic {} partition [{}] @ offset {}".format(msg.topic(), msg.partition(), msg.offset()))


        avroProducer = AvroProducer({
            'bootstrap.servers': 'kafka-broker:9092',
            'on_delivery': delivery_report,
            'schema.registry.url': 'http://schema-registry:8081'
        }, default_key_schema=key_schema, default_value_schema=value_schema)

        u_names = ["Brijesh K", "Neeta K", "Keshvi K", "Tejas K"]
        while True:

            #
            # int(time.timestamp() * 1000)
            event_datetime = datetime.now()
            d_in_ms = int(event_datetime.strftime("%s"))
            user_object = {
                'id': random.randint(1000, 5000),
                'uuid': str(uuid4()),
                'name': random.choice(u_names),
                'emailAddr': "abc@gmail.com",
                'age': random.randint(18, 70),
                'dob': random.randint(18, 70),
                'height': round(random.uniform(5.0, 7.0)),
                'roles': ['admin', 'Technology'],
                'status': 'Active',
                'addTs': d_in_ms,
                'updTs': d_in_ms
            }
            key = user_object['uuid']
            # Serve on_delivery callbacks from previous calls to produce()
            avroProducer.poll(0.0)
            #
            print("Producing Avro Record: {}\t{} at time {}".format(user_object['uuid'], user_object['name'], user_object['addTs']))
            avroProducer.produce(topic=topic, key=key, value=user_object)
            sleep(5)

        avroProducer.flush()
        print("{} messages were produced to topic {}!".format(delivered_records, topic))

    else:
        print("Avro Schema Can not be Blank.")
