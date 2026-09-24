"""Acceso compatible a las funciones F1/F2 y las clases del núcleo POO de F3.

Las implementaciones se distribuyen por responsabilidad sin duplicar código.
"""
from .entorno import (
    versiones_entorno,
)
from .datos import (
    sha256_archivo,
    ContratoEsquema,
    LectorDatos,
    LectorCSV,
    leer_datos_f1,
    exportar_datos_procesados,
)
from .preprocesamiento import (
    excluir_columnas_vacias,
    normalizar_categorias,
    convertir_fechas,
    generar_variables_derivadas,
    codificar_nominales,
)
from .analisis import (
    resumen_exploracion,
    tablas_frecuencia,
    tabla_proporciones,
)
from .pipeline import (
    LimpiadorLicitaciones,
    limpiar_datos_f2,
)
from .validacion import (
    ReglaValidacion,
    ReglaColumnasVacias,
    ReglaIntegridadFilas,
    ReglaColumnasObligatorias,
    ReglaResultadoOferta,
    ReglaFechas,
    ReglaVariablesDerivadas,
    ValidadorDatasetProcesado,
    validar_dataset_procesado,
    validar_codificacion,
)

__all__ = [
    "versiones_entorno",
    "sha256_archivo",
    "ContratoEsquema",
    "LectorDatos",
    "LectorCSV",
    "leer_datos_f1",
    "resumen_exploracion",
    "excluir_columnas_vacias",
    "normalizar_categorias",
    "convertir_fechas",
    "generar_variables_derivadas",
    "LimpiadorLicitaciones",
    "tablas_frecuencia",
    "tabla_proporciones",
    "limpiar_datos_f2",
    "ReglaValidacion",
    "ReglaColumnasVacias",
    "ReglaIntegridadFilas",
    "ReglaColumnasObligatorias",
    "ReglaResultadoOferta",
    "ReglaFechas",
    "ReglaVariablesDerivadas",
    "ValidadorDatasetProcesado",
    "validar_dataset_procesado",
    "codificar_nominales",
    "exportar_datos_procesados",
    "validar_codificacion",
]
