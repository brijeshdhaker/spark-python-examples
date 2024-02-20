#!/usr/bin/python2

import random
import json
from confluent_kafka import Producer, KafkaError
from random import randint
from time import sleep
from com.example.models.Transaction import Transaction

if __name__ == '__main__':

    # Read arguments and configurations and initialize
    topic = 'txn-delimiter-stream-topic'

    # Create topic if needed

    # Create Producer instance
    producer_conf = {
        'bootstrap.servers': 'kafkabroker.sandbox.net:9092',
    }
    producer = Producer(producer_conf)


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
            print("Produced record to topic {} partition [{}] @ offset {}".format(msg.topic(), msg.partition(), msg.offset()))


    while True:
        # Serve on_delivery callbacks from previous calls to produce()
        producer.poll(0.0)
        try:
            transaction = Transaction.random()
            record_key = "|"
            record_value = transaction.to_delimited_text(record_key)
            print("Producing record: {}\t{}".format(record_key, record_value))
            producer.produce(topic, key=record_key, value=record_value, on_delivery=acked)
            sleep(1)
        except KeyboardInterrupt:
            break
        except ValueError:
            print("Invalid input, discarding record...")
            continue

    producer.flush()

    print("{} messages were produced to topic {}!".format(delivered_records, topic))