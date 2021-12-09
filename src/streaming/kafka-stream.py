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

    spark = SparkSession \
        .builder \
        .appName("SparkStreaming-Kafka") \
        .getOrCreate()

    # `from_avro` requires Avro schema in JSON string format.
    # jsonFormatSchema = open("/home/brijeshdhaker/git-repos/spark-python-examples/resources/user-record.avsc", "r").read()
    binary_to_string = fn.udf(lambda x: str(int.from_bytes(x, byteorder='big')), StringType())

    # startingOffsets:earliest    to read all data available in the topic
    # startingOffsets:latest      to reads only new data that’s yet to process
    data_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "users-topic") \
        .option("startingOffsets", "earliest") \
        .option("failOnDataLoss", "false") \
        .option("mode", "PERMISSIVE") \
        .load()

    data_df.printSchema()

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

    #
    from_avro_options = {"mode": "PERMISSIVE"}
    structuredGpsDf = (
        data_df.select(
            from_avro(fn.expr("substring(value, 6, length(value)-5)"), users_schema, from_avro_options).alias("users")
        ).selectExpr("users.*")
    )

    fina_df = structuredGpsDf.fillna(value="", subset=["addTs", "updTs"])

    fina_df.writeStream\
        .outputMode("update")\
        .format("console")\
        .start()\
        .awaitTermination()

    # structuredGpsDf.write.format('jdbc')\
    #     .option("url", "jdbc:mysql://localhost/database_name") \
    #     .option("driver", "com.mysql.jdbc.Driver") \
    #     .option("dbtable", "jdbc:mysql://localhost/database_name") \
    #     .option("user", "jdbc:mysql://localhost/database_name") \
    #     .option("password", "jdbc:mysql://localhost/database_name") \
    #     .mode('append')\
    #     .save()

    spark.stop()
