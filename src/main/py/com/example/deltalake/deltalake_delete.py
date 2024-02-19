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

    # Update Delta Lake table
    test_table = DeltaTable.forPath(spark, "/deltalake/test_table")

    # delete rows where id = 6
    test_table.delete(
        condition=expr("id == 6"))

    df = test_table.toDF()
    df.show()