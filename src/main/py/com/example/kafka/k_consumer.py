from confluent_kafka import Consumer


c = Consumer({
    'bootstrap.servers': 'kafka-broker:9092',
    'group.id': 'python-cg',
    'auto.offset.reset': 'earliest'
})

c.subscribe(["test-topic"])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()
