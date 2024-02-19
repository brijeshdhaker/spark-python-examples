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

    # Create a staging DataFrame for merge.
    df_stg = spark.range(9, 15)
    df_stg = df_stg.withColumn('value', lit('EDF'))

    # Merge into test_table
    merge = test_table.alias('tgt').merge(df_stg.alias('src'),"src.id = tgt.id") \
        .whenMatchedUpdate(set={"value": col("src.value")}) \
        .whenNotMatchedInsert(values={"id": col("src.id"), "value": col("src.value")})
    merge.execute()

    df = test_table.toDF()
    df.show()