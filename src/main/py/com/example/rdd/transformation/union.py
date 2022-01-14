#
import sys
import com.example.utils.commons as commons
from pyspark.sql import SparkSession

#
if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usages: spark-file <in-path> <out-path>")
        sys.exit(-1)

#
spark = SparkSession \
    .builder \
    .appName("PythonRDD-Union") \
    .getOrCreate()

data_1 = [
    ("James", "Sales", "NY", 90000, 34, 10000),
    ("Michael", "Sales", "NY", 86000, 56, 20000),
    ("Robert", "Sales", "CA", 81000, 30, 23000),
    ("Maria", "Finance", "CA", 90000, 24, 23000),
    ("Raman", "Finance", "CA", 99000, 40, 24000)
]

data_2 = [
    ("Scott", "Finance", "NY", 83000, 36, 19000),
    ("Jen", "Finance", "NY", 79000, 53, 15000),
    ("Jeff", "Marketing", "CA", 80000, 25, 18000),
    ("Kumar", "Marketing", "NY", 91000, 50, 21000)
]

rdd_1 = spark.sparkContext.parallelize(data_1)
print("RDD-1 Record Count : %i " % (rdd_1.count()))

commons.print_separator()

rdd_2 = spark.sparkContext.parallelize(data_2)
print("RDD-2 Record Count : %i " % (rdd_2.count()))

commons.print_separator()

rdd_3 = rdd_1.union(rdd_2)
print(rdd_3.collect())
print("RDD-3 Record Count : %i " % (rdd_3.count()))

commons.print_separator()

print("Details available at http://localhost:4040")
option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()

