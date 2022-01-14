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

dataFrame = spark.createDataFrame(dataset, ["category", "product",  "revenue"])
dataFrame.show()


windowSpec = Window.partitionBy(dataFrame['category']).orderBy(dataFrame['revenue'].desc())
#from pyspark.sql.functions import row_number, rank
#reveDiff = "max(dataFrame.revenue).over(windowSpec) - dataFrame.revenue"

dataFrame.withColumn("revenue_diff", max(col("revenue")).over(windowSpec) - dataFrame['revenue']).show(truncate=False)

# ROW_NUMBER
dataFrame.withColumn("row_number", row_number().over(windowSpec)) \
    .show(truncate=False)

# RANK
dataFrame.withColumn("rank", rank().over(windowSpec)) \
    .show(truncate=False)

"""dens_rank"""
dataFrame.withColumn("dense_rank", dense_rank().over(windowSpec)) \
    .show()

""" percent_rank """
dataFrame.withColumn("percent_rank", percent_rank().over(windowSpec)) \
    .show()

""" Aggregate Functions """
dataFrame.withColumn("row", row_number().over(windowSpec)) \
    .withColumn("avg", avg(col("revenue")).over(windowSpec)) \
    .withColumn("sum", sum(col("revenue")).over(windowSpec)) \
    .withColumn("min", min(col("revenue")).over(windowSpec)) \
    .withColumn("max", max(col("revenue")).over(windowSpec)) \
    .where(col("row") == 1).select("category", "avg", "sum", "min", "max") \
    .show()

#
spark.stop()