#
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


spark = SparkSession \
    .builder \
    .master("local[4]") \
    .appName("txn-json-stream") \
    .getOrCreate()

spark.conf.set("spark.sql.streaming.checkpointLocation", "/user/brijeshdhaker/structured-json-stream/checkpoints/")
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
    .option("subscribe", "txn-json-stream-topic") \
    .option("startingOffsets", "earliest")\
    .option("failOnDataLoss", "false") \
    .load() \
    .withColumn('key', col("key").cast(StringType())) \
    .withColumn('value', from_json(col("value").cast(StringType()), txnSchema))

# Returns True for DataFrames that have streaming sources
print("structureStreamDf.isStreaming : " + str(structureStreamDf.isStreaming))
print("Schema for structureStreamDf  : ")
structureStreamDf.printSchema()

#resultStreamDF = structureStreamDf.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

recordsDF = structureStreamDf.select("value.*", "timestamp")

# Apply watermarks on event-time columns
recordsDFWithWatermark = recordsDF.selectExpr("id", "cardtype", "website", "product", "amount", "city", "country", "addts", "timestamp") \
    .withWatermark("addts", "30 seconds")  \
    .groupBy(window(recordsDF.addts, "10 seconds", "5 seconds"), recordsDF.country) \
    .count()

# Writing to console sink (for debugging)
recordsDFWithWatermark.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("maxRows", 50) \
    .option("truncate", False) \
    .trigger(processingTime="5 seconds")\
    .start() \
    .awaitTermination()

spark.stop()