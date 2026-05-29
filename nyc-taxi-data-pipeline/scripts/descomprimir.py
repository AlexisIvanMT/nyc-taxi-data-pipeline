import gzip
import shutil

input_file = "yellow_tripdata_2021-01.csv.gz"
output_file = "yellow_tripdata_2021-01.csv"

print(f"Descomprimiendo {input_file}...")

with gzip.open(input_file, 'rb') as f_in:
    with open(output_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print("✅ ¡Listo! Archivo creado:", output_file)