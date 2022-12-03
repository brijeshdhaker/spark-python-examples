#
import sys
from pyspark.sql import SparkSession

if __name__ == "__main__":

    if len(sys.argv) == 0:
        print("Usages: spark-file <in-path> <out-path>")
        sys.exit(-1)

    def print_separator():
        print(" " * 30)
        print(" #" * 30)
        print(" " * 30)

    def flatMapFun(x):
        l = []
        for e in x[1]:
            l.append((x[0], e))
        return l

    spark = SparkSession\
      .builder\
      .appName("PythonRDD-FlatMap")\
      .getOrCreate()

    data = [
        (1, ['A', 'B', 'C']),
        (2, ['D', 'E', 'F']),
        (3, ['G', 'H', 'I']),
        (4, ['J', 'K', 'L']),
        (5, ['M', 'N', 'O']),
        (6, ['P', 'Q', 'R']),
        (7, ['S', 'T', 'U']),
        (8, ['V', 'W', 'X']),
        (9, ['Y', 'Z', 'A']),
        (10, ['B', 'C', 'D'])
    ]

    rdd_1 = spark.sparkContext.parallelize(data, 2)
    print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))
    print("RDD-1 Record Count : %i " % (rdd_1.count()))
    print(rdd_1.collect())

    print_separator()

    rdd_2 = rdd_1.flatMap(flatMapFun, False)
    print("RDD-2 Partition Count : %i " % (rdd_2.getNumPartitions()))
    print("RDD-2 Record Count : %i " % (rdd_2.count()))
    print(rdd_2.collect())

    print_separator()

    rdd_3 = rdd_1.flatMap(lambda x: (x[0], x[0]**2, x[0]*10))
    print("RDD-2 Partition Count : %i " % (rdd_3.getNumPartitions()))
    print("RDD-2 Record Count : %i " % (rdd_3.count()))
    print(rdd_3.collect())

    print_separator()

    # print("Details available at http://localhost:4040")
    # option = input("Do You Want to Kill Spark Job Process Y/N : ")

    spark.stop()