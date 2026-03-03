cd C:\Users\Mamud\Downloads\confluent
confluent login

>confluent version

>confluent login --prompt --save

>confluent plugin install confluent-flink-quickstart

####### Environment ##############
#Create a new environment
confluent environment create my-flink-env

#List the environments
confluent environment list

#Use the environment
confluent environment use env-8d752r

#Delete an environment
confluent environment delete env-3dk9nw

####### Kafka Cluster ##############
#Create a Kafka cluster
confluent kafka cluster create sql-cluster --cloud aws --region us-east-1 --type basic

+-------------+--------------+
| Current     | false        |
| ID          | lfcp-k9x192  |
| Name        | my-pool      |
| Environment | env-xk0mv1   |
| Current CFU | 0            |
| Max CFU     | 5            |
| Cloud       | AWS          |
| Region      | us-east-1    |
| Status      | PROVISIONING |
+-------------+--------------+

#List the clusters
confluent kafka cluster list

#Use a specific cluster
confluent kafka cluster use lkc-o05dzx

#Describe the Schema Registry cluster for your environment:
confluent schema-registry cluster describe

 
####### Compute Pool ##############
#Create a Flink Compute Pool
confluent flink compute-pool create sql-course --region us-east-1 --cloud aws --max-cfu 5

#List
confluent flink compute-pool list


####### Flink SQL Shell ##############
confluent flink shell --compute-pool lfcp-73oxkp

#Delete
confluent flink compute-pool delete lfcp-wnykrm

+-------------+--------------+
| KAFKA       | FLINK        |
|-------------|--------------|
| environment | catalog      |
| cluster     | database     |
| topic+schema| table        |
+-------------+--------------+
Flink provides SQL interface on top of Confluent Cloud 

####### Catalog Commands ##############

SHOW CATALOGS;
USE CATALOG env-8d752r;
SHOW DATABASES;
USE terraform-cluster;
SHOW TABLES;

#Create a table
create table events (
	event_name varchar,
	event_id varchar,
	event_locationpin Integer,
	event_time TIMESTAMP(3),
    	WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) distributed by hash(event_name) into 2 buckets
with (
'kafka.retention.time'='1d'
);

drop table events;

show create table events;

INSERT INTO events VALUES ('Music Fest', 'e1', 700091, CURRENT_TIMESTAMP);
INSERT INTO events VALUES ('Music Fest','e4', 700091, CURRENT_TIMESTAMP);
INSERT INTO events VALUES ('Sanskriti','e2', 700014, CURRENT_TIMESTAMP);
INSERT INTO events VALUES ('Open Sale','e3', 700150, CURRENT_TIMESTAMP);
INSERT INTO events VALUES ('Open Sale','e6', 700150, CURRENT_TIMESTAMP);

SET 'sql.tables.scan.idle-timeout' = '1s';

select * from events;
select event_id, event_name, event_locationpin, $rowtime from events;
select *, $rowtime, current_watermark($rowtime) as wm from events;
set 'sql.tables.scan.idle-timeout' = '1 seconds';
select *, $rowtime, current_watermark(event_time ) as wm from events order by $rowtime;


create table `small-orders` (
	order_id string NOT NULL,
	customer_id INT NOT NULL,
	product_id STRING NOT NULL,
	price DOUBLE NOT NULL
);

describe extended events;

1) watermarkdelays
2) idle timeout
3) max allowed watermark drift









