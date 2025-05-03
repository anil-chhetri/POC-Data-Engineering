from consumer import KafkaConsumer
from custom_logging import CustomLogger


def main(id):
    logger = CustomLogger(__name__)
    logger.info("Starting Kafka consumer...")
    try: 
        consumer = KafkaConsumer(config={"group.id": id})
        consumer.start_consuming()
    except Exception as e:
        logger.error(f"Error starting Kafka consumer: {e}")



if __name__ == "__main__":
    main(4)

