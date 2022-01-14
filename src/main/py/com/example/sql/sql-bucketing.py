import com.example.utils.commons as commons
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col


conf = SparkConf() \
    .set("spark.eventLog.enabled", "true") \
    .set("spark.eventLog.dir", "file:///apps/hostpath/spark/logs/")

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("PysparkSQL-Columns") \
    .config(conf=conf) \
    .getOrCreate()

#
spark.setLogLevel("ERROR")

#
#
# spark.conf.get("spark.sql.sources.bucketing.enabled")
# spark.sql.sources.bucketing.maxBuckets
# spark.sql.sources.bucketing.autoBucketedScan.enabled
# spark.sql.sources.bucketing.autoBucketedScan.enabled
# spark.sql.bucketing.coalesceBucketsInJoin.maxBucketRatio
# spark.sql.legacy.bucketedTableScan.outputOrdering
# spark.sql.shuffle.partitions
#

data = [("James", 23), ("Ann", 40)]
df = spark.createDataFrame(data).toDF("name.fname", "gender")
df.printSchema()

# this will create a DataFrame with one column id


# Mode : append/overwrite
df.write.bucketBy(4, "id")\
    .sortBy("id")\
    .mode("overwrite")\
    .saveAsTable("bucketed_large");

# Spark will shuffle both tables because of the UDF
(
    tableA.withColumn('x', my_udf('some_col'))
        .join(tableB, 'user_id')
)
# One-side shuffle-free join:
(
    tableA.withColumn('x', my_udf('some_col'))
        .repartition(50, 'user_id') # assuming we have 50 buckets
        .join(tableB, 'user_id')
)
# One-side shuffle-free join:
# set number of shuffle partitions to number of buckets (or less):
spark.conf.set('spark.sql.shuffle.partitions', 50)
(
    tableA.withColumn('x', my_udf('some_col'))
        .join(tableB, 'user_id')
)
