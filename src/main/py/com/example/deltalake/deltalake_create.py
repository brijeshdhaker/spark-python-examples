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

    # Create a DataFrame
    df = spark.range(1, 10)
    df = df.withColumn('value', lit('ABC'))
    df.show()

    # Save as delta table
    df.write.format('delta').save('/deltalake/test_table')