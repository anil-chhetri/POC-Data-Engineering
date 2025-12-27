{{config(
    materialized='table',
    file_format='parquet',
    partition_by=['inserted_date_time'],
    schema="staging"
)}}

WITH cte AS (

    SELECT
        data->>'user_id' as user_id,
        {{ function('get_filename_from_path') }} (data->>'filename') as source_file_name,
        /* ---------------------- CONTENT ---------------------- */
        data->>'content.id'              AS content_id,
        data->>'content.type'            AS content_type,
        data->>'content.title'           AS content_title,
        data->>'content.genre'           AS content_genre,
        data->>'content.season'          AS content_season,
        data->>'content.episode'         AS content_episode,
        data->>'content.duration'        AS content_duration,
        data->>'content.language'        AS content_language,
        data->>'content.provider'        AS content_provider,
        data->>'content.release_year'    AS content_release_year,

        /* ---------------------- EVENT ------------------------ */
        data->>'timestamp'                       AS created_date_time,
        data->>'event_type'                      AS event_type,
        data->>'event_details.paused'            AS event_details_paused,
        data->>'event_details.bandwidth'         AS event_details_bandwidth,
        data->>'event_details.completed'         AS event_details_completed,
        data->>'event_details.network_type'      AS event_details_network_type,
        data->>'event_details.play_duration'     AS event_details_play_duration,
        data->>'event_details.playback_speed'    AS event_details_playback_speed,
        data->>'event_details.play_percentage'   AS event_details_play_percentage,
        data->>'event_details.playback_quality'  AS event_details_playback_quality,
        data->>'event_details.buffering_incidents' AS event_details_buffering_incidents,

        /* ---------------------- DEVICE ----------------------- */
        data->>'device.os'            AS device_operating_system,
        data->>'device.type'          AS device_type,
        data->>'device.model'         AS device_model,
        data->>'device.os_version'    AS device_os_version,
        data->>'device.app_version'   AS device_app_version,

        /* ---------------------- LOCATION --------------------- */
        data->>'location.city'        AS location_city,
        data->>'location.region'      AS location_region,
        data->>'location.country'     AS location_country,
        data->>'location.timezone'    AS location_timezone,

        /* ---------------------- USER SUBSCRIPTION ------------ */
        data->>'user_subscription.plan'          AS user_subscription_plan,
        data->>'user_subscription.start_date'    AS user_subscription_start_date,
        data->>'user_subscription.billing_cycle' AS user_subscription_billing_cycle,
        ARRAY(
            SELECT TRIM(BOTH '"' FROM element.value::text)
            FROM jsonb_array_elements(data->'user_subscription.connected_services') AS element
        ) AS user_subscription_connected_services,

        /* ---------------------- USER RECOMMENDATIONS --------- */
        user_recommendations->>'clicked'     AS user_recommendations_clicked,
        user_recommendations->>'position'    AS user_recommendations_position,
        user_recommendations->>'algorithm'   AS user_recommendations_algorithm,
        user_recommendations->>'content_id'  AS user_recommendations_content_id,

        /* ---------------------- USER SEARCH HISTORY ---------- */
        user_search_history->>'query'         AS user_search_history_query,
        user_search_history->>'search_id'     AS user_search_id,
        user_search_history->>'timestamp'     AS user_search_history_timestamp,
        user_search_history->>'results_count' AS user_search_history_results_count,

        /* ---------------------- USER ACTION ------------------ */
        user_action->>'duration'     AS user_action_duration,
        user_action->>'completed'    AS user_action_completed,
        user_action->>'new_speed'    AS user_action_new_speed,
        user_action->>'old_speed'    AS user_action_old_speed,
        user_action->>'action_type'  AS user_action_type,
        user_action->>'timestamp'    AS user_action_timestamp,
        user_action->>'new_quality'  AS user_action_new_quality,
        user_action->>'old_quality'  AS user_action_old_quality

    FROM {{ source('staging', 'customer') }} AS b
    , jsonb_array_elements(b.data->'user_action') AS user_action
    , jsonb_array_elements(b.data->'search_history') AS user_search_history
    , jsonb_array_elements(b.data->'recommendations') AS user_recommendations
)

SELECT
    *,
    {{ compute_hash(["content_id", "created_date_time", "CURRENT_date"]) }} AS event_id,
    CURRENT_date AS inserted_date_time
FROM cte
