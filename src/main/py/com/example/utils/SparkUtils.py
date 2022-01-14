from pyspark.sql import SparkSession


def getSparkSession(name=None, conf=None):
    #appName = name if name is None else ""
    spark = SparkSession.builder.appName(name).getOrCreate(conf=conf)
    spark.sparkContext.setLogLevel("WARN")
    return spark