
### 1.
create 'test_table', 'cf'
### 2.
put 'test_table', 'row1', 'cf:a', 'value-A'
put 'test_table', 'row2', 'cf:b', 'value-B'
put 'test_table', 'row3', 'cf:c', 'value-C'

### 3.
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