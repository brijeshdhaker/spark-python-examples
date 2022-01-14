## Read HBase table from PySpark

===============================================================================================================================

Ono of the Real-time Project Scenario is read HBase from PySpark | Part 1 | Hands-On

Step 1: Create HBase table

create 'transaction_detail_hbase_tbl','transaction_data','customer_data'
```commandline
$ hbase shell
Java HotSpot(TM) 64-Bit Server VM warning: Using incremental CMS is deprecated and will likely be removed in a future release
HBase Shell
Use "help" to get list of supported commands.
Use "exit" to quit this interactive shell.
For Reference, please visit: http://hbase.apache.org/2.0/book.html#shell
Version 2.1.0-cdh6.2.0, rUnknown, Wed Mar 13 23:39:58 PDT 2019
Took 0.0041 seconds
$ hbase(main):001:0>
$hbase(main):002:0> create 'transaction_detail_hbase_tbl','transaction_data','customer_data'
Created table transaction_detail_hbase_tbl
Took 5.7059 seconds
=> Hbase::Table - transaction_detail_hbase_tbl
hbase(main):003:0>
```

### Step 2: Insert/Put few records to HBase table
```commandline
put 'transaction_detail_hbase_tbl','1','transaction_data:transaction_amount','50.85'
put 'transaction_detail_hbase_tbl','1','transaction_data:transaction_card_type','MasterCard'
put 'transaction_detail_hbase_tbl','1','transaction_data:transaction_ecommerce_website_name','www.ebay.com'
put 'transaction_detail_hbase_tbl','1','transaction_data:transaction_datetime','2019-05-14 15:24:12'
put 'transaction_detail_hbase_tbl','1','transaction_data:transaction_product_name','Laptop'
put 'transaction_detail_hbase_tbl','1','customer_data:transaction_city_name','Mumbai'
put 'transaction_detail_hbase_tbl','1','customer_data:transaction_country_name','India'

put 'transaction_detail_hbase_tbl','2','transaction_data:transaction_amount','259.12'
put 'transaction_detail_hbase_tbl','2','transaction_data:transaction_card_type','MasterCard'
put 'transaction_detail_hbase_tbl','2','transaction_data:transaction_ecommerce_website_name','www.amazon.com'
put 'transaction_detail_hbase_tbl','2','transaction_data:transaction_datetime','2019-05-14 15:24:13'
put 'transaction_detail_hbase_tbl','2','transaction_data:transaction_product_name','Wrist Band'
put 'transaction_detail_hbase_tbl','2','customer_data:transaction_city_name','Pune'
put 'transaction_detail_hbase_tbl','2','customer_data:transaction_country_name','India'

put 'transaction_detail_hbase_tbl','3','transaction_data:transaction_amount','328.16'
put 'transaction_detail_hbase_tbl','3','transaction_data:transaction_card_type','MasterCard'
put 'transaction_detail_hbase_tbl','3','transaction_data:transaction_ecommerce_website_name','www.flipkart.com'
put 'transaction_detail_hbase_tbl','3','transaction_data:transaction_datetime','2019-05-14 15:24:14'
put 'transaction_detail_hbase_tbl','3','transaction_data:transaction_product_name','TV Stand'
put 'transaction_detail_hbase_tbl','3','customer_data:transaction_city_name','New York City'
put 'transaction_detail_hbase_tbl','3','customer_data:transaction_country_name','United States'

put 'transaction_detail_hbase_tbl','4','transaction_data:transaction_amount','399.06'
put 'transaction_detail_hbase_tbl','4','transaction_data:transaction_card_type','Visa'
put 'transaction_detail_hbase_tbl','4','transaction_data:transaction_ecommerce_website_name','www.snapdeal.com'
put 'transaction_detail_hbase_tbl','4','transaction_data:transaction_datetime','2019-05-14 15:24:15'
put 'transaction_detail_hbase_tbl','4','transaction_data:transaction_product_name','TV Stand'
put 'transaction_detail_hbase_tbl','4','customer_data:transaction_city_name','New Delhi'
put 'transaction_detail_hbase_tbl','4','customer_data:transaction_country_name','India'

put 'transaction_detail_hbase_tbl','5','transaction_data:transaction_amount','194.52'
put 'transaction_detail_hbase_tbl','5','transaction_data:transaction_card_type','Visa'
put 'transaction_detail_hbase_tbl','5','transaction_data:transaction_ecommerce_website_name','www.ebay.com'
put 'transaction_detail_hbase_tbl','5','transaction_data:transaction_datetime','2019-05-14 15:24:16'
put 'transaction_detail_hbase_tbl','5','transaction_data:transaction_product_name','External Hard Drive'
put 'transaction_detail_hbase_tbl','5','customer_data:transaction_city_name','Rome'
put 'transaction_detail_hbase_tbl','5','customer_data:transaction_country_name','Italy'

```

### Step 3: Create Hive table pointing to HBase table using HBaseStorageHandler
```commandline

$ beeline -u jdbc:hive2://quickstart-bigdata:10000 scott tiger
0: jdbc:hive2://quickstart-bigdata:10000> 

drop table transaction_detail_hive_tbl;

CREATE EXTERNAL TABLE transaction_detail_hive_tbl(
    transaction_id int, 
    transaction_card_type string, 
    transaction_ecommerce_website_name string, 
    transaction_product_name string, 
    transaction_datetime string, 
    transaction_amount double, 
    transaction_city_name string, 
    transaction_country_name string
)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES ("hbase.columns.mapping"=":key,transaction_data:transaction_card_type,transaction_data:transaction_ecommerce_website_name,transaction_data:transaction_product_name,transaction_data:transaction_datetime,transaction_data:transaction_amount,customer_data:transaction_city_name,customer_data:transaction_country_name")
TBLPROPERTIES ("hbase.table.name"="transaction_detail_hbase_tbl");
```

###
```
0: jdbc:hive2://> describe transaction_detail_hive_tbl;
OK
+-------------------------------------+------------+----------+
|              col_name               | data_type  | comment  |
+-------------------------------------+------------+----------+
| transaction_id                      | int        |          |
| transaction_card_type               | string     |          |
| transaction_ecommerce_website_name  | string     |          |
| transaction_product_name            | string     |          |
| transaction_datetime                | string     |          |
| transaction_amount                  | double     |          |
| transaction_city_name               | string     |          |
| transaction_country_name            | string     |          |
+-------------------------------------+------------+----------+
8 rows selected (0.057 seconds)
0: jdbc:hive2://> 

```


### Step 4: Query Hive table from Hive CLI or Hue browser to verify Hive table and HBase table integration is working
```commandline
0: jdbc:hive2://quickstart-bigdata:10000> select * from transaction_detail_hive_tbl;
```

### ===============================================================================================================================

Ono of the Real-time Project Scenario is read HBase from PySpark | Part 2 | Hands-On

### Step 1: Create SparkSession object with Hive enable option in PySpark program
```python
from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("Read HBase Table using PySpark Demo") \
    .config("spark.jars", "/opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hive/lib/hive-hbase-handler-2.1.1-cdh6.3.2.jar") \
    .config("spark.executor.extraClassPath", "/opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hive/lib/hive-hbase-handler-2.1.1-cdh6.3.2.jar") \
    .config("spark.executor.extraLibrary", "/opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hive/lib/hive-hbase-handler-2.1.1-cdh6.3.2.jar") \
    .config("spark.driver.extraClassPath", "/opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hive/lib/hive-hbase-handler-2.1.1-cdh6.3.2.jar") \
    .enableHiveSupport()\
    .getOrCreate()
```

### Step 2: Read/query Hive table using SparkSession object which internally uses HiveContext to make Hive connection(Metastore) and get the records
```python

spark.sql("show tables").show()
spark.sql("use default")
spark.sql("select * from transaction_detail_hive_tbl").show()

```

### Step 3: As usual do some analysis on the data in the DataFrame from Hive table


DataSet used:
-------------
```commandline
+--------------+---------------------+----------------------------------+------------------------+--------------------+------------------+---------------------+------------------------+
|transaction_id|transaction_card_type|transaction_ecommerce_website_name|transaction_product_name|transaction_datetime|transaction_amount|transaction_city_name|transaction_country_name|
+--------------+---------------------+----------------------------------+------------------------+--------------------+------------------+---------------------+------------------------+
|             1|           MasterCard|                      www.ebay.com|                  Laptop| 2019-05-14 15:24:12|             50.85|               Mumbai|                   India|
|             2|           MasterCard|                    www.amazon.com|              Wrist Band| 2019-05-14 15:24:13|            259.12|                 Pune|                   India|
|             3|           MasterCard|                  www.flipkart.com|                TV Stand| 2019-05-14 15:24:14|            328.16|        New York City|           United States|
|             4|                 Visa|                  www.snapdeal.com|                TV Stand| 2019-05-14 15:24:15|            399.06|            New Delhi|                   India|
|             5|                 Visa|                      www.ebay.com|     External Hard Drive| 2019-05-14 15:24:16|            194.52|                 Rome|                   Italy|
+--------------+---------------------+----------------------------------+------------------------+--------------------+------------------+---------------------+------------------------+
```


### Reference link for other option for reading HBase table using Spark/PySpark:

https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-using-spark-query-hbase
https://mapr.com/developer-portal/mapr-tutorials/loading-hbase-tables-spark

#
# Run Spark Application
#
spark-submit \
--name "PySpark SHC Hbase Demo" \
--master local[*] \
--packages com.hortonworks:shc-core:1.1.1-2.1-s_2.11 \
--repositories http://repo.hortonworks.com/content/groups/public/ \
--files /opt/sandbox/hbase-2.4.9/conf/hbase-site.xml \
/home/brijeshdhaker/IdeaProjects/pyspark-hbase-integration/pyspark-shc-hbase.py

#
### Run using Spark HBase Connector ( hbase-spark )
#

<!-- https://mvnrepository.com/artifact/org.apache.hbase.connectors.spark/hbase-spark -->
<dependency>
    <groupId>org.apache.hbase.connectors.spark</groupId>
    <artifactId>hbase-spark</artifactId>
    <version>1.0.0</version>
</dependency>

spark-submit \
--name "PySpark Hbase Spark Demo" \
--master local[*] \
--packages org.apache.hbase.connectors.spark:hbase-spark:1.0.0 \
--repositories https://repo1.maven.org/maven2/ \
--files /opt/sandbox/hbase-2.4.9/conf/hbase-site.xml \
/home/brijeshdhaker/IdeaProjects/pyspark-hbase-integration/pyspark-spark-hbase.py

#
### Run using Cloudera “hbase-spark” connector
#
<!-- https://mvnrepository.com/artifact/org.apache.hbase/hbase-spark -->
<dependency>
    <groupId>org.apache.hbase</groupId>
    <artifactId>hbase-spark</artifactId>
    <version>2.1.0-cdh6.3.2</version>
</dependency>

spark-submit \
--name "PySpark Hbase Spark Demo" \
--master local[*] \
--packages org.apache.hbase:hbase-spark:2.1.0-cdh6.3.2 \
--repositories https://repository.cloudera.com/content/repositories/releases/ \
--files /opt/sandbox/hbase-2.4.9/conf/hbase-site.xml \
/home/brijeshdhaker/IdeaProjects/pyspark-hbase-integration/pyspark-spark-hbase.py

#
### Run using Hortonworks “hbase-spark” connector
#

<!-- https://mvnrepository.com/artifact/org.apache.hbase/hbase-spark -->
<dependency>
    <groupId>org.apache.hbase</groupId>
    <artifactId>hbase-spark</artifactId>
    <version>2.1.6.3.1.7.0-79</version>
</dependency>

spark-submit \
--name "PySpark Hbase Spark Demo" \
--master local[*] \
--packages org.apache.hbase:hbase-spark:2.1.6.3.1.7.0-79 \
--repositories 	https://repo.hortonworks.com/content/repositories/releases/ \
--files /opt/sandbox/hbase-2.4.9/conf/hbase-site.xml \
/home/brijeshdhaker/IdeaProjects/pyspark-hbase-integration/pyspark-spark-hbase.py


spark-submit \
--name "PySpark Hbase Spark Demo" \
--master local[*] \
/home/brijeshdhaker/IdeaProjects/pyspark-hbase-integration/pyspark-spark-hbase.py


#
# Run using “hbase-spark” connector
#
spark-submit \
--name "Sample Spark Application" \
--master local[*] \
--jars /opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hbase/hbase-spark-2.1.0-cdh6.3.2.jar \
--files /opt/sandbox/hbase-2.4.9/conf/hbase-site.xml \
/home/brijeshdhaker/IdeaProjects/pyspark-data-pipelines/com/example/spark/streams/stream-hbase-transformer.py
