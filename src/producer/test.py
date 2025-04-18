import CustomerEvents as c
from custom_logging import CustomLogger
from kafka_configuration import KafkaConfiguration
from kafka_producer import KafkaProducer


logger = CustomLogger(__name__)
logger.info("Starting Kafka configuration Test")
kafka_config = KafkaConfiguration()
logger.info("Creating topic")
kafka_config.create_topic()
logger.info("Kafka configuration Test completed")



logger.info("Starting Customer Events Test")


logger.info('producing the event to customer events topic')
producer = KafkaProducer()
for i in range(1, 2):
    customer_events = c.generate_consumer_event_data()
    logger.debug("Creating customer events")

    logger.debug("Produced customer events")
    producer.produce(i, customer_events)

logger.debug(f"{i=} produced to kafka topic")

