---
--- Add User
---
CREATE USER 'brijeshdhaker'@'%' IDENTIFIED BY 'Accoo7@k47';
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'brijeshdhaker'@'%' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'superuser'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

SHOW GRANTS FOR 'brijeshdhaker'@'%';
---


create database SANDBOXDB;

SHOW DATABASES;

USE SANDBOXDB;

show tables;

drop table if exists kafka_stream_data;
create table kafka_stream_data(stream_key varchar(50), stream_value varchar(512));

drop table if exists kafka_topic_offsets;
create table kafka_topic_offsets(topic_name varchar(50), `partition` int, `offset` BigInt);
commit;

truncate table SANDBOXDB.kafka_topic_offsets;

insert into kafka_topic_offsets values('kafka-python-partitioned-topic', 0, 0);
insert into kafka_topic_offsets values('kafka-python-partitioned-topic', 1, 0);
insert into kafka_topic_offsets values('kafka-python-partitioned-topic', 2, 0);
insert into kafka_topic_offsets values('kafka-python-partitioned-topic', 3, 0);
insert into kafka_topic_offsets values('kafka-python-partitioned-topic', 4, 0);

commit;

update kafka_topic_offsets set offset=0 where topic_name='kafka-python-partitioned-topic';

update kafka_topic_offsets set offset=0 where topic_name='kafka-python-partitioned-topic' and `partition`=0;
update kafka_topic_offsets set offset=0 where topic_name='kafka-python-partitioned-topic' and `partition`=1;
update kafka_topic_offsets set offset=0 where topic_name='kafka-python-partitioned-topic' and `partition`=2;
update kafka_topic_offsets set offset=0 where topic_name='kafka-python-partitioned-topic' and `partition`=3;
update kafka_topic_offsets set offset=0 where topic_name='kafka-python-partitioned-topic' and `partition`=4;

update kafka_topic_offsets set topic_name='kafka-python-partitioned-topic';

commit;

select * from kafka_topic_offsets;

select count(*) from kafka_stream_data;
select * from kafka_stream_data;


