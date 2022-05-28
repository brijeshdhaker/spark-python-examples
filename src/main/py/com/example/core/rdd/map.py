#
import sys
import com.example.utils.commons as commons
from pyspark.sql import SparkSession

if __name__ == "__main__":

    if len(sys.argv) == 0:
        print("Usages: spark-file <inpath> <outpath>")
        sys.exit(-1)

    spark = SparkSession\
      .builder\
      .appName("PythonRDD-Map")\
      .getOrCreate()

    data = range(1, 101)
    rdd_1 = spark.sparkContext.parallelize(data, 2)
    print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))
    print("Values in RDD-1 : {0} ".format(rdd_1.collect()))

    commons.print_separator()

    rdd_2 = rdd_1.map(lambda x: (x, x*2))
    print("RDD-1 Partition Count : %i " % (rdd_2.getNumPartitions()))
    print("Values in RDD-2 : {0} ".format(rdd_2.collect()))

    print("Details available at http://localhost:4040")
    option = input("Do You Want to Kill Spark Job Process Y/N : ")

    spark.stop()