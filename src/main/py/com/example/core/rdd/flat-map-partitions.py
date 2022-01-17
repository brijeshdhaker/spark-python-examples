import sys
import com.example.utils.commons as commons
#
from pyspark.sql import SparkSession

if __name__ == "__main__":

    if len(sys.argv) == 0:
        print("Usages: spark-file <in-path> <out-path>")
        sys.exit(-1)

    def flatMapFun(x):
        return x[1]

    spark = SparkSession\
      .builder\
      .appName("PythonRDD-FlatMap")\
      .getOrCreate()

    data = [
        (1, ['A', 'B', 'C']),
        (2, ['A', 'B', 'C']),
        (3, ['A', 'B', 'C']),
        (4, ['A', 'B', 'C']),
        (5, ['A', 'B', 'C']),
        (6, ['A', 'B', 'C']),
        (7, ['A', 'B', 'C']),
        (8, ['A', 'B', 'C']),
        (9, ['A', 'B', 'C']),
        (10, ['A', 'B', 'C'])
    ]

    rdd_1 = spark.sparkContext.parallelize(data, 2)
    print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))
    print("RDD-1 Record Count : %i " % (rdd_1.count()))
    print(rdd_1.collect())

    commons.print_separator()

    rdd_2 = rdd_1.flatMap(flatMapFun, False)
    print("RDD-2 Partition Count : %i " % (rdd_2.getNumPartitions()))
    print("RDD-2 Record Count : %i " % (rdd_2.count()))
    print(rdd_2.collect())

    print("Details available at http://localhost:4040")
    option = input("Do You Want to Kill Spark Job Process Y/N : ")

    spark.stop()