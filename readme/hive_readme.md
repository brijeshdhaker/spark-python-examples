
$HIVE_HOME/bin/beeline -u jdbc:hive2://hiveserver:10000/default;user=scott;password=tiger

#### 1. At the command line, copy the Hue sample_07 and sample_08 CSV files to HDFS
```commandline
export HADOOP_HOME=/opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hadoop
cd ~/PycharmProjects/pyspark-hive-integration

hdfs dfs -put data/sample_07.csv 
hdfs dfs -put data/sample_08.csv 
# or
$HADOOP_HOME/bin/hadoop fs -put data/sample_07.csv 
$HADOOP_HOME/bin/hadoop fs -put data/sample_08.csv 
```

#### 2. Start spark-shell
```commandline
#
export SPARK_HOME=/opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/spark
#
$SPARK_HOME/bin/pyspark
```

#### 3. Create Hive tables sample_07 and sample_08
```python
>>> spark.sql("CREATE TABLE sample_07 (code string,description string,total_emp int,salary int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TextFile")
>>> spark.sql("CREATE TABLE sample_08 (code string,description string,total_emp int,salary int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TextFile")
```

#### 4. In Beeline, show the Hive tables:
```commandline
$HIVE_HOME/bin/beeline -u jdbc:hive2://hiveserver.sandbox.net:10000 scott tiger

[0: jdbc:hive2://hiveserver:> show tables;
+------------+--+
|  tab_name  |
+------------+--+
| sample_07  |
| sample_08  |
+------------+--+
```

#### 5. Load the data in the CSV files into the tables:
```python
>>> spark.sql("LOAD DATA INPATH '/user/brijeshdhaker/sample_07.csv' OVERWRITE INTO TABLE sample_07")
>>> spark.sql("LOAD DATA INPATH '/user/brijeshdhaker/sample_08.csv' OVERWRITE INTO TABLE sample_08")
```

#### 6. Create DataFrames containing the contents of the sample_07 and sample_08 tables:
```python
>>> df_07 = spark.sql("SELECT * from sample_07")
>>> df_08 = spark.sql("SELECT * from sample_08")
```
#### 7. Show all rows in df_07 with salary greater than 150,000:

```
>>> df_07.filter(df_07.salary > 150000).show()
# The output should be:
+-------+--------------------+---------+------+
|   code|         description|total_emp|salary|
+-------+--------------------+---------+------+
|11-1011|    Chief executives|   299160|151370|
|29-1022|Oral and maxillof...|     5040|178440|
|29-1023|       Orthodontists|     5350|185340|
|29-1024|     Prosthodontists|      380|169360|
|29-1061|   Anesthesiologists|    31030|192780|
|29-1062|Family and genera...|   113250|153640|
|29-1063| Internists, general|    46260|167270|
|29-1064|Obstetricians and...|    21340|183600|
|29-1067|            Surgeons|    50260|191410|
|29-1069|Physicians and su...|   237400|155150|
+-------+--------------------+---------+------+
```

#### 8. Create the DataFrame df_09 by joining df_07 and df_08, retaining only the code and description columns.

```
>>> df_09 = df_07.join(df_08, df_07.code == df_08.code).select(df_07.code,df_07.description)
>>> df_09.show()
# The new DataFrame looks like:
+-------+--------------------+
|   code|         description|
+-------+--------------------+
|00-0000|     All Occupations|
|11-0000|Management occupa...|
|11-1011|    Chief executives|
|11-1021|General and opera...|
|11-1031|         Legislators|
|11-2011|Advertising and p...|
|11-2021|  Marketing managers|
|11-2022|      Sales managers|
|11-2031|Public relations ...|
|11-3011|Administrative se...|
|11-3021|Computer and info...|
|11-3031|  Financial managers|
|11-3041|Compensation and ...|
|11-3042|Training and deve...|
|11-3049|Human resources m...|
|11-3051|Industrial produc...|
|11-3061| Purchasing managers|
|11-3071|Transportation, s...|
|11-9011|Farm, ranch, and ...|
|11-9012|Farmers and ranchers|
+-------+--------------------+
```
#### 9. Save DataFrame df_09 as the Hive table sample_09:
```python
>>> df_09.write.saveAsTable("sample_09")
```

#### 10. In Beeline, show the Hive tables:
```commandline
$beeline -u jdbc:hive2://hiveserver:10000 scott tiger

$beeline -u jdbc:hive2://hiveserver:10000 -n hive -p hive

[0: jdbc:hive2://hiveserver:> show tables;
+------------+--+
|  tab_name  |
+------------+--+
| sample_07  |
| sample_08  |
| sample_09  |
+------------+--+
```
#### 11 . The equivalent program in Python, that you could submit using spark-submit, would be:
```python
from pyspark import SparkContext, SparkConf, HiveContext

if __name__ == "__main__":

  # create Spark context with Spark configuration
  conf = SparkConf().setAppName("Data Frame Join")
  sc = SparkContext(conf=conf)
  sqlContext = HiveContext(sc)
  df_07 = sqlContext.sql("SELECT * from sample_07")
  df_07.filter(df_07.salary > 150000).show()
  df_08 = sqlContext.sql("SELECT * from sample_08")
  tbls = sqlContext.sql("show tables")
  tbls.show()
  df_09 = df_07.join(df_08, df_07.code == df_08.code).select(df_07.code,df_07.description)
  df_09.show()
  df_09.write.saveAsTable("sample_09")
  tbls = sqlContext.sql("show tables")
  tbls.show()
```

#
### Make Sure Table deleted before Spark Job Run
#

```commandline
$beeline -u jdbc:hive2://hiveserver:10000 scott tiger
0: jdbc:hive2://hiveserver:10000> drop table sample_09;
```

#
### Run PySpark Job
#

```commandline
export PYSPARK_DRIVER_PYTHON=/opt/sandbox/conda/envs/pyspark3.7/bin/python
export PYSPARK_PYTHON=/opt/sandbox/conda/envs/pyspark3.7/bin/python
$SPARK_HOME/bin/spark-submit \
    --name "PySpark HiveContext" \
    --master local[*] \
    --py-files /home/brijeshdhaker/PycharmProjects/pyspark-hive-integration.zip pyspark-hive-integration/pyspark-hive-context.py

```

###

```commandline
export PYSPARK_DRIVER_PYTHON=/opt/sandbox/conda/envs/pyspark3.7/bin/python
export PYSPARK_PYTHON=/opt/sandbox/conda/envs/pyspark3.7/bin/python
#
$SPARK_HOME/bin/spark-submit \
    --name "PySpark Hive Session" \
    --master local[*] \
    --py-files /home/brijeshdhaker/PycharmProjects/pyspark-hive-integration.zip pyspark-hive-integration/pyspark-hive-session.py
```