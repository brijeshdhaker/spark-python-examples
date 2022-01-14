#!/usr/bin/python2

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid4
import json

def handle_rdd(rdd):
    if not rdd.isEmpty():
        global ss, catalog
        df = ss.createDataFrame(rdd, schema=['uuid', 'text', 'words', 'length'])
        df.show()
        # .option("newtable", "5") \
        df.write.option("catalog", catalog).option("newtable", "5").format("org.apache.spark.sql.execution.datasources.hbase").save()
        #df.write.format("org.apache.hadoop.hbase.spark")\
        #    .option("hbase.columns.mapping", "uuid STRING :key, text STRING Sentence:text, words STRING Measure:words, length STRING Measure:length")\
        #    .option("hbase.table", "tweeter_tweets")\
        #    .option("hbase.spark.use.hbasecontext", False)\
        #    .save()



sc = SparkContext(appName="tweets-hbase-transformer")

ssc = StreamingContext(sc, 1)

ss = SparkSession.builder \
    .appName("tweets-hbase-transformer") \
    .enableHiveSupport() \
    .getOrCreate()

ss.sparkContext.setLogLevel('WARN')

catalogDict = {
    "table": {"namespace": "default", "name": "tweeter_tweets", "tableCoder": "PrimitiveType"},
    "rowkey": "key",
    "columns": {
        "uuid": {"cf": "rowkey", "col": "key", "type": "string"},
        "text": {"cf": "Sentence", "col": "text", "type": "string"},
        "words": {"cf": "Measure", "col": "words", "type": "string"},
        "length": {"cf": "Measure", "col": "length", "type": "string"}
    }
}
catalog = json.dumps(catalogDict)

TOPIC = 'tweeter-tweets'
ks = KafkaUtils.createDirectStream(ssc, [TOPIC], {'metadata.broker.list': 'localhost:19092'})

lines = ks.map(lambda x: x[1])

transform = lines.map(lambda tweet: (str(uuid4()), tweet, int(len(tweet.split())), int(len(tweet))))

transform.foreachRDD(handle_rdd)

ssc.start()
ssc.awaitTermination()
