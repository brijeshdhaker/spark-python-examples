
# Kafka - Broker Validations
```shell

docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkaclient sh -c "kafkacat -V"

docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker /bin/bash

```

#
### Topic - Actions :
#
```shell

docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker /bin/bash

kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 1 --replication-factor 1 --topic kafka-simple-topic --if-not-exists
kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 4 --replication-factor 1 --topic kafka-partitioned-topic --if-not-exists
kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 3 --replication-factor 1 --topic kafka-avro-topic --if-not-exists
kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 3 --replication-factor 1 --topic kafka-json-topic --if-not-exists

kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 3 --replication-factor 1 --topic transaction-text-topic --if-not-exists
kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 3 --replication-factor 1 --topic transaction-json-topic --if-not-exists
kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 3 --replication-factor 1 --topic transaction-avro-topic --if-not-exists

# Topic - List
kafka-topics --list --bootstrap-server kafkabroker.sandbox.net:9092
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-topics --list --bootstrap-server kafkabroker.sandbox.net:9092"

# Topic - Describe
kafka-topics --describe --topic kafka-simple-topic --bootstrap-server kafkabroker.sandbox.net:9092
docker compose -f  docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-topics --describe --topic kafka-simple-topic --bootstrap-server kafkabroker.sandbox.net:9092 "

# Topic - Alter
kafka-topics --alter --topic kafka-partitioned-topic --partitions 5 --bootstrap-server kafkabroker.sandbox.net:9092
docker compose -f  docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-topics --alter --topic kafka-partitioned-topic --partitions 5 --bootstrap-server kafkabroker.sandbox.net:9092 "

# Topic - Delete
kafka-topics --delete --topic kafka-simple-topic --bootstrap-server kafkabroker.sandbox.net:9092
docker compose -f  docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-topics --delete --topic kafka-simple-topic --bootstrap-server kafkabroker.sandbox.net:9092 "

# Topic - Check Retention period
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-configs --bootstrap-server kafkabroker.sandbox.net:9092 --entity-type topics --entity-name kafka-simple-topic --describe "
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-configs --bootstrap-server kafkabroker.sandbox.net:9092 --entity-type topics --entity-default --alter --add-config delete.retention.ms=172800000 "

### Change Kafka Retention Time
docker compose -f  docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-topics --bootstrap-server kafkabroker.sandbox.net:9092 --alter --topic kafka-avro-topic --config retention.ms=1000 "
docker compose -f  docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-topics --bootstrap-server localhost:9092 --topic kafka-simple-topic --create --partitions 3 --replication-factor 1 "

### Setup Default  7 days (168 hours , retention.ms= 604800000)
```

#
### Producer :
#

```shell

docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-console-producer \
--topic kafka-simple-topic \
--broker-list kafkabroker.sandbox.net:9092"

#### With Key
#### Note : \t is default key seperator
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-console-producer \
--topic kafka-simple-topic \
--broker-list kafkabroker.sandbox.net:9092 \
--producer.config /apps/sandbox/kafka/cnf/client_plaintext.config \
--property parse.key=true \
< /apps/sandbox/kafka/json_messages.txt \
2>/dev/null"

# --property parse.key=true \
```

#
### Consumer :
#
```shell

docker compose -f  docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-console-consumer \
--topic kafka-simple-topic \
--bootstrap-server kafkabroker.sandbox.net:9092 \
--consumer.config /apps/sandbox/kafka/cnf/client_plaintext.config \
--timeout-ms 5000 2>/dev/null"

#
docker compose -f  docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-console-consumer \
--topic kafka-simple-topic \
--bootstrap-server kafkabroker.sandbox.net:19092 \
--consumer.config /apps/sandbox/kafka/cnf/client_plaintext.config \
--offset 0 \
--partition 0 \
--property print.key=true \
--property key.separator=' - ' \
--timeout-ms 5000 2>/dev/null"

docker compose -f  docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-console-consumer \
--topic kafka-simple-topic \
--group kafka-simple-cg \
--bootstrap-server kafkabroker.sandbox.net:9092 \
--consumer.config /apps/sandbox/kafka/cnf/client_plaintext.config \
--property print.key=true \
--property key.separator='  -  ' \
--timeout-ms 5000 2>/dev/null"

```
docker system prune -a --volumes --filter "label=io.confluent.docker"

# Application Setup

docker-compose -f  docker-sandbox/dc-kafka-cluster.yaml up -d

docker-compose exec kafkabroker kafka-topics --create \
--topic users-topic-avro \
--bootstrap-server kafkabroker.sandbox.net:9092 \
--partitions 1 \
--replication-factor 1
--if-not-exists


# To check the end offset set parameter time to value -1
kafka-run-class kafka.tools.GetOffsetShell \
--broker-list localhost:9092 \
--topic users-topic-avro \
--time -1

# To check the start offset, use --time -2
kafka-run-class kafka.tools.GetOffsetShell \
--broker-list localhost:9092 \
--topic users-topic-avro \
--time -2


### Get Detail Info about Your Consumer Group –
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-consumer-groups --bootstrap-server kafkabroker.sandbox.net:9092 --list"
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-consumer-groups --bootstrap-server kafkabroker.sandbox.net:9092 --describe --group kafka-simple-cg "

#### Delete Offset
docker-compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-consumer-groups --bootstrap-server kafkabroker.sandbox.net:9092 --delete --group kafka-simple-cg "

#### Reset Offset
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-consumer-groups --bootstrap-server kafkabroker.sandbox.net:9092 --reset-offsets --to-earliest --all-topics --execute --group kafka-simple-cg "

##### --shift-by :- Reset the offset by incrementing the current offset position by take both +ve or -ve number
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-consumer-groups --bootstrap-server kafkabroker.sandbox.net:9092 --group kafka-simple-cg --reset-offsets --shift-by 10 --topic sales_topic --execute "

##### --to-datetime :- Reset offsets to offset from datetime. Format: ‘YYYY-MM-DDTHH:mm:SS.sss’
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-consumer-groups --bootstrap-server kafkabroker.sandbox.net:9092 --group kafka-simple-cg --reset-offsets --to-datetime 2020-11-01T00:00:00Z --topic sales_topic --execute "

##### --to-earliest :- Reset offsets to earliest (oldest) offset available in the topic.
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-consumer-groups --bootstrap-server kafkabroker.sandbox.net:9092 --group kafka-simple-cg --reset-offsets --to-earliest --topic sales_topic --execute "

##### --to-latest :- Reset offsets to latest (recent) offset available in the topic.
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec kafkabroker sh -c "kafka-consumer-groups --bootstrap-server kafkabroker.sandbox.net:9092 --group kafka-simple-cg --reset-offsets --to-latest --topic taxi-rides --execute "

### View Only 10  Messages on the Terminal –

```shell
#!/bin/bash
echo "Enter name of topic to empty:"
read topicName
kafka-configs --zookeeper zookeeper.sandbox.net:2181 --alter --entity-type topics --entity-name $topicName --add-config retention.ms=1000
sleep 5
kafka-configs --zookeeper zookeeper.sandbox.net:2181 --alter --entity-type topics --entity-name $topicName --delete-config retention.ms
```

#
##  schemaregistry
#
docker compose -f docker-sandbox/dc-kafka-cluster.yaml exec schemaregistry /bin/bash


kafka-avro-console-producer --topic users-topic-avro \
--bootstrap-server kafkabroker.sandbox.net:9092 \
--property value.schema="$(< /opt/app/schema/user.avsc)"

# Register a new version of a schema under the subject "Kafka-key"
$ curl -X POST -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"schema": "{\"type\": \"string\"}"}' \
http://schemaregistry:8081/subjects/auditlog-topic-avro-value/versions

# Register a new version of a schema under the subject "Kafka-value"
$ curl -X POST -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"schema": "{\"type\": \"string\"}"}' \
http://schemaregistry:8081/subjects/auditlog-topic-avro-value/versions

# List all subjects
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://schemaregistry:8081/subjects

# List all schema versions registered under the subject "Kafka-value"
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://schemaregistry:8081/subjects/auditlog-topic-avro-value/versions

# Fetch a schema by globally unique id 1
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://schemaregistry:8081/schemas/ids/1

# Fetch version 1 of the schema registered under subject "Kafka-value"
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://schemaregistry:8081/subjects/auditlog-topic-avro-value/versions/1

# Fetch the most recently registered schema under subject "Kafka-value"
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://schemaregistry:8081/subjects/auditlog-topic-avro-value/versions/latest

# Check whether a schema has been registered under subject "Kafka-key"
$ curl -X POST -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"schema": "{\"type\": \"string\"}"}' \
http://schemaregistry:8081/subjects/Kafka-key

# Test compatibility of a schema with the latest schema under subject "Kafka-value"
$ curl -X POST -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"schema": "{\"type\": \"string\"}"}' \
http://schemaregistry:8081/compatibility/subjects/auditlog-topic-avro-value/versions/latest

# Get top level config
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://schemaregistry:8081/config

# Update compatibility requirements globally
$ curl -X PUT -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"compatibility": "NONE"}' \
http://schemaregistry:8081/config

# Update compatibility requirements under the subject "Kafka-value"
$ curl -X PUT -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"compatibility": "BACKWARD"}' \
http://schemaregistry:8081/config

#
# Avro Producer & Consumer
#
kafka-avro-console-consumer --topic users \
--bootstrap-server kafkabroker.sandbox.net:9092

kafka-avro-console-consumer --topic users \
--bootstrap-server kafkabroker.sandbox.net:9092 \
--property schema.registry.url=http://schemaregistry:8081 \
--from-beginning

http://schemaregistry:8081/subjects
["users-value","order-updated-value","order-created-value"]

http://schemaregistry:8081/schemas/types

http://schemaregistry:8081/subjects/order-updated-value/versions
http://schemaregistry:8081/schemas/ids/1

http://schemaregistry:8081/subjects?deleted=true



docker-compose exec connect sh -c "curl -L -O -H 'Accept: application/vnd.github.v3.raw' https://api.github.com/repos/confluentinc/kafka-connect-datagen/contents/config/connector_pageviews_cos.config"
docker-compose exec connect sh -c "curl -X POST -H 'Content-Type: application/json' --data @connector_pageviews_cos.config http://schemaregistry:8083/connectors"

docker-compose exec connect sh -c "curl -L -O -H 'Accept: application/vnd.github.v3.raw' https://api.github.com/repos/confluentinc/kafka-connect-datagen/contents/config/connector_users_cos.config"
docker-compose exec connect sh -c "curl -X POST -H 'Content-Type: application/json' --data @connector_users_cos.config http://schemaregistry:8083/connectors"

docker container stop $(docker container ls -a -q -f "label=io.confluent.docker")
docker container stop $(docker container ls -a -q -f "label=io.confluent.docker") && docker system prune -a -f --volumes



