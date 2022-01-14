
# Topic - Creation
docker-compose -f dc-sandbox-cluster2.yml exec broker-0 kafka-topics \
--create \
--bootstrap-server kafka-broker:9092 \
--partitions 3 \
--replication-factor 2 \
--topic test-topic

# Topic - List
docker-compose -f dc-sandbox-cluster2.yml exec kafka-broker kafka-topics --list --bootstrap-server kafka-broker:9092

# Topic - Describe
docker-compose -f dc-sandbox-cluster2.yml exec kafka-broker kafka-topics --describe --topic test-topic --bootstrap-server kafka-broker:9092

# Topic - Alter
kafka-topics --alter --topic test-topic --partitions 9 --bootstrap-server kafka-broker:9092

# Topic - Delete
kafka-topics --delete --topic warm-topic --bootstrap-server kafka-broker:9092

# Kafka - Broker Console
docker-compose -f dc-sandbox-cluster2.yml exec kafka-broker bash

# Producer :
docker-compose -f dc-sandbox-cluster2.yml exec kafka-broker bash

kafka-console-producer --topic test-topic --broker-list kafka-broker:9092

docker-compose exec broker kafka-console-producer \
--topic test-topic
--broker-list kafka-broker:9092 \
--property parse.key=true \
--property key.separator=":" \

# Consumer :
docker-compose -f dc-sandbox-cluster2.yml exec kafka-broker bash
kafka-console-consumer \
--topic test-topic \
--group test-cg \
--bootstrap-server kafka-broker:9092,broker-1:19093,broker-2:19094

OR
docker exec kafka-broker kafka-console-consumer \
--topic test-topic \
--group test-cg \
--bootstrap-server kafka-broker:9092,broker-1:19093,broker-2:19094

docker-compose exec kafka-broker kafka-console-consumer \
--topic test-topic \
--group test-cg \
--bootstrap-server kafka-broker:9092,broker-1:19093,broker-2:19094 \
--from-beginning \
--property print.key=true \
--property key.separator="-"

docker-compose -f dc-sandbox-cluster2.yml exec -T kafka-broker kafka-consumer-groups --bootstrap-server kafka-broker:9092 --list

docker-compose -f dc-sandbox-cluster2.yml exec -T kafka-broker kafka-consumer-groups --bootstrap-server kafka-broker:9092 --describe --group python-custom-cg

docker system prune -a --volumes --filter "label=io.confluent.docker"

# Application Setup

docker-compose up -d
docker-compose exec broker kafka-topics --create \
--topic users-topic-avro \
--bootstrap-server broker:9092 \
--partitions 1 \
--replication-factor 1

docker-compose exec schema-registry bash

kafka-avro-console-producer --topic users-topic-avro \
--bootstrap-server broker:9092 \
--property value.schema="$(< /opt/app/schema/user.avsc)"

# Register a new version of a schema under the subject "Kafka-key"
$ curl -X POST -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"schema": "{\"type\": \"string\"}"}' \
http://localhost:8081/subjects/auditlog-topic-avro-value/versions

# Register a new version of a schema under the subject "Kafka-value"
$ curl -X POST -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"schema": "{\"type\": \"string\"}"}' \
http://localhost:8081/subjects/auditlog-topic-avro-value/versions

# List all subjects
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://localhost:8081/subjects

# List all schema versions registered under the subject "Kafka-value"
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://localhost:8081/subjects/auditlog-topic-avro-value/versions

# Fetch a schema by globally unique id 1
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://localhost:8081/schemas/ids/1

# Fetch version 1 of the schema registered under subject "Kafka-value"
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://localhost:8081/subjects/auditlog-topic-avro-value/versions/1

# Fetch the most recently registered schema under subject "Kafka-value"
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://localhost:8081/subjects/auditlog-topic-avro-value/versions/latest

# Check whether a schema has been registered under subject "Kafka-key"
$ curl -X POST -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"schema": "{\"type\": \"string\"}"}' \
http://localhost:8081/subjects/Kafka-key

# Test compatibility of a schema with the latest schema under subject "Kafka-value"
$ curl -X POST -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"schema": "{\"type\": \"string\"}"}' \
http://localhost:8081/compatibility/subjects/auditlog-topic-avro-value/versions/latest

# Get top level config
$ curl -X GET -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
http://localhost:8081/config

# Update compatibility requirements globally
$ curl -X PUT -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"compatibility": "NONE"}' \
http://localhost:8081/config

# Update compatibility requirements under the subject "Kafka-value"
$ curl -X PUT -i -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"compatibility": "BACKWARD"}' \
http://localhost:8081/config

kafka-avro-console-consumer --topic users \
--bootstrap-server broker:9092

kafka-avro-console-consumer --topic users \
--bootstrap-server broker:9092 \
--property schema.registry.url=http://schema-registry:8081 \
--from-beginning

http://dockerhost:8081/subjects
["users-value","order-updated-value","order-created-value"]

http://dockerhost:8081/schemas/types

http://dockerhost:8081/subjects/order-updated-value/versions
http://dockerhost:8081/schemas/ids/1

http://dockerhost:8081/subjects?deleted=true



docker-compose exec connect sh -c "curl -L -O -H 'Accept: application/vnd.github.v3.raw' https://api.github.com/repos/confluentinc/kafka-connect-datagen/contents/config/connector_pageviews_cos.config"
docker-compose exec connect sh -c "curl -X POST -H 'Content-Type: application/json' --data @connector_pageviews_cos.config http://localhost:8083/connectors"

docker-compose exec connect sh -c "curl -L -O -H 'Accept: application/vnd.github.v3.raw' https://api.github.com/repos/confluentinc/kafka-connect-datagen/contents/config/connector_users_cos.config"
docker-compose exec connect sh -c "curl -X POST -H 'Content-Type: application/json' --data @connector_users_cos.config http://localhost:8083/connectors"

docker container stop $(docker container ls -a -q -f "label=io.confluent.docker")
docker container stop $(docker container ls -a -q -f "label=io.confluent.docker") && docker system prune -a -f --volumes


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

### Change Kafka Retention Time
kafka-topics --zookeeper zookeeper:2181 --alter --topic users-topic-avro --config retention.ms=1000