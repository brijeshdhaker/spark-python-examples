import sys
import com.example.utils.commons as commons
from com.example.data.sampledata import t_key_values
from pyspark.sql import SparkSession

#
if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usages: spark-file <in-path> <out-path>")
        sys.exit(-1)


def f(iterator):
    yield len(list(iterator))


def group_by_f(element):
    key = element[0]
    items = element[1]
    for e in items:
        print("Key :{key} and value is : {e}".format(key, e))


#
spark = SparkSession \
    .builder \
    .appName("PythonRDD-GroupByKey") \
    .getOrCreate()

rdd_1 = spark.sparkContext.parallelize(t_key_values)
print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))

commons.print_separator()

rdd_3 = rdd_1.groupByKey()
print("RDD-3 Partition count after re-partitions is  : %i " % (rdd_3.getNumPartitions()))
rdd_3.map(group_by_f)
#print(rdd_3.collect())



commons.print_separator()

print("Details available at http://localhost:4040")
#option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()

