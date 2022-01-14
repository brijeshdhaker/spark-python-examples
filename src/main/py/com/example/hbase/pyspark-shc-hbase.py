#
#
#
from pyspark.sql import SparkSession
import json
#
#
#
spark = SparkSession \
    .builder \
    .appName("PySpark SHC Hbase Demo") \
    .enableHiveSupport()\
    .getOrCreate()
print(spark.sparkContext.appName)

catalogDict = {
    "table": {"namespace": "default", "name": "books"},
    "rowkey": "key",
    "columns": {
        "title": {"cf": "rowkey", "col": "key", "type": "string"},
        "author": {"cf": "info", "col": "author", "type": "string"},
        "year": {"cf": "info", "col": "year", "type": "string"},
        "views": {"cf": "analytics", "col": "views", "type": "string"}
    }
}

## Write
books = [('My Life', 'Brijesh K', '2011', '190'), ('Good Hobbies', 'Neeta K', '2012', '90'), ('My Games', 'Tejas K', '2012', '08'), ('My Schools', 'Keshvi D.', '2012', '909'), ('Ramayna', 'Tulsidaas', '1212', '199990')]
bookRDD = spark.sparkContext.parallelize(books)
booksDF = spark.createDataFrame(bookRDD, schema=["title", "author", "year", "views"])
booksDF.write.options(catalog=catalog) \
    .option("newtable", "5") \
    .format("org.apache.spark.sql.execution.datasources.hbase") \
    .save()

## Read
catalog = json.dumps(catalogDict)
df = spark.read.options(catalog=catalog).format('org.apache.spark.sql.execution.datasources.hbase').load()
df.show()

spark.stop()
