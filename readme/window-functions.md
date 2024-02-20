
$HIVE_HOME/bin/beeline -u jdbc:hive2://hive-server.sandbox.net:10000 scott tiger

```scala
val dataset = Seq(
("Thin",       "cell phone", 6000),
("Normal",     "tablet",     1500),
("Mini",       "tablet",     5500),
("Ultra thin", "cell phone", 5000),
("Very thin",  "cell phone", 6000),
("Big",        "tablet",     2500),
("Bendable",   "cell phone", 3000),
("Foldable",   "cell phone", 3000),
("Pro",        "tablet",     4500),
("Pro2",       "tablet",     6500)).toDF("product", "category", "revenue")

dataset.write.saveAsTable("default.PRODUCT_REVENUE")
dataset.show

// dataset.write.saveAsTable(name="default.PRODUCT_REVENUE", format="hive", mode="append")
// dataset.show

+----------+----------+-------+
|   product|  category|revenue|
+----------+----------+-------+
|      Thin|cell phone|   6000|
|    Normal|    tablet|   1500|
|      Mini|    tablet|   5500|
|Ultra thin|cell phone|   5000|
| Very thin|cell phone|   6000|
|       Big|    tablet|   2500|
|  Bendable|cell phone|   3000|
|  Foldable|cell phone|   3000|
|       Pro|    tablet|   4500|
|      Pro2|    tablet|   6500|
+----------+----------+-------+


```
```scala

scala> dataset.where('category === "tablet").show
+-------+--------+-------+
|product|category|revenue|
+-------+--------+-------+
| Normal|  tablet|   1500|
|   Mini|  tablet|   5500|
|    Big|  tablet|   2500|
|    Pro|  tablet|   4500|
|   Pro2|  tablet|   6500|
+-------+--------+-------+
```

```roomsql
SELECT
product,
category,
revenue,
rank() OVER (PARTITION BY category ORDER BY revenue DESC) as rank,
dense_rank() OVER (PARTITION BY category ORDER BY revenue DESC) as dense_rank
FROM PRODUCT_REVENUE;

+-------------+-------------+----------+-------+-------------+
|   product   |  category   | revenue  | rank  | dense_rank  |
+-------------+-------------+----------+-------+-------------+
| Very thin   | cell phone  | 6000     | 1     | 1           |
| Thin        | cell phone  | 6000     | 1     | 1           |
| Ultra thin  | cell phone  | 5000     | 3     | 2           |
| Foldable    | cell phone  | 3000     | 4     | 3           |
| Bendable    | cell phone  | 3000     | 4     | 3           |
| Pro2        | tablet      | 6500     | 1     | 1           |
| Mini        | tablet      | 5500     | 2     | 2           |
| Pro         | tablet      | 4500     | 3     | 3           |
| Big         | tablet      | 2500     | 4     | 4           |
| Normal      | tablet      | 1500     | 5     | 5           |
+-------------+-------------+----------+-------+-------------+

```

```roomsql

SELECT
product,
category,
revenue,
dense_rank() OVER (PARTITION BY category ORDER BY revenue DESC) as rank
FROM PRODUCT_REVENUE;

+-------------+-------------+----------+-------+
| Very thin   | cell phone  | 6000     | 1     |
| Thin        | cell phone  | 6000     | 1     |
| Ultra thin  | cell phone  | 5000     | 2     |
| Foldable    | cell phone  | 3000     | 3     |
| Bendable    | cell phone  | 3000     | 3     |
| Pro2        | tablet      | 6500     | 1     |
| Mini        | tablet      | 5500     | 2     |
| Pro         | tablet      | 4500     | 3     |
| Big         | tablet      | 2500     | 4     |
| Normal      | tablet      | 1500     | 5     |
+-------------+-------------+----------+-------+

```

### 1. What are the best-selling and the second best-selling products in every category?
```roomsql
SELECT
    product,
    category,
    revenue
FROM (
    SELECT
    product,
    category,
    revenue,
    dense_rank() OVER (PARTITION BY category ORDER BY revenue DESC) as rank
    FROM PRODUCT_REVENUE
) tmp
WHERE
rank <= 2
```

```scala
import org.apache.spark.sql.expressions.Window
val overCategory = Window.partitionBy('category).orderBy('revenue.desc)
val ranked = data.withColumn("rank", dense_rank.over(overCategory))
scala> ranked.show

+----------+----------+-------+----+
|   product|  category|revenue|rank|
+----------+----------+-------+----+
|      Pro2|    tablet|   6500|   1|
|      Mini|    tablet|   5500|   2|
|       Pro|    tablet|   4500|   3|
|       Big|    tablet|   2500|   4|
|    Normal|    tablet|   1500|   5|
|      Thin|cell phone|   6000|   1|
| Very thin|cell phone|   6000|   1|
|Ultra thin|cell phone|   5000|   2|
|  Bendable|cell phone|   3000|   3|
|  Foldable|cell phone|   3000|   3|
+----------+----------+-------+----+


scala> ranked.where('rank <= 2).show

+----------+----------+-------+----+
|   product|  category|revenue|rank|
+----------+----------+-------+----+
|      Pro2|    tablet|   6500|   1|
|      Mini|    tablet|   5500|   2|
|      Thin|cell phone|   6000|   1|
| Very thin|cell phone|   6000|   1|
|Ultra thin|cell phone|   5000|   2|
+----------+----------+-------+----+
```