#
import com.example.utils.commons as commons
import sys
#
from pyspark.sql import SparkSession
from com.example.data.sampledata import t_key_values

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usages: spark-file <in-path> <out-path>")
        sys.exit(-1)

#
spark = SparkSession \
    .builder \
    .appName("PythonRDD-SortByKey") \
    .getOrCreate()

rdd_1 = spark.sparkContext.parallelize(t_key_values)
print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))
print("Values in RDD-1 : {0} ".format(rdd_1.collect()))

commons.print_separator()

#
rdd_2 = rdd_1.sortByKey(True)
print("Values in RDD-2 : {0} ".format(rdd_2.collect()))


print("Details available at http://localhost:18080")
option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()

