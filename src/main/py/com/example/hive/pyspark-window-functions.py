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


# Create Data Frame From Hive table
dataFrame = spark.table("PRODUCT_REVENUE")
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