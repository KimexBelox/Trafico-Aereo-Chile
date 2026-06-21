import pandas as pd
import config


def mapear_tipo_sql(columna, dtype):
    dtype = str(dtype)

    if columna in ["Año", "Mes"]:
        return "INT"

    if dtype.startswith("int") or dtype.startswith("float"):
        return "FLOAT"

    if dtype.startswith("datetime"):
        return "DATE"

    return "NVARCHAR(255)"


def main():
    input_path = f"{config.PROCESSED_FOLDER}/{config.TRANSFORMED_FILE_NAME}"
    output_path = f"{config.SQL_FOLDER}/{config.SQL_SCRIPT_NAME}"

    df = pd.read_csv(
    input_path,
    sep=";",
    parse_dates=["Fecha"]
)

    columnas_sql = []

    for columna, dtype in df.dtypes.items():
        tipo_sql = mapear_tipo_sql(columna, dtype)
        columna_limpia = columna.replace(" ", "_").replace("(", "").replace(")", "")
        columnas_sql.append(f"    [{columna_limpia}] {tipo_sql} NULL")

    create_table = f"USE {config.DATABASE_NAME};\nGO\n\n"
    create_table += (
        f"IF OBJECT_ID('{config.STAGING_SCHEMA}.{config.STAGING_TABLE}', 'U') "
        "IS NOT NULL\n"
    )
    create_table += f"    DROP TABLE {config.STAGING_SCHEMA}.{config.STAGING_TABLE};\nGO\n\n"
    create_table += f"CREATE TABLE {config.STAGING_SCHEMA}.{config.STAGING_TABLE} (\n"
    create_table += ",\n".join(columnas_sql)
    create_table += "\n);\nGO\n"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(create_table)

    print("Script SQL generado correctamente")
    print("Ruta:", output_path)


if __name__ == "__main__":
    main()