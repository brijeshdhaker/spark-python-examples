#
#
#
from pyspark import SparkConf, SparkContext


#
#
#
sparkconf = SparkConf.setAppName("PySpark : Broadcast ").setMaster("local[4]")
sc = SparkContext.getOrCreate(conf=sparkconf)

states = {"NY": "New York", "IL": "Illinois", "CA": "California"}
broadcastVar = sc.broadcast(states)

data = [
    ("John", "Software Engineer", "CA"),
    ("Jerry", "Project Manager", "IL"),
    ("Emily", "Developer", "NY")
]

print("{}".format(broadcastVar.value))
