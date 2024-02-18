"""
This is the "front door" of your application which gets submitted
to Spark and serves as the starting point. If you needed to
implement a command-line inteface, for example, you'd invoke the
setup from here.
"""
import os
from pyspark.sql import SparkSession


# This is only needed for windows
def setEnv():

    # Replace with your Spark dir in windows
    os.environ['SPARK_HOME'] = '/opt/spark-3.1.2'
    os.environ['HADOOP_HOME'] = '/opt/hadoop-3.1.1'

    print(os.environ['SPARK_HOME'])


if __name__ == '__main__':

    # If running on windows , set env variables , for Linux skip
    if os.name == 'nt':
        setEnv()

    spark = (
        SparkSession.builder.master("local[*]").
            appName('Sample Spark Application').
            getOrCreate()
    )
    spark.sparkContext.setLogLevel('WARN')

    names = spark.createDataFrame(data=[(1000, 'Nick'), (1001, 'John'), (1002, 'Frank')], schema=['id', 'name'])
    names.select('id', 'name').show()
