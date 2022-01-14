import src.utils.commons as commons
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

conf = (
    SparkConf()
        .setAppName("Spark minIO Test")
        .set("spark.eventLog.enabled", "true")
        .set("spark.eventLog.dir", "file:///apps/hostpath/spark/logs/")
        .set("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000")
        .set("spark.hadoop.fs.s3a.access.key", "abc")
        .set("spark.hadoop.fs.s3a.secret.key", "xyzxyzxyz")
        .set("spark.hadoop.fs.s3a.path.style.access", True)
        .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
)

spark = SparkSession.builder.appName("Spark minIO Test").config(conf=conf).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

airlineSchema = StructType([
    StructField("id", IntegerType(), True),
    StructField("airlineName", StringType(),True),
    StructField("alias", StringType(),True),
    StructField("iataCode", StringType(), True),
    StructField("icaoCode", StringType(), True),
    StructField("callsign", StringType(), True),
    StructField("country", StringType(), True),
    StructField("active", StringType(), True)
])


airlinesWithSchema = spark.read.format("csv") \
    .option("header", False) \
    .option("delimiter", ',') \
    .schema(airlineSchema)\
    .load("s3a://word-count/flights-data/airlines.csv")

airlinesWithSchema.printSchema()
airlinesWithSchema.show()

#print(sc.wholeTextFiles('s3a://word-count/flights-data/airlines.csv').collect())