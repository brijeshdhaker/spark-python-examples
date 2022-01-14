#
# Importing Python Related Packages
import time
from pyspark.sql import SparkSession

#
if __name__ == "__main__":
    print("PySpark Examples")

    # reduceByKey - Merge the values for each key using an associative and commutative reduce function.
    # This will also perform the merging locally on each mapper before sending results to a reducer, similarly to a combiner in MapReduce.

    # Why reduceByKey RDD transformation is preferred instead of groupByKey in PySpark | PySpark 101
    spark = SparkSession \
        .builder \
        .appName("PythonRDD-ReduceByKey") \
        .master("local[*]") \
        .enableHiveSupport() \
        .getOrCreate()

    str_list = ["Three", "Five", "One", "Five", "One"]
    print("Printing str_list: ")
    print(str_list)

    str_rdd = spark.sparkContext.parallelize(str_list, 3)

    print("Get Partition Count: ")
    print(str_rdd.getNumPartitions())

    kv_rdd = str_rdd.map(lambda e: (e, 1)).reduceByKey(lambda a, b: a + b)

    print(kv_rdd.collect())

    print("Printing current datetime - 1: ")
    print(time.strftime("%Y-%m-%D %H:%M:%S"))

    '''
    input_file_path = "/data/input/kv_pair_data/words_datagen.txt"
    lines_rdd = spark.sparkContext.textFile(input_file_path)
    words_rdd = lines_rdd.flatMap(lambda e: e.split(','))
    words_kv_pair_rdd = words_rdd.map(lambda e: (e, 1))

    results_kv_rdd = words_kv_pair_rdd.reduceByKey(lambda x, y: x + y)
    print(results_kv_rdd.collect())
    '''


    print("Printing current datetime - 2: ")
    print(time.strftime("%Y-%m-%D %H:%M:%S"))

    print("Please wait for 10 minutes before stopping SparkSession object ... ")
    time.sleep(600)
    print(time.strftime("%Y-%m-%D %H:%M:%S"))
    print("Stopping the SparkSession object")

    spark.stop()
