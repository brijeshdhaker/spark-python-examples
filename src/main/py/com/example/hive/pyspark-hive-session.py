from pyspark.sql import SparkSession
#
#
#
if __name__ == "__main__":

    # create Spark context with Spark configuration
    spark = SparkSession \
        .builder \
        .appName("Hive Session Data Frame Join") \
        .enableHiveSupport() \
        .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse") \
        .getOrCreate()

    print(spark.sparkContext.appName)

    #
    spark.sql("show tables").show()

    #
    transactionDF = spark.sql("SELECT * from transaction_details")
    transactionDF.printSchema()
    transactionDF.filter(transactionDF.amount > 10000).show()

    #
    #df_08 = spark.sql("SELECT * from sample_08")
    #tbls = spark.sql("show tables")
    #tbls.show()

    #
    #df_09 = df_07.join(df_08, df_07.code == df_08.code).select(df_07.code, df_07.description)
    #df_09.show()

    #
    #df_09.write.saveAsTable("sample_09")
    #tbls = spark.sql("show tables")
    #tbls.show()
