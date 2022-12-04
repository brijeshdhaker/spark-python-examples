from datetime import datetime, timedelta
import pendulum
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.models import Variable

local_ist = pendulum.timezone("Asia/Kolkata")

default_args = {
    'owner': 'brijeshdhaker',
    'depends_on_past': False,
    'start_date': datetime(2020, 10, 10, tzinfo=local_ist),
    'email': ['brijeshdhaker@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(dag_id='spark_yarn_test',
          default_args=default_args,
          catchup=False,
          schedule_interval="0 * * * *",
          tags=["spark"])
pyspark_app_home = "/apps/hostpath/pyspark-apps/pyspark-airflow"

flight_search_ingestion = SparkSubmitOperator(task_id='flight_search_ingestion',
                                              conn_id='spark-yarn',
                                              application=f'{pyspark_app_home}/flat-map.py',
                                              total_executor_cores=4,
                                              packages="io.delta:delta-core_2.12:1.0.0",
                                              executor_cores=2,
                                              executor_memory='640m',
                                              driver_memory='640m',
                                              name='flight_search_ingestion',
                                              execution_timeout=timedelta(minutes=10),
                                              conf={
                                                  "spark.submit.deployMode": "cluster",
                                                  "spark.yarn.archive": "hdfs://namenode:9000/archives/spark-3.1.2.zip",
                                                  "spark.yarn.dist.archives": "hdfs://namenode:9000/archives/pyspark3.7-20221125.tar.gz#environment",
                                                  "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
                                                  "spark.sql.catalog.spark_catalog": "io.delta:delta-core_2.12:1.0.0"
                                              },
                                              dag=dag
                                              )

flight_search_waiting_time = SparkSubmitOperator(task_id='flight_search_waiting_time',
                                                 conn_id='spark-yarn',
                                                 application=f'{pyspark_app_home}/flat-map.py',
                                                 total_executor_cores=4,
                                                 packages="io.delta:delta-core_2.12:1.0.0",
                                                 executor_cores=2,
                                                 executor_memory='640M',
                                                 driver_memory='640M',
                                                 name='flight_search_waiting_time',
                                                 execution_timeout=timedelta(minutes=10),
                                                 conf={
                                                     "spark.submit.deployMode": "cluster",
                                                     "spark.yarn.archive": "hdfs://namenode:9000/archives/spark-3.1.2.zip",
                                                     "spark.yarn.dist.archives": "hdfs://namenode:9000/archives/pyspark3.7-20221125.tar.gz#environment",
                                                     "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
                                                     "spark.sql.catalog.spark_catalog": "io.delta:delta-core_2.12:1.0.0"
                                                 },
                                                 dag=dag
                                                 )

flight_nb_search = SparkSubmitOperator(task_id='flight_nb_search',
                                       conn_id='spark-yarn',
                                       application=f'{pyspark_app_home}/flat-map.py',
                                       total_executor_cores=4,
                                       packages="io.delta:delta-core_2.12:1.0.0",
                                       executor_cores=2,
                                       executor_memory='640M',
                                       driver_memory='640M',
                                       name='flight_nb_search',
                                       execution_timeout=timedelta(minutes=10),
                                       conf={
                                           "spark.submit.deployMode": "cluster",
                                           "spark.yarn.archive": "hdfs://namenode:9000/archives/spark-3.1.2.zip",
                                           "spark.yarn.dist.archives": "hdfs://namenode:9000/archives/pyspark3.7-20221125.tar.gz#environment",
                                           "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
                                           "spark.sql.catalog.spark_catalog": "io.delta:delta-core_2.12:1.0.0"
                                       },
                                       dag=dag
                                       )
flight_search_ingestion >> [flight_search_waiting_time, flight_nb_search]
