#
from pyspark.sql import SparkSession
import pyspark.sql.functions as fn
from pyspark.sql.types import StringType

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("pyspark-schema-merge") \
    .getOrCreate()

print("Schema Without Merge : ")
df_1 = spark.read.parquet("file:///home/brijeshdhaker/IdeaProjects/pyspark-schema-merge/data/employee-*.parquet")
df_1.show()


print("Schema With Merge : ")
df_2 = spark.read.option("mergeSchema", True).parquet("file:///home/brijeshdhaker/IdeaProjects/pyspark-schema-merge/data/employee-*.parquet")
df_2.show()

spark.stop()