
"""
This is the "front door" of your application which gets submitted
to Spark and serves as the starting point. If you needed to
implement a command-line inteface, for example, you'd invoke the
setup from here.
"""
import pyspark
import jellyfish
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf

if __name__ == '__main__':
  spark = (
    pyspark.sql.SparkSession.builder.master("local[*]")
      # This doesn't seem to have an impact on YARN.
      # Use `spark-submit --name` instead.
      # .appName('Sample Spark Application')
      .getOrCreate())
  spark.sparkContext.setLogLevel('WARN')


  def metaphone(str):
    return jellyfish.metaphone(str)

  metaphone_udf = udf(metaphone, StringType())

  names = (
    spark.createDataFrame(
      data=[
        ('Nick',),
        ('John',),
        ('Frank',),
      ],
      schema=['name']
    ))
  names.select('name', metaphone_udf('name')).show()