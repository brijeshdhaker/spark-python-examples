import src.utils.commons as commons
from pyspark.sql import SparkSession

conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)

spark = SparkSession\
    .builder\
    .master("local[*]")\
    .appName("")\
    .getOrCreate()

spark.sparkContext.setLogLevel('WARN')