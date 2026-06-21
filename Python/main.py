from datetime import datetime
import os

import extract
import transform
import profile_dataset
import generate_sql
import load
import config


def escribir_log(mensaje):
    os.makedirs(config.LOG_FOLDER, exist_ok=True)

    log_path = f"{config.LOG_FOLDER}/etl_log.txt"

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a", encoding="utf-8") as file:
        file.write(f"{fecha_hora} | {mensaje}\n")


def ejecutar_paso(numero, total, nombre, funcion):
    print(f"\n[{numero}/{total}] {nombre}")
    escribir_log(f"INICIO - {nombre}")

    try:
        funcion()
        escribir_log(f"OK - {nombre}")
    except Exception as error:
        escribir_log(f"ERROR - {nombre}: {error}")
        print(f"ERROR en {nombre}: {error}")
        raise


def main():

    print("===================================")
    print("INICIO PIPELINE ETL")
    print("===================================")

    escribir_log("===================================")
    escribir_log("INICIO PIPELINE ETL")

    ejecutar_paso(1, 5, "Extract", extract.main)
    ejecutar_paso(2, 5, "Transform", transform.main)
    ejecutar_paso(3, 5, "Profile Dataset", profile_dataset.main)
    ejecutar_paso(4, 5, "Generate SQL", generate_sql.main)
    ejecutar_paso(5, 5, "Load SQL Server", load.main)

    escribir_log("PIPELINE ETL FINALIZADO CORRECTAMENTE")
    escribir_log("===================================")

    print("\n===================================")
    print("PIPELINE ETL FINALIZADO CORRECTAMENTE")
    print("===================================")


if __name__ == "__main__":
    main()