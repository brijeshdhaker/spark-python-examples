from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from uuid import uuid4
import json

#
#
spark = SparkSession \
    .builder \
    .appName("PySpark Spark Hbase (CDH) Demo") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print(spark.sparkContext.appName)

#
data_source_format = 'org.apache.hadoop.hbase.spark'

#
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
catalog = json.dumps(catalogDict)


# Writing
bookname = "Book-"+str(uuid4())

books = [(bookname+"1", 'Brijesh K', '2011', '190'),
         (bookname+"2", 'Neeta K', '2012', '90'),
         (bookname+"3", 'Tejas K', '2012', '08'),
         (bookname+"4", 'Keshvi D.', '2012', '909'),
         (bookname+"5", 'Tulsidaas', '1212', '199990')
         ]

bookRDD = spark.sparkContext.parallelize(books)
booksDF = spark.createDataFrame(bookRDD, schema=["title", "author", "year", "views"])

# Write Hbase Table
booksDF.write\
    .option('hbase.use.hbase.context', False) \
    .option('hbase.config.resources', 'file:///etc/hbase/conf/hbase-site.xml') \
    .option('hbase-push.down.column.filter', False) \
    .options(catalog=catalog).format(data_source_format).save()

# Reading
dfr = spark.read.option('hbase.use.hbase.context', False) \
    .option('hbase.config.resources', 'file:///etc/hbase/conf/hbase-site.xml') \
    .option('hbase-push.down.column.filter', False) \
    .options(catalog=catalog).format(data_source_format).load()
dfr.show()

spark.sparkContext.stop()