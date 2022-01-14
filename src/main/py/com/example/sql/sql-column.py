import com.example.utils.commons as commons
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col


conf = SparkConf()\
        .set("spark.eventLog.enabled", "true") \
        .set("spark.eventLog.dir", "file:///apps/hostpath/spark/logs/")

spark = SparkSession\
    .builder\
    .master("local[*]")\
    .appName("PysparkSQL-Columns") \
    .config(conf=conf) \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

colObj = lit("sparkbyexamples.com")
print(type(colObj))

data = [("James", 23), ("Ann", 40)]
df = spark.createDataFrame(data).toDF("name.fname", "gender")
df.printSchema()


# Using DataFrame object (df)
df.select(df.gender).show()
df.select(df["gender"]).show()

#Accessing column name with dot (with backticks)
df.select(df["`name.fname`"]).show()

#Using SQL col() function
df.select(col("gender")).show()

#Accessing column name with dot (with backticks)
df.select(col("`name.fname`")).show()


#
#
#
data=[(100,2,1),(200,3,4),(300,4,4)]
df=spark.createDataFrame(data).toDF("col1", "col2", "col3")

#Arthmetic operations
df.select(df.col1 + df.col2).show()
df.select(df.col1 - df.col2).show()
df.select(df.col1 * df.col2).show()
df.select(df.col1 / df.col2).show()
df.select(df.col1 % df.col2).show()

df.select(df.col2 > df.col3).show()
df.select(df.col2 < df.col3).show()
df.select(df.col2 == df.col3).show()


spark.stop()