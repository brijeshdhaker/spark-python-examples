import sys
from kafka import KafkaConsumer, ConsumerRebalanceListener
import json

from kafka.consumer.fetcher import ConsumerRecord


def msg_process(msg):
    m_value = msg.value
    print('Received message: {}'.format(m_value))


def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))


running = True


def shutdown():
    running = False


def default_offset_commit_callback(offsets, response):
    print(str(offsets))


"""
#
# Exactly Once Consumer
#
"""


class SaveOffsetsRebalanceListener(ConsumerRebalanceListener):

    def __init__(self, consumer):
        self.consumer = consumer

    def on_partitions_revoked(self, revoked):
        pass

    def on_partitions_assigned(self, assigned):
        pass


"""
#
#
#
"""
TOPIC = "kafka-python-json-topic"
key_deserializer = lambda k: k.decode("utf-8")
value_deserializer = lambda v: json.loads(v.decode("utf-8"))

consumer = KafkaConsumer(
    bootstrap_servers='kafka-broker:9092',
    client_id='python-kafka-client',
    group_id='python-kafka-client-cg',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    default_offset_commit_callback=default_offset_commit_callback,
    key_deserializer=key_deserializer,
    value_deserializer=value_deserializer
)

consumer.subscribe([TOPIC])
MIN_COMMIT_COUNT = 10

try:
    msg_count = 0
    while True:

        # msg = next(consumer)
        results = consumer.poll(timeout_ms=2000)

        if results is None:
            continue
        else:
            # application-specific processing
            for messages in results.values():
                for m in messages:
                    print("topic=%s | partition=%d | offset=%d | key=%s | value=%s" % (m.topic, m.partition, m.offset, m.key, m.value))
                    # msg_process(msg)
                    msg_count += 1
                    if msg_count % MIN_COMMIT_COUNT == 0:
                        print("Try for commit.")
                        # commits the latest offsets returned by poll
                        # consumer.commit()
                        # consumer.commit(asynchronous=True)

except:
    print("Something went wrong")

finally:
    # Close down consumer to commit final offsets.
    consumer.close()
