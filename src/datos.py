"""Lectura orientada a objetos, exportación y trazabilidad."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import hashlib
import pandas as pd


def sha256_archivo(ruta):
    """Calcula la huella por bloques, sin cargar todo el archivo en memoria."""
    resumen = hashlib.sha256()
    with Path(ruta).open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            resumen.update(bloque)
    return resumen.hexdigest()


@dataclass(frozen=True)
class ContratoEsquema:
    """Contrato inmutable que define el esquema mínimo de una fuente de datos."""

    columnas_requeridas: tuple[str, ...]

    def __post_init__(self):
        if not self.columnas_requeridas:
            raise ValueError("El contrato debe declarar al menos una columna requerida.")
        if len(set(self.columnas_requeridas)) != len(self.columnas_requeridas):
            raise ValueError("El contrato no admite columnas requeridas duplicadas.")

    def validar(self, datos):
        """Valida presencia de columnas y existencia de registros."""
        faltantes = sorted(set(self.columnas_requeridas) - set(datos.columns))
        if faltantes:
            raise ValueError(f"Faltan columnas requeridas: {', '.join(faltantes)}")
        if datos.empty:
            raise ValueError("El dataset no contiene registros.")


class LectorDatos(ABC):
    """Interfaz polimórfica para lectores sujetos a un contrato de esquema."""

    def __init__(self, contrato):
        if not isinstance(contrato, ContratoEsquema):
            raise TypeError("contrato debe ser una instancia de ContratoEsquema.")
        self._contrato = contrato

    @property
    def contrato(self):
        return self._contrato

    @abstractmethod
    def leer(self, ruta):
        """Lee y valida una fuente de datos."""


class LectorCSV(LectorDatos):
    """Lector concreto de CSV con configuración encapsulada."""

    def __init__(self, contrato, sep=";", encoding="latin-1"):
        super().__init__(contrato)
        self._sep = sep
        self._encoding = encoding

    def leer(self, ruta):
        ruta = Path(ruta)
        if not ruta.is_file():
            raise FileNotFoundError(f"No existe un archivo de datos en: {ruta}")
        datos = pd.read_csv(
            ruta, sep=self._sep, encoding=self._encoding, low_memory=False
        )
        self.contrato.validar(datos)
        return datos


def leer_datos_f1(ruta, columnas_requeridas, sep=";", encoding="latin-1"):
    """Adaptador compatible con F1 que usa :class:`LectorCSV`."""
    contrato = ContratoEsquema(tuple(columnas_requeridas))
    return LectorCSV(contrato, sep=sep, encoding=encoding).leer(ruta)


def exportar_datos_procesados(df, ruta_salida, sep=";", encoding="latin-1"):
    """Exporta el DataFrame procesado a CSV y calcula su huella SHA-256."""
    ruta = Path(ruta_salida)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, sep=sep, encoding=encoding, index=False)
    huella = sha256_archivo(ruta)
    tamanio_mb = ruta.stat().st_size / (1024 * 1024)
    return {
        "archivo": ruta.name,
        "ruta": str(ruta),
        "filas": len(df),
        "columnas": len(df.columns),
        "tamanio_mb": round(tamanio_mb, 2),
        "sha256": huella
    }
