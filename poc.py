import findspark
import re
findspark.init('/apps/spark')
import pyspark

COMMA_DELIMITER = ',(?=([^"]*"[^"]*")*[^"]*$)'
COMMA_DELIMITER = ',(?=([^"\\]*"\\[^"\\]*"\\)*[^"\\]*$)'

def myFun(x):
    splits = re.split(r",", x)
    return splits[1]+", "+splits[6]

line = '1,"Goroka","Goroka","Papua New Guinea","GKA","AYGA",-6.081689,145.391881,5282,10,"U","Pacific/Port_Moresby"'
# line = line.replace('"', '')
cols = re.split(r",(?![^(]*?\))\s*", line)
val = float(cols[6])
print(val > 40 )

