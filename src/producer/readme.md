# Producer Module

This module implements a Kafka producer for generating and sending customer event data to a Kafka topic. It is part of a Proof of Concept (POC) for Data Engineering, focusing on streaming data pipelines.

## Overview

The producer generates synthetic customer event data representing user interactions with a media streaming platform. The data includes details about devices, locations, content, user actions, recommendations, and more. This data is serialized using Avro and sent to a Kafka topic for consumption by downstream processing systems.

## Key Components

### 1. Kafka Configuration (`kafka_configuration.py`)
- Handles Kafka admin operations
- Creates the `customer_events` topic with specified partitions and replication factor
- Uses Confluent Kafka AdminClient for topic management

### 2. Schema Registry (`kafka_schema_registry.py`)
- Manages Avro schemas for data serialization
- Registers schemas with the Confluent Schema Registry
- Handles schema versioning and compatibility checks
- Loads schemas from local `Schema/` directory

### 3. Kafka Producer (`kafka_producer.py`)
- Implements the main producer logic using Confluent Kafka SerializingProducer
- Serializes messages using Avro schemas
- Handles message delivery reports and error handling
- Configured for reliability with retries, compression, and acknowledgments

### 4. Custom Logging (`custom_logging.py`)
- Provides colored console logging with custom formatting
- Supports different log levels with appropriate colors
- Extends Python's logging module for better visibility

### 5. Customer Events Data Generation (`CustomerEvents/`)
This folder contains classes for generating synthetic event data:

- **`generate_consumer.py`**: Main function to generate complete event data
- **`device.py`**: Generates device information (type, OS, model, versions)
- **`location.py`**: Generates user location data (country, city, region, timezone)
- **`content.py`**: Generates content metadata (title, type, episode, season, etc.)
- **`user_subscriptions.py`**: Generates user subscription details
- **`eventdetails.py`**: Generates playback event details (duration, quality, buffering, etc.)
- **`user_action.py`**: Generates user interaction actions (play, pause, seek, etc.)
- **`recommendations.py`**: Generates recommendation data
- **`searchhistory.py`**: Generates search history data

### 6. Avro Schema (`Schema/v1.avsc`)
- Defines the Avro schema for the `UserEvent` record
- Includes nested records for Device, Location, Content, UserSubscription, EventDetails, and arrays for UserAction, Recommendations, and SearchHistory

## Data Flow

1. **Initialization**: Kafka configuration creates the topic if it doesn't exist
2. **Schema Management**: Schema Registry ensures the latest Avro schema is registered and compatible
3. **Data Generation**: Synthetic event data is generated using Faker and random data
4. **Serialization**: Data is serialized using Avro according to the registered schema
5. **Production**: Messages are sent to the `customer_events` Kafka topic
6. **Monitoring**: Delivery reports and logging provide visibility into the production process

## Usage

Run the producer using:

```bash
python run_producer.py
```

This will start an infinite loop generating and sending events to Kafka. Use Ctrl+C to stop.

## Dependencies

- `confluent-kafka`: For Kafka producer and schema registry operations
- `faker`: For generating realistic fake data
- `deepdiff`: For schema comparison

## Configuration

Key configuration points:

- **Kafka Broker**: `kafka:9092` (configured for Docker environment)
- **Schema Registry**: `http://schema-registry:8081`
- **Topic**: `customer_events`
- **Partitions**: 3 (configurable)
- **Replication Factor**: 1 (for single-node setup)

## Event Types

The producer generates three main event types:
- `content_play`: User playing content
- `search`: User performing searches
- `browse`: User browsing the platform

Each event includes comprehensive metadata to simulate real-world streaming platform interactions.