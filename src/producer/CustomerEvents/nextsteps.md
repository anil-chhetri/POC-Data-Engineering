# Next Steps for Denormalizing CustomerEvents Data

This document outlines the steps to denormalize the `CustomerEvents` module's data structure, preparing it for normalization in dbt (e.g., for Snowflake star schema or Data Vault modeling). The goal is to flatten nested objects, separate 1:N relationships into distinct tables, and add unique identifiers for easier dbt ingestion and transformation.

## Overview of Changes
- **Flatten 1:1 Relationships**: Convert nested objects (e.g., `device`, `location`) into prefixed top-level attributes in a main `ConsumerEvent` table.
- **Separate 1:N Relationships**: Create individual tables for lists (e.g., `user_actions`, `recommendations`), each linked by `event_id`.
- **Add Identifiers**: Introduce `event_id` (unique per event) and `user_id` (for user tracking) to enable relational modeling.
- **Data Types**: Ensure all fields are serializable (e.g., strings for timestamps) for database ingestion.
- **Output Structure**: Modify `generate_consumer_event_data()` to return a dictionary of tables (e.g., `{"consumer_event": [...], "user_actions": [...], ...}`) instead of a single nested dict.

## Step-by-Step Implementation

### 1. Update Core Classes for Flattening
   - Modify each class (e.g., `Device`, `Location`) to include a `to_flat_dict()` method that returns a flat dictionary with prefixed keys (e.g., `device_type` instead of nested `{"type": ...}`).
   - For lists within classes (e.g., `connected_services` in `UserSubscriptions`), serialize as JSON strings or comma-separated values.
   - Example for `device.py`:
     ```python
     class Device:
         # ... existing init and generate methods ...
         
         def to_flat_dict(self):
             return {
                 "device_type": self.type,
                 "device_os": self.os,
                 "device_os_version": self.os_version,
                 "device_app_version": self.app_version,
                 "device_model": self.model
             }
     ```
   - Apply similar changes to `Location`, `Content`, `UserSubscriptions`, and `EventDetails`.

### 2. Modify `generate_consumer_event_data()` in `generate_consumer.py`
   - Import `uuid` for generating IDs.
   - Generate `event_id` and `user_id` as UUIDs.
   - Instantiate components and call their `to_flat_dict()` methods to flatten.
   - For 1:N entities (`UserAction`, `Recommendations`, `SearchHistory`), generate lists of dicts, each including `event_id` as a foreign key.
   - Return a dictionary of tables instead of a single event dict.
   - Example structure:
     ```python
     import uuid
     from . import Device, Location, Content, UserSubscriptions, EventDetails, UserAction, Recommendations, SearchHistory
     
     def generate_consumer_event_data():
         event_id = str(uuid.uuid4())
         user_id = str(uuid.uuid4())
         
         # Generate and flatten 1:1 components
         device = Device().to_flat_dict()
         location = Location().to_flat_dict()
         content = Content().to_flat_dict()
         subscription = UserSubscriptions().to_flat_dict()
         event_details = EventDetails().to_flat_dict()
         
         # Main event dict (flattened)
         consumer_event = {
             "event_id": event_id,
             "user_id": user_id,
             "event_type": "playback",  # Or randomize
             "timestamp": "2025-12-26T12:00:00Z",  # ISO string
             **device,
             **location,
             **content,
             **subscription,
             **event_details
         }
         
         # 1:N tables
         user_actions = [action.to_dict() | {"event_id": event_id} for action in UserAction().generate_list()]
         recommendations = [rec.to_dict() | {"event_id": event_id} for rec in Recommendations().generate_list()]
         search_history = [sh.to_dict() | {"event_id": event_id} for sh in SearchHistory().generate_list()]
         
         return {
             "consumer_event": [consumer_event],  # List for batching
             "user_actions": user_actions,
             "recommendations": recommendations,
             "search_history": search_history
         }
     ```
   - Ensure `UserAction`, `Recommendations`, and `SearchHistory` have `to_dict()` methods and `generate_list()` to produce variable-length lists.

### 3. Update 1:N Classes for Dict Output
   - Add `to_dict()` methods to `UserAction`, `Recommendations`, and `SearchHistory` for serialization.
   - Modify generation logic to produce lists of instances (e.g., 0-5 actions per event).
   - Example for `user_action.py`:
     ```python
     class UserAction:
         # ... existing code ...
         
         def to_dict(self):
             return {
                 "action_type": self.action_type,
                 "timestamp": self.timestamp,
                 "duration": self.duration,
                 "completed": self.completed,
                 "old_quality": self.old_quality,
                 "new_quality": self.new_quality,
                 "old_speed": self.old_speed,
                 "new_speed": self.new_speed
             }
         
         @staticmethod
         def generate_list():
             # Return a list of UserAction instances (random count)
             return [UserAction() for _ in range(random.randint(0, 5))]
     ```

### 4. Test the Updated Generation
   - Run `generate_consumer_event_data()` and verify the output is a dict of lists, with no nested objects.
   - Check that `event_id` is consistent across tables.
   - Validate data types (e.g., all strings/ints/floats) for database compatibility.
   - Use Python's `json.dumps()` to ensure serializability.

### 5. Integrate with Producer and Database Ingestion
   - Update [src/producer/run_producer.py](http://_vscodecontentref_/0) to handle the new multi-table output (e.g., send each table to Kafka or directly to DB).
   - Ingest into PostgreSQL/DuckDB using your existing setup (e.g., via [init/postgres](http://_vscodecontentref_/1)).
   - Ensure tables are created with appropriate schemas (e.g., `event_id` as VARCHAR, timestamps as TEXT).

### 6. Set Up dbt Staging Models
   - Create dbt sources in [dbt/src](http://_vscodecontentref_/2) for each table (e.g., `source_consumer_event`).
   - Build staging models in dbt/models/staging/ to clean and type-cast data.
   - Example `staging_consumer_event.sql`:
     ```sql
     SELECT
         event_id::varchar AS event_id,
         user_id::varchar AS user_id,
         event_type,
         timestamp::timestamp AS event_timestamp,
         device_type,
         -- ... other fields
     FROM {{ source('raw_events', 'consumer_event') }}
     ```
   - Add dbt tests for uniqueness (e.g., `event_id`) and relationships.

### 7. Implement Normalization in dbt
   - **For Snowflake Schema**: Create fact tables (e.g., `fact_events` from `consumer_event`) and dimensions (e.g., `dim_device` from flattened device fields).
   - **For Data Vault**:
     - Hubs: `hub_events` (key: `event_id`), `hub_users` (key: `user_id`).
     - Links: `link_event_user` (connecting hubs).
     - Satellites: `sat_event_details` (attributes from `consumer_event`), `sat_user_actions` (from `user_actions` table).
   - Use dbt macros (e.g., `dbt_utils.surrogate_key`) for keys and incremental loads.

### 8. Validate and Iterate
   - Run dbt tests and builds to ensure normalization works.
   - Generate sample data at scale and check performance.
   - Update the ERD in [README.md](http://_vscodecontentref_/3) to reflect the new denormalized structure.
   - If issues arise (e.g., data inconsistencies), refine Faker seeding or validation.

## Dependencies and Tools
- **Python Libraries**: Add `uuid` to imports; ensure `faker` is seeded for reproducibility.
- **dbt**: Use dbt-postgres or dbt-duckdb adapters based on your setup.
- **Testing**: Use pytest for Python unit tests; dbt's built-in testing for models.

## Risks and Considerations
- **Performance**: Generating large lists for 1:N may slow down if not batched.
- **Schema Evolution**: Add version fields if the structure changes.
- **Data Quality**: Implement validation in classes to prevent invalid data (e.g., negative durations).

Once these steps are complete, the data will be fully denormalized for flexible dbt transformations. If you encounter issues, share error logs or specific files for further assistance.