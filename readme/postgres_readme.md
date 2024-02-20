
# 

```shell
-$  /bin/psql -h localhost -p 5432 -U postgres postgres
```

# list schemas
```sqlite-psql
postgres-# \l
```

# List tables
```sqlite-psql
postgres-# \dt

postgres=# \c testdb;
```

\list or \l: list all databases

\c <db name>: connect to a certain database

\dt: list all tables in the current database using your search_path

\dt *.: list all tables in the current database regardless your search_path

\dn+ --list schemas

postgres=# DROP DATABASE testdb;