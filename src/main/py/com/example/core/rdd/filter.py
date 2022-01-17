#
import sys
import com.example.utils.commons as commons
from pyspark.sql import SparkSession

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usages: spark-file <in-path> <out-path>")
        sys.exit(-1)


def m_filter(element):
    return element[4] > 30

#
spark = SparkSession \
    .builder \
    .master("spark://spark-master:7077")\
    .appName("PythonRDD-Filter") \
    .getOrCreate()

data = [
    ("James", "Sales", "NY", 90000, 34, 10000),
    ("Kenith", "Marketing", "CA", 66000, 36, 40000),
    ("Michael", "Sales", "NY", 86000, 56, 20000),
    ("Robert", "Sales", "CA", 81000, 30, 23000),
    ("Maria", "Finance", "CA", 90000, 24, 23000),
    ("Raman", "Finance", "CA", 99000, 40, 24000),
    ("Scott", "Finance", "NY", 83000, 36, 19000),
    ("Jen", "Finance", "NY", 79000, 53, 15000),
    ("Jeff", "Marketing", "CA", 80000, 25, 18000),
    ("Shelly", "Marketing", "NY", 60000, 15, 18000),
    ("Kumar", "Marketing", "NY", 91000, 50, 21000)
]

rdd_1 = spark.sparkContext.parallelize(data)
print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))
print("RDD-1 Record Count : %i " % (rdd_1.count()))

commons.print_separator()
rdd_2 = rdd_1.filter(lambda x: x[4] > 30)
print(rdd_2.collect())
print("RDD-2 Partition Count : %i " % (rdd_2.getNumPartitions()))
print("RDD-2 Record Count : %i " % (rdd_2.count()))

commons.print_separator()

rdd_3 = rdd_1.filter(m_filter)
print(rdd_3.collect())
print("RDD-3 Partition Count : %i " % (rdd_3.getNumPartitions()))
print("RDD-3 Record Count : %i " % (rdd_3.count()))

commons.print_separator()

print("Details available at http://localhost:4040")
#option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()

