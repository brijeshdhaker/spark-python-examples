#
#
#
from pyspark import SparkConf, SparkContext


#
#
#
sparkconf = SparkConf.setAppName("PySpark : Broadcast ").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf=sparkconf)
broadcastVar = sc.broadcast([1, 2, 3])
print("{}".format(broadcastVar.value))
