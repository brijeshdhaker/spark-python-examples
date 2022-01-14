#
#
#
import re
import random
import time

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


def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)

# We can test function by calling it.
if __name__ == "__main__":

    line = '1,"Goroka","Goroka","Papua New Guinea","GKA","AYGA",-6.081689,145.391881,5282,10,"U","Pacific/Port_Moresby"'
    cols = split_csv_line(line)
    records = split_csv(",", line)

