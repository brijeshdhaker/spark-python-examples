import src.utils.commons as commons
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

#
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("PythonSQL-StructType") \
    .getOrCreate()

#
data = [("James", "", "Smith", "36636", "M", 3000),
        ("Michael", "Rose", "", "40288", "M", 4000),
        ("Robert", "", "Williams", "42114", "M", 4000),
        ("Maria", "Anne", "Jones", "39192", "F", 4000),
        ("Jen", "Mary", "Brown", "", "F", -1)
        ]

schema = StructType([ \
    StructField("firstname", StringType(), True), \
    StructField("middlename", StringType(), True), \
    StructField("lastname", StringType(), True), \
    StructField("id", StringType(), True), \
    StructField("gender", StringType(), True), \
    StructField("salary", IntegerType(), True) \
    ])

df = spark.createDataFrame(data=data, schema=schema)
df.printSchema()
df.show(truncate=False)

commons.print_separator()

structureData = [
    (("James", "", "Smith"), "36636", "M", 3100),
    (("Michael", "Rose", ""), "40288", "M", 4300),
    (("Robert", "", "Williams"), "42114", "M", 1400),
    (("Brijesh", "K", "Dhaker"), "400706", "M", 3000),
    (("Maria", "Anne", "Jones"), "39192", "F", 5500),
    (("Jen", "Mary", "Brown"), "", "F", -1)
]
structureSchema = StructType([
    StructField('name', StructType([
        StructField('firstname', StringType(), True),
        StructField('middlename', StringType(), True),
        StructField('lastname', StringType(), True)
    ])),
    StructField('id', StringType(), True),
    StructField('gender', StringType(), True),
    StructField('salary', IntegerType(), True)
])

df2 = spark.createDataFrame(data=structureData, schema=structureSchema)
df2.printSchema()
df2.show(truncate=False)

commons.print_separator()

from pyspark.sql.functions import col,struct,when

updatedDF = df2.withColumn("OtherInfo",
                           struct(col("id").alias("identifier"),
                                  col("gender").alias("gender"),
                                  col("salary").alias("salary"),
                                  when(col("salary").cast(IntegerType()) < 2000, "Low")
                                  .when(col("salary").cast(IntegerType()) < 4000, "Medium")
                                  .otherwise("High").alias("Salary_Grade")
                           )).drop("id", "gender", "salary")

updatedDF.printSchema()
updatedDF.show(truncate=False)

print("Details available at http://localhost:18080")
# option = input("Do You Want to Kill Spark Job Process Y/N : ")
#
spark.stop()
