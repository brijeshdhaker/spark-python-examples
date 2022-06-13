from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import expr
from pyspark.sql.functions import avg
from pyspark.sql.functions import window

from pyspark.sql.functions import rand

spark = SparkSession.builder \
    .appName("stream-stream-join") \
    .getOrCreate()
spark.conf.set("spark.sql.streaming.checkpointLocation", "/home/brijeshdhaker/stream-stream-join/checkpoints/")
spark.sparkContext.setLogLevel('ERROR')
spark.conf.set("spark.sql.shuffle.partitions", "1")

impressions = (
    spark.readStream.format("rate").option("rowsPerSecond", "5").option("numPartitions", "1").load()
        .selectExpr("value AS adId", "timestamp AS impressionTime")
)

clicks = (
    spark.readStream.format("rate").option("rowsPerSecond", "5").option("numPartitions", "1").load()
        .where((rand() * 100).cast("integer") < 10)  # 10 out of every 100 impressions result in a click
        .selectExpr("(value - 50) AS adId ",
                    "timestamp AS clickTime")  # -50 so that a click with same id as impression is generated later (i.e. delayed data).
        .where("adId > 0")
)

from pyspark.sql.functions import expr

# Define watermarks
impressionsWithWatermark = impressions \
    .selectExpr("adId AS impressionAdId", "impressionTime") \
    .withWatermark("impressionTime", "10 seconds ")

clicksWithWatermark = clicks \
    .selectExpr("adId AS clickAdId", "clickTime") \
    .withWatermark("clickTime", "20 seconds")  # max 20 seconds late

joinresults = impressionsWithWatermark.join(
    clicksWithWatermark,
    expr(""" 
      clickAdId = impressionAdId AND 
      clickTime >= impressionTime AND 
      clickTime <= impressionTime + interval 1 minutes    
      """
         )
)

# Writing to console sink (for debugging)
joinresults.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("maxRows", 50) \
    .option("truncate", False) \
    .trigger(processingTime="5 seconds") \
    .start() \
    .awaitTermination()
