from fastapi import FastAPI
from pydantic import BaseModel, Field
from confluent_kafka import Producer
from datetime import datetime
import json
import os


from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry import record_subject_name_strategy
app = FastAPI()

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': os.getenv("KAFKA_API_KEY"),
    'sasl.password': os.getenv("KAFKA_API_SECRET")
}

# 1. Setup Schema Registry Client
sr_conf = {'url': os.getenv("SCHEMA_REGISTRY_URL"), 
           'basic.auth.user.info': (
        f"{os.getenv('SCHEMA_REGISTRY_API_KEY')}:"
        f"{os.getenv('SCHEMA_REGISTRY_API_SECRET')}"
      )
      }


# Check environment variables
print("\n===== ENVIRONMENT VARIABLES =====")
print("KAFKA_BOOTSTRAP_SERVERS:", os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
print("KAFKA_API_KEY:", os.getenv("KAFKA_API_KEY"))
print("KAFKA_API_SECRET:", os.getenv("KAFKA_API_SECRET"))
print("SCHEMA_REGISTRY_URL:", os.getenv("SCHEMA_REGISTRY_URL"))
print("SCHEMA_REGISTRY_API_KEY:", os.getenv("SCHEMA_REGISTRY_API_KEY"))
print("SCHEMA_REGISTRY_API_SECRET:", os.getenv("SCHEMA_REGISTRY_API_SECRET"))
print("================================\n")

# ============================================================
# Create Kafka Producer
# ============================================================

producer = Producer(conf)

sr_client = SchemaRegistryClient(sr_conf)

topic = "orders-topic"

class order(BaseModel): 
    order_id: str
    customer_id: str
    total_amount: float
    currency: str
    updated_at: datetime = Field(default_factory=datetime.now)

class event(BaseModel): 
    event_id: str
    event_name: str

class mapping(BaseModel):  
    order_id: str
    event_id: str

# ============================================================
# Test Kafka connection
# ============================================================

@app.get("/kafka-test")
def kafka_test():

    print("Testing Kafka connection...")

    try:

        metadata = producer.list_topics(timeout=10)

        print("Kafka connection SUCCESS")
        print("Cluster ID:", metadata.cluster_id)

        return {
            "status": "Kafka connection successful",
            "cluster_id": metadata.cluster_id
        }

    except Exception as e:

        print("Kafka connection FAILED")
        print(type(e).__name__, str(e))

        return {
            "status": "Kafka connection failed",
            "error": str(e)
        }

@app.post("/produce/order")
def produce_order(msg: order):
    print("Producer application kicked off ....")

    # 2. Define the Avro Serializer
    schema_str = """{
        "type": "record",
        "name": "orders",
        "namespace": "com.testdb",
        "doc": "Schema for the orders",
        "fields": 
        [
            {
            "name": "order_id",
            "type": "string",
            "doc": "Unique identifier for the order"
            },
            {
            "name": "customer_id",
            "type": "string",
            "doc": "ID of the customer placing the order"
            },
            {
            "name": "total_amount",
            "type": "double",
            "doc": "Total price of the transaction"
            },
            {
            "name": "currency",
            "type": "string",
            "doc": "Currency code for the transaction"
            },
            {
            "name": "updated_at",
            "type": {
                    "type": "long",
                    "logicalType": "timestamp-millis"
                    },
            "doc": "Timestamp for Snowflake change tracking"
            }
        ]
        }"""

    avro_serializer = AvroSerializer(
        sr_client, 
        schema_str, 
        conf={
        "subject.name.strategy": record_subject_name_strategy
        }
    )
    string_serializer = StringSerializer('utf_8')

    producer.produce(
        topic=topic,
        key=string_serializer(msg.order_id),
        value=avro_serializer 
            (
            msg.model_dump(),
            SerializationContext(topic, MessageField.VALUE)
            )
        )

    producer.flush()
    return {"status": "Message sent"}


@app.post("/produce/event")
def produce_event(msg: event):
    print("Producer application kicked off ....")
    
    # 2. Define the Avro Serializer
    schema_str = """{
        "type": "record",
        "name": "events",
        "namespace": "com.testdb",
        "doc": "Schema for the events table in the unified event topic",
        "fields": [
            {
            "name": "event_id",
            "type": "string",
            "doc": "Unique identifier for the event"
            },
            {
            "name": "event_name",
            "type": "string",
            "doc": "identifier for the event name"
            }
        ]
    }"""
    avro_serializer = AvroSerializer(
        sr_client, 
        schema_str, 
        conf={
            "subject.name.strategy": record_subject_name_strategy
            }
        )
    string_serializer = StringSerializer('utf_8')

    producer.produce(
        topic=topic,
        key=string_serializer(msg.event_id),
        value=avro_serializer 
            (
            msg.model_dump(),
            SerializationContext(topic, MessageField.VALUE)
            )
        )

    producer.flush()
    return {"status": "Message sent"}

@app.post("/produce/mapping")
def produce_mapping(msg: mapping):
    print("Producer application kicked off ....")

    # 2. Define the Avro Serializer
    schema_str = """{
        "type": "record",
        "name": "mapping",
        "namespace": "com.testdb",
        "doc": "Schema for the orders table in the unified event topic",
        "fields": [
            {
            "name": "order_id",
            "type": "string",
            "doc": "Unique identifier for the order"
            },
            {
            "name": "event_id",
            "type": "string",
            "doc": "Unique identifier for the event"
            }
        ]
    }"""
    avro_serializer = AvroSerializer(
        sr_client, 
        schema_str, 
        conf={
            "subject.name.strategy": record_subject_name_strategy
            }
        )  
    string_serializer = StringSerializer('utf_8')  

    producer.produce(
        topic=topic,
        key=string_serializer(msg.order_id),
        value=avro_serializer 
            (
            msg.model_dump(),
            SerializationContext(topic, MessageField.VALUE)
            )
        )
    producer.flush()
    return {"status": "Message sent"}
