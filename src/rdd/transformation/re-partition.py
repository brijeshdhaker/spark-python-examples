import src.utils.commons as commons
import sys
#
from pyspark.sql import SparkSession

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usages: spark-file <in-path> <out-path>")
        sys.exit(-1)


def f(iterator):
    yield len(list(iterator))


    #


spark = SparkSession \
    .builder \
    .appName("PythonRDD-Repartition") \
    .getOrCreate()

data = list(range(1, 101))
rdd_1 = spark.sparkContext.parallelize(data, 2)
print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))
print(rdd_1.collect())

commons.print_separator()

rdd_2 = rdd_1.repartition(4)
print("RDD-2 Partition count after re-partitions is  : %i " % (rdd_2.getNumPartitions()))
print(rdd_2.collect())

commons.print_separator()

print("Details available at http://localhost:4040")
option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()
