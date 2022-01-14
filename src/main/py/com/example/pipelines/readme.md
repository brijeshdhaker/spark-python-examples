# Building a Data Pipeline with 
#### Kafka, Spark Streaming and Cassandra

We'll create a simple application in Java using Spark which will integrate with the Kafka topic we created earlier. 
The application will read the messages as posted and count the frequency of words in every message. 
This will then be updated in the Cassandra table we created earlier.

Let's quickly visualize how the data will flow:
![](../../../../images/Simple-Data-Pipeline-1.jpg)
#

#
##### Topic - Creation
kafka-topics --create --zookeeper quickstart-bigdata:2181 --partitions 1 --replication-factor 1 --topic tweeter-tweets

##### Topic - List
kafka-topics --list --zookeeper quickstart-bigdata:2181

##### Topic - Describe
kafka-topics --describe --topic tweeter-tweets --zookeeper quickstart-bigdata:2181

##### Topic - Alter
kafka-topics --alter --topic tweeter-tweets --partitions 3 --bootstrap-server quickstart-bigdata:2181

##### Topic - Delete
kafka-topics --delete --topic tweeter-tweets --zookeeper quickstart-bigdata:2181
kafka-topics --delete --topic tweeter-tweets --bootstrap-server quickstart-bigdata:9092

##### Command Line Producer :
kafka-console-producer --topic tweeter-tweets --broker-list quickstart-bigdata:9092

kafka-console-producer --topic tweeter-tweets --broker-list quickstart-bigdata:9092 --property parse.key=true --property key.separator=":"

##### Command Line Consumer :
kafka-console-consumer --topic tweeter-tweets --group pyspark-structured-stream-cg --bootstrap-server quickstart-bigdata:9092

listeners=PLAINTEXT://quickstart-bigdata:9092
advertised.listeners=PLAINTEXT://localhost:19092

#
### Create Hive Table
#
```
beeline -u jdbc:hive2://quickstart-bigdata:10000 

set hive.server2.enable.doAs=false;

use default;
drop table IF EXISTS tweeter_tweets;
CREATE TABLE if not exists tweeter_tweets (
    uuid STRING,
    text STRING, 
    words INT, 
    length INT
) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\\|'
STORED AS TEXTFILE;

select count(*) from tweeter_tweets;
```

#
### Create Cassandra Table
#
```
docker-compose -f dc-sandbox-cluster3.yml up -d cassandra


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

