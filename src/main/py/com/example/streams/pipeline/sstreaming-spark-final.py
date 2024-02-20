'''
spark/bin/spark-submit \
    --master local --driver-memory 4g \
    --num-executors 2 --executor-memory 4g \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 \
    src/main/py/com/example/streams/pipeline/sstreaming-spark-final.py

# as spark user from master02.cluster host
$SPARK_HOME/bin/spark-submit \
--master yarn
--deploy-mode client \
--num-executors 2
--executor-cores 1 \
--executor-memory 5g
--driver-memory 4g \
--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.0 \
--conf spark.sql.hive.thriftServer.singleSession=true \
src/main/py/com/example/streams/pipeline/sstreaming-spark-final.py

$SPARK_HOME/bin/spark-submit \
    --master local \
    --driver-memory 4g \
    --num-executors 2 \
    --executor-memory 4g \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 \
    src/main/py/com/example/streams/pipeline/sstreaming-spark-final.py

%SPARK_HOME%/bin/spark-submit ^
    --name "structured-stream-pipeline" ^
    --master local[4] ^
    --driver-memory 512MB ^
    --num-executors 2 ^
    --executor-memory 512MB ^
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 ^
    src/main/py/com/example/streams/pipeline/sstreaming-spark-final.py



spark-submit --name "sstreaming-spark-final" \
--master local[4] \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
src/main/py/com/example/streams/pipeline/sstreaming-spark-final.py


'''

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import expr
from pyspark.sql.functions import avg
from pyspark.sql.functions import window


def isPointInPath(x, y, poly):
    """check if point x, y is in poly
    poly -- a list of tuples [(x, y), (x, y), ...]"""
    num = len(poly)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                 (poly[j][1] - poly[i][1])):
            c = not c
        j = i
    return c


def parse_data_from_kafka_message(sdf, schema):
    from pyspark.sql.functions import split
    assert sdf.isStreaming == True, "DataFrame doesn't receive treaming data"
    col = split(sdf['value'], ',')  # split attributes to nested array in one Column
    # now expand col to multiple top-level columns
    for idx, field in enumerate(schema):
        sdf = sdf.withColumn(field.name, col.getItem(idx).cast(field.dataType))
    return sdf.select([field.name for field in schema])


spark = SparkSession.builder \
    .appName("Spark Structured Streaming from Kafka") \
    .getOrCreate()
spark.conf.set("spark.sql.streaming.checkpointLocation", "/home/brijeshdhaker/sstreaming-spark-final/checkpoints/")
spark.sparkContext.setLogLevel('ERROR')


sdfRides = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafkabroker.sandbox.net:9092") \
    .option("subscribe", "taxi-rides") \
    .option("startingOffsets", "latest") \
    .option("kafka.group.id", "taxi-rides-cg") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

sdfFares = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafkabroker.sandbox.net:9092") \
    .option("subscribe", "taxi-fares") \
    .option("startingOffsets", "latest") \
    .option("kafka.group.id", "taxi-fares-cg") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

taxiFaresSchema = StructType([ \
    StructField("rideId", LongType()), StructField("taxiId", LongType()), \
    StructField("driverId", LongType()), StructField("startTime", TimestampType()), \
    StructField("paymentType", StringType()), StructField("tip", FloatType()), \
    StructField("tolls", FloatType()), StructField("totalFare", FloatType())])

taxiRidesSchema = StructType([ \
    StructField("rideId", LongType()), StructField("isStart", StringType()), \
    StructField("endTime", TimestampType()), StructField("startTime", TimestampType()), \
    StructField("startLon", FloatType()), StructField("startLat", FloatType()), \
    StructField("endLon", FloatType()), StructField("endLat", FloatType()), \
    StructField("passengerCnt", ShortType()), StructField("taxiId", LongType()), \
    StructField("driverId", LongType())])

sdfRides = parse_data_from_kafka_message(sdfRides, taxiRidesSchema)
sdfFares = parse_data_from_kafka_message(sdfFares, taxiFaresSchema)

# Data cleaning
LON_EAST, LON_WEST, LAT_NORTH, LAT_SOUTH = -73.7, -74.05, 41.0, 40.5
sdfRides = sdfRides.filter( \
    sdfRides["startLon"].between(LON_WEST, LON_EAST) & \
    sdfRides["startLat"].between(LAT_SOUTH, LAT_NORTH) & \
    sdfRides["endLon"].between(LON_WEST, LON_EAST) & \
    sdfRides["endLat"].between(LAT_SOUTH, LAT_NORTH))
sdfRides = sdfRides.filter(sdfRides["isStart"] == "END")  # Keep only finished!

# Apply watermarks on event-time columns
sdfFaresWithWatermark = sdfFares \
    .selectExpr("rideId AS rideId_fares", "startTime", "totalFare", "tip") \
    .withWatermark("startTime", "30 minutes")  # maximal delay

sdfRidesWithWatermark = sdfRides \
    .selectExpr("rideId", "endTime", "driverId", "taxiId", \
                "startLon", "startLat", "endLon", "endLat") \
    .withWatermark("endTime", "30 minutes")  # maximal delay

# Join with event-time constraints and aggregate
sdf = sdfFaresWithWatermark \
    .join(sdfRidesWithWatermark, \
          expr(""" 
       rideId_fares = rideId AND 
        endTime > startTime AND
        endTime <= startTime + interval 2 hours
        """))

""" *** FEATURE ENGINEERING NEIGHBORHOODS *** """
nbhds_df = spark.read.json("/datasets/nbhd.jsonl")  # nbhd.jsonl file has to be available!
lookupdict = nbhds_df.select("name", "coord").rdd.collectAsMap()
broadcastVar = spark.sparkContext.broadcast(lookupdict)  # use broadcastVar.value from now on
manhattan_bbox = [[-74.0489866963, 40.681530375], [-73.8265135518, 40.681530375], [-73.8265135518, 40.9548628598],
                  [-74.0489866963, 40.9548628598], [-74.0489866963, 40.681530375]]
from pyspark.sql.functions import udf


def find_nbhd(lon, lat):
    '''takes geo point as lon, lat floats and returns name of neighborhood it belongs to
    needs broadcastVar available'''
    if not isPointInPath(lon, lat, manhattan_bbox): return "Other"
    for name, coord in broadcastVar.value.items():
        if isPointInPath(lon, lat, coord):
            return str(name)  # cast unicode->str
    return "Other"  # geo-point not in neighborhoods


find_nbhd_udf = udf(find_nbhd, StringType())
sdf = sdf.withColumn("stopNbhd", find_nbhd_udf("endLon", "endLat"))
sdf = sdf.withColumn("startNbhd", find_nbhd_udf("startLon", "startLat"))
""" *** END OF FEATURE ENGINEERING NEIGHBORHOODS *** """


""" *** AGG *** """
# .withWatermark("endTime", "30 minutes") \
tips = sdf \
    .groupBy(
    window("endTime", "30 minutes", "10 minutes"),
    "stopNbhd") \
    .agg(avg("tip"))
""" *** END OF AGG *** """

""" LAUNCH STS
from py4j.java_gateway import java_import
java_import(spark.sparkContext._gateway.jvm, "")
spark.sparkContext._gateway.jvm.org.apache.spark.sql.hive.thriftserver \
    .HiveThriftServer2.startWithContext(spark._jwrapped)
STS RUNNING """

tips.writeStream \
    .outputMode("append") \
    .format("console") \
    .queryName("tipss") \
    .option("truncate", False) \
    .start() \
    .awaitTermination()
