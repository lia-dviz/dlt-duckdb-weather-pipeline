{{ config(materialized='table') }}

SELECT 
    city,
    date_trunc('hour', timestamp_ingestion::TIMESTAMP) AS ingestion_hour,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(MAX(temperature), 2) AS max_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    COUNT(*) AS total_events
FROM {{ source('raw_staging', 'weather_raw') }}
GROUP BY 1, 2
