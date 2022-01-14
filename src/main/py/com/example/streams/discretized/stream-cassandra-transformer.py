#!/usr/bin/python2

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid4

#
#
def handle_rdd(rdd):
    if not rdd.isEmpty():
        global ss
        df = ss.createDataFrame(rdd, schema=['uuid', 'text', 'words', 'length'])
        df.show()
        df.write.format("org.apache.spark.sql.cassandra").options(table="tweeter_tweets", keyspace="spark_stream").save(mode="append")

#
#
conf = SparkConf("tweets-cassandra-transformer")\
    .setMaster("local[*]")\
    .set("spark.cassandra.connection.host", "127.0.0.1")

sc = SparkContext().getOrCreate(conf=conf)
ssc = StreamingContext(sc, 5)
#ssc.checkpoint(".checkpoint")

ss = SparkSession.builder \
    .appName("tweets-cassandra-transformer") \
    .enableHiveSupport() \
    .getOrCreate()

ss.sparkContext.setLogLevel('WARN')

TOPIC = 'tweeter-tweets'
kafkaParams = {
    'metadata.broker.list': 'quickstart-bigdata:9092',
    'group.id': 'tweet_stream_cassandra_cg',
    'auto.offset.reset': 'largest'
}
ks = KafkaUtils.createDirectStream(ssc, [TOPIC], kafkaParams)

lines = ks.map(lambda x: x[1])

transform = lines.map(lambda tweet: (str(uuid4()), tweet, int(len(tweet.split())), int(len(tweet))))

transform.foreachRDD(handle_rdd)

ssc.start()
ssc.awaitTermination()
