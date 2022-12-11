
#
# Create Table
# 
create 'test_table', 'cf'

#
# Add Data
# 
put 'test_table', 'row1', 'cf:a', 'value-A'
put 'test_table', 'row2', 'cf:b', 'value-B'
put 'test_table', 'row3', 'cf:c', 'value-C'

#
# Delete Record
#
deleteall 'emp', '1'

#
# List Tables
# 
list 

### 4.
list 'test_table'

### 5.
describe 'test_table'

### 6.
scan 'test_table'

### 7.
get 'test_table', 'row1'

### 8. Disable Table
disable 'test_table'

### 9. Drop Table
drop 'test_table'