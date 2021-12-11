#
#
#
import re

COMMA_DELIMITER_1 = ',(?=([^"]*"[^"]*")*[^"]*$)'
COMMA_DELIMITER_2 = ',(?=([^"\\]*"\\[^"\\]*"\\)*[^"\\]*$)'

#
#
def print_separator():
    print(" " * 30)
    print(" #" * 30)
    print(" " * 30)

#
# line2 = '1;"Goroka";"Goroka";"Papua New Guinea";"GKA";"AYGA";-6.081689;145.391881;5282;10;"U";"Pacific/Port_Moresby"'
# records = commons.split_csv(";", line2)
# print(float(records[6]) > 40)
#
#
def split_csv(d, x):
    splits = re.split(r"{}".format(d), x)
    return splits

#
# line = '1,"Goroka","Goroka","Papua New Guinea","GKA","AYGA",-6.081689,145.391881,5282,10,"U","Pacific/Port_Moresby"'
# cols = commons.split_csv_line(line)
#
def split_csv_line(line):
    cols = re.split(r",(?![^(]*?\))\s*", line)
    return cols


# We can test function by calling it.
if __name__ == "__main__":

    line = '1,"Goroka","Goroka","Papua New Guinea","GKA","AYGA",-6.081689,145.391881,5282,10,"U","Pacific/Port_Moresby"'
    cols = split_csv_line(line)
    records = split_csv(",", line)