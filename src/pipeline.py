"""Coordinación de limpieza y estado de la última ejecución."""
from .preprocesamiento import (
    excluir_columnas_vacias,
    normalizar_categorias,
    convertir_fechas,
    generar_variables_derivadas,
)


class LimpiadorLicitaciones:
    """Coordina el pipeline F2 y conserva el estado de su última ejecución.

    El DataFrame de entrada nunca se modifica. El estado expuesto es una copia para
    impedir que código externo altere accidentalmente la trazabilidad del objeto.
    """

    COLUMNAS_CLAVE = (
        "NroLicitacion", "TipoLicitacion", "TamanoProveedor",
        "ResultadoOferta", "EstadoLicitacion",
    )
    COLUMNAS_VACIAS = (
        "LicitacionBaseTipo", "ContratoRenovable", "UnidadTiempoRenovacion",
    )
    COLUMNAS_FECHA = (
        "FechaPublicacion", "FechaInicioPreguntas", "FechaFinalPreguntas",
        "FechaPublicacionRespuestas", "FechaActoAperturaTecnica",
        "FechaActoAperturaEconomica", "FechaCierre", "FechaAdjudicacion",
        "FechaActaAprobacion", "FechaEstimadaEvaluacionOfertas",
    )
    COLUMNAS_TEXTO = (
        "TipoLicitacion", "TamanoProveedor", "ResultadoOferta",
        "EstadoLicitacion", "EstadoOferta", "Sector", "MonedaOferta",
    )

    def __init__(self, excluir_vacias=True, normalizar_texto=True):
        self._excluir_vacias = bool(excluir_vacias)
        self._normalizar_texto = bool(normalizar_texto)
        self._ultima_ejecucion = None

    @property
    def ultima_ejecucion(self):
        """Resumen defensivo de la ejecución más reciente, o ``None``."""
        return None if self._ultima_ejecucion is None else self._ultima_ejecucion.copy()

    def limpiar(self, df):
        """Aplica las transformaciones de F2 en un orden explícito y trazable."""
        if df.empty:
            raise ValueError("No es posible preprocesar un DataFrame vacío.")
        faltantes = [c for c in self.COLUMNAS_CLAVE if c not in df.columns]
        if faltantes:
            raise KeyError(
                f"Faltan columnas clave para el preprocesamiento: {faltantes}"
            )

        salida = df.copy()
        columnas_excluidas = []
        if self._excluir_vacias:
            columnas_excluidas = [
                c for c in self.COLUMNAS_VACIAS
                if c in salida and salida[c].isna().all()
            ]
            salida = excluir_columnas_vacias(salida, self.COLUMNAS_VACIAS)
        salida = convertir_fechas(
            salida,
            self.COLUMNAS_FECHA,
            anios_excluidos={"FechaEstimadaEvaluacionOfertas": [1900]},
        )
        if self._normalizar_texto:
            salida = normalizar_categorias(salida, self.COLUMNAS_TEXTO)
        salida = generar_variables_derivadas(salida)
        self._ultima_ejecucion = {
            "filas_entrada": len(df),
            "filas_salida": len(salida),
            "columnas_entrada": len(df.columns),
            "columnas_salida": len(salida.columns),
            "columnas_excluidas": tuple(columnas_excluidas),
        }
        return salida


def limpiar_datos_f2(df, excluir_vacias=True, normalizar_texto=True):
    """
    Ejecuta el pipeline de preprocesamiento y transformación de datos para F2.
    
    Operaciones:
    1. Exclusión justificada de columnas 100% vacías.
    2. Corrección de fechas anómalas (año 1900) a NaT.
    3. Conversión de fechas textuales a tipo datetime.
    4. Normalización de cadenas de texto (strip de espacios).
    5. Preservación explícita de TamanoProveedor ('NoClasificado').
    6. Generación de variables analíticas derivadas:
       - oferta_ganadora (bool)
       - licitacion_adjudicada (bool)
       - plazo_cierre_dias (float)
    """
    return LimpiadorLicitaciones(
        excluir_vacias=excluir_vacias,
        normalizar_texto=normalizar_texto,
    ).limpiar(df)
