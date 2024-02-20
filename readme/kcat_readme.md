kafkacat is one of my go-to tools when working with Kafka. It’s a producer and consumer, but also a swiss-army knife of debugging and troubleshooting capabilities. So when I built a new Fedora server recently, I needed to get it installed. Unfortunately there’s no pre-packed install available on yum, so here’s how to do it manually.

Note
kafkacat is now known as kcat (ref). When invoking the command you will need to use kcat in place of kafkacat.
Pre-requisite installs 🔗
We’ll need some packages from the Confluent repo so set this up for yum first by creating /etc/yum.repos.d/confluent.repo:
```shell
[Confluent.dist]
name=Confluent repository (dist)
baseurl=https://packages.confluent.io/rpm/5.4/7
gpgcheck=1
gpgkey=https://packages.confluent.io/rpm/5.4/archive.key
enabled=1

[Confluent]
name=Confluent repository
baseurl=https://packages.confluent.io/rpm/5.4
gpgcheck=1
gpgkey=https://packages.confluent.io/rpm/5.4/archive.key
enabled=1
Now install the dependencies:
```
# Update yum
```shell
sudo yum update -y
```

# Install build tools
```shell
sudo yum group install "Development Tools" -y
```
# Install librdkafka and other deps
```shell
sudo yum install -y librdkafka-devel yajl-devel avro-c-devel
```

Build kafkacat 🔗
Pull down the kafkacat repo:
```shell
git clone https://github.com/edenhill/kafkacat.git
cd kafkacat
```
Prepare the install - make sure that this step does not result in an error!
```shell
./configure
```

If you get errors here, it’s off to Google you go to try and figure them out, because there’s no point continuing if you can’t. You might find some failed steps that don’t result in an actual error - this is a "soft fail" and means that certain functionality won’t be available in the kafkacat that you install (in this case, Avro/Schema Registry). Here’s an example of one:

checking for serdes (by pkg-config)... failed
checking for serdes (by compile)... failed (disable)
Install! 🔗
```shell
make
sudo make install
```

Check that it works:
```shell
➜ kafkacat -V
kafkacat - Apache Kafka producer and consumer tool
https://github.com/edenhill/kafkacat
Copyright (c) 2014-2019, Magnus Edenhill
Version 1.5.0-5-ge98256 (JSON, librdkafka 1.3.0 builtin.features=gzip,snappy,ssl,sasl,regex,lz4,sasl_gssapi,sasl_plain,sasl_scram,plugins,zstd,sasl_oauthbearer)
```
Test it:
```shell
➜ kafkacat -b localhost:9092 -L
Metadata for all topics (from broker 3: localhost:9092/3):
3 brokers:
broker 2 at localhost:19092
broker 3 at localhost:9092 (controller)
broker 1 at localhost:9092
```
Note
kafkacat is now known as kcat (ref). When invoking the command you will need to use kcat in place of kafkacat.
This all seems like too much hassle? 🔗
Yeah, that’s why Docker was invented ;-)

If you want to run kafkacat but can’t get it installed, do not fear! You can run it anyway:

docker run --rm edenhill/kafkacat:1.5.0 \
kafkacat -V
You just need to make sure you wrap your head around Docker networking if you do this, because localhost to a Docker container is not the same (by default) as localhost on your host machine:

➜ docker run --rm edenhill/kafkacat:1.5.0 \
kafkacat -b localhost:9092 -L
% ERROR: Failed to acquire metadata: Local: Broker transport failure
If you add --network=host then it will use the network as if executing locally:

➜ docker run --rm --network=host edenhill/kafkacat:1.5.0 \
kafkacat -b localhost:9092 -L

Metadata for all topics (from broker 3: localhost:9092/3):
3 brokers:
broker 2 at localhost:19092
broker 3 at localhost:9092 (controller)
broker 1 at localhost:9092