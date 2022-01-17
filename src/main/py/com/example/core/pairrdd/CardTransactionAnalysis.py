#
#
#
import json
from pyspark import SparkContext, SparkConf


#
conf = SparkConf()\
    .setAppName("CardTransactionAnalysis")\
    .setMaster("local[4]")

#
#
sc = SparkContext.getOrCreate(conf=conf)
#sc.setLogLevel("WARN")
#
#
#

raw_rdd = sc.textFile("/datasets/card_transactions.json")
input_rdd = raw_rdd.map(lambda x: json.loads(x)).filter(lambda x: 1580515200 <= x.get("ts") < 1583020800).cache()
# for e0 in input_rdd.take(3): print(e0)

#
# 1. Total amount spent by each user
# [(userid, amount-1),(userid, amount-1)] --> [(userid, total-amount)]

user_expense_rdd = input_rdd.map(lambda x: (x.get('user_id'), x.get('amount')))
result_rdd = user_expense_rdd.reduceByKey(lambda x, y: x + y)
for e1 in result_rdd.take(3): print(e1)
