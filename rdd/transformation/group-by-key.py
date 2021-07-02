import utils.commons as commons
import sys
import re
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
    .appName("PythonRDD-GroupByKey") \
    .getOrCreate()

data = [
    ("James", "Sales", "NY", 90000, 34, 10000),
    ("Michael", "Sales", "NY", 86000, 56, 20000),
    ("Robert", "Sales", "CA", 81000, 30, 23000),
    ("Maria", "Finance", "CA", 90000, 24, 23000),
    ("Raman", "Finance", "CA", 99000, 40, 24000),
    ("Scott", "Finance", "NY", 83000, 36, 19000),
    ("Jen", "Finance", "NY", 79000, 53, 15000),
    ("Jeff", "Marketing", "CA", 80000, 25, 18000),
    ("Kumar", "Marketing", "NY", 91000, 50, 21000)
]

rdd_1 = spark.sparkContext.parallelize(data)
print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))

rdd_2 = rdd_1.map(lambda x: (x[1], x))
print(rdd_2.collect())

commons.print_separator()

rdd_3 = rdd_2.groupByKey()
print("RDD-3 Partition count after re-partitions is  : %i " % (rdd_3.getNumPartitions()))
#print(rdd_3.collect())

commons.print_separator()

rdd_4 = rdd_3.reduceByKey(lambda a, b: a[3] + b[3])
print(rdd_4.collect())

print("Details available at http://localhost:4040")
option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()

