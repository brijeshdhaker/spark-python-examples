import src.utils.commons as commons
import sys
#
from pyspark.sql import SparkSession
from src.data.sampledata import t_student_marks

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usages: spark-file <in-path> <out-path>")
        sys.exit(-1)


# Defining Sequential Operation and Combiner Operations
# Sequence operation : Finding Maximum Marks from a single partition
# [U] => [V]
def seq_op(accumulator, element):
    if(accumulator > element[1]):
        return accumulator
    else:
        return element[1]


# Combiner Operation : Finding Maximum Marks out Partition-Wise Accumulators
# [U] op [U] => [U]
def comb_op(accumulator1, accumulator2):
    if(accumulator1 > accumulator2):
        return accumulator1
    else:
        return accumulator2


# Zero Value: Zero value in our case will be 0 as we are finding Maximum Marks
zero_val = 0

#
spark = SparkSession \
    .builder \
    .appName("PythonRDD-AggregateByKey") \
    .getOrCreate()

student_rdd = spark.sparkContext.parallelize(t_student_marks, 3)
commons.print_separator()
aggr_rdd = student_rdd.map(lambda t: (t[0], (t[1], t[2]))).aggregateByKey(zero_val, seq_op, comb_op)

# Check the Outout
for tpl in aggr_rdd.collect():
    print(tpl)


print("Details available at http://localhost:18080")
# option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()

