import sys
import com.example.utils.commons as commons
#
from pyspark.sql import SparkSession

if __name__ == "__main__":

    if len(sys.argv) == 0:
        print("Usages: spark-file <inpath> <outpath>")
        sys.exit(-1)

    spark = SparkSession.builder.appName("PythonRDD-Accumulator").getOrCreate()

    # Create Accumulator
    sc_acc = spark.sparkContext.accumulator(0)

    #
    data = range(1, 101)
    rdd_1 = spark.sparkContext.parallelize(data, 8)
    print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))
    print("Values in RDD-1 : {0} ".format(rdd_1.collect()))

    #
    # commons.print_separator()

    # Accessed By Driver
    rdd_1.foreach(lambda x: sc_acc.add(x))
    print("Total Sum  {0} ".format(sc_acc.value))

    print("Details available at http://localhost:4040")
#    option = input("Do You Want to Kill Spark Job Process Y/N : ")
    spark.stop()
