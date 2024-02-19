import sys

from confluent_kafka import Consumer, KafkaException, KafkaError


def msg_process(msg):
    print('Received message: {}'.format(msg.value().decode('utf-8')))


def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))

running = True
def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False


# Synchronous commits
def synchronous_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        msg_count = 0
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=False)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

# Delivery guarantees
def delivery_guarantees_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                consumer.commit(asynchronous=False)
                msg_process(msg)

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


# Asynchronous Commits
def asynchronous_commits_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        msg_count = 0
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()
#
#
#
TOPIC = "kcat-test-topic"

#
#     'enable.auto.commit': False,
#
consumer = Consumer({
    'bootstrap.servers': 'kafkabroker.sandbox.net:19093',
    'sasl.mechanism': 'GSSAPI',
    'security.protocol': 'SASL_SSL',
    'sasl.kerberos.service.name': 'kafka',
    'sasl.kerberos.keytab': '/etc/kerberos/keytabs/kafkaclient.keytab',
    'sasl.kerberos.principal': 'kafkaclient@SANDBOX.NET',
    'ssl.key.location': '/etc/kafka/secrets/clients.key',
    'ssl.key.password': 'confluent',
    'ssl.certificate.location': '/etc/kafka/secrets/clients-signed.crt',
    'ssl.ca.location': '/etc/kafka/secrets/sandbox-ca.pem',
    'group.id': 'confluent_kafka_sasl_ssl_cg',
    'on_commit': commit_completed
})

consumer.subscribe([TOPIC])
MIN_COMMIT_COUNT = 10

try:
    msg_count = 0
    while True:

        msg = consumer.poll(1.0)
        if msg is None: continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                 (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            # application-specific processing
            msg_process(msg)
            msg_count += 1
#            if msg_count % MIN_COMMIT_COUNT == 0:
#                consumer.commit(asynchronous=True)

except:
    print("Something went wrong")

finally:
    # Close down consumer to commit final offsets.
    consumer.close()
