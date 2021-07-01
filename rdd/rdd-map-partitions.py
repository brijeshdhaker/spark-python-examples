import sys
import re
#
from pyspark.sql import SparkSession

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usages: spark-file <inpath> <outpath>")
        sys.exit(-1)

    def f(iterator):
        yield sum(iterator)
#

    spark = SparkSession\
      .builder\
      .appName("PythonSpark")\
      .getOrCreate()

    data = range(1, 100)
    rdd_1 = spark.sparkContext.parallelize(data, 2)
    print("Records Count : %i " % (rdd_1.getNumPartitions()))

    rdd_2 = rdd_1.repartition(4)
    print("Partition count after re-partitions is  : %i " % (rdd_2.getNumPartitions()))

    rdd_3 = rdd_2.mapPartitions(f)
    print(rdd_3.collect())
#
    spark.stop()