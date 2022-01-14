#!/usr/bin/python2

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid4


def handle_rdd(rdd):
    if not rdd.isEmpty():
        global ss
        df = ss.createDataFrame(rdd, schema=['uuid', 'text', 'words', 'length'])
        df.show()
        df.write.saveAsTable(name='default.tweeter_tweets', format='hive', mode='append')

sc = SparkContext(appName="hive-stream-transformer")

ssc = StreamingContext(sc, 5)

ss = SparkSession.builder \
    .appName("hive-stream-transformer") \
    .enableHiveSupport() \
    .getOrCreate()

ss.sparkContext.setLogLevel('WARN')

TOPIC = 'tweeter-tweets'
ks = KafkaUtils.createDirectStream(ssc, [TOPIC], {'metadata.broker.list': 'localhost:19092'})

lines = ks.map(lambda x: x[1])

transform = lines.map(lambda tweet: (str(uuid4()), tweet, int(len(tweet.split())), int(len(tweet))))

transform.foreachRDD(handle_rdd)

ssc.start()

ssc.awaitTermination()


