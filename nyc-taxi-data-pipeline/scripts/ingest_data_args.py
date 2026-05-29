import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine


def main(params):

    # Parámetros recibidos desde terminal
    calendar_month = params.calendar_month
    data_path = params.data_path
    table_name = params.table_name

    # Construcción dinámica del nombre del archivo
    csv_file = f"{data_path}/yellow_tripdata_{calendar_month}.csv"

    print(f"[INFO] Leyendo archivo: {csv_file}")

    # =========================================================
    # CONEXIÓN A POSTGRESQL
    #
    # IMPORTANTE:
    # Docker expone:
    # HOST (Windows) -> 5433
    # CONTENEDOR -> 5432
    #
    # Como Python corre en Windows,
    # debemos usar 5433.
    # =========================================================
 
    engine = create_engine(
       "postgresql+pg8000://root:root@pgdatabase:5432/ny_taxi"
    )

    print("[OK] Conexion a PostgreSQL establecida")

    # =========================================================
    # LEER CSV POR CHUNKS
    # =========================================================

    df_iter = pd.read_csv(
        csv_file,
        iterator=True,
        chunksize=100000
    )

    # =========================================================
    # PRIMER CHUNK
    # =========================================================

    df = next(df_iter)

    # Convertir fechas
    df["tpep_pickup_datetime"] = pd.to_datetime(
        df["tpep_pickup_datetime"]
    )

    df["tpep_dropoff_datetime"] = pd.to_datetime(
        df["tpep_dropoff_datetime"]
    )

    # =========================================================
    # CREAR TABLA
    # =========================================================

    df.head(n=0).to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"[INFO] Tabla '{table_name}' creada")

    # =========================================================
    # INSERTAR PRIMER CHUNK
    # =========================================================

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False
    )

    print("[OK] Primer chunk insertado")
    print("\n[INFO] Modo prueba: no se procesará el resto de los chunks.")
    return

    # =========================================================
    # RESTO DE CHUNKS
    # =========================================================

    chunk_count = 1

    while True:

        try:

            t_start = time()

            df = next(df_iter)

            # Convertir fechas
            df["tpep_pickup_datetime"] = pd.to_datetime(
                df["tpep_pickup_datetime"]
            )

            df["tpep_dropoff_datetime"] = pd.to_datetime(
                df["tpep_dropoff_datetime"]
            )

            # Insertar chunk
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists="append",
                index=False
            )

            chunk_count += 1

            t_end = time()

            print(
                f"[OK] Bloque #{chunk_count} insertado "
                f"en {t_end - t_start:.3f} segundos"
            )

        except StopIteration:

            print(
                f"\n[FIN] Ingesta completada. "
                f"Total: {chunk_count} bloques"
            )

            break


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--calendar_month",
        required=True,
        help="Mes del dataset, ejemplo: 2021-01"
    )

    parser.add_argument(
        "--data_path",
        required=True,
        help="Ruta donde está el CSV"
    )

    parser.add_argument(
        "--table_name",
        required=True,
        help="Nombre de la tabla en PostgreSQL"
    )

    args = parser.parse_args()

    main(args)