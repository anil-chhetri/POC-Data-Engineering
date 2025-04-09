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
flowchart LR
    A["Kafka Producer"] L_A_B_0@--> B["Kafka Topic"]
    B L_B_C_0@--> C["KSQL Stream Processing"]
    C L_C_D_0@--> D["dbt Models"]
    D L_D_E_0@--> E["DuckDB Analytics"]


    L_A_B_0@{ animation: slow } 
    L_B_C_0@{ animation: slow } 
    L_C_D_0@{ animation: slow } 
    L_D_E_0@{ animation: slow } 


