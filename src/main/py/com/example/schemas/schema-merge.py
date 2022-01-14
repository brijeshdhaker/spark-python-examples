#
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("pyspark-schema-merge") \
    .getOrCreate()

spark.sparkContext.setLogLevel('WARN')

print("Schema Version - 1 : ")
df_v1 = spark.read.parquet("file:///home/brijeshdhaker/IdeaProjects/spark-bigdata-examples/data/employee-v1.parquet")
df_v1.show()

print("Schema Version - 2 : ")
df_v2 = spark.read.parquet("file:///home/brijeshdhaker/IdeaProjects/spark-bigdata-examples/data/employee-v2.parquet")
df_v2.show()

print("Schema Version - 3 : ")
df_v3 = spark.read.parquet("file:///home/brijeshdhaker/IdeaProjects/spark-bigdata-examples/data/employee-v3.parquet")
df_v3.show()

print("Schema Without Merge : ")
df_1 = spark.read.parquet("file:///home/brijeshdhaker/IdeaProjects/spark-bigdata-examples/data/employee-*.parquet")
df_1.show()

print("Schema With Merge : ")
df_2 = spark.read.option("mergeSchema", True).parquet("file:///home/brijeshdhaker/IdeaProjects/spark-bigdata-examples/data/employee-*.parquet")
df_2.show()

spark.stop()