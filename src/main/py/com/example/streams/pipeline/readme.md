
# Topic - Delete

docker-compose -f dc-kafka-cluster.yml exec kafkabroker.sandbox.net kafka-topics --delete --topic taxi-rides --bootstrap-server kafkabroker.sandbox.net:9092
docker-compose -f dc-kafka-cluster.yml exec kafkabroker.sandbox.net kafka-topics --delete --topic taxi-fares --bootstrap-server kafkabroker.sandbox.net:9092


#### 1. Create Required Topics
```shell
docker-compose -f dc-kafka-cluster.yaml exec kafkabroker.sandbox.net kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 1 --replication-factor 1 --topic taxi-rides

docker-compose -f dc-kafka-cluster.yaml exec kafkabroker.sandbox.net kafka-topics --create --bootstrap-server kafkabroker.sandbox.net:9092 --partitions 1 --replication-factor 1 --topic taxi-fares
```

#### 2. Publish NY Taxi Data on topics
```shell
docker-compose -f dc-kafka-cluster.yaml exec kafkabroker.sandbox.net bash


( zcat /apps/hostpath/datasets/nycTaxiRides.gz \
  | split -l 10000 --filter="kafka-console-producer --broker-list kafkabroker.sandbox.net:9092 --topic taxi-rides; sleep 0.2" \
  > /dev/null ) &
  
( zcat /apps/hostpath/datasets/nycTaxiFares.gz \
  | split -l 10000 --filter="kafka-console-producer --broker-list kafkabroker.sandbox.net:9092 --topic taxi-fares; sleep 0.2" \
  > /dev/null ) &


root@kafkabroker.sandbox.net:/# zcat /apps/hostpath/datasets/nycTaxiRides.gz | split -l 10000 --filter="kafka-console-producer --broker-list kafkabroker.sandbox.net:9092 --topic taxi-rides; sleep 0.2" > /dev/null  &
root@kafkabroker.sandbox.net:/# zcat /apps/hostpath/datasets/nycTaxiFares.gz | split -l 10000 --filter="kafka-console-producer --broker-list kafkabroker.sandbox.net:9092 --topic taxi-fares; sleep 0.2" > /dev/null  &

```
#### 3. Cleanup Existing Data on Topics
```shell
#!/bin/bash
echo "Enter name of topic to empty:"
read topicName
docker-compose -f dc-kafka-cluster.yaml exec kafkabroker.sandbox.net kafka-configs --bootstrap-server kafkabroker.sandbox.net:9092 --alter --entity-type topics --entity-name taxi-fares --add-config retention.ms=1000
sleep 5
docker-compose -f dc-kafka-cluster.yaml exec kafkabroker.sandbox.net kafka-configs --bootstrap-server kafkabroker.sandbox.net:9092 --alter --entity-type topics --entity-name taxi-fares --delete-config retention.ms

docker-compose -f dc-kafka-cluster.yaml exec kafkabroker.sandbox.net kafka-configs --bootstrap-server kafkabroker.sandbox.net:9092 --alter --entity-type topics --entity-name taxi-rides --add-config retention.ms=1000
sleep 5
docker-compose -f dc-kafka-cluster.yaml exec kafkabroker.sandbox.net kafka-configs --bootstrap-server kafkabroker.sandbox.net:9092 --alter --entity-type topics --entity-name taxi-rides --delete-config retention.ms

```

#### 4. Validate Data on Kafka Topics
```shell
docker-compose -f dc-kafka-cluster.yaml exec kafkabroker.sandbox.net kafka-console-consumer --bootstrap-server kafkabroker.sandbox.net:9092 --topic taxi-rides --group test-taxi-rides-cg --from-beginning

docker-compose -f dc-kafka-cluster.yaml exec kafkabroker.sandbox.net kafka-console-consumer --bootstrap-server kafkabroker.sandbox.net:9092 --topic taxi-fares --group test-taxi-fares-cg --from-beginning
```