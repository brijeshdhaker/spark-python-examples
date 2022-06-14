
import sys
from kafka import KafkaConsumer, OffsetAndMetadata, ConsumerRebalanceListener
import json
import mysql.connector
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

consumer = KafkaConsumer(
    bootstrap_servers='kafka-broker:9092',
    client_id='kafka_python_exactly_once_consumer-client',
    group_id='kafka_python_exactly_once_consumer-cg',
    key_deserializer=key_deserializer,
    value_deserializer=value_deserializer,
    enable_auto_commit=False
)
consumer.subscribe(TOPIC)

def shutdown():
    RUNNING = False

def msg_process(msg):
    m_value = msg.value
    print('Received message: {}'.format(m_value))


class KafkaDBHelper(object):

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
        val = (message.key, message.value)
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
database = KafkaDBHelper()


class SaveOffsetsRebalanceListener(ConsumerRebalanceListener):

    def __init__(self, consumer):
        self.consumer = consumer

    def on_partitions_revoked(self, revoked):
        # here commit the current open db transaction if possible to avoid having to reprocess the current
        # un-persisted but processed batch messages -- not 100% necessary
        print("Following Partitions Revoked ....")
        for topic_partition in revoked:
            print("{}, ".format(topic_partition.partition))

        database.commit_transaction()


    # on a rebalancing of partitions this method will be called if a new partition is assigned to this consumer
    def on_partitions_assigned(self, assigned):
        print("Following Partitions Assigned ....")
        for topic_partition in assigned:
            print("{}, ".format(topic_partition.partition))
            self.consumer.seek(topic_partition.partition, database.get_offset(topic_partition))


def consume_messages():

    # subscribe to the topic we want to consume
    consumer.subscribe([TOPIC], listener=SaveOffsetsRebalanceListener(consumer))

    # poll once to ensure joining of consumer group and partitions assigned
    consumer.poll(0)

    # seek to the offsets stored in the DB
    for topic_partition in consumer.assignment():
        # we use the offsets stored in our database rather than kafka
        offset = database.get_offset(topic_partition)
        consumer.seek(topic_partition, offset)

    while True:
        message_batch = consumer.poll()

        # enter DB transaction for batch
        try:

            for topic_partition, partition_batch in message_batch.items():
                for message in partition_batch:
                    database.store_message(message)
                    database.store_offset(message.offset, topic_partition)
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
