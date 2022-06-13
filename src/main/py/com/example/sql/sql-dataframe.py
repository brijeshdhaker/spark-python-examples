import com.example.utils.commons as commons
import sys
#
from pyspark import SparkConf
from pyspark.sql import SparkSession
from com.example.data.sampledata import t_r_data
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, BooleanType

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usages: spark-file <in-path> <out-path>")
        sys.exit(-1)

conf = SparkConf() \
    .set("spark.eventLog.enabled", "true") \
    .set("spark.eventLog.dir", "file:///apps/hostpath/spark/logs/")

#
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("PysparkSQL-DataFrame") \
    .config(conf=conf) \
    .getOrCreate()

cloumns = ["name", "department", "State", "Salary", "Age", "Bonus"]

rdd = spark.sparkContext.parallelize(t_r_data);
print("Partitioner :: " + str(rdd.partitioner))
rddDF = rdd.toDF(cloumns)
rddDF.printSchema()
rddDF.show()

commons.print_separator()

employeeDF = spark.createDataFrame(t_r_data, cloumns)
employeeDF.printSchema()
employeeDF.show()

commons.print_separator()

schema = StructType([ \
    StructField("name", StringType(), True), \
    StructField("department", StringType(), True), \
    StructField("State", StringType(), True), \
    StructField("Salary", IntegerType(), True), \
    StructField("Age", IntegerType(), True), \
    StructField("Bonus", IntegerType(), True) \
    ])

dfFromSchema = spark.createDataFrame(data=t_r_data, schema=schema)
dfFromSchema.printSchema()
dfFromSchema.show(truncate=False)

commons.print_separator()

dfFromCSV = spark.read \
    .option("header", True) \
    .option("delimiter", ',') \
    .options(inferSchema='True', delimiter=',') \
    .csv("hdfs://namenode:9000/datasets/zipcodes.csv")
dfFromCSV.printSchema()
dfFromCSV.show(truncate=False)

commons.print_separator()

dfFromJSON = spark.read.json("hdfs://namenode:9000/datasets/people.json")
dfFromJSON.printSchema()
dfFromJSON.show(truncate=False)

commons.print_separator()
print(" User Defined ")
commons.print_separator()

uschema = StructType() \
    .add("RecordNumber", IntegerType(), True) \
    .add("Zipcode", IntegerType(), True) \
    .add("ZipCodeType", StringType(), True) \
    .add("City", StringType(), True) \
    .add("State", StringType(), True) \
    .add("LocationType", StringType(), True) \
    .add("Lat", DoubleType(), True) \
    .add("Long", DoubleType(), True) \
    .add("Xaxis", IntegerType(), True) \
    .add("Yaxis", DoubleType(), True) \
    .add("Zaxis", DoubleType(), True) \
    .add("WorldRegion", StringType(), True) \
    .add("Country", StringType(), True) \
    .add("LocationText", StringType(), True) \
    .add("Location", StringType(), True) \
    .add("Decommisioned", BooleanType(), True) \
    .add("TaxReturnsFiled", StringType(), True) \
    .add("EstimatedPopulation", IntegerType(), True) \
    .add("TotalWages", IntegerType(), True) \
    .add("Notes", StringType(), True)

df_with_schema = spark.read.format("csv") \
    .option("header", True) \
    .schema(uschema) \
    .load("hdfs://namenode:9000/datasets/zipcodes.csv")

df_with_schema.printSchema()
df_with_schema.show(truncate=False)

print("Details available at http://localhost:18080")
# option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()
