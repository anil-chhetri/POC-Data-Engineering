# CustomerEvents Module

This module is part of a Proof of Concept (POC) for Data Engineering, specifically designed to generate synthetic customer event data for a media streaming platform. It simulates user interactions, content details, device information, and other related data points to mimic real-world streaming service events.

The module uses the Faker library to generate realistic fake data and provides a structured way to produce event data that can be used for testing, analytics, or data pipeline development.

## Overview

The `CustomerEvents` folder contains Python classes and functions that model various aspects of customer events in a streaming service. Each class represents a component of the event data, such as content metadata, user device details, location information, and user actions. The main entry point is the `generate_consumer_event_data()` function, which combines data from all components to create a complete event dictionary.

## Modules

### `__init__.py`
- Defines the module version and imports all the key classes and functions for easy access.
- Imports: `generate_consumer_event_data`, `Content`, `Device`, `EventDetails`, `Location`, `UserSubscriptions`, `UserAction`, `Recommendations`, `SearchHistory`, `MediaContentProvider`.

### `content.py`
- Defines the `Content` class, which represents media content (e.g., movies, TV shows).
- Attributes include ID, title, type, episode, season, provider, genre, release year, duration, and language.
- Provides methods to convert to dictionary and generate fake content data using Faker and a custom `MediaContentProvider`.

### `device.py`
- Defines the `Device` class for user device information.
- Includes device type (mobile, desktop, tablet, smartTV), OS, OS version, app version, and model.
- Generates random device data based on the device type.

### `eventdetails.py`
- Defines the `EventDetails` class for playback event specifics.
- Attributes cover play duration, percentage, quality, buffering, speed, pause status, completion, network type, and bandwidth.
- Generates random event details data.

### `generate_consumer.py`
- Contains the main `generate_consumer_event_data()` function.
- Combines data from all other classes to produce a comprehensive consumer event dictionary.
- Includes fields like device, location, content, event type, user subscription, timestamp, event details, user actions, recommendations, and search history.

### `location.py`
- Defines the `Location` class for user geographical data.
- Supports multiple countries with appropriate Faker locales.
- Generates random location data including country, city, region, and timezone.

### `mediaprovider.py`
- Implements a custom Faker provider (`MediaContentProvider`) for generating media-specific data.
- Includes methods for generating titles, content types, seasons/episodes, durations, languages, providers, genres, and release years.
- Uses predefined lists and formats to create realistic media content metadata.

### `recommendations.py`
- Defines the `Recommendations` class for generating content recommendations.
- Produces a list of recommendations with content ID, position, algorithm type, and click status.

### `searchhistory.py`
- Defines the `SearchHistory` class for user search activities.
- Generates a list of search entries with search ID, timestamp, query, and results count.

### `user_action.py`
- Defines the `UserAction` class for various user interactions during playback.
- Supports actions like pause, completion, quality change, and playback speed adjustment.
- Generates detailed action data with timestamps and relevant parameters.

### `user_subscriptions.py`
- Defines the `UserSubscriptions` class for user subscription information.
- Includes plan type, start date, billing cycle, and connected services.
- Generates random subscription data.

## Data Model (ERD)

Based on the generated event data, the following Entity-Relationship Diagram (ERD) represents the relationships between the key data structures. The main entity is `ConsumerEvent`, which aggregates data from various sub-entities.

### Key Assumptions
- **Entities**: Each major class or data structure is an entity.
- **Relationships**: One-to-one (1:1) for single objects, one-to-many (1:N) for lists.
- **Purpose**: Conceptual schema for relational modeling of streaming events.

### ERD Diagram (ASCII Art)
```
+-------------------+       +-------------------+
|  ConsumerEvent    |       |     Device        |
+-------------------+       +-------------------+
| - event_type      |1:1    | - type            |
| - timestamp       |------>| - os              |
+-------------------+       | - os_version      |
                            | - app_version     |
                            | - model           |
                            +-------------------+

+-------------------+       +-------------------+
|  ConsumerEvent    |       |    Location       |
+-------------------+       +-------------------+
|                   |1:1    | - country         |
|                   |------>| - city            |
+-------------------+       | - region          |
                            | - timezone        |
                            +-------------------+

+-------------------+       +-------------------+
|  ConsumerEvent    |       |     Content       |
+-------------------+       +-------------------+
|                   |1:1    | - id              |
|                   |------>| - title           |
+-------------------+       | - type            |
                            | - episode         |
                            | - season          |
                            | - provider        |
                            | - genre           |
                            | - release_year    |
                            | - duration        |
                            | - language        |
                            +-------------------+

+-------------------+       +-------------------+
|  ConsumerEvent    |       | UserSubscription  |
+-------------------+       +-------------------+
|                   |1:1    | - plan            |
|                   |------>| - start_date      |
+-------------------+       | - billing_cycle   |
                            | - connected_services (list)|
                            +-------------------+

+-------------------+       +-------------------+
|  ConsumerEvent    |       |  EventDetails     |
+-------------------+       +-------------------+
|                   |1:1    | - play_duration   |
|                   |------>| - play_percentage |
+-------------------+       | - playback_quality|
                            | - buffering_incidents|
                            | - playback_speed  |
                            | - paused          |
                            | - completed       |
                            | - network_type    |
                            | - bandwidth       |
                            +-------------------+

+-------------------+       +-------------------+
|  ConsumerEvent    |       |   UserAction      |
+-------------------+       +-------------------+
|                   |1:N    | - action_type     |
|                   |------>| - timestamp       |
+-------------------+       | - duration        |
                            | - completed       |
                            | - old_quality     |
                            | - new_quality     |
                            | - old_speed       |
                            | - new_speed       |
                            +-------------------+

+-------------------+       +-------------------+
|  ConsumerEvent    |       | Recommendation    |
+-------------------+       +-------------------+
|                   |1:N    | - content_id      |
|                   |------>| - position        |
+-------------------+       | - algorithm       |
                            | - clicked         |
                            +-------------------+

+-------------------+       +-------------------+
|  ConsumerEvent    |       |  SearchHistory    |
+-------------------+       +-------------------+
|                   |1:N    | - search_id       |
|                   |------>| - timestamp       |
+-------------------+       | - query           |
                            | - results_count   |
                            +-------------------+
```

### Entity Descriptions and Attributes

1. **ConsumerEvent** (Main entity)
   - **Attributes**: `event_type` (string), `timestamp` (string).
   - **Relationships**: Central hub linking to all others.

2. **Device**
   - **Attributes**: `type`, `os`, `os_version`, `app_version`, `model` (all strings).
   - **Relationships**: 1:1 with ConsumerEvent.

3. **Location**
   - **Attributes**: `country`, `city`, `region`, `timezone` (all strings).
   - **Relationships**: 1:1 with ConsumerEvent.

4. **Content**
   - **Attributes**: `id`, `title`, `type`, `provider`, `genre`, `language` (strings); `episode`, `season`, `release_year`, `duration` (ints).
   - **Relationships**: 1:1 with ConsumerEvent.

5. **UserSubscription**
   - **Attributes**: `plan`, `start_date`, `billing_cycle` (strings); `connected_services` (list of strings).
   - **Relationships**: 1:1 with ConsumerEvent.

6. **EventDetails**
   - **Attributes**: `play_duration` (int), `play_percentage` (float), `playback_quality`, `network_type`, `bandwidth` (strings); `buffering_incidents` (int), `playback_speed` (float); `paused`, `completed` (bools).
   - **Relationships**: 1:1 with ConsumerEvent.

7. **UserAction**
   - **Attributes**: `action_type`, `timestamp` (strings); `duration` (int); `completed` (bool); `old_quality`, `new_quality` (strings); `old_speed`, `new_speed` (floats).
   - **Relationships**: 1:N with ConsumerEvent.

8. **Recommendation**
   - **Attributes**: `content_id` (string), `position` (int), `algorithm` (string), `clicked` (bool).
   - **Relationships**: 1:N with ConsumerEvent.

9. **SearchHistory**
   - **Attributes**: `search_id`, `timestamp`, `query` (strings); `results_count` (int).
   - **Relationships**: 1:N with ConsumerEvent.

## Usage

To generate a sample consumer event:

```python
from CustomerEvents import generate_consumer_event_data

event = generate_consumer_event_data()
print(event)
```

This will output a dictionary containing all the simulated event data.

## Dependencies

- `faker`: For generating fake data.
- Standard Python libraries: `random`, `datetime`, `json`.

## Purpose

This module is designed for data engineering POC work, allowing developers to create realistic streaming event data without relying on actual user data. It can be used to test data pipelines, analytics systems, or machine learning models that process streaming service events.