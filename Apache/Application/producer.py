from fastapi import FastAPI
from pydantic import BaseModel
from confluent_kafka import Producer
import json
import os

app = FastAPI()

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': os.getenv("KAFKA_API_KEY"),
    'sasl.password': os.getenv("KAFKA_API_SECRET")
}

producer = Producer(conf)
topic = "orders-topic"



class Order(BaseModel):
    order_id: int
    customer: str
    amount: float

@app.post("/produce")
def produce_order(order: Order):
    print("Producer application kicked off ....")
    print(os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    print(os.getenv("KAFKA_API_KEY"))
    print(os.getenv("KAFKA_API_SECRET"))
    producer.produce(
        topic,
        key=order.customer, 
        value=json.dumps(order.dict()))
    producer.flush()
    return {"status": "Message sent"}