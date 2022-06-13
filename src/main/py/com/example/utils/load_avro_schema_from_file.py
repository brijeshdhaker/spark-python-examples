import json
from confluent_kafka import avro

def load_avro_schema_as_str(schema_file):
    #
    key_schema_string = """
    {"type": "string"}
    """
    #
    with open(schema_file, 'r') as file:
        value_schema_string = file.read().rstrip()

    return key_schema_string, str(value_schema_string)

def load_avro_schema_as_json(schema_file):
    #
    key_schema_string = """
    {"type": "string"}
    """
    #
    with open(schema_file, 'r') as file:
        value_schema_string = file.read().rstrip()

    return json.loads(key_schema_string), json.loads(value_schema_string)


def load_avro_schema_as_schema(schema_file):
    key_schema_string = """
    {"type": "string"}
    """

    key_schema = avro.loads(key_schema_string)
    value_schema = avro.load(schema_file)

    return key_schema, value_schema