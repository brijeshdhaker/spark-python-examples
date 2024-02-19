from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from delta import *

if __name__ == "__main__":
    app_name = "PySpark Delta Lake Example"
    master = "local"

    # Create Spark session with Delta extension

    builder = SparkSession.builder.appName(app_name) \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .master(master)

    spark = builder.getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # Read from Delta Lake table (the latest version)
    df = spark.read.format('delta').load("/deltalake/test_table")
    df.show()

    # Read version 1
    df_v1 = spark.read.format('delta').option('versionAsOf', 1).load("/deltalake/test_table")
    df_v1.show()