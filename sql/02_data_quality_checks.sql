SELECT *
FROM yellow_taxi_data
WHERE
    "PULocationID" IS NULL
    OR "DOLocationID" IS NULL;