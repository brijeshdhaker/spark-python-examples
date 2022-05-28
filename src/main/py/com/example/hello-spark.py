
"""
This is the "front door" of your application which gets submitted
to Spark and serves as the starting point. If you needed to
implement a command-line inteface, for example, you'd invoke the
setup from here.
"""
from pyspark.sql import SparkSession

if __name__ == '__main__':

  spark = (
    SparkSession.builder.master("local[*]").
      appName('Sample Spark Application').
      getOrCreate()
  )
  spark.sparkContext.setLogLevel('WARN')

  names = spark.createDataFrame(data=[(1000, 'Nick'), (1001, 'John'), (1002, 'Frank')], schema=['id', 'name'])
  names.select('id', 'name').show()
