# Building a Data Pipeline with
#### Kafka, Spark Streaming and Cassandra

We'll create a simple application in Java using Spark which will integrate with the Kafka topic we created earlier.
The application will read the messages as posted and count the frequency of words in every message.
This will then be updated in the Cassandra table we created earlier.

Let's quickly visualize how the data will flow:

![](../../../../../../../images/Twitter Sentiment with Watson TA and PI architecture diagram.png)

#
```shell

# Topic - Creation
kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 1 --replication-factor 1 --topic tweeter-tweets --if-not-exists

kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 2 --replication-factor 1 --topic test-partitioned-topic

kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 1 --replication-factor 1 --topic txn-text-stream-topic --if-not-exists
kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 1 --replication-factor 1 --topic txn-json-stream-topic
kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 1 --replication-factor 1 --topic txn-avro-stream-topic
kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 1 --replication-factor 1 --topic txn-xml-stream-topic
kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 1 --replication-factor 1 --topic txn-delimiter-stream-topic

##### Topic - List
kafka-topics --list --bootstrap-server kafkabroker.sandbox.net:9092

##### Topic - Describe
kafka-topics --describe --topic tweeter-tweets --bootstrap-server kafkabroker.sandbox.net:9092

##### Topic - Alter
kafka-topics --alter --topic tweeter-tweets --partitions 3 --bootstrap-server zookeeper.sandbox.net:2181

##### Topic - Delete
kafka-topics --delete --topic tweeter-tweets --bootstrap-server kafkabroker.sandbox.net:9092

##### Command Line Producer :
kafka-console-producer --topic tweeter-tweets --broker-list kafkabroker.sandbox.net:9092

kafka-console-producer --topic tweeter-tweets --broker-list kafkabroker.sandbox.net:9092 --property parse.key=true --property key.separator=":"

##### Command Line Consumer :
kafka-console-consumer --topic tweeter-tweets --group pyspark-structured-stream-cg --bootstrap-server kafkabroker.sandbox.net:9092

```

listeners=PLAINTEXT://kafkabroker.sandbox.net:9092
advertised.listeners=PLAINTEXT://localhost:19092

### Create Hive Table
```
beeline -u jdbc:hive2://quickstart-bigdata:10000 

set hive.server2.enable.doAs=false;
use default;
DROP TABLE transaction_details;
CREATE EXTERNAL TABLE IF NOT EXISTS transaction_details (
    id int,
    uuid string,
    cardtype string,
    website string,
    product string,
    amount double,
    city string,
    country string,
    addts bigint
)
COMMENT 'Transaction Details External Table'
PARTITIONED BY(txn_receive_date string)
STORED AS Parquet
LOCATION  'hdfs://namenode:9000/transaction_details/'
TBLPROPERTIES("creator"="Brijesh K Dhaker");

drop table IF EXISTS tweeter_tweets;
CREATE TABLE if not exists tweeter_tweets (
    uuid STRING,
    text STRING, 
    words INT, 
    length INT
) 
STORED AS ORC;

select count(*) from tweeter_tweets;

```
### Create Cassandra Table
```
docker-compose -f docker-sandbox/dc-cassandra.yaml up -d cassandra


CREATE KEYSPACE spark_stream WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
use spark_stream;
CREATE TABLE tweeter_tweets(uuid text PRIMARY KEY, text text, words int, length int);

```

https://repo1.maven.org/maven2/com/datastax/spark/spark-cassandra-connector-assembly_2.11/2.5.1/spark-cassandra-connector-assembly_2.11-2.5.1.jar

#
### Create Required HBase Table
#

create 'tweeter_tweets', 'Sentence', 'Measure'
put 'tweeter_tweets', '16fd2706-8baf-433b-82eb-8c7fada847da', 'Sentence:text', 'Raymond Hello World'
put 'tweeter_tweets', '16fd2706-8baf-433b-82eb-8c7fada847da', 'Measure:words', '3'
put 'tweeter_tweets', '16fd2706-8baf-433b-82eb-8c7fada847da', 'Measure:length', '19'

#
# Run Spark Application
#
spark-submit \
--name "structured-kafka-stream" \
--master local[4] \
--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 \
/home/brijeshdhaker/IdeaProjects/spark-bigdata-examples/pyspark-examples/src/main/py/com/example/streams/structured/structured-kafka-stream.py

spark-submit \
--name "structured-kafka-stream" \
--master local[4] \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
/home/brijeshdhaker/IdeaProjects/spark-python-examples/src/main/py/com/example/streams/structured/KafkaStreamDemo.py

spark-submit \
--name "structured-kafka-stream" \
--master local[4] \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
/home/brijeshdhaker/IdeaProjects/pyspark-examples/src/main/py/com/example/streams/structured/structured-kafka-stream.py

spark-submit \
--name "structured-kafka-stream" \
--master yarn \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
/home/brijeshdhaker/IdeaProjects/pyspark-examples/src/main/py/com/example/streams/structured/structured-kafka-stream.py


spark-submit ^
--name "structured-kafka-stream" ^
--master local[4] ^
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 ^
C:\Users\brije\IdeaProjects\spark-python-examples\src\main\py\com\example\streams\structured\structured-kafka-stream.py


spark-submit --name "structured-kafka-stream" --master local[4] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 structured-kafka-stream.py
spark-submit --name "structured-delimiter-stream" --master local[4] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 src/main/py/com/example/streams/structured/structured-delimiter-stream.py


spark-submit \
--name "Sample Spark Application" \
--master local[*] \
--packages com.hortonworks:shc-core:1.1.1-2.1-s_2.11 \
--repositories http://repo.hortonworks.com/content/groups/public/ \
--files /opt/sandbox/hbase-2.4.9/conf/hbase-site.xml \
/home/brijeshdhaker/IdeaProjects/pyspark-data-pipelines/com/example/spark/streams/stream-hbase-transformer.py


spark-submit \
--name "Sample Spark Application" \
--master local[*] \
--jars /opt/cloudera/parcels/CDH-6.3.2-1.cdh6.3.2.p0.1605554/lib/hbase/hbase-spark-2.1.0-cdh6.3.2.jar \
--files /opt/sandbox/hbase-2.4.9/conf/hbase-site.xml \
/home/brijeshdhaker/IdeaProjects/pyspark-data-pipelines/com/example/spark/streams/stream-hbase-transformer.py
