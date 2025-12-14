# Consumer Module

This module implements a Kafka consumer for processing customer event data from a Kafka topic and persisting it to Parquet files. It is part of a Proof of Concept (POC) for Data Engineering, focusing on streaming data consumption and storage.

## Overview

The consumer subscribes to the `customer_events` Kafka topic, consumes messages containing Avro-serialized customer event data, deserializes them, and periodically saves batches of data to Parquet files for further analysis or processing.

## Key Components

### 1. Kafka Consumer (`consumer.py`)
- Implements the main consumer logic using Confluent Kafka Consumer
- Subscribes to the `customer_events` topic
- Handles message deserialization using Avro schemas from Schema Registry
- Processes messages in batches and accumulates data for bulk saving
- Provides error handling and graceful shutdown

### 2. Data Persistence (`savejson.py`)
- Handles saving consumed data to Parquet format using PyArrow
- Normalizes nested JSON data into flat tabular structure using pandas
- Generates unique filenames for each Parquet file
- Saves files to the `parquet_data/data/` directory

### 3. Custom Logging (`custom_logging.py`)
- Provides colored console logging with custom formatting
- Supports different log levels with appropriate colors
- Extends Python's logging module for better visibility

## Data Flow

1. **Subscription**: Consumer subscribes to the `customer_events` Kafka topic
2. **Consumption**: Polls for messages in batches of 5 with a 1-second timeout
3. **Deserialization**: Uses Avro deserializer to convert binary messages back to Python objects
4. **Accumulation**: Collects messages in memory until reaching 1200 messages
5. **Persistence**: Saves accumulated data to a Parquet file and resets the counter
6. **Monitoring**: Logs consumption progress and handles errors

## Usage

Run the consumer using:

```bash
python run_consumer.py
```

This will start consuming messages from Kafka. The consumer will:
- Process messages continuously
- Save data to Parquet every 1200 messages
- Handle keyboard interrupts gracefully by saving any remaining data
- Provide detailed logging of the consumption process

## Configuration

Key configuration points:

- **Kafka Broker**: `kafka:9092` (configured for Docker environment)
- **Schema Registry**: `http://schema-registry:8081`
- **Topic**: `customer_events`
- **Group ID**: Configurable (default: 4)
- **Batch Size**: 1200 messages per Parquet file
- **Poll Timeout**: 1 second
- **Auto Commit**: Enabled with 5-second intervals

## Data Processing

- **Input**: Avro-serialized binary messages from Kafka
- **Deserialization**: Converts to Python dictionaries using registered Avro schemas
- **Normalization**: Flattens nested JSON structures into tabular format
- **Output**: Parquet files with efficient columnar storage

## Dependencies

- `confluent-kafka`: For Kafka consumer and schema registry operations
- `pyarrow`: For Parquet file writing
- `pandas`: For data normalization and manipulation

## Error Handling

- Handles message consumption errors
- Manages deserialization failures
- Provides graceful shutdown on keyboard interrupt
- Logs all errors with detailed information

## Output

Consumed data is saved as Parquet files in the `parquet_data/data/` directory with UUID-based filenames. Each file contains up to 1200 customer events in a flattened, queryable format suitable for analytics workloads.