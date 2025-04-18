from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
from custom_logging import CustomLogger


KAFKA_BROKER = "kafka:9092"
TOPIC_NAME = "customer_events"

class KafkaConfiguration:

    def __init__(self, broker: str = KAFKA_BROKER, topic: str = TOPIC_NAME):
        self.logger = CustomLogger(__name__)
        self.broker = broker or KAFKA_BROKER
        self.topic = topic or TOPIC_NAME
        self.admin_client = self.get_client()
        self.logger.info(f"Kafka Admin Client initialized with broker: {self.broker}")
        self.logger.info(f"Topic set to: {self.topic}")

    def get_client(self):
        try:
            admin_client = AdminClient({"bootstrap.servers": self.broker})
            self.logger.info("Admin client created successfully.")
        except KafkaException as e:
            self.logger.error(f"Failed to create admin client: {e}")
            raise Exception(f"Failed to create admin client: {e}")
        
        return admin_client
        

    def create_topic(self, num_partitions: int = 3, replication_factor: int = 1):
        try:
            new_topic = NewTopic(self.topic, num_partitions=num_partitions, replication_factor=replication_factor)
            self.admin_client.create_topics([new_topic])
            self.logger.info(f"Topic '{self.topic}' created successfully.")
        except KafkaException as e:
            self.logger.error(f"Failed to create topic '{self.topic}': {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    kafka_config = KafkaConfiguration()
    kafka_config.create_topic() 