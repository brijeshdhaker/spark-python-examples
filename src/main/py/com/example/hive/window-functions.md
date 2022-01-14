
$HIVE_HOME/bin/beeline -u jdbc:hive2://quickstart-bigdata:10000 scott tiger
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

```
dataset.write.saveAsTable(name='default.PRODUCT_REVENUE', format='hive', mode='append')
dataset.show

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

scala> data.where('category === "tablet").show
+-------+--------+-------+
|product|category|revenue|
+-------+--------+-------+
| Normal|  tablet|   1500|
|   Mini|  tablet|   5500|
|    Big|  tablet|   2500|
|    Pro|  tablet|   4500|
|   Pro2|  tablet|   6500|
+-------+--------+-------+

SELECT
product,
category,
revenue,
rank() OVER (PARTITION BY category ORDER BY revenue DESC) as rank,
dense_rank() OVER (PARTITION BY category ORDER BY revenue DESC) as dense_rank
FROM PRODUCT_REVENUE;

SELECT
product,
category,
revenue,
dense_rank() OVER (PARTITION BY category ORDER BY revenue DESC) as rank
FROM PRODUCT_REVENUE;

### 1. What are the best-selling and the second best-selling products in every category?
```sql
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

```
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
```

scala> ranked.where('rank <= 2).show
```
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