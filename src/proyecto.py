"""Utilidades para verificar el entorno y la entrada de datos de F1."""
from importlib.metadata import version
from pathlib import Path
import hashlib

import pandas as pd

def versiones_entorno():
    """Registra versiones; falla si falta una dependencia requerida."""
    paquetes = ("numpy", "pandas", "jupyterlab", "ipykernel",
                "nbformat", "nbconvert", "nbclient")
    return {nombre: version(nombre) for nombre in paquetes}


def sha256_archivo(ruta):
    """Calcula la huella por bloques, sin cargar todo el archivo en memoria."""
    resumen = hashlib.sha256()
    with Path(ruta).open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            resumen.update(bloque)
    return resumen.hexdigest()


def leer_datos_f1(ruta, columnas_requeridas, sep=";", encoding="latin-1"):
    """Lee el CSV sin limpiarlo y comprueba su esquema mínimo."""
    ruta = Path(ruta)
    if not ruta.is_file():
        raise FileNotFoundError(f"No existe un archivo de datos en: {ruta}")
    datos = pd.read_csv(ruta, sep=sep, encoding=encoding, low_memory=False)
    faltantes = sorted(set(columnas_requeridas) - set(datos.columns))
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(faltantes)}")
    if datos.empty:
        raise ValueError("El dataset no contiene registros.")
    return datos

