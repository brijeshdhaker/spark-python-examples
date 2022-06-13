from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError


c = AvroConsumer({
    'bootstrap.servers': 'kafka-broker:9092',
    'group.id': 'python-avro-cg',
    'schema.registry.url': 'http://schema-registry:8081',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['users-topic-avro'])

while True:
    try:
        msg = c.poll(10)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue

    print(msg.value())

c.close()