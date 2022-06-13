import avro.schema
import io, random
from avro.io import DatumWriter, DatumReader
import avro.io

# Path to user.avsc avro schema
schema_path= "confluent/user.avsc"
schema = avro.schema.parse(open(schema_path).read())


for i in range(1):
    writer = avro.io.DatumWriter(schema)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write({"name": "123", "favorite_color": "111", "favorite_number": random.randint(0, 10)}, encoder)
    raw_bytes = bytes_writer.getvalue()

    print(raw_bytes)

    bytes_reader = io.BytesIO(raw_bytes)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    user1 = reader.read(decoder)
    print(" USER = {}".format(user1))