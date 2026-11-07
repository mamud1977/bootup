from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

import os

# ============================================================
# Kafka configuration
# ============================================================

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': os.getenv("KAFKA_API_KEY"),
    'sasl.password': os.getenv("KAFKA_API_SECRET"),
    'group.id': 'orders-consumer-group',
    'auto.offset.reset': 'earliest'
}

# ============================================================
# Schema Registry configuration
# ============================================================

sr_conf = {
    "url": os.getenv("SCHEMA_REGISTRY_URL"),
    "basic.auth.user.info": (
        f"{os.getenv('SCHEMA_REGISTRY_API_KEY')}:"
        f"{os.getenv('SCHEMA_REGISTRY_API_SECRET')}"
    )
}

sr_client = SchemaRegistryClient(sr_conf)

# ============================================================
# Avro Deserializer
# ============================================================

avro_deserializer = AvroDeserializer(sr_client)


# ============================================================
# Kafka Consumer
# ============================================================

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

        # ====================================================
        # Deserialize Avro message
        # ====================================================

        order = avro_deserializer(
            msg.value(),
            SerializationContext(
                msg.topic(),
                MessageField.VALUE
            )
        )

        print("Received:", order)

except KeyboardInterrupt:
    print("\nStopping consumer...")

finally:
    consumer.close()
    print("Consumer closed.")