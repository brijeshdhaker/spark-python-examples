### Solution for 'For input string: "0x100" '
export TERM=xterm-color

###

$SPARK_HOME/bin/spark-shell \
--jars \
$HIVE_HOME/lib/hive-metastore-2.3.6.jar,\
$HIVE_HOME/lib/hive-exec-2.3.6.jar,\
$HIVE_HOME/lib/hive-common-2.3.6.jar,\
$HIVE_HOME/lib/hive-serde-2.3.6.jar,\
$HIVE_HOME/lib/guava-14.0.1.jar \
--conf spark.sql.hive.metastore.version=2.3 \
--conf spark.sql.hive.metastore.jars=$HIVE_HOME"/lib/*" \
--conf spark.sql.warehouse.dir=hdfs://localhost:9000/user/hive/warehouse

### HIVE ON HDP
```
$HIVE_HOME/bin/hiveserver2

$HIVE_HOME/bin/beeline -u jdbc:hive2://hiveserver:10000/default;user=scott;password=tiger
$HIVE_HOME/bin/beeline -u jdbc:hive2:// -n scott -p tiger

$HIVE_HOME/bin/beeline -u jdbc:hive2://hiveserver:10000 scott tiger
$HIVE_HOME/bin/beeline -u jdbc:hive2://hiveserver:10000 scott tiger

bin/beeline -u jdbc:hive2:// scott tiger
bin/beeline -u jdbc:hive2:// -n scott -p tiger

$HIVE_HOME/bin/beeline
beeline>!connect jdbc:hive2://hiveserver:10000 -n scott -p tiger
beeline>!connect jdbc:hive2://localhost:10000 -n scott -p tiger
beeline>!connect jdbc:hive2:// -n scott -p tiger
```

#### Documentation
https://cwiki.apache.org/confluence/display/Hive/Home#Home-HiveDocumentation

#### Use presto for Hive Access
```
$ wget https://repo1.maven.org/maven2/io/prestosql/presto-cli/308/presto-cli-308-executable.jar
$ mv presto-cli-308-executable.jar presto.jar
$ chmod +x presto.jar
$ ./presto.jar --server localhost:8080 --catalog hive --schema default
presto> select * from pokes;
./presto --server localhost:8080 --catalog hive --schema default
```

#### Hive Properties
```
SET hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;
SET hive.support.concurrency=true;
SET hive.support.concurrency=false;
Note :  This property is not needed if you are using Hive 2.x or later
set hive.enforce.bucketing = true;
```

#
```hive

show databases;
CREATE DATABASE IF NOT EXISTS SPARK_APPS;
DROP DATABASE [IF EXISTS] SPARK_APPS [RESTRICT|CASCADE];

#
## Regular INTERNAL Tables
# empId,empName,job,manager,hiredate,salary,comm,deptno
# 7839, KING, PRESIDENT, null,17-11-1981,5000, null, 10
DROP TABLE IF EXISTS SPARK_APPS.EMPLOYEE;

CREATE TABLE IF NOT EXISTS SPARK_APPS.EMPLOYEE (
    empId int,
    empName string,
    job string,
    manager int,
    hiredate string,
    salary int,
    comm int,
    deptno int
)
COMMENT 'Employee Table'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS textfile
TBLPROPERTIES("creator"="Brijesh K Dhaker", "skip.header.line.count"="1");
```
#### Direct data from local file
```
INSERT INTO EMPLOYEE VALUES 
(8001, 'Brijesh', 10, null, '17-11-1981',5000, null, 10),
(8002, 'Tejas', 12, null, '10-12-2021',7000, null, 20),
(8002, 'Keshvi', 14, null, '10-12-2021',6000, null, 20);
```

#### load data from local file
```
LOAD DATA LOCAL INPATH '/home/brijeshdhaker/Downloads/Employee.txt' INTO TABLE SPARK_APPS.EMPLOYEE;
# Note : This command will remove content at source directory and create a internal table
```
#### load data from hdfs://namenode:9000/data/Employee.txt
```
LOAD DATA INPATH '/data/Employee.txt' OVERWRITE INTO TABLE SPARK_APPS.EMPLOYEE;
```

use SPARK_APPS;
show tables;
select * from EMPLOYEE where manager=7566;

#### HIVE External table 
```hive
DROP TABLE IF EXISTS SPARK_APPS.EMPLOYEE_EXTERNAL_TABLE;

CREATE EXTERNAL TABLE IF NOT EXISTS SPARK_APPS.EMPLOYEE_EXTERNAL_TABLE (
    empId int,
    empName string,
    job string,
    manager int,
    hiredate string,
    salary int,
    comm int,
    deptno int
)
COMMENT 'Employee External Table'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS textfile
LOCATION '/user/brijeshdhaker/hiveexttable'
TBLPROPERTIES(
    "creator"="Brijesh K Dhaker", 
    "skip.header.line.count"="1"
);

LOAD DATA INPATH '/data/Employee.txt' OVERWRITE INTO TABLE SPARK_APPS.EMPLOYEE_EXTERNAL_TABLE;

select * from EMPLOYEE_EXTERNAL_TABLE where manager=7566;
```
#### Create Regular Tables from existing table
```
CREATE TABLE q1_miniwikistats
AS
SELECT projcode, sum(pageviews)
FROM miniwikistats
WHERE dt >= '20110101' AND dt <= '20110105'
GROUP BY projcode;

```
#### Temporary Tables
```
CREATE TEMPORARY TABLE emp.employee_tmp (
    id int,
    name string,
    age int,
    gender string)
    ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';

CREATE TABLE emp.similar LIKE emp.employee;
```
#### Create Temp table from query results
```
CREATE TMP TABLE tmp_stats AS
SELECT * FROM miniwikistats
WHERE projcode LIKE 'ab%' AND dt > '20110101';
```
#### Parquet
```
create external table nation_s3_parquet (
    N_NATIONKEY INT, 
    N_NAME STRING, 
    N_REGIONKEY INT, 
    N_COMMENT STRING
)
STORED AS Parquet
LOCATION  's3://qtest-qubole-com/datasets/presto/functional/nation_s3_orc'

```
### #ORC Tables : The Optimized Row Columnar (ORC) file format offers an efficient way for storing Hive data.
```
create external table nation_s3_orc (
    N_NATIONKEY INT, 
    N_NAME STRING, 
    N_REGIONKEY INT, 
    N_COMMENT STRING
)
STORED AS ORC
LOCATION  's3://qtest-qubole-com/datasets/presto/functional/nation_s3_orc'
TBLPROPERTIES (
"hive.exec.dynamic.partition"="true",
"hive.exec.dynamic.partition.mode"="nonstrict",
"orc.compress"="SNAPPY"
);
```
#### AVRO Tables 
#### 1. Get Avro Schema 
```
$ java -jar avro-tools-1.7.4.jar getschema episodes.avro
{
    "type" : "record",
    "name" : "episodes",
    "namespace" : "testing.hive.avro.serde",
    "fields" : [{
        "name" : "title",
        "type" : "string",
        "doc"  : "episode title"
        }, {
        "name" : "air_date",
        "type" : "string",
        "doc"  : "initial date"
        }, {
        "name" : "doctor",
        "type" : "int",
        "doc"  : "main actor playing the Doctor in episode"
    }]
}
```
#### 2. DDL Statement
```
CREATE EXTERNAL TABLE episodes
ROW FORMAT
SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
WITH SERDEPROPERTIES ('avro.schema.literal'='
{
"type" : "record",
"name" : "episodes",
"namespace" : "testing.hive.avro.serde",
"fields" : [ {
"name" : "title",
"type" : "string",
"doc" : "episode title"
}, {
"name" : "air_date",
"type" : "string",
"doc" : "initial date"
}, {
"name" : "doctor",
"type" : "int",
"doc" : "main actor playing the Doctor in episode"
} ]
}
')
STORED AS
INPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
LOCATION 's3://public-qubole/datasets/avro/episodes';

```
#
#### Hive Partition Table
#
```
CREATE TABLE zipcodes(
    RecordNumber int,
    Country string,
    City string,
    Zipcode int
)
PARTITIONED BY(state string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';

hadoop fs -mv /data /datasets
hdfs dfs -put /apps/hostpath/datasets/zipcodes20.csv /datasets/
LOAD DATA INPATH '/datasets/zipcodes20.csv' INTO TABLE zipcodes;
LOAD DATA local INPATH '/apps/hostpath/datasets/zipcodes20.csv' INTO TABLE zipcodes;
Note: Remember the partitioned column should be the last column on the file to loaded data into right partitioned column of the table.

OR

1) CREATE TABLE zipcodes_tmp(RecordNumber int,Country string,City string,Zipcode int,State string) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
2) LOAD DATA local INPATH '/apps/hostpath/datasets/zipcodes20.csv' INTO TABLE zipcodes_tmp;
3) INSERT OVERWRITE TABLE zipcodes PARTITION(state) SELECT RecordNumber,Country,City,Zipcode,State from  zipcodes_tmp;

SHOW PARTITIONS zipcodes;
SHOW PARTITIONS zipcodes PARTITION(state='NC');

ALTER TABLE zipcodes ADD PARTITION (state='CA') LOCATION '/user/data/zipcodes_ca';
ALTER TABLE zipcodes PARTITION (state='AL') RENAME TO PARTITION (state='NY');
ALTER TABLE zipcodes DROP IF EXISTS PARTITION (state='AL');
ALTER TABLE zipcodes RECOVER PARTITIONS LIKE 'state=*'
MSCK REPAIR TABLE zipcodes SYNC PARTITIONS;
DESCRIBE FORMATTED zipcodes;
DESCRIBE FORMATTED zipcodes PARTITION(state='PR');
SHOW TABLE EXTENDED LIKE zipcodes PARTITION(state='PR');
```
#### Hive Bucketing Example
```
DROP TABLE IF EXISTS zipcodes;
CREATE TABLE zipcodes(
    RecordNumber int,
    Country string,
    City string,
    Zipcode int
)
PARTITIONED BY(state string)
CLUSTERED BY (Zipcode) INTO 32 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';

#This property is not needed if you are using Hive 2.x or later
set hive.enforce.bucketing = true;

LOAD DATA INPATH '/data/zipcodes.csv' INTO TABLE zipcodes;
SELECT * FROM zipcodes WHERE state='PR' and country=704;

CREATE TABLE IF NOT EXISTS buckets_test.nytaxi_sample_bucketed (
    trip_id INT,
    vendor_id STRING,
    pickup_datetime TIMESTAMP
)
CLUSTERED BY (trip_id)
INTO 20 BUCKETS
STORED AS PARQUET
LOCATION ‘s3:///buckets_test/hive-clustered/’;
```

#
#
```
scala> spark.conf.get("spark.sql.catalogImplementation")
scala> spark.catalog.listTables.show
scala> spark.sharedState.externalCatalog.listTables("default")
scala> sql("DESCRIBE EXTENDED tweeter_tweets").show(Integer.MAX_VALUE, truncate = false)
```