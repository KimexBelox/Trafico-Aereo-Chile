import pandas as pd
import config


def main():

    input_path = f"{config.RAW_FOLDER}/{config.RAW_FILE_NAME}"
    output_path = f"{config.PROCESSED_FOLDER}/{config.TRANSFORMED_FILE_NAME}"

    df = pd.read_csv(input_path, sep=";")

    df["Fecha"] = pd.to_datetime(
        df["Año"].astype(str) + "-" + df["Mes"].astype(str) + "-01"
    )

    print("===== VALIDACIÓN FECHA =====")
    print(df[["Año", "Mes", "Fecha"]].head())

    print("\n===== TIPO DE DATO FECHA =====")
    print(df["Fecha"].dtype)

    print("\n===== VALIDACIÓN FECHA NULA =====")
    print(df["Fecha"].isnull().sum())

    print("\n===== RANGO DE FECHAS =====")
    print("Fecha mínima:", df["Fecha"].min())
    print("Fecha máxima:", df["Fecha"].max())

    print("\n===== PERIODOS DISPONIBLES =====")
    periodos = df["Fecha"].drop_duplicates().sort_values().reset_index(drop=True)
    print(periodos)

    print("\n===== CANTIDAD DE PERIODOS =====")
    print(df["Fecha"].nunique())

    # ==========================================
    # VALIDACIONES FINALES
    # ==========================================

    print("\n===== VALIDACIONES FINALES =====")

    registros_iniciales = len(df)

    fechas_nulas = df["Fecha"].isnull().sum()
    print("Fechas nulas:", fechas_nulas)

    periodos = df["Fecha"].nunique()
    print("Periodos únicos:", periodos)

    duplicados = df.duplicated().sum()
    print("Filas duplicadas exactas:", duplicados)

    columnas = len(df.columns)
    print("Columnas finales:", columnas)

    if fechas_nulas == 0:
        print("OK: No existen fechas nulas.")
    else:
        print("ALERTA: Existen fechas nulas.")

    if duplicados == 0:
        print("OK: No existen filas duplicadas exactas.")
    else:
        print("ALERTA: Existen filas duplicadas exactas. "
            "No se eliminan automáticamente; se dejan para análisis de negocio.")


    if duplicados > 0:
        print("\n===== MUESTRA DE DUPLICADOS =====")
        print(df[df.duplicated(keep=False)].sort_values(["Año", "Mes"]).head(20))

    # ==========================================
    # EXPORTAR
    # ==========================================

    df.to_csv(
        output_path,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nArchivo transformado generado correctamente")
    print("Ruta:", output_path)
    print("Registros exportados:", registros_iniciales)

    #============VALIDACION============
    print("\n===== TOTALES CONTROL =====")
    print("PASAJEROS:", df["PASAJEROS"].sum())
    print("CARGA:", df["CARGA (Ton)"].sum())
    print("CORREO:", df["CORREO"].sum())
#===============================================

if __name__ == "__main__":
    main()