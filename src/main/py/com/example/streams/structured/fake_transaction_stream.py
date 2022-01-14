#!/usr/bin/python2

from kafka import KafkaProducer
from random import randint
from time import sleep
from com.example.models.Transaction import Transaction
import sys

BROKER = 'kafka-broker:9092'
TOPIC = 'structured-stream-source'

try:
    p = KafkaProducer(bootstrap_servers=BROKER)
except Exception as e:
    print("ERROR --> {e}")
    sys.exit(1)

while True:
    transaction = Transaction.random()
    print(">>> '{}'".format(transaction.to_dict()))
    p.send(topic=TOPIC, value=bytes(str(transaction.to_dict()), encoding='utf8'), key=bytes(str(transaction.uuid), encoding='utf8'))
    sleep(.1)

