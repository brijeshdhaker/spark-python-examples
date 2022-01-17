#
import sys
import re
#
from pyspark.sql import SparkSession

if __name__ == "__main__":

    #    if len(sys.argv) != 3:
    #        print("Usages: spark-file <inpath> <outpath>")
    #        sys.exit(-1)

    #
    #
    #
    def f(partitionIndex, iterator):
        yield (partitionIndex, len(list(iterator)))


    #        yield (partitionIndex, sum(1 for _ in iterator))
    #
    spark = SparkSession.builder.appName("PythonRDD-MapPartitionWithIndex").master("local[*]").getOrCreate()

    #    data = range(1, 100)
    data = list(range(1, 100))
    rdd_1 = spark.sparkContext.parallelize(data, 4)
    print("Records Count : %i " % (rdd_1.getNumPartitions()))

    rdd_2 = rdd_1.mapPartitionsWithIndex(f)
    print(rdd_2.collect())
    #
    spark.stop()
