import sys
import re
#
from pyspark.sql import SparkSession

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usages: spark-file <inpath> <outpath>")
        sys.exit(-1)

    def applyFunction(x):
        splits = re.split(r",", x)
        return splits[1] + ", " + splits[6]

    def applyFilter(x):
        f = re.split(r",(?![^(]*?\))\s*", x)[6]
        try:
            y = float(f)
        except ValueError:
            return False
        else:
            if y > 40:
                return True
            else:
                return False

    spark = SparkSession\
      .builder\
      .appName("PythonSpark")\
      .getOrCreate()

#   lines = spark.read.text("file:///apps/hostpath/spark/in/airports.text").rdd
    lines = spark.sparkContext.textFile("file:///apps/hostpath/spark/in/airports.text")

    print("Partition Size : " + str(lines.getNumPartitions()))
    filtered_data = lines.filter(lambda x: applyFilter(x))
    results = filtered_data.map(lambda x: applyFunction(x))
    results.foreach(lambda x: print(x))
    total = results.count()
#    print("Records Count : " + str(total))
    print("Records Count : %i " % (total))
#
    spark.stop()
