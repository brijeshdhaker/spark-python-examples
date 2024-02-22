#
# Beeline Shell Commands
#

# The output should be:
| COMMAND                 | DESCRIPTION                                                                       | EXAMPLE                                             |
|-------------------------|:----------------------------------------------------------------------------------|:----------------------------------------------------|
| !help                   | Print a summary of command usage                                                  |                                                     |
| !quit                   | Exits the Beeline client.                                                         |                                                     |
| !history                | Display the command history                                                       |                                                     |
| !table <sql_query_file> | Run SQL query from file                                                           |                                                     |
| set                     | Prints a list of configuration variables that are overridden by the user or Hive. |                                                     |
| set -v                  | Prints all Hadoop and Hive configuration variables.                               |                                                     |
| reset                   | Resets the configuration to the default values.                                   |                                                     |
| !record <file_name>     | Save result set to a file in local file system                                    | !record /user/dummy_local_user/myquery1_results.out |
| !sh                     | Run shell CMD                                                                     | !sh date                                            |
| !sh hadoop fs           | Run HDFS CMD                                                                      | !sh hadoop fs -ls /                                 |
| !dbinfo                 | Check Hive version                                                                |                                                     |
| dfs                     | Executes a dfs command.                                                           | dfs -ls /user ;                                     |

#
# Beeline Command line options
#
COMMAND	DESCRIPTION	BEELINE COMMAND LINE OPTION	INSIDE BEELINE SHELL
Ctrl + r	Search on history of commands		
Autocomplete	Press Tab key
Display all 436 possibilities? (y or n)
If you enter y, you’ll get a long list of all the keywords		
Navigation Keystrokes	Use the up↑ and down↓ arrow keys to scroll through previous commands
Ctrl+A goes to the beginning of the line
Ctrl+E goes to the end of the line
Delete key will delete the character to the left of the cursor		
set system:user.name; (or)
set system:user.name=yourusername;	System Namespace (provides read-write access to Java system properties)
set env:HOME; env Namespace (provides read-only access to environment variables)

-- Comment line1
-- Comment line2
Comments in Hive Scripts.		
beeline -e < Hive query >	Run query	beeline -e " show databases"
beeline -f < Hive query >	Run query from file	beeline -f /user/dummy_local_user/myquery1.sql
--hiveconf property=value
(or)
SET property=value;	Use value for the given configuration property. Properties that are listed in hive.conf.restricted.list cannot be reset with hiveconf	beeline --hiveconf hive.auto.convert.join=false;
--Display the configuration value
SET hive.auto.convert.join;

SET hive.auto.convert.join=false;
--Display the configuration value
SET hive.auto.convert.join;

--hivevar name=value
(or)
SET name=value;	Hive variable name and value.
This is a Hive-specific setting in which variables can be set at the session level and referenced in Hive commands or queries.	beeline --hivevar myvar=hello
--Display the variable value
SELECT "${myvar}";


SET hivevar:myvar=hello;
--Display the variable value
SELECT "${myvar}";

outputformat	Format mode for result display. Default is table. Options [
csv/tsv/csv2/tsv2/dsv/
table/
vertical/
xmlattr/
xmlelements
]	beeline --outputformat=tsv2	Ex: !set outputformat tsv2
Ex: !set outputformat xmlattr
Result of the query select id, value, comment from test_table






color	Control whether color is used for display. Default is false	beeline --color=true	!set color true
verbose	Show verbose error messages and debug information (true) or do not show (false). Default is false.	beeline --verbose=true	!set verbose true
headerInterval	The interval for redisplaying column headers, in number of rows, when outputformat is table. Default is 100.	beeline --headerInterval=true	!set headerInterval 10000
showHeader	Show column names in query results (true) or not (false). Default is true.	beeline --showHeader=true	!set showHeader false
force	Continue running script even after errors (true) or do not continue (false). Default is false.	beeline --force=true	!set force true
silent	Reduce the amount of informational messages displayed (true) or not (false).
It also stops displaying the log messages for the query from HiveServer2.
Default is false.	beeline --silent=true	!set silent true
delimiterForDSV	The delimiter for delimiter-separated values output format. Default is ‘|’ character.	beeline --outputformat=dsv --delimiterForDSV="-"	!set outputformat dsv
!set delimiterForDSV “-”
Hive queries


PURPOSE	QUERY
Display current database being used	
```shell
SELECT CURRENT_DATABASE();
```

Load data from a local file to the hive table	
```shell
LOAD DATA LOCAL INPATH '/unix-path/myfile' INTO TABLE mytable;
```

Load data from hdfs file to the hive table	
```shell
LOAD DATA INPATH '/hdfs-path/myfile' INTO TABLE mytable;
```