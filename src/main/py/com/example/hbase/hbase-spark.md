#
## Spark & Hbase Integration
#

#### 1. Create Hbase Table with String Key

```commandline # Create Books Table
$ hbase> 
create 'books', 'info', 'analytics'
put 'books', 'In Search of Lost Time', 'info:author', 'Marcel Proust'
put 'books', 'In Search of Lost Time', 'info:year', '1922'
put 'books', 'In Search of Lost Time', 'analytics:views', '3298'
put 'books', 'Godel, Escher, Bach', 'info:author', 'Douglas Hofstadter'
put 'books', 'Godel, Escher, Bach', 'info:year', '1979'
put 'books', 'Godel, Escher, Bach', 'analytics:views', '820'

## The table returns the following result when scanning:
$ hbase> scan 'books'
ROW                                              COLUMN+CELL                                                                                                                                 
 Godel, Escher, Bach                             column=analytics:views, timestamp=2021-12-26T09:44:17.455, value=820                                                                        
 Godel, Escher, Bach                             column=info:author, timestamp=2021-12-26T09:44:15.823, value=Douglas Hofstadter                                                             
 Godel, Escher, Bach                             column=info:year, timestamp=2021-12-26T09:44:15.844, value=1979                                                                             
 In Search of Lost Time                          column=analytics:views, timestamp=2021-12-26T09:44:15.798, value=3298                                                                       
 In Search of Lost Time                          column=info:author, timestamp=2021-12-26T09:44:15.761, value=Marcel Proust                                                                  
 In Search of Lost Time                          column=info:year, timestamp=2021-12-26T09:44:15.780, value=1922                                                                             
2 row(s)
Took 0.1034 seconds 
```

#### 2. Create Hbase Table with Integer Key
```
# Create Person Table
$ hbase>
create 'Person', 'Name', 'Address'
put 'Person', '1', 'Name:First', 'Raymond'
put 'Person', '1', 'Name:Last', 'Tang'
put 'Person', '1', 'Address:Country', 'Australia'
put 'Person', '1', 'Address:State', 'VIC'

put 'Person', '2', 'Name:First', 'Dnomyar'
put 'Person', '2', 'Name:Last', 'Gnat'
put 'Person', '2', 'Address:Country', 'USA'
put 'Person', '2', 'Address:State', 'CA'

## The table returns the following result when scanning:
$ hbase> scan 'Person'
ROW                             COLUMN+CELL
1                              column=Address:Country, timestamp=2021-02-05T20:48:42.088, value=Australia
1                              column=Address:State, timestamp=2021-02-05T20:48:46.750, value=VIC
1                              column=Name:First, timestamp=2021-02-05T20:48:32.544, value=Raymond
1                              column=Name:Last, timestamp=2021-02-05T20:48:37.085, value=Tang
2                              column=Address:Country, timestamp=2021-02-05T20:49:00.692, value=USA
2                              column=Address:State, timestamp=2021-02-05T20:49:04.972, value=CA
2                              column=Name:First, timestamp=2021-02-05T20:48:51.653, value=Dnomyar
2                              column=Name:Last, timestamp=2021-02-05T20:48:56.665, value=Gnat
2 row(s)
```

#
## 1. Using Hive External Tables
#

### 1.1 Create Hive External Table
```
$ hive>

CREATE EXTERNAL TABLE IF NOT EXISTS `default`.`books_ext` (
    `title` string,
    `author` string,
    `year` int,
    `views` double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.hbase.HBaseSerDe'
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES (
   'hbase.columns.mapping'=':key,info:author,info:year,analytics:views'
)
TBLPROPERTIES (
    'hbase.mapred.output.outputtable'='books',
    'hbase.table.name'='books'
);

##
CREATE EXTERNAL TABLE IF NOT EXISTS `default`.`person_hbase` (
    `id`    int,  
    `fname` string,
    `lname` string,
    `state` string,
    `country` string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.hbase.HBaseSerDe'
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES (
   'hbase.columns.mapping'=':key,Name:First,Name:Last,Address:State,Address:Country'
)
TBLPROPERTIES (
    'hbase.mapred.output.outputtable'='Person',
    'hbase.table.name'='Person'
);

```
### 1.2 Query Hive table from Spark using the SQLContext or Spark session:
```
spark-shell --jars file:///opt/hive-3.1.2/lib/hive-hbase-handler-3.1.2.jar
spark-shell --jars file:///opt/hive-2.3.9/lib/hive-hbase-handler-2.3.9.jar

spark.table("default.books_ext").show()

+--------------------+------------------+----+------+
|               title|            author|year| views|
+--------------------+------------------+----+------+
| Godel, Escher, Bach|Douglas Hofstadter|1979| 820.0|
|In Search of Lost...|     Marcel Proust|1922|3298.0|
+--------------------+------------------+----+------+

spark.table("default.person_hbase").show()

+---+-------+-----+-----+---------+
| id|  fname|lname|state|  country|
+---+-------+-----+-----+---------+
|  1|Raymond| Tang|  VIC|Australia|
|  2|Dnomyar| Gnat|   CA|      USA|
+---+-------+-----+-----+---------+


// for optimal performance
spark.sql('SET hbase.scan.cache=10000')
spark.sql('SET hbase.client.scanner.cache=10000')
```

Note : The last point means that accessing HBase from Spark through Hive is only a good option when doing operations on the entire table, such as full table scans. Otherwise, keep reading!

#
## 2. Using Spark-HBase Connector
#

### 1. Build HBase Spark connector
```
   git clone https://github.com/apache/hbase-connectors.git
   cd hbase-connectors/
   
   #
   mvn -Dspark.version=2.3.4 -Dscala.version=2.11.12 -Dscala.binary.version=2.11 -Dhbase.version=2.2.4 -Dhadoop.profile=2.0 -Dhadoop-three.version=2.10.1 -DskipTests -Dcheckstyle.skip -U clean package
   
   # for spark 2.4.0
   mvn -Dspark.version=2.4.8 -Dscala.version=2.11.12 -Dscala.binary.version=2.11 clean install
   
   # for spark 3.2.1
   mvn -Dspark.version=3.0.1 -Dscala.version=2.12.10 -Dscala.binary.version=2.12 -Dhbase.version=2.2.4 -Dhadoop.profile=3.0 -Dhadoop-three.version=3.2.0 -DskipTests -Dcheckstyle.skip -U clean package
   
   # for spark 3.2.1
   mvn -Dspark.version=3.0.1 -Dscala.version=2.12.10 -Dscala.binary.version=2.12 -Dhbase.version=2.4.9 -Dhadoop.profile=3.0 -Dhadoop-three.version=3.3.4 -DskipTests -Dcheckstyle.skip -U clean package
   
   The version arguments need to match with your Hadoop, Spark and HBase versions.
```

### 2. Run Sparkshell
```

spark-shell --jars /home/brijeshdhaker/IdeaProjects/hbase-connectors/spark/hbase-spark/target/hbase-spark-1.0.1-SNAPSHOT.jar
export HBASE_CONN_PATH=/opt/sandbox/spark-2.4.8/hbase
export HBASE_CLASSPATH=$HBASE_CONN_PATH/hbase-spark-1.0.1_2.11-2.4.8.jar:$HBASE_CONN_PATH/hbase-spark-it-1.0.1_2.11-2.4.8.jar:$HBASE_CONN_PATH/hbase-spark-protocol-1.0.1_2.11-2.4.8.jar:$HBASE_CONN_PATH/hbase-spark-protocol-shaded-1.0.1_2.11-2.4.8.jar
spark-shell --jars $HBASE_CONN_PATH/hbase-spark-1.0.1_2.11-2.4.8.jar,$HBASE_CONN_PATH/hbase-spark-it-1.0.1_2.11-2.4.8.jar,$HBASE_CONN_PATH/hbase-spark-protocol-1.0.1_2.11-2.4.8.jar,$HBASE_CONN_PATH/hbase-spark-protocol-shaded-1.0.1_2.11-2.4.8.jar

```

#### 1) First import the required classes:
```
import org.apache.hadoop.hbase.spark.HBaseContext
import org.apache.hadoop.hbase.HBaseConfiguration
val conf = HBaseConfiguration.create()
conf.set("hbase.zookeeper.quorum", "127.0.0.1:2181")
conf.set("hbase.zookeeper.property.clientPort","2181")
conf.set("hbase.spark.config.location", "file:///opt/sandbox/hbase-2.4.9/conf/hbase-site.xml")

## Create HBase context 
new HBaseContext(spark.sparkContext, conf)

## Create DataFram for Book Table
val bookDF = spark.read.format("org.apache.hadoop.hbase.spark")
.option("hbase.columns.mapping","title STRING :key, author STRING info:author, year STRING info:year, views STRING analytics:views")
.option("hbase.table", "books")
.option("hbase.use.hbase.context", false)
.option("hbase.config.resources", "file:///opt/sandbox/hbase-2.4.9/conf/hbase-site.xml") 
.option("hbase-push.down.column.filter", false) 
.load()

bookDF.printSchema()
bookDF.show()

## Create DataFrame for Person Table
val personDF = spark.read.format("org.apache.hadoop.hbase.spark")
  .option("hbase.columns.mapping","rowKey STRING :key, firstName STRING Name:First, lastName STRING Name:Last, country STRING Address:Country, state STRING Address:State")
  .option("hbase.table", "Person")
  .option("hbase.use.hbase.context", false)
  .option("hbase.config.resources", "file:///opt/sandbox/hbase-2.4.9/conf/hbase-site.xml") 
  .option("hbase-push.down.column.filter", false)
  .load()

The columns mapping matches with the definition in the steps above.
```
#### 5) Show DataFrame schema
```
   scala> personDF.schema
   res2: org.apache.spark.sql.types.StructType = StructType(StructField(lastName,StringType,true), StructField(country,StringType,true), StructField(state,StringType,true), StructField(firstName,StringType,true), StructField(rowKey,StringType,true))
```
#### 6) Show data
```
scala> personDF.show()
```

#### Use catalog

We can also define a catalog for the table Person created above and then use it to read data.

##### 1) Define catalog

   def catalog = s"""{
   |"table":{"namespace":"default", "name":"Person"},
   |"rowkey":"key",
   |"columns":{
   |"rowkey":{"cf":"rowkey", "col":"key", "type":"string"},
   |"firstName":{"cf":"Name", "col":"First", "type":"string"},
   |"lastName":{"cf":"Name", "col":"Last", "type":"string"},
   |"country":{"cf":"Address", "col":"Country", "type":"string"},
   |"state":{"cf":"Address", "col":"State", "type":"string"}
   |}
   |}""".stripMargin

##### 2) Use catalog

   Now the catalog can be directly passed into as tableCatalog option:
   
   import org.apache.hadoop.hbase.spark.datasources._
   
   var hbaseDF = spark.read.options(Map(HBaseTableCatalog.tableCatalog->catalog)).format("org.apache.hadoop.hbase.spark").load()
   hbaseDF.show()

   The code can also be simplified as:

   var hbaseDF = spark.read.format("org.apache.hadoop.hbase.spark").option("catalog",catalog).load()
   hbaseDF.show()

## Output:
   +--------+------+---------+-----+---------+
   |lastName|rowkey|  country|state|firstName|
   +--------+------+---------+-----+---------+
   |    Tang|     1|Australia|  VIC|  Raymond|
   |    Gnat|     2|      USA|   CA|  Dnomyar|
   +--------+------+---------+-----+---------+

## Summary
Unfortunately the connector packages for Spark 3.x are not published to Maven central repositories yet.
To save time for building hbase-connector project, you can download it from the ones I built using WSL: Release 1.0.1 HBase Connectors for Spark 3.0.1 · kontext-tech/hbase-connectors.


#
## 3. PySpark & Hbase with Hortonworks SHC connector
#

### 1. copy hbase-site.xml to $SPARK_HOME/conf/ directory

   cp /usr/hdp/current/hbase-client/conf/hbase-site.xml spark2-client/conf/hbase-site.xml
#  export SPARK_CLASSPATH=/usr/hdp/current/hbase-client/lib/hbase-common.jar:/usr/hdp/current/hbase-client/lib/hbase-client.jar:/usr/hdp/current/hbase-client/lib/hbase-server.jar:/usr/hdp/current/hbase-client/lib/hbase-protocol.jar:/usr/hdp/current/hbase-client/lib/guava-12.0.1.jar

### 2. 

   pyspark --packages com.hortonworks:shc-core:1.1.1-2.1-s_2.11 --repositories http://repo.hortonworks.com/content/groups/public/ --files /usr/hdp/current/hbase-master/conf/hbase-site.xml

   pyspark --packages com.hortonworks:shc-core:1.1.1-2.1-s_2.11 --repositories http://repo.hortonworks.com/content/groups/public/ --files /opt/sandbox/hbase-2.4.9/conf/hbase-site.xml

   <dependency>
     <groupId>com.hortonworks</groupId>
     <artifactId>shc-core</artifactId>
     <version>1.1.3-2.4-s_2.11</version>
   </dependency>

   $SPARK_HOME/bin/pyspark --packages com.hortonworks:shc-core:1.1.3-2.4-s_2.11 --repositories http://repo.hortonworks.com/content/groups/public/ --files /opt/sandbox/hbase-2.4.9/conf/hbase-site.xml


### 3. Define Catalog for Hbase Table
   
### 4. 
#### Scala
```   
import org.apache.spark.sql.execution.datasources.hbase._
import org.apache.spark.sql.{DataFrame, SparkSession}

val catalog = "{\"table\": {\"namespace\": \"default\", \"name\": \"books\"}, \"rowkey\": \"key\", \"columns\": {\"title\": {\"cf\": \"rowkey\", \"col\": \"key\", \"type\": \"string\"}, \"author\": {\"cf\": \"info\", \"col\": \"author\", \"type\": \"string\"} } }"

def withCatalog(cat: String): DataFrame = {
  spark.read.options(Map(HBaseTableCatalog.tableCatalog->cat)).format("org.apache.spark.sql.execution.datasources.hbase").load()
}
// Load the dataframe
val df = withCatalog(catalog)
df.show()

//SQL example
df.createOrReplaceTempView("table")
sqlContext.sql("select count(col1) from table").show

```

#### Python

```  
catalog = '{"table": {"namespace": "default", "name": "books"}, "rowkey": "key", "columns": {"title": {"cf": "rowkey", "col": "key", "type": "string"}, "author": {"cf": "info", "col": "author", "type": "string"} } }'
df = spark.read.options(catalog=catalog).format('org.apache.spark.sql.execution.datasources.hbase').load()
df.show()

   +--------------------+------------------+
   |               title|            author|
   +--------------------+------------------+
   | Godel, Escher, Bach|Douglas Hofstadter|
   |In Search of Lost...|     Marcel Proust|
   +--------------------+------------------+
```

### 5.
 
```
   df.write.options(catalog=catalog) \
   .format("org.apache.spark.sql.execution.datasources.hbase") \
   .save()
```
