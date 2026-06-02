SELECT
    CAST(tpep_pickup_datetime AS DATE) AS dia,
    COUNT(*) AS viajes
FROM yellow_taxi_data
GROUP BY dia
ORDER BY dia;