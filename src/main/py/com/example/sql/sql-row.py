import com.example.utils.commons as commons
from pyspark.sql import SparkSession, Row


spark = SparkSession.builder.master("local[*]").appName("PythonSQL-ROW").getOrCreate()

data = [
        Row(name="James,,Smith", lang=["Java", "Scala", "C++"], state="CA"),
        Row(name="Michael,Rose,", lang=["Spark", "Java", "C++"], state="NJ"),
        Row(name="Robert,,Williams", lang=["CSharp", "VB"], state="NV")
]

rdd = spark.sparkContext.parallelize(data)
collData = rdd.collect()

print(collData)

for row in collData:
    print(row.name + "," +str(row.lang))


#DataFrame Example 1
columns = ["name", "languagesAtSchool", "currentState"]
df1 = spark.createDataFrame(data)
df1.printSchema()
df1.show()

collData=df1.collect()
print(collData)
for row in collData: print(row.name + "," +str(row.lang))

commons.print_separator()

#DataFrame Example 2

columns = ["name", "languagesAtSchool", "currentState"]
df2 = spark.createDataFrame(data).toDF(*columns)
df2.printSchema()
df2.show()

print("Details available at http://localhost:18080")
# option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()