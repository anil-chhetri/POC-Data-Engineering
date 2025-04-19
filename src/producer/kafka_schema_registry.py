from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from confluent_kafka.schema_registry.error import SchemaRegistryError
from confluent_kafka.schema_registry.avro import AvroSerializer

from pathlib import Path
from typing import Tuple
import json
import deepdiff

from custom_logging import CustomLogger

class KafkaSchemaRegistry:
    
    SCHEMA_REISTRY_URL = 'http://schema-registry:8081'
    KAFKA_REGISTRY_URL = 'kafka:9092'
    KAFKA_TOPIC = 'customer_events'
    LOCAL_SCHEMA_PATH = Path(__file__).parent.joinpath('Schema')

    def __init__(self, url=None, subject_name=None):
        self.logger = CustomLogger(__name__)
        self.url = url or self.SCHEMA_REISTRY_URL
        self.schema_registry_client = self.get_schema_client()
        self.subject_name = subject_name or KafkaSchemaRegistry.KAFKA_TOPIC + '-value'


    def get_schema_client(self):
        return SchemaRegistryClient({'url': self.url})

    def get_latest_version_from_folder(self):
        schema_folder_location = KafkaSchemaRegistry.LOCAL_SCHEMA_PATH
        schema_files = list(schema_folder_location.glob('*'))
        
        schema_files.sort(key=lambda x: x.stem[1], reverse=True)
        latest_schema_file = schema_files[0]
        return latest_schema_file
    
    def get_local_schema(self):
        latest_schema_file = self.get_latest_version_from_folder()
        with open(latest_schema_file, 'r') as file:
            schema = file.read()
        return schema
    
    def get_check_subject_exists(self) -> Tuple[bool, str]:
        try:
            latest_schema = self.schema_registry_client.get_latest_version(self.subject_name)
            self.logger.debug(f"Schema already registered with version: {latest_schema.version}")
            return (True, latest_schema.schema.schema_str)
        except SchemaRegistryError as e:
            self.logger.debug(f'error code: {e.http_status_code}')
            if e.http_status_code == 404:
                self.logger.info(f"Schema registered with subject name: {self.subject_name} not found.")
                return (False, None)
            else: 
                self.logger.error(e.error_message)
                return (False, None)

    def register_schema(self):

        schema_exists, schema_str = self.get_check_subject_exists()
        if not schema_exists:
            schema_str = self.get_local_schema()
            try:
                schema_id =  self.schema_registry_client.register_schema(
                    subject_name=self.subject_name,
                    schema=Schema(schema_str, schema_type='AVRO')
                )
                self.logger.info(f"Schema registered with subject: {self.subject_name}, schema id: {schema_id}")
                self.logger.info(f"changing schema compatibility to FUll")
                self.schema_registry_client.set_compatibility(
                    subject_name=self.subject_name,
                    level='FULL'
                )
            except SchemaRegistryError as e:
                self.logger.error(f"Failed to register schema: {e.error_message}")

        current_latest_schema = dict(json.loads(self.get_local_schema()))
        current_latest_schema_registry_schema = dict(json.loads(
            self.schema_registry_client
            .get_latest_version(self.subject_name)
            .schema.schema_str
        ))

        compare_result = deepdiff.DeepDiff(
            current_latest_schema,
            current_latest_schema_registry_schema,
            ignore_order=True
        )
        
        if compare_result:
            self.logger.info(f"Schema has changed, updating schema.")
            try:
                new_schema = Schema(schema_str=self.get_local_schema(), schema_type='AVRO')
                compability_test = self.schema_registry_client.test_compatibility(
                    subject_name=self.subject_name,
                    schema=new_schema
                )   

                if compability_test:    
                    self.logger.info(f"Schema is compatible with the existing schema.")
                    schema_id =  self.schema_registry_client.register_schema(
                        subject_name=self.subject_name,
                        schema=Schema(schema_str, schema_type='AVRO')
                    )
                    self.logger.info(f"Schema registered with subject: {self.subject_name}, schema id: {schema_id}")
                    self.logger.info(f"changing schema compatibility to FUll")
                    self.schema_registry_client.set_compatibility(
                        subject_name=self.subject_name,
                        level='FULL'
                    )
                else: 
                    self.logger.error(f"Schema is not compatible with the existing schema.")
            except SchemaRegistryError as e:
                self.logger.error(f"Failed to register schema: {e.error_message}")
        else:
            self.logger.info(f"Current local schema is up to date with the schema registry.")

        return AvroSerializer(
            self.schema_registry_client,
            schema_str,
        )
        



            