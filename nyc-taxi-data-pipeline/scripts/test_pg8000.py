from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+pg8000://",
    connect_args={
        "host": "localhost",
        "port": 5433,
        "database": "ny_taxi",
        "user": "root",
        "password": "root"
    }
)

with engine.connect() as conn:
    result = conn.exec_driver_sql("SELECT 1 AS test")
    print("Conexion exitosa:", result.scalar())