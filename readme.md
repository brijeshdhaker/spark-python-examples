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