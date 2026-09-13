"""Módulo de utilidades del proyecto: entorno, trazabilidad y pipeline de datos F1/F2."""
from importlib.metadata import version
from pathlib import Path
import hashlib
import numpy as np
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


def resumen_exploracion(df):
    """Calcula métricas estructurales para el análisis exploratorio (F2)."""
    if df.empty:
        raise ValueError("El DataFrame a explorar no contiene registros.")
    
    n_filas, n_cols = df.shape
    conteo_nulos = df.isna().sum()
    cols_100_nulos = [c for c in df.columns if conteo_nulos[c] == n_filas]
    cols_con_nulos = [c for c in df.columns if 0 < conteo_nulos[c] < n_filas]
    cols_completas = [c for c in df.columns if conteo_nulos[c] == 0]
    cols_constantes = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
    
    tipos = df.dtypes.value_counts().to_dict()
    tipos_str = {str(k): int(v) for k, v in tipos.items()}
    
    return {
        "total_filas": n_filas,
        "total_columnas": n_cols,
        "columnas_completas": len(cols_completas),
        "columnas_con_nulos": len(cols_con_nulos),
        "columnas_100_nulos": cols_100_nulos,
        "columnas_constantes": cols_constantes,
        "distribucion_tipos": tipos_str,
    }


def limpiar_datos_f2(df, excluir_vacias=True, normalizar_texto=True):
    """
    Ejecuta el pipeline de preprocesamiento y transformación de datos para F2.
    
    Operaciones:
    1. Exclusión justificada de columnas 100% vacías.
    2. Corrección de fechas centinela (año 1900) a NaT.
    3. Conversión de fechas textuales a tipo datetime.
    4. Normalización de cadenas de texto (strip de espacios).
    5. Preservación explícita de TamanoProveedor ('NoClasificado').
    6. Generación de variables analíticas derivadas:
       - oferta_ganadora (bool)
       - licitacion_adjudicada (bool)
       - plazo_cierre_dias (float)
    """
    if df.empty:
        raise ValueError("No es posible preprocesar un DataFrame vacío.")
    
    columnas_clave = ["NroLicitacion", "TipoLicitacion", "TamanoProveedor",
                      "ResultadoOferta", "EstadoLicitacion"]
    faltantes = [c for c in columnas_clave if c not in df.columns]
    if faltantes:
        raise KeyError(f"Faltan columnas clave para el preprocesamiento: {faltantes}")
    
    df_limpio = df.copy()
    
    # 1. Exclusión de columnas 100% vacías
    cols_vacias = ["LicitacionBaseTipo", "ContratoRenovable", "UnidadTiempoRenovacion"]
    if excluir_vacias:
        df_limpio = df_limpio.drop(columns=[c for c in cols_vacias if c in df_limpio.columns])
    
    # 2. Corrección de fechas centinela en FechaEstimadaEvaluacionOfertas
    if "FechaEstimadaEvaluacionOfertas" in df_limpio.columns:
        mascara_1900 = df_limpio["FechaEstimadaEvaluacionOfertas"].astype(str).str.startswith("1900")
        df_limpio.loc[mascara_1900, "FechaEstimadaEvaluacionOfertas"] = np.nan
    
    # 3. Conversión de columnas temporales a datetime
    columnas_fecha = [
        "FechaPublicacion", "FechaInicioPreguntas", "FechaFinalPreguntas",
        "FechaPublicacionRespuestas", "FechaActoAperturaTecnica",
        "FechaActoAperturaEconomica", "FechaCierre", "FechaAdjudicacion",
        "FechaActaAprobacion"
    ]
    for col in columnas_fecha:
        if col in df_limpio.columns:
            df_limpio[col] = pd.to_datetime(df_limpio[col], errors="coerce")
    
    # 4. Normalización de texto en variables categóricas
    if normalizar_texto:
        columnas_cat = ["TipoLicitacion", "TamanoProveedor", "ResultadoOferta",
                        "EstadoLicitacion", "EstadoOferta", "Sector", "MonedaOferta"]
        for col in columnas_cat:
            if col in df_limpio.columns and df_limpio[col].dtype == object:
                df_limpio[col] = df_limpio[col].astype(str).str.strip()
    
    # 5. Generación de variables derivadas
    df_limpio["oferta_ganadora"] = df_limpio["ResultadoOferta"] == "Ganadora"
    df_limpio["licitacion_adjudicada"] = df_limpio["EstadoLicitacion"] == "Adjudicada"
    
    if "FechaPublicacion" in df_limpio.columns and "FechaCierre" in df_limpio.columns:
        plazo_seg = (df_limpio["FechaCierre"] - df_limpio["FechaPublicacion"]).dt.total_seconds()
        df_limpio["plazo_cierre_dias"] = plazo_seg / 86400.0
    
    return df_limpio


def validar_dataset_procesado(df):
    """
    Comprueba integralmente la consistencia del dataset procesado (F2).
    Lanza AssertionError si alguna regla de calidad no se cumple.
    """
    if df.empty:
        raise AssertionError("Validación fallida: el DataFrame procesado está vacío.")
    
    # 1. No deben existir las columnas 100% vacías descartadas
    cols_descartadas = {"LicitacionBaseTipo", "ContratoRenovable", "UnidadTiempoRenovacion"}
    presentes = cols_descartadas.intersection(set(df.columns))
    assert not presentes, f"Validación fallida: columnas vacías aún presentes: {presentes}"
    
    # 2. Integridad de filas
    assert len(df) > 0, "Validación fallida: no contiene filas."
    
    # 3. Variables obligatorias sin nulos
    cols_sin_nulos = ["TipoLicitacion", "TamanoProveedor", "ResultadoOferta", "EstadoLicitacion"]
    for col in cols_sin_nulos:
        assert col in df.columns, f"Validación fallida: falta columna obligatoria '{col}'."
        nulos = df[col].isna().sum()
        assert nulos == 0, f"Validación fallida: '{col}' contiene {nulos} valores nulos."
    
    # 4. Valores válidos en ResultadoOferta
    valores_res = set(df["ResultadoOferta"].unique())
    assert valores_res.issubset({"Ganadora", "Perdedora"}), f"Valores inesperados en ResultadoOferta: {valores_res}"
    
    # 5. Fechas sin valores centinela 1900
    if "FechaEstimadaEvaluacionOfertas" in df.columns:
        n_1900 = df["FechaEstimadaEvaluacionOfertas"].astype(str).str.startswith("1900").sum()
        assert n_1900 == 0, f"Validación fallida: aún quedan {n_1900} fechas de 1900."
    
    # 6. Columnas derivadas generadas correctamente
    assert "oferta_ganadora" in df.columns, "Falta columna derivada 'oferta_ganadora'."
    assert "licitacion_adjudicada" in df.columns, "Falta columna derivada 'licitacion_adjudicada'."
    
    return {
        "filas_validadas": len(df),
        "columnas_validadas": len(df.columns),
        "reglas_superadas": 6,
        "estado": "OK"
    }


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
