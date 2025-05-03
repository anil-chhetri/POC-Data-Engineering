from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer, SerializationContext, MessageField

from savejson import SaveJson

from typing import Tuple

from custom_logging import CustomLogger


class KafkaConsumer: 

    SCHEMA_REISTRY_URL = 'http://schema-registry:8081'
    KAFKA_BROKER = 'kafka:9092'
    CONSUMER_CONFIG = {
        'bootstrap.servers': KAFKA_BROKER,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'auto.commit.interval.ms': 5000,
        'max.poll.interval.ms': 300000
    }
    KAFAK_TOPIC = "customer_events"

    def __init__(self, config):
        self.logger = CustomLogger(__name__)
        # config = config | {
        #     "key.deserializer": StringDeserializer('utf_8'),
        #     "value.deserializer": self.get_arvo_deserializer()
        # }
        self.config = config | KafkaConsumer.CONSUMER_CONFIG
        self.logger.info(f"Kafka consumer config: {self.config}")
        self.consumer = Consumer(self.config)
        self.consumer.subscribe([self.KAFAK_TOPIC], on_assign=self.on_assign)
        self.logger.info(f"Kafka consumer created and subscribed to topic: {self.KAFAK_TOPIC}")

    def on_assign(self, consumer, partitions):
        self.logger.info(f"Partitions assigned: {partitions}")
        

    def get_schema_from_registry(self) -> Tuple[SchemaRegistryClient, str]:
        registry_client = SchemaRegistryClient({
            'url': KafkaConsumer.SCHEMA_REISTRY_URL
        })
        latest_schema = registry_client.get_latest_version(self.KAFAK_TOPIC + '-value')
        return (registry_client, latest_schema.schema.schema_str)
    
    def get_arvo_deserializer(self):
        registry_client, schema_str = self.get_schema_from_registry()
        return AvroDeserializer(
            registry_client,
            schema_str
        )

    def start_consuming(self):
        try:
            self.logger.info("Starting Kafka consumer...")
            while True:
                self.logger.info("Waiting for messages...")
                msg = self.consumer.consume(num_messages=5, timeout=1)
                if len(msg) == 0:
                    self.logger.info("No messages received.")
                    continue
                if any([x.error() is not None for x in msg]):
                    print([x.error() for x in msg])
                    self.logger.info('error found in message.')
                    continue
                context = SerializationContext(self.KAFAK_TOPIC, MessageField.VALUE)
                message_value = [self.get_arvo_deserializer()(x.value(), context) for x in msg]
                print(message_value)
                SaveJson.save_as_parquet(message_value)
        except KeyboardInterrupt:
            self.logger.info("Stopping Kafka consumer...")
        except Exception as e:
            self.logger.error(f"Error consuming messages: {e.__str__()}")
            raise Exception(f"Error consuming messages: {e}")
        finally:
            self.consumer.close()