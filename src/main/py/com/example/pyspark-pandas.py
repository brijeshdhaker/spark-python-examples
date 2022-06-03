import pandas as pd
from pyspark.sql.functions import pandas_udf
from pyspark.sql import SparkSession

def main(spark):

    @pandas_udf("col1 string, col2 long")
    def func(s1: pd.Series, s2: pd.Series, s3: pd.DataFrame) -> pd.DataFrame:
        s3['col2'] = s1 + s2.str.len()
        return s3

    # Create a Spark DataFrame that has three columns including a struct column.
    df = spark.createDataFrame(
        [[1, "a string", ("a nested string",)]],
        "long_col long, string_col string, struct_col struct<col1:string>")

    df.printSchema()
    # root
    # |-- long_column: long (nullable = true)
    # |-- string_column: string (nullable = true)
    # |-- struct_column: struct (nullable = true)
    # |    |-- col1: string (nullable = true)

    df.select(func("long_col", "string_col", "struct_col")).printSchema()
    # |-- func(long_col, string_col, struct_col): struct (nullable = true)
    # |    |-- col1: string (nullable = true)
    # |    |-- col2: long (nullable = true)


if __name__ == "__main__":

    session = SparkSession.builder.getOrCreate()
    session.sparkContext.setLogLevel("WARN")
    session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    main(session)