import requests
import config


def main():

    print("Iniciando conexión...")
    #response = requests.get(config.CSV_URL) -- Se queda colgado, se cambió por:
    response = requests.get(config.CSV_URL, timeout=60)
    response.raise_for_status()

    print("Código de respuesta:", response.status_code)
    print("URL final:", response.url)
    print("Tipo de contenido:", response.headers.get("Content-Type"))

    if response.status_code == 200:

        file_path = (
            f"{config.RAW_FOLDER}/"
            f"{config.RAW_FILE_NAME}"
        )

        with open(file_path, "wb") as file:
            file.write(response.content)

        print()
        print("Archivo guardado correctamente")
        print("Ruta:", file_path)

    else:
        print("Error al descargar archivo")


if __name__ == "__main__":
    main()