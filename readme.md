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
docker run -p 8080:8080 --rm -v /apps/hostpath/zeppelin/logs:/logs -v /apps/hostpath/zeppelin/notebook:/notebook \
-e ZEPPELIN_LOG_DIR='/logs' -e ZEPPELIN_NOTEBOOK_DIR='/notebook' \
--name zeppelin apache/zeppelin:0.9.0

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

