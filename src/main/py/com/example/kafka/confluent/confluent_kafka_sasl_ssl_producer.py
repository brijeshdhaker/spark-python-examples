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
#
# =============================================================================
from time import sleep
from confluent_kafka import Producer, KafkaError
import random
#
#
#
TOPIC = "kcat-test-topic"

# Create Producer instance
producer = Producer({
    'bootstrap.servers': 'kafkabroker.sandbox.net:19093',
    'sasl.mechanism': 'GSSAPI',
    'security.protocol': 'SASL_SSL',
    'sasl.kerberos.service.name': 'kafka',
    'sasl.kerberos.keytab': '/etc/kerberos/keytabs/kafkaclient.keytab',
    'sasl.kerberos.principal': 'kafkaclient@SANDBOX.NET',
    'ssl.key.location': '/etc/kafka/secrets/clients.key',
    'ssl.key.password': 'confluent',
    'ssl.certificate.location': '/etc/kafka/secrets/clients-signed.crt',
    'ssl.ca.location': '/etc/kafka/secrets/sandbox-ca.pem'
})

#
#
#
def acked(err, msg):
    delivered_records = 0
    """Delivery report handler called on successful or failed delivery of message """
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        delivered_records += 1
        print("Produced record to topic {} partition [{}] @ offset {}"
              .format(msg.topic(), msg.partition(), msg.offset()))

#
#
#
def produce_message(event):
    #
    producer.produce(TOPIC, key=event["key"], value=event["value"], on_delivery=acked)
    # from previous produce() calls.
    producer.poll(0)
    # flush the message buffer to force message delivery to broker on each iteration
    producer.flush()


if __name__ == '__main__':
    produced_records = 0
    while True:
        #
        produced_records += 1
        #
        KEYS = ["A", "B", "C", "D"]
        record_key = random.choice(KEYS)
        # record_value = json.dumps({'key': record_key, 'index': produced_records})
        record_value = "This is test event {} of type {}".format(produced_records, record_key)
        produce_message({"key": record_key, "value": record_value})
        sleep(1)

    print("{} messages were produced to topic {}!".format(delivered_records, topic))

