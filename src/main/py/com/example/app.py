import os
import numpy as np  # type: ignore[import]
import pandas as pd  # type: ignore[import]
from pyspark.sql.functions import pandas_udf
from pyspark.sql import SparkSession
from typing import Iterator
from pyspark.sql.pandas.utils import require_minimum_pandas_version, require_minimum_pyarrow_version

require_minimum_pandas_version()
require_minimum_pyarrow_version()

# This is only needed for windows
def setEnv():

    # Replace with your Spark dir in windows
    os.environ['PYSPARK_DRIVER_PYTHON'] = '/opt/conda/envs/pyspark3.7/bin/python'
    os.environ['PYSPARK_PYTHON'] = '/opt/conda/envs/pyspark3.7/bin/python'

    print(os.environ['SPARK_HOME'])


def main(spark):
    pdf = pd.DataFrame([1, 2, 3], columns=["x"])
    df = spark.createDataFrame(pdf)

    # Declare the function and create the UDF
    @pandas_udf("long")
    def plus_one(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
        for x in iterator:
            yield x + 1

    df.select(plus_one("x")).show()


if __name__ == "__main__":

    # If running on windows , set env variables , for Linux skip
    if os.name == 'nt':
        setEnv()

    session = SparkSession.builder.getOrCreate()
    session.sparkContext.setLogLevel("WARN")
    # Enable Arrow-based columnar data transfers
    session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    #
    main(session)