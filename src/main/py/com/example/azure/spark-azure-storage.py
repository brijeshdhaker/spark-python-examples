from __future__ import print_function
from pyspark.sql import SparkSession
from pyspark.sql.functions import when
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType
from pyspark.mllib.regression import LabeledPoint

if __name__ == "__main__":
    spark = SparkSession.builder.appName("spark-azure-store").getOrCreate()
    sc=spark.sparkContext

    #
    # Load data from Azure Storage
    #
    df = spark.read.csv(
        "wasbs://container001@csg100320025a786393.blob.core.windows.net/flight_weather.csv",
        header=True,
        nullValue="NA",
        inferSchema=True
    )

    #
    # Select only label and features
    #
    df = df.select(
        "ARR_DEL15",
        "MONTH",
        "DAY_OF_MONTH",
        "DAY_OF_WEEK",
        "UNIQUE_CARRIER",
        "ORIGIN",
        "DEST",
        "CRS_DEP_TIME",
        "CRS_ARR_TIME",
        "RelativeHumidityOrigin",
        "AltimeterOrigin",
        "DryBulbCelsiusOrigin",
        "WindSpeedOrigin",
        "VisibilityOrigin",
        "DewPointCelsiusOrigin",
        "RelativeHumidityDest",
        "AltimeterDest",
        "DryBulbCelsiusDest",
        "WindSpeedDest",
        "VisibilityDest",
        "DewPointCelsiusDest")

    #
    # Drop rows having null field
    #

    df = df.dropna()

    #
    # Convert categorical value to numeric index (0, 1, ...)
    #

    # MONTH
    df = df.withColumn("MONTH", df.MONTH - 1)

    # DAY_OF_MONTH
    df = df.withColumn("DAY_OF_MONTH", df.DAY_OF_MONTH - 1)

    # DAY_OF_WEEK
    df = df.withColumn("DAY_OF_WEEK", df.DAY_OF_WEEK - 1)

    # UNIQUE_CARRIER
    rows_unique_carrier = df.select("UNIQUE_CARRIER").distinct().collect()
    list_unique_carrier = [i.UNIQUE_CARRIER for i in rows_unique_carrier]
    convUniqueCarrier = udf(
        lambda x: list_unique_carrier.index(x), IntegerType())
    df = df.withColumn("UNIQUE_CARRIER",
                       when(df["UNIQUE_CARRIER"].isNotNull(),
                            convUniqueCarrier(df.UNIQUE_CARRIER)).otherwise(len(list_unique_carrier)))

    # ORIGIN
    rows_origin = df.select("ORIGIN").distinct().collect()
    list_origin = [i.ORIGIN for i in rows_origin]
    convOrigin = udf(lambda x: list_origin.index(x), IntegerType())
    df = df.withColumn("ORIGIN",
                       when(df["ORIGIN"].isNotNull(),
                            convOrigin(df.ORIGIN)).otherwise(len(list_origin)))

    # DEST
    rows_dest = df.select("DEST").distinct().collect()
    list_dest = [i.DEST for i in rows_dest]
    convDest = udf(lambda x: list_dest.index(x), IntegerType())
    df = df.withColumn("DEST",
                       when(df["DEST"].isNotNull(),
                            convDest(df.DEST)).otherwise(len(list_dest)))

    #
    # Create LabeledPoint object (label is "ARR_DEL15")
    #
    rdd = df.rdd.map(
        lambda row: LabeledPoint(
            row.ARR_DEL15,
            [
                row.MONTH,
                row.DAY_OF_MONTH,
                row.DAY_OF_WEEK,
                row.UNIQUE_CARRIER,
                row.ORIGIN,
                row.DEST,
                row.CRS_DEP_TIME,
                row.CRS_ARR_TIME,
                row.RelativeHumidityOrigin,
                row.AltimeterOrigin,
                row.DryBulbCelsiusOrigin,
                row.WindSpeedOrigin,
                row.VisibilityOrigin,
                row.DewPointCelsiusOrigin,
                row.RelativeHumidityDest,
                row.AltimeterDest,
                row.DryBulbCelsiusDest,
                row.WindSpeedDest,
                row.VisibilityDest,
                row.DewPointCelsiusDest
            ]))

    #
    # Split data for training (70%) and testing (30%)
    #
    trainrdd, testrdd = rdd.randomSplit([0.7, 0.3], 17)

    #
    # Run Decision Tree algorithms in MLlib
    #
    from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
    model = DecisionTree.trainClassifier(
        trainrdd,
        numClasses=2,
        categoricalFeaturesInfo={
            0: 12,
            1: 31,
            2: 7,
            3: len(list_unique_carrier) + 1,
            4: len(list_origin) + 1,
            5: len(list_dest) + 1,
            6: 24,
            7: 24},
        impurity='entropy',
        maxDepth=15,
        maxBins=3000)

    #
    # Save model in Azure blob
    #
    model.save(sc, "wasbs://container01@dummyst.blob.core.windows.net/model/flightdelay")

    #
    # Predict using test data and set row index
    #
    preds = model.predict(testrdd.map(lambda p: p.features))
    preds = preds.zipWithIndex()
    preds = preds.map(lambda x: (x[1], x[0]))

    #
    # Get actual label and set row index
    #
    labels = testrdd.map(lambda x: x.label)
    labels = labels.zipWithIndex()
    labels = labels.map(lambda x: (x[1], x[0]))

    #
    # Join and Get accuracy
    #
    labels_and_preds = labels.join(preds)
    accuracy = labels_and_preds.filter(
        lambda x: x[1][0] == x[1][1]).count() / float(testrdd.count())
    print("Accuracy is %f" % accuracy)  # output accuracy

    spark.stop()