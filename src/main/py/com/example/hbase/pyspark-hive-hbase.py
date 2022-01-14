#
#
#

from pyspark.sql import SparkSession

#
#
#
spark = SparkSession \
    .builder \
    .appName("Read HBase Table using PySpark Demo") \
    .config("spark.jars", "file:///opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hive/lib/hive-hbase-handler-2.1.1-cdh6.3.2.jar") \
    .config("spark.executor.extraClassPath", "file:///opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hive/lib/hive-hbase-handler-2.1.1-cdh6.3.2.jar") \
    .config("spark.executor.extraLibrary", "file:///opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hive/lib/hive-hbase-handler-2.1.1-cdh6.3.2.jar") \
    .config("spark.driver.extraClassPath", "file:///opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hive/lib/hive-hbase-handler-2.1.1-cdh6.3.2.jar") \
    .enableHiveSupport()\
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print(spark.sparkContext.appName)

#
transaction_detail_df = spark.sql("use default")
transaction_detail_df = spark.sql("select * from transaction_detail_hive_tbl")

# transaction_detail_df = spark.sql("select * from default.transaction_detail_hive_tbl")
transaction_detail_df.printSchema()

transaction_detail_df.show(2, False)
transaction_detail_df.count()

transaction_detail_df_stg1 = transaction_detail_df.select("transaction_card_type", "transaction_country_name", "transaction_amount")
transaction_detail_df_stg1.show(20, False)

transaction_detail_df_stg1.groupby('transaction_card_type').agg({'transaction_amount': 'sum'}).show()
spark.stop()
