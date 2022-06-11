create database SANDBOXDB;
use SANDBOXDB;

show tables;

create table kafka_stream_data(stream_key varchar(50), stream_value varchar(512));

drop table if exists kafka_topic_offsets;
create table kafka_topic_offsets(topic_name varchar(50), `partition` int, `offset` BigInt);
commit;


insert into kafka_topic_offsets values('partitioned-test-topic', 0, 0);
insert into kafka_topic_offsets values('partitioned-test-topic', 1, 0);
insert into kafka_topic_offsets values('partitioned-test-topic', 2, 0);
insert into kafka_topic_offsets values('partitioned-test-topic', 3, 0);
insert into kafka_topic_offsets values('partitioned-test-topic', 4, 0);

update kafka_topic_offsets set offset=0 where topic_name='partitioned-test-topic' and `partition`=0

commit;

select count(*) from kafka_stream_data;
select * from kafka_stream_data;
select * from kafka_topic_offsets;

update kafka_topic_offsets set `offset`=999 where `topic_name`='partitioned-test-topic' and `partition`=1
update kafka_topic_offsets set `offset`=256 where `topic_name`='partitioned-test-topic' and `partition`=2
update kafka_topic_offsets set `offset`=733 where `topic_name`='partitioned-test-topic' and `partition`=3
update kafka_topic_offsets set `offset`=2012 where `topic_name`='partitioned-test-topic' and `partition`=0

update kafka_topic_offsets set `offset`=256 where `topic_name`='partitioned-test-topic' and `partition`=2
update kafka_topic_offsets set `offset`=1244 where `topic_name`='partitioned-test-topic' and `partition`=1
update kafka_topic_offsets set `offset`=2503 where `topic_name`='partitioned-test-topic' and `partition`=0
update kafka_topic_offsets set `offset`=998 where `topic_name`='partitioned-test-topic' and `partition`=3


update kafka_topic_offsets set `offset`=256 where `topic_name`='partitioned-test-topic' and `partition`=2
update kafka_topic_offsets set `offset`=1489 where `topic_name`='partitioned-test-topic' and `partition`=1
update kafka_topic_offsets set `offset`=1248 where `topic_name`='partitioned-test-topic' and `partition`=3
update kafka_topic_offsets set `offset`=3009 where `topic_name`='partitioned-test-topic' and `partition`=0