#
#
from pyspark import SparkConf, SparkContext
import com.example.utils.commons as commons
#

sparkconf = SparkConf().setAppName("PySpark-Test").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf=sparkconf)
sc.setLogLevel('WARN')

#
#
print("Spark Version : " + sc.version)

#
#
rawdata = [
    ('i100121', ('Math', 990)),
    ('i100121', ('English', 890)),
    ('i100121', ('Hindi', 789)),
    ('i100121', ('Science', 995)),
    ('i100122', ('Math', 890)),
    ('i100122', ('English', 790)),
    ('i100122', ('Hindi', 795)),
    ('i100122', ('Science', 985))
]

rdd = sc.parallelize(rawdata, 2)
for e in rdd.collect(): print(e)

commons.print_separator()
print(" Max Aggregation Results : ")
# Sequence operation for aggregation
def seq_max(accumulator, element):
    if accumulator > element[1]:
        return accumulator
    else:
        return element[1]


# Reduce/Combine operation for max aggregation#
def comb_max(accumulator1, accumulator2):
    return max(accumulator1, accumulator2)


maxRDD = rdd.aggregateByKey(0, seq_max, comb_max)
for e in maxRDD.collect(): print(e)


#
#
#
commons.print_separator()
print(" Sum Aggregation Results : ")
# Sequence operation for aggregation
def seq_max(accumulator, element):
    return accumulator + element[1]


# Reduce/Combine operation for max aggregation#
def comb_max(accumulator1, accumulator2):
    return accumulator1 + accumulator2

aggRDD = rdd.aggregateByKey(0, seq_max, comb_max)
for e in aggRDD.collect(): print(e)