# Real-Time Data Pipeline with Kafka, KSQL, dbt, and DuckDB

## Overview
- **Purpose**: Stream and process IoT data in real-time, transform batches with dbt, and analyze with DuckDB.
- **Tech Stack**:
  - **Streaming**: Kafka (producers/consumers in Python), KSQL for stream processing.
  - **Transformations**: dbt for SQL-based modeling.
  - **Analytics**: DuckDB for embedded OLAP queries.
  - **Orchestration**: Python scripts for workflow automation.

## Architecture
```mermaid
graph LR
  A[Kafka Producer] --> B[Kafka Topic]
  B --> C[KSQL Stream Processing]
  C --> D[dbt Models]
  D --> E[DuckDB Analytics]


