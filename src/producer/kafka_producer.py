from confluent_kafka import Producer
from custom_logging import CustomLogger


class KafkaProducer:
    def __init__(self, config=None, topic=None):
        self.logger = CustomLogger(__name__)
        self.config = self.provide_additional_config(config or {})
        self.topic = topic or "customer_events" 
        self.producer = Producer(self.config)

    def provide_additional_config(self, config):
        additional_config = {
            'bootstrap.servers':'kafka:9092',
            'client.id': 'kafka_producer',
            'acks': 'all',
            'retries': 3,
            'linger.ms': 5,
            'retry.backoff.ms': 500,
            'compression.type': 'snappy',
        }

        return additional_config | config
    
    def delivery_report(self, err, msg):
        if err is not None:
            self.logger.error(f"Message delivery failed: {err}")
        else:
            self.logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

    
    def produce(self, id, events):
        try:
            self.logger.info(f"Producing events to topic {self.topic}")
            self.producer.produce(self.topic
                    , key=str(id).encode('utf-8')
                    , value=events.encode('utf-8')
                    , on_delivery=self.delivery_report
            )

            Number_of_events = len(self.producer)
            self.logger.info(f"Number of events waiting to be produced: {Number_of_events}")

            event_processed = self.producer.poll(timeout=10) 
            self.logger.info(f"Polll execute: Event processed: {event_processed}")


        except Exception as e:
            self.logger.error(f"Failed to produce event: {e}")
            raise Exception("Failed to produce event")
        

        finally:
            self.producer.flush()
            self.logger.info(f"Flushed producer for topic {self.topic}")            