import sys
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import *


# create Spark context with Spark configuration
spark = SparkSession \
    .builder \
    .appName("PySpark Window Functions") \
    .enableHiveSupport() \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Create Data Frame From Hive table
dataset = [
    ("Thin",       "cell phone", 6000),
    ("Normal",     "tablet",     1500),
    ("Mini",       "tablet",     5500),
    ("Ultra thin", "cell phone", 5000),
    ("Very thin",  "cell phone", 6000),
    ("Big",        "tablet",     2500),
    ("Bendable",   "cell phone", 3000),
    ("Foldable",   "cell phone", 3000),
    ("Pro",        "tablet",     4500),
    ("Pro2",       "tablet",     6500)
]

df = spark.createDataFrame(dataset, ["category", "product",  "revenue"])
df.show()

windowSpec = Window.partitionBy(df['category']).orderBy(df['revenue'].desc())

""" cume_dist """
from pyspark.sql.functions import cume_dist
df.withColumn("cume_dist", cume_dist().over(windowSpec)).show()

"""lag"""
from pyspark.sql.functions import lag
df.withColumn("lag", lag("revenue", 2).over(windowSpec)).show()

"""lead"""
from pyspark.sql.functions import lead
df.withColumn("lead", lead("revenue", 2).over(windowSpec)).show()

#
spark.stop()