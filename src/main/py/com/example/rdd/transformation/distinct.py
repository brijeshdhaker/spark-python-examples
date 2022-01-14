#
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("SparkRDD-distinct").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf=conf)

data = ["Learn", "Apache", "Spark", "Learn", "Spark", "RDD", "Functions"]

rdd_1 = sc.parallelize(data)
print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))
print("RDD-1 Record Count : %i " % (rdd_1.count()))

rdd_2 = rdd_1.distinct()
print("RDD-2 Partition Count : %i " % (rdd_2.getNumPartitions()))
print("RDD-2 Record Count : %i " % (rdd_2.count()))

# print
for e in rdd_2.collect(): print(e)

#
sc.stop()