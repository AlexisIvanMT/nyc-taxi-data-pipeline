import argparse
import os
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main():
# Cambiamos el puerto de 5432 a 5433
    db_url = "postgresql+pg8000://root:root@localhost:5433/ny_taxi"
    engine = create_engine(db_url)
    print("[OK] Conexion a PostgreSQL establecida")

    # 2. Archivo CSV
    csv_file = "yellow_tripdata_2021-01.csv"
    print(f"[INFO] Leyendo {csv_file} en bloques de 100,000 filas...")

    # 3. Crear iterador
    df_iter = pd.read_csv(csv_file, iterator=True, chunksize=100000)

    # 4. Procesar PRIMER bloque
    df = next(df_iter)
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    
    df.head(n=0).to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="replace",
        index=False
    )
    print("[INFO] Tabla 'yellow_taxi_data' creada")

    df.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append",
        index=False
    )
    print("[OK] Primer bloque insertado")

    # 5. Procesar el RESTO de bloques
    chunk_count = 1
    while True:
        try:
            t_start = time()
            df = next(df_iter)
            df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
            df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
            df.to_sql(name="yellow_taxi_data", con=engine, if_exists="append", index=False)
            chunk_count += 1
            t_end = time()
            print(f"[OK] Bloque #{chunk_count} insertado en {t_end - t_start:.3f} segundos")
        except StopIteration:
            print(f"\n[FIN] Ingesta completada. Total: {chunk_count} bloques")
            break

if __name__ == "__main__":
    main()