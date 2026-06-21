import pandas as pd
import pyodbc
import config
from datetime import datetime


def main():

    print("===== INICIO CARGA SQL SERVER =====")

    input_path = f"{config.PROCESSED_FOLDER}/{config.TRANSFORMED_FILE_NAME}"

    df = pd.read_csv(
        input_path,
        sep=";",
        parse_dates=["Fecha"]
    )

    df.columns = [
    columna.replace(" ", "_").replace("(", "").replace(")", "")
    for columna in df.columns
    ]

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    print("Registros CSV:", len(df))

    conexion = pyodbc.connect(
        f"DRIVER={{SQL Server}};"
        f"SERVER={config.SQL_SERVER};"
        f"DATABASE={config.DATABASE_NAME};"
        f"Trusted_Connection=yes;"
    )

    cursor = conexion.cursor()

    print("Conexión exitosa")

    cursor.execute(
        f"TRUNCATE TABLE {config.STAGING_SCHEMA}.{config.STAGING_TABLE}"
    )

    conexion.commit()

    print("Tabla limpiada")

    columnas = ",".join(f"[{c}]" for c in df.columns)

    placeholders = ",".join(["?"] * len(df.columns))

    insert_sql = f"""
    INSERT INTO {config.STAGING_SCHEMA}.{config.STAGING_TABLE}
    ({columnas})
    VALUES ({placeholders})
    """

    cursor.fast_executemany = False

    cursor.executemany(
        insert_sql,
        df.values.tolist()
    )

    conexion.commit()

    print("Carga completada")

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM {config.STAGING_SCHEMA}.{config.STAGING_TABLE}
        """
    )

    registros_sql = cursor.fetchone()[0]

    print()
    print("===== VALIDACIÓN =====")
    print("CSV:", len(df))
    print("SQL:", registros_sql)

    if len(df) == registros_sql:
        print("OK: Conteos coinciden")
    else:
        print("ALERTA: Conteos distintos")

    estado = "OK" if len(df) == registros_sql else "ALERTA"

    cursor.execute(
        """
        INSERT INTO stg.Ejecucion_ETL
        (Fecha_Ejecucion, Registros_Cargados, Estado)
        VALUES (?, ?, ?)
        """,
        datetime.now(),
        registros_sql,
        estado
    )

    conexion.commit()

    print("Registro de ejecución ETL guardado")

    cursor.close()
    conexion.close()


if __name__ == "__main__":
    main()