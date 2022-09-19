
import sys

from confluent_kafka import Consumer, DeserializingConsumer, KafkaError, TopicPartition
import json
import mysql.connector
from base64 import b64encode, b64decode
"""
An at-most-once consumer will commit offsets to kafka as early as possible to avoid reprocessing of the same messages.
This will sometimes result in missed messages.

This consumer will pull a batch of messages and immediately commit the offsets, then proceed to iterate over 
process them. This will ensure that messages are never processed more than once. It will however mean that if a consumer 
unexpectedly exits after comitting but before finishing processing every message in a batch, the unprocessed messages 
will be lost.

docker-compose -f dc-kafka-cluster.yml exec kafka-broker kafka-console-consumer --bootstrap-server kafka-broker:9092 --topic test-topic --from-beginning --max-messages 100

"""

RUNNING = True
TOPIC = "kafka-python-partitioned-topic"
MIN_COMMIT_COUNT = 10
key_deserializer = lambda k: k.decode("utf-8")
value_deserializer = lambda v: json.loads(v.decode("utf-8"))

def shutdown():
    RUNNING = False

def msg_process(msg):
    m_value = msg.value
    print('Received message: {}'.format(m_value))


class MysqlDBHelper(object):

    connection = None

    # The init method or constructor
    def __init__(self):
        self.connection = mysql.connector.connect(
            user="root",
            password="p@SSW0rd",
            host="mysqlserver",
            port="3306",
            database="SANDBOXDB",
            autocommit=False
        )
        self.connection.autocommit = False
        print(self.connection)

    def get_offset(self, topic_partition):
        cursor = self.connection.cursor()
        sql = "select offset from kafka_topic_offsets where `topic_name`=%s and `partition`=%s"
        val = (topic_partition.topic, topic_partition.partition)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        # print(cursor.rowcount, "record effected.")
        return int(result[0])

    def store_message(self, message):
        cursor = self.connection.cursor()
        sql = "INSERT INTO kafka_stream_data(stream_key, stream_value) VALUES (%s, %s)"
        val = (message["key"], message["value"])
        cursor.execute(sql, val)
        insert_count = cursor.rowcount
        # print(insert_count, "record inserted.")
        return insert_count

    def store_offset(self, offset, topic_partition):
        cursor = self.connection.cursor()
        update_sql = "update kafka_topic_offsets set `offset`={} where `topic_name`='{}' and `partition`={}".format(offset, topic_partition.topic, topic_partition.partition)
        val = (offset, topic_partition.topic, topic_partition.partition)
        cursor.execute(update_sql)
        update_count = cursor.rowcount
        print(update_sql)
        return update_count

    def commit_transaction(self):
        self.connection.commit()

    def rollback_transaction(self):
        self.connection.rollback()

    def close(self):
        print("close")
        # if self.connection.is_connected():
            # self.connection.close()


# stand in for database
database = MysqlDBHelper()

def on_partitions_assigned(consumer, assigned_partitions):
    print("Following Partitions Assigned ....")
    partitions=[]
    for topic_partition in assigned_partitions:
        print("{}, ".format(topic_partition.partition))
        partitions.append(TopicPartition(topic_partition.topic, topic_partition.partition, database.get_offset(topic_partition)))
    consumer.assign(partitions)

def on_partitions_revoked(consumer, revoked_partitions):
    # here commit the current open db transaction if possible to avoid having to reprocess the current
    # un-persisted but processed batch messages -- not 100% necessary
    print("Following Partitions Revoked ....")
    for topic_partition in revoked_partitions:
        print("{}, ".format(topic_partition.partition))
    database.commit_transaction()


def on_partitions_lost(consumer, lost_partitions):
    print("Following Partitions lost ....")
    for topic_partition in lost_partitions:
        print("{}, ".format(topic_partition.partition))


# 'key.deserializer': key_deserializer,
# 'value.deserializer': value_deserializer,
# 'auto.offset.reset': 'earliest',
consumer_conf = {
    'bootstrap.servers': 'kafka-broker:9092',
    'client.id': 'confluent_kafka_exactly_once_consumer_client',
    'group.id': 'confluent_kafka_exactly_once_consumer_cg',
    'enable.auto.commit': False
}
consumer = Consumer(consumer_conf)

# subscribe to the topic we want to consume
consumer.subscribe([TOPIC], on_assign=on_partitions_assigned, on_revoke=on_partitions_revoked, on_lost=on_partitions_lost)

def consume_messages():

    eof = {}
    msg_cnt = 0

    while True:

        # read message from input_topic
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue

        topic, partition, offset = msg.topic(), msg.partition(), msg.offset()
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                eof[(topic, partition)] = True
                print("=== Reached the end of {} [{}] at {}====".format(topic, partition, msg.offset()))

                if len(eof) == len(consumer.assignment()):
                    print("=== Reached end of input ===")
                    break
            continue

        # clear EOF if a new message has been received
        eof.pop((topic, partition), None)
        msg_cnt += 1
        record_key, record_value = key_deserializer(msg.key()), value_deserializer(msg.value())
        try:
            database.store_message({"key": record_key, "value": record_value})
            database.store_offset(msg.offset(), TopicPartition(topic, partition, offset))
            database.commit_transaction()

        except mysql.connector.Error as error:
            print("Failed to update record to database rollback: {}".format(error))
            # reverting changes because of exception
            database.rollback_transaction()

#        finally:
#            print("In Finally")


if __name__ == '__main__':
    consume_messages()
    shutdown()
