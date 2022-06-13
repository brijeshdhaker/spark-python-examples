from fastavro import schemaless_writer, schemaless_reader, parse_schema
from io import BytesIO

schema = parse_schema(
    {
        "type": "record",
        "name": "User",
        "namespace": "example.avro",
        "fields": [
            {
                "name": "name",
                "type": "string"
            },
            {
                "name": "favorite_number",
                "type": [
                    "int",
                    "null"
                ]
            },
            {
                "name": "favorite_color",
                "type": [
                    "string",
                    "null"
                ]
            }
        ]
    }
)

#rb = BytesIO(b'{"name": "Alyssa", "favorite_number": 256}')
#msg = schemaless_reader(rb, schema)
#print(msg)


rb = BytesIO()
schemaless_writer(rb, schema, {"name": "Alyssa", "favorite_number": 256})
raw_bytes = rb.getvalue()  # b'\x0cAlyssa\x00\x80\x04\x02'
print(raw_bytes)

rb = BytesIO(raw_bytes)
data = schemaless_reader(rb, schema)
print(data)
# {'name': 'Alyssa', 'favorite_number': 256, 'favorite_color': None}