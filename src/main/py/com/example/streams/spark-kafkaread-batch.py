import sys
from confluent_kafka.schema_registry import SchemaRegistryClient
import pyspark.sql.functions as fn
from pyspark.sql.types import StringType
#
from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro, to_avro

#
# https://blogit.michelin.io/kafka-to-delta-lake-using-apache-spark-streaming-avro/
#
if __name__ == "__main__":

    if len(sys.argv) == 0:
        print("Usages: spark-file <inpath> <outpath>")
        sys.exit(-1)

    import pyspark.sql.functions as fn
    from pyspark.sql.avro.functions import from_avro

    def parseAvroDataWithSchemaId(df, ephoch_id):
        cachedDf = df.cache()

        fromAvroOptions = {"mode":"FAILFAST"}

        def getSchema(id):
            return str(schema_registry_client.get_schema(id).schema_str)

        distinctValueSchemaIdDF = cachedDf.select(fn.col('valueSchemaId').cast('integer')).distinct()

        for valueRow in distinctValueSchemaIdDF.collect():
            currentValueSchemaId = sc.broadcast(valueRow.valueSchemaId)
            currentValueSchema = sc.broadcast(getSchema(currentValueSchemaId.value))
            filterValueDF = cachedDf.filter(fn.col('valueSchemaId') == currentValueSchemaId.value)
            filterValueDF \
                .select('topic', 'partition', 'offset', 'timestamp', 'timestampType', 'key', from_avro('fixedValue', currentValueSchema.value, fromAvroOptions).alias('parsedValue')) \
                .write \
                .format("delta") \
                .mode("append") \
                .option("mergeSchema", "true") \
                .save(deltaTablePath)




    spark = SparkSession \
        .builder \
        .appName("SparkStreaming-Kafka") \
        .getOrCreate()

    # `from_avro` requires Avro schema in JSON string format.
    # jsonFormatSchema = open("/home/brijeshdhaker/git-repos/spark-python-examples/resources/user-record.avsc", "r").read()
    binary_to_string = fn.udf(lambda x: str(int.from_bytes(x, byteorder='big')), StringType())


    clickstreamTestDf = (
        spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "localhost:9092")
            .option("subscribe", "users-topic")
            .option("startingOffsets", "earliest")
            .option("failOnDataLoss", "false")
            .load()
            .withColumn('key', fn.col("key").cast(StringType()))
            .withColumn('fixedValue', fn.expr("substring(value, 6, length(value)-5)"))
            .withColumn('valueSchemaId', binary_to_string(fn.expr("substring(value, 2, 4)")))
            .select('topic', 'partition', 'offset', 'timestamp', 'timestampType', 'key', 'valueSchemaId', 'fixedValue')
    )

    #
    # Confluent Schema Registry
    #
    schema_registry_conf = {
        'url': 'http://localhost:8081',
        'basic.auth.user.info': '{}:{}'.format('userid', 'password')
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    users_schema_response = schema_registry_client.get_latest_version("users-topic-value").schema
    users_schema = users_schema_response.schema_str

    # Set the option for what to do with corrupt data in from_avro - either stop on the first failure it finds (FAILFAST) or just set corrupt data to null (PERMISSIVE)
    #fromAvroOptions = {"mode":"FAILFAST"}
    fromAvroOptions = {"mode": "PERMISSIVE"}
    structuredGpsDf = (
        # .select('topic', 'partition', 'offset', 'timestamp', 'timestampType', 'key', from_avro('fixedValue', currentValueSchema.value, fromAvroOptions).alias('parsedValue'))
        clickstreamTestDf.select(from_avro('fixedValue', users_schema, fromAvroOptions).alias("users")).selectExpr("users.*")
    )

    structuredGpsDf.writeStream \
        .outputMode("update") \
        .format("console") \
        .start() \
        .awaitTermination()

    spark.stop()
