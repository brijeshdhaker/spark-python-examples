import src.utils.commons as commons
#
from pyspark.sql import SparkSession

if __name__ == "__main__":
    #    if len(sys.argv) != 3:
    #        print("Usages: spark-file <inpath> <outpath>")
    #        sys.exit(-1)

    def f(partition_data):
        yield len(list(partition_data))


    #
    spark = SparkSession \
        .builder \
        .appName("PythonRDD-MapPartition") \
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

    rdd_3 = rdd_2.mapPartitions(f)
    print("RDD-3 Partition count after transformation is : %i " % (rdd_3.getNumPartitions()))
    print(rdd_3.collect())
#   print(rdd_3.glom().collect())

    commons.print_separator()

    print("Details available at http://localhost:4040")
    option = input("Do You Want to Kill Spark Job Process Y/N : ")
    #
    spark.stop()
