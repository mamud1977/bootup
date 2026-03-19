from confluent_kafka import Consumer
import os
import json

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': os.getenv("KAFKA_API_KEY"),
    'sasl.password': os.getenv("KAFKA_API_SECRET"),
    'group.id': 'orders-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
topic = "orders-topic"

consumer.subscribe([topic])

print("Consumer started... Listening for messages 🚀")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("Error:", msg.error())
            continue

        value = msg.value().decode("utf-8")
        order = json.loads(value)

        print("Received:", order)

except KeyboardInterrupt:
    print("\nStopping consumer...")

finally:
    consumer.close()
    print("Consumer closed.")