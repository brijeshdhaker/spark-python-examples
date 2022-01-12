#
#
#
python -m pip install --upgrade pip

#
#
#
conda create -n venv_spark
#conda env create venv_spark
conda env list
conda activate venv_spark
conda install pyspark==3.1.2

#
# 
#
jupyter toree install --spark_home /apps/spark --interpreters=Scala,PySpark,SQL --user

#
#
#
https://spark.apache.org/docs/latest/api/python/getting_started/quickstart.html

#
# For Grapths & Charts
#
pip3 install matplotlib
pip3 install PyQt5
sudo dnf install python3-tkinter

#
#
#
pip install confluent-kafka

#
# 
#
docker run -p 8080:8080 --rm 
-v /apps/hostpath/zeppelin/logs:/logs \
-v /apps/hostpath/zeppelin/notebook:/notebook \
-e ZEPPELIN_LOG_DIR='/logs' -e ZEPPELIN_NOTEBOOK_DIR='/notebook' \
--name zeppelin apache/zeppelin:0.9.0

#
#
# Run on a YARN cluster
export HADOOP_CONF_DIR=/opt/hadoop-2.7.4/etc/hadoop
#
./bin/spark-submit \
--class org.apache.spark.examples.SparkPi \
--master yarn \
--deploy-mode cluster \
--executor-memory 1G \
--num-executors 2 \
--conf "spark.yarn.archive=hdfs:///apps/spark-2.3.1/spark-2.3.1-jars.zip" \
/opt/spark-2.3.1/examples/jars/spark-examples_2.11-2.3.1.jar 2

#
#
#
$SPARK_HOME/bin/spark-submit \
--name "Sample Spark Application" \
--master local[*] \
--conf "spark.executorEnv.PYSPARK_DRIVER_PYTHON=python" \
--conf "spark.executorEnv.PYSPARK_PYTHON=./venv/bin/python" \
--archives "file:///apps/hostpath/spark/artifacts/venv.zip#venv" \
--py-files "file:///apps/hostpath/spark/artifacts/application.zip" /apps/hostpath/spark/artifacts/hello.py

#
#
#
docker exec spark-master /usr/local/spark/bin/spark-submit \
--name "Sample Spark Application" \
--master local[*] \
--py-files "file:///apps/hostpath/spark/artifacts/application.zip" /apps/hostpath/spark/artifacts/hello.py

#
#
#
docker exec spark-master /usr/local/spark/bin/spark-submit \
--name "Docker Spark Application" \
--master spark://spark-master:7077 \
--conf "spark.executorEnv.PYSPARK_DRIVER_PYTHON=python" \
--conf "spark.executorEnv.PYSPARK_PYTHON=./venv/bin/python" \
--archives "file:///apps/hostpath/spark/artifacts/venv.zip#venv" \
--py-files "file:///apps/hostpath/spark/artifacts/application.zip" /apps/hostpath/spark/artifacts/hello.py

#
#
#
$SPARK_HOME/bin/spark-submit \
--name "Sample Spark Application" \
--master spark://172.18.0.3:7077 \
--conf "spark.executorEnv.PYSPARK_DRIVER_PYTHON=python" \
--conf "spark.executorEnv.PYSPARK_PYTHON=./venv/bin/python" \
--archives "file:///apps/hostpath/spark/artifacts/venv.zip#venv" \
--py-files "file:///apps/hostpath/spark/artifacts/application.zip" /apps/hostpath/spark/artifacts/hello.py

#
#
#
$SPARK_HOME/bin/spark-submit \
--name "Sample Spark Application" \
--master spark://172.18.0.3:7077 \
--py-files "file:///apps/hostpath/spark/artifacts/application.zip" /apps/hostpath/spark/artifacts/hello.py


spark.kubernetes.driverEnv.[EnvironmentVariableName]
spark.executorEnv.[EnvironmentVariableName]

spark.kubernetes.pyspark.pythonVersion
spark.pyspark.python=
spark.pyspark.driver.python=

PYSPARK_PYTHON
PYSPARK_DRIVER_PYTHON

$SPARK_HOME/bin/spark-submit \
--master "k8s://https://raspberry:6443" \
--deploy-mode "cluster" \
--name "spark-pi" \
--conf "spark.executor.instances=2" \
--conf "spark.kubernetes.file.upload.path=/apps/hostpath/spark/cluster-uploads" \
--conf "spark.pyspark.python=python3" \
--conf "spark.pyspark.driver.python=./venv/bin/python" \
--conf "spark.kubernetes.container.image=spark-py:3.1.2" \
--conf "spark.kubernetes.authenticate.driver.serviceAccountName=spark" \
--conf "spark.kubernetes.driver.volumes.hostPath.hostpath-volume.mount.path=/apps/hostpath/spark" \
--conf "spark.kubernetes.driver.volumes.hostPath.hostpath-volume.mount.readOnly=false" \
--conf "spark.kubernetes.driver.volumes.hostPath.hostpath-volume.options.path=/apps/hostpath/spark" \
--conf "spark.kubernetes.driver.volumes.hostPath.hostpath-volume.options.type=Directory" \
--conf "spark.kubernetes.executor.volumes.hostPath.hostpath-volume.mount.path=/apps/hostpath/spark" \
--conf "spark.kubernetes.executor.volumes.hostPath.hostpath-volume.mount.readOnly=false" \
--conf "spark.kubernetes.executor.volumes.hostPath.hostpath-volume.options.path=/apps/hostpath/spark" \
--conf "spark.kubernetes.executor.volumes.hostPath.hostpath-volume.options.type=Directory" \
--conf "spark.driver.extraJavaOptions=-Divy.cache.dir=/tmp -Divy.home=/tmp" \
--archives "local:///apps/hostpath/spark/artifacts/py/venv.zip#venv" \
--py-files "local:///apps/hostpath/spark/artifacts/py/application.zip" \
local:///apps/hostpath/spark/artifacts/py/py-hello.py

--class "org.apache.spark.examples.SparkPi \
local:///opt/spark/examples/jars/spark-examples_2.12-3.1.2.jar
