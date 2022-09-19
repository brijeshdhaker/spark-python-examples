#
import com.example.utils.commons as commons
import sys
#
from pyspark.sql import SparkSession

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usages: spark-file <in-path> <out-path>")
        sys.exit(-1)

#
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("PythonRDD-AggregateByKey") \
    .getOrCreate()
spark.sparkContext.setLogLevel('WARN')

# Creating PairRDD student_rdd with key value pairs
t_student_marks = [
    ("Joseph", "Maths", 83),
    ("Joseph", "Physics", 74),
    ("Joseph", "Chemistry", 91),
    ("Joseph", "Biology", 82),
    ("Jimmy", "Maths", 69),
    ("Jimmy", "Physics", 62),
    ("Jimmy", "Chemistry", 97),
    ("Jimmy", "Biology", 80),
    ("Tina", "Maths", 78),
    ("Tina", "Physics", 73),
    ("Tina", "Chemistry", 68),
    ("Tina", "Biology", 87),
    ("Thomas", "Maths", 87),
    ("Thomas", "Physics", 93),
    ("Thomas", "Chemistry", 91),
    ("Thomas", "Biology", 74),
    ("Cory", "Maths", 56),
    ("Cory", "Physics", 65),
    ("Cory", "Chemistry", 71),
    ("Cory", "Biology", 68),
    ("Jackeline", "Maths", 86),
    ("Jackeline", "Physics", 62),
    ("Jackeline", "Chemistry", 75),
    ("Jackeline", "Biology", 83),
    ("Juan", "Maths", 63),
    ("Juan", "Physics", 69),
    ("Juan", "Chemistry", 64),
    ("Juan", "Biology", 60)
]

# Zero Value: Zero value in our case will be 0 as we are finding Maximum Marks
zero_val = 0

#
student_rdd = spark.sparkContext.parallelize(t_student_marks, 3)
for i in student_rdd.collect(): print(i)
commons.print_separator()

#
mapped_student_rdd = student_rdd.map(lambda t: (t[0], (t[1], t[2])))
for i in mapped_student_rdd.collect(): print(i)
commons.print_separator()

#
print(" Max Aggregation Results : ")
# Sequence operation : Finding Maximum Marks from a single partition
# [U] => [V]
# Sequence operation for aggregation
def seq_max(accumulator, element):
    # accumulator if accumulator < element[1] else element[1]
    if accumulator > element[1]:
        return accumulator
    else:
        return element[1]

# Defining Sequential Operation and Combiner Operations
# Combiner Operation : Finding Maximum Marks out Partition-Wise Accumulators
# [U] op [U] => [U]
# Reduce/Combine operation for max aggregation#
def comb_max(accumulator1, accumulator2):
    return max(accumulator1, accumulator2)


maxRDD = mapped_student_rdd.aggregateByKey(0, seq_max, comb_max)
for e in maxRDD.collect(): print(e)
commons.print_separator()

#
print(" Sum Aggregation Results : ")
# Defining Sequential Operation and Combiner Operations
# Sequence operation for aggregation
def seq_agg(accumulator, element):
    return accumulator + element[1]


# Reduce/Combine operation for max aggregation#
def comb_agg(accumulator1, accumulator2):
    return accumulator1 + accumulator2

aggRDD = mapped_student_rdd.aggregateByKey(0, seq_max, comb_max)
for e in aggRDD.collect(): print(e)

print("Details available at http://localhost:18080")
# option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()
