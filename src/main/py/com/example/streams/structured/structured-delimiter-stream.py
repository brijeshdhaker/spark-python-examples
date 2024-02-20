#
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


spark = SparkSession \
    .builder \
    .master("local[4]") \
    .appName("txn-delimiter-stream") \
    .getOrCreate()

spark.conf.set("spark.sql.streaming.checkpointLocation", "/user/brijeshdhaker/structured-delimiter-stream/checkpoints/")
spark.conf.set("spark.sql.shuffle.partitions", "1")
spark.conf.set("spark.sql.hive.convertMetastoreParquet", "false")

spark.sparkContext.setLogLevel('ERROR')

txnSchema = StructType([
    StructField("id", IntegerType()),
    StructField("uuid", StringType()),
    StructField("cardtype", StringType()),
    StructField("website", StringType()),
    StructField("product", StringType()),
    StructField("amount", DoubleType()),
    StructField("city", StringType()),
    StructField("country", StringType()),
    StructField("addts", TimestampType())
])

# Subscribe to 1 topic
structureStreamDf = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafkabroker.sandbox.net:9092") \
    .option("subscribe", "txn-delimiter-stream-topic") \
    .option("startingOffsets", "earliest")\
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Returns True for DataFrames that have streaming sources
print("structureStreamDf.isStreaming : " + str(structureStreamDf.isStreaming))
print("Schema for structureStreamDf  : ")
structureStreamDf.printSchema()

#resultStreamDF = structureStreamDf.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")


def parse_data_from_kafka_message(sdf, schema):

    assert sdf.isStreaming == True, "DataFrame doesn't receive streaming data"
    # split_col = split(lit("2263|10796490-43c6-4d03-b54b-a61f0156fb77|RuPay|Myntra|Laptop,21279.45,New York,USA,1653799085"), "\\|", -1)
    # fdf = sdf.withColumn('id', split_col.getItem(0)).withColumn('uuid', split_col.getItem(1)).withColumn('cardtype', split_col.getItem(2))

    # -- split attributes to nested array in one Column
    split_col = pyspark.sql.functions.split(sdf['value'], '\\|')
    # -- now expand col to multiple top-level columns
    for idx, field in enumerate(schema):
        sdf = sdf.withColumn(field.name, split_col.getItem(idx).cast(field.dataType))
    return sdf.select([field.name for field in schema])

sdfTransaction = parse_data_from_kafka_message(structureStreamDf, txnSchema)
# parse_data_from_kafka_message(resultStreamDF, schema)

# Writing to console sink (for debugging)
sdfTransaction.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("maxRows", 50) \
    .option("truncate", False) \
    .trigger(processingTime="5 seconds")\
    .start() \
    .awaitTermination()

spark.stop()