#
#
#
from pyspark import SparkContext, SparkConf, HiveContext

if __name__ == "__main__":

    # create Spark context with Spark configuration
    conf = SparkConf().setAppName("Hive Context Data Frame Join")
    conf.set("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse")

    #
    sc = SparkContext(conf=conf)
    sqlContext = HiveContext(sc)

    #
    df_07 = sqlContext.sql("SELECT * from sample_07")
    df_07.filter(df_07.salary > 150000).show()

    #
    df_08 = sqlContext.sql("SELECT * from sample_08")
    tbls = sqlContext.sql("show tables")
    tbls.show()

    #
    df_09 = df_07.join(df_08, df_07.code == df_08.code).select(df_07.code, df_07.description)
    df_09.show()

    #
    df_09.write.saveAsTable("sample_09")
    tbls = sqlContext.sql("show tables")
    tbls.show()
