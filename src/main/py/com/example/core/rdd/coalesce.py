#
from pyspark import SparkContext, SparkConf

#
conf = SparkConf().setAppName("SparkRDD-distinct").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf=conf)

data = list(range(0, 5000))

rdd_1 = sc.parallelize(data, 8)
print("RDD-1 Partition Count : %i " % (rdd_1.getNumPartitions()))
print("RDD-1 Record Count : %i " % (rdd_1.count()))

# To Reduce Partition Count
rdd_2 = rdd_1.coalesce(4)
print("RDD-2 Partition Count : %i " % (rdd_2.getNumPartitions()))
print("RDD-2 Record Count : %i " % (rdd_2.count()))

# print
# rdd_2.foreach(lambda x : print(x))

sc.stop()