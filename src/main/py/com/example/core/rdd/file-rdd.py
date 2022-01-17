import math
import re
import pyspark

COMMA_DELIMITER = ',(?=([^"]*"[^"]*")*[^"]*$)'

def myFun(x):
    splits = re.split(r",", x)
    return splits[1]+", "+splits[6]

def myFilter(x):
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


sc = pyspark.SparkContext(appName="spark-rdd")

rdd_1 = sc.textFile("file:///apps/hostpath/datasets/airports.text")
ps = rdd_1.getNumPartitions()
print("Partition Size : " + str(ps))
# rdd_2 = rdd_1.map(lambda x: x.replace('"', ''))
rdd_3 = rdd_1.filter(lambda x: myFilter(x))
rdd_4 = rdd_3.map(lambda x: myFun(x))
for e in rdd_4.collect(): print(e)

total = rdd_4.count()
print(total)
sc.stop()

