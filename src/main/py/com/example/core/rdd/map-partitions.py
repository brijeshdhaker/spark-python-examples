#
#
#
import com.example.utils.commons as commons
#
from pyspark.sql import SparkSession

if __name__ == "__main__":
    #    if len(sys.argv) != 3:
    #        print("Usages: spark-file <inpath> <outpath>")
    #        sys.exit(-1)

    def formatWithYield(partition_data):
        for record in partition_data:
            sex = 'Female' if  record.sex == 'F' else 'Male'
            bonus = record.salary * 10/100
            yield record.first + " " + record.last, sex, record.salary, bonus

    def formatWithIter(partition_data):
        p_data = []
        for record in partition_data:
            sex = 'Female' if  record.sex == 'F' else 'Male'
            bonus = record.salary * 10/100
            p_data.append([record.first + " " + record.last, sex, record.salary, bonus])
        return iter(p_data)

    #
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("PythonRDD-MapPartition") \
        .getOrCreate()


    data = [
        ('Brijesh', 'Dhaker', 'M', 10000),
        ('Neeta', 'Dhakad', 'F', 70000),
        ('Keshvi', 'Dhaker', 'F', 20000),
        ('Tejas', 'Kumar', 'M', 45000),
        ('Sunil', 'Gupta', 'M', 10000)
    ]
    columns = ['first', 'last', 'sex', 'salary']

    df1 = spark.createDataFrame(data=data, schema=columns)
    df1.printSchema()

    print("DF-1 Partition Count : %i " % (df1.rdd.getNumPartitions()))
    # print(rdd_1.glom().collect())

    commons.print_separator()

    df2 = df1.rdd.mapPartitions(formatWithYield).toDF(['fullname', 'sex', 'salary', 'bonus'])
    print("DF-2 Partition count after transformation is : %i " % (df2.rdd.getNumPartitions()))
    df2.printSchema()
    df2.show()

    commons.print_separator()
    df3 = df1.rdd.mapPartitions(formatWithIter).toDF(['fullname', 'sex', 'salary', 'bonus'])
    print("DF-3 Partition count after transformation is : %i " % (df3.rdd.getNumPartitions()))
    df3.printSchema()
    df3.show()


    #
    spark.stop()
