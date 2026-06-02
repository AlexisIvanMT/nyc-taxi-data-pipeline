SELECT current_database();

SELECT COUNT(*)
FROM yellow_taxi_data;

SELECT
    MIN(tpep_pickup_datetime) AS fecha_min,
    MAX(tpep_pickup_datetime) AS fecha_max
FROM yellow_taxi_data;