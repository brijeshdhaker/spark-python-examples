
import sys
from kafka import KafkaConsumer
import json

"""
The simplest way to use the iterator API is to complete the processing and persisting of the result data of the message 
each iteration. This will give you at-least-once behaviour as the latest processed offset may or may not be committed to 
kafka before each iteration meaning that in the event of a failure the consumer will restart from the last comitted 
offset which may not be the latest message that was successfully processed.

docker-compose -f dc-kafka-cluster.yml exec kafka-broker kafka-console-consumer --bootstrap-server kafka-broker:9092 --topic kafka-python-json-topic --from-beginning --max-messages 100

"""

RUNNING = True
TOPIC = "kafka-python-json-topic"
MIN_COMMIT_COUNT = 10
key_deserializer = lambda k: k.decode("utf-8")
value_deserializer = lambda v: json.loads(v.decode("utf-8"))

consumer = KafkaConsumer(
    bootstrap_servers='kafka-broker:9092',
    client_id='kafka_python_batch_consumer-client',
    group_id='kafka_python_batch_consumer_consumer-cg',
    key_deserializer=key_deserializer,
    value_deserializer=value_deserializer
)
consumer.subscribe(TOPIC)

def shutdown():
    RUNNING = False

def msg_process(msg):
    m_value = msg.value
    print('Received message: {}'.format(m_value))

def consume_messages():
    batch = []

    for message in consumer:
        if len(batch) >= 5:
            print("--------------------------")
            # atomically store results of processing
            for message in batch:
                msg_process(message)
            #
            batch = []

        # add result of message processing to batch
        batch.append(message)

if __name__ == '__main__':
    consume_messages()
    shutdown()
