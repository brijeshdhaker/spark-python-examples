import findspark
findspark.init('/apps/spark')
import pyspark
import random

odd = []
even = []
def disFun(val):
    if(val/2 == 0):
        odd.append(val)
        return odd
    else:
        even.append(val)
        return even

sc = pyspark.SparkContext(appName="spark-rdd")
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rdd_1 = sc.parallelize(data, 2)
ps = rdd_1.getNumPartitions()
print("Partition Size : " + str(ps))
rdd_2 = rdd_1.map(lambda x: x+2)
# rdd_2.foreach(lambda x: print(x))
rdd_3 = rdd_2.flatMap(lambda x: disFun(x))
rdd_3.foreach(lambda x: print(x))
sc.stop()

