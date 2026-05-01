from fastapi import FastAPI
from pydantic import BaseModel
from confluent_kafka import Producer
from datetime import datetime
import json
import os

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField

app = FastAPI()

conf = {
    'bootstrap.servers': "pkc-oxqxx9.us-east-1.aws.confluent.cloud:9092",
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': "DI7ZNEWFEWAANTPI",
    'sasl.password': "cfltpuxiMh2IimthrZnIKX5LsH6ntuEgb27YfZrGCl+LnxfWXG9lIzwRzMeuqvhg"
}

# 1. Setup Schema Registry Client
sr_conf = {'url': "https://psrc-1ry6wml.us-east-1.aws.confluent.cloud", 
           'basic.auth.user.info': "4BETAP7QEI5YTUXI:cfltU8FzemLQD/QFS9YrBC3vmYV/1cZ89RW8Wt90HVF68zPfEaFMmfbM2NiX0gdQ"}
sr_client = SchemaRegistryClient(sr_conf)

#conf = {
#   'bootstrap.servers': "<>",
#    'security.protocol': "<>",
#    'sasl.mechanism': "<>",
#    'sasl.username': "<>",
#    'sasl.password': "<>"
#}

producer = Producer(conf)
topic = "topic-multi-1"

class order(BaseModel): 
    order_id: str
    customer_id: int
    total_amount: float
    currency: str

class event(BaseModel): 
    event_id: str
    event_name: str

class mapping(BaseModel):  
    order_id: str
    event_id: str

@app.post("/produce/order")
def produce_order(msg: order):
    print("Producer application kicked off ....")

    # 2. Define the Avro Serializer
    schema_str = """{
  "type": "record",
  "name": "orders",
  "namespace": "com.testdb",
  "doc": "Schema for the orders table in the unified event topic",
  "fields": [
    {
      "name": "order_id",
      "type": "string",
      "doc": "Unique identifier for the order"
    },
    {
      "name": "customer_id",
      "type": "int",
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
      "default": "INR",
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
    avro_serializer = AvroSerializer(sr_client, schema_str)
    string_serializer = StringSerializer('utf_8')

    producer.produce(
            topic=topic,
            key=string_serializer(str(msg.customer_id)),
            value=avro_serializer(msg, SerializationContext(topic, MessageField.VALUE))
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
}}"""
    avro_serializer = AvroSerializer(sr_client, schema_str)
    string_serializer = StringSerializer('utf_8')

    producer.produce(
            topic=topic,
            key=string_serializer(str(msg.customer_id)),
            value=avro_serializer(msg, SerializationContext(topic, MessageField.VALUE))
        )

    producer.flush()
    return {"status": "Message sent"}

@app.post("/produce/mapping")
def produce_order(msg: mapping):
    print("Producer application kicked off ....")

    # 2. Define the Avro Serializer
    schema_str = """{
  "type": "record",
  "name": "mapping",
  "namespace": "com.testdb",
  "doc": "Schema for the orders table in the unified event topic",
  "fields": [
    {
      "name": "event_id",
      "type": "string",
      "doc": "Unique identifier for the event"
    },
    {
      "name": "customer_id",
      "type": "int",
      "doc": "ID of the customer placing the order"
    }
  ]
}"""
    avro_serializer = AvroSerializer(sr_client, schema_str)  
    string_serializer = StringSerializer('utf_8')  

    producer.produce(
        topic=topic,
        key=str(msg.order_id),   # convert int → str
        value=json.dumps(msg.dict()).encode("utf-8")  # ensure value is bytes
        )
    producer.flush()
    return {"status": "Message sent"}
