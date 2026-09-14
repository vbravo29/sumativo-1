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


def excluir_columnas_vacias(df, columnas):
    """Devuelve una copia sin las columnas indicadas que estén completamente vacías."""
    return df.drop(columns=[c for c in columnas if c in df and df[c].isna().all()]).copy()


def normalizar_categorias(df, columnas):
    """Recorta espacios en las columnas presentes y conserva los valores faltantes."""
    salida = df.copy()
    for col in columnas:
        if col in salida:
            salida[col] = salida[col].astype("string").str.strip()
    return salida


def convertir_fechas(df, columnas, anios_excluidos=None):
    """Convierte fechas presentes; permite excluir años por columna de forma explícita.

    anios_excluidos es un diccionario columna -> lista de años. Una fecha no
    interpretable detiene la conversión; los NA originales se conservan.
    """
    salida = df.copy()
    for col in columnas:
        if col not in salida:
            continue
        original = salida[col]
        convertida = pd.to_datetime(original, errors="coerce", format="mixed")
        invalidas = original.notna() & convertida.isna()
        if invalidas.any():
            raise ValueError(f"{col}: {int(invalidas.sum())} fechas no interpretables; revisar el origen.")
        excluidos = (anios_excluidos or {}).get(col, [])
        salida[col] = convertida.mask(convertida.dt.year.isin(excluidos)).astype("datetime64[ns]")
    return salida


def generar_variables_derivadas(df):
    """Añade indicadores de resultado/estado y, si hay fechas, el plazo en días."""
    salida = df.copy()
    salida["oferta_ganadora"] = salida["ResultadoOferta"].eq("Ganadora")
    salida["licitacion_adjudicada"] = salida["EstadoLicitacion"].eq("Adjudicada")
    if "FechaPublicacion" in salida and "FechaCierre" in salida:
        salida["plazo_cierre_dias"] = (
            salida["FechaCierre"] - salida["FechaPublicacion"]
        ).dt.total_seconds() / 86400
    return salida


def tablas_frecuencia(df, columnas):
    """Devuelve una tabla de frecuencias por variable, incluyendo los faltantes."""
    return {col: df[col].value_counts(dropna=False).to_frame("Frecuencia") for col in columnas}


def tabla_proporciones(df, grupo, estado="Adjudicada"):
    """Cuenta resultados válidos por grupo en un estado, con denominadores y total.

    Grupos sin resultados válidos conservan total cero y porcentajes no definidos.
    Los resultados desconocidos/faltantes se informan por separado.
    """
    datos = df.loc[df["EstadoLicitacion"].eq(estado)]
    if datos[grupo].isna().any():
        raise ValueError(f"{grupo}: resolver faltantes antes de agrupar.")
    categorias = pd.Index(sorted(datos[grupo].unique()), name=grupo)
    if "All" in categorias:
        raise ValueError("La categoría All está reservada para el total.")
    tabla = pd.DataFrame(index=categorias)
    for valor in ["Ganadora", "Perdedora"]:
        tabla[valor] = datos.loc[datos.ResultadoOferta.eq(valor)].groupby(grupo).size().reindex(categorias, fill_value=0)
    tabla["Sin resultado válido"] = datos.loc[~datos.ResultadoOferta.isin(["Ganadora", "Perdedora"])].groupby(grupo).size().reindex(categorias, fill_value=0)
    tabla["All"] = tabla["Ganadora"] + tabla["Perdedora"]
    tabla.loc["All"] = tabla.sum()
    denominador = tabla["All"].replace(0, np.nan)
    for valor in ["Ganadora", "Perdedora"]:
        tabla[f"% {valor}"] = (tabla[valor] / denominador * 100).round(2)
    return tabla


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
    if df.empty:
        raise ValueError("No es posible preprocesar un DataFrame vacío.")
    
    columnas_clave = ["NroLicitacion", "TipoLicitacion", "TamanoProveedor",
                      "ResultadoOferta", "EstadoLicitacion"]
    faltantes = [c for c in columnas_clave if c not in df.columns]
    if faltantes:
        raise KeyError(f"Faltan columnas clave para el preprocesamiento: {faltantes}")
    
    # Cada etapa puede reutilizarse por separado; aquí se define su orden.
    df_limpio = df.copy()
    if excluir_vacias:
        df_limpio = excluir_columnas_vacias(
            df_limpio, ["LicitacionBaseTipo", "ContratoRenovable", "UnidadTiempoRenovacion"])
    df_limpio = convertir_fechas(df_limpio, [
        "FechaPublicacion", "FechaInicioPreguntas", "FechaFinalPreguntas",
        "FechaPublicacionRespuestas", "FechaActoAperturaTecnica",
        "FechaActoAperturaEconomica", "FechaCierre", "FechaAdjudicacion",
        "FechaActaAprobacion", "FechaEstimadaEvaluacionOfertas"
    ], anios_excluidos={"FechaEstimadaEvaluacionOfertas": [1900]})
    if normalizar_texto:
        df_limpio = normalizar_categorias(df_limpio, [
            "TipoLicitacion", "TamanoProveedor", "ResultadoOferta",
            "EstadoLicitacion", "EstadoOferta", "Sector", "MonedaOferta"])
    return generar_variables_derivadas(df_limpio)


def validar_dataset_procesado(df, filas_esperadas):
    """
    Comprueba integralmente la consistencia del dataset procesado (F2).
    Lanza AssertionError si alguna regla de calidad no se cumple.
    """
    if df.empty:
        raise AssertionError("Validación fallida: el DataFrame procesado está vacío.")
    
    # 1. No deben existir las columnas 100% vacías descartadas
    cols_descartadas = {"LicitacionBaseTipo", "ContratoRenovable", "UnidadTiempoRenovacion"}
    presentes = {c for c in cols_descartadas.intersection(df.columns) if df[c].isna().all()}
    assert not presentes, f"Validación fallida: columnas vacías aún presentes: {presentes}"
    
    # 2. Integridad de filas
    assert len(df) == filas_esperadas, "Validación fallida: cambió el número de filas."
    
    # 3. Variables obligatorias sin nulos
    cols_sin_nulos = ["NroLicitacion", "TipoLicitacion", "TamanoProveedor", "ResultadoOferta", "EstadoLicitacion"]
    for col in cols_sin_nulos:
        assert col in df.columns, f"Validación fallida: falta columna obligatoria '{col}'."
        nulos = df[col].isna().sum()
        assert nulos == 0, f"Validación fallida: '{col}' contiene {nulos} valores nulos."
        assert df[col].astype("string").str.strip().ne("").all(), f"{col}: etiqueta vacía."
    
    # 4. Valores válidos en ResultadoOferta
    valores_res = set(df["ResultadoOferta"].unique())
    assert valores_res.issubset({"Ganadora", "Perdedora"}), f"Valores inesperados en ResultadoOferta: {valores_res}"
    
    # 5. Fechas sin fechas anómalas de 1900
    if "FechaEstimadaEvaluacionOfertas" in df.columns:
        n_1900 = df["FechaEstimadaEvaluacionOfertas"].astype(str).str.startswith("1900").sum()
        assert n_1900 == 0, f"Validación fallida: aún quedan {n_1900} fechas de 1900."
    
    # 6. Columnas derivadas generadas correctamente
    assert "oferta_ganadora" in df.columns, "Falta columna derivada 'oferta_ganadora'."
    assert "licitacion_adjudicada" in df.columns, "Falta columna derivada 'licitacion_adjudicada'."
    for derivada, fuente, valor in [("oferta_ganadora", "ResultadoOferta", "Ganadora"),
                                    ("licitacion_adjudicada", "EstadoLicitacion", "Adjudicada")]:
        assert pd.api.types.is_bool_dtype(df[derivada]), f"{derivada}: tipo no booleano."
        assert df[derivada].notna().all() and df[derivada].eq(df[fuente].eq(valor)).all(), f"{derivada}: valores incoherentes."
    for col in ["FechaPublicacion", "FechaCierre"]:
        assert col in df and pd.api.types.is_datetime64_any_dtype(df[col]), f"{col}: fecha requerida."
        assert df[col].notna().all(), f"{col}: fechas faltantes; revisar antes de calcular plazos."
    assert "plazo_cierre_dias" in df, "Falta plazo_cierre_dias."
    esperado = (df["FechaCierre"] - df["FechaPublicacion"]).dt.total_seconds() / 86400
    assert pd.api.types.is_numeric_dtype(df["plazo_cierre_dias"]), "Plazo no numérico."
    assert np.allclose(df["plazo_cierre_dias"], esperado, rtol=0, atol=1e-9), "Plazo incoherente con fechas."
    assert esperado.ge(0).all(), "Plazo negativo: revisar registros sin eliminarlos automáticamente."
    
    return {
        "filas_validadas": len(df),
        "columnas_validadas": len(df.columns),
        "reglas_superadas": 6,
        "estado": "OK"
    }


def codificar_nominales(df, columnas=("TipoLicitacion", "TamanoProveedor")):
    """Añade indicadores enteros 0/1 sin eliminar ni ordenar las categorías originales.

    Las categorías se obtienen del archivo explorado, no de datos de entrenamiento.
    Si se incorpora un modelo, su codificador deberá ajustarse solo al entrenamiento.
    Los faltantes requieren tratamiento explícito previo, no se codifican como ceros.
    """
    if df.empty:
        raise ValueError("No se puede codificar un dataset vacío.")
    if not columnas or len(set(columnas)) != len(columnas):
        raise ValueError("Indicar columnas distintas para codificar.")
    faltantes = set(columnas) - set(df.columns)
    if faltantes:
        raise KeyError(f"Faltan columnas para codificar: {sorted(faltantes)}")
    if df[list(columnas)].isna().any().any():
        raise ValueError("Resolver los faltantes antes de codificar las categorías.")
    bloques = []
    for col in columnas:
        bloque = pd.get_dummies(df[col], prefix=f"oh_{col}", prefix_sep="__", dtype="int8")
        if set(bloque.columns).intersection(df.columns):
            raise ValueError(f"Ya existen indicadores para {col}.")
        bloques.append(bloque)
    return pd.concat([df.copy(), *bloques], axis=1)


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


def validar_codificacion(original, codificado, columnas):
    """Comprueba filas, categorías originales e indicadores enteros one-hot."""
    indicadores = [c for c in codificado if c not in original.columns]
    pd.testing.assert_frame_equal(codificado[original.columns], original)
    assert codificado.index.equals(original.index)
    for col in columnas:
        bloque = [c for c in indicadores if c.startswith(f"oh_{col}__")]
        assert len(bloque) == original[col].nunique()
        assert codificado[bloque].isin([0, 1]).all().all()
        assert all(pd.api.types.is_integer_dtype(codificado[c]) for c in bloque)
        assert codificado[bloque].sum(axis=1).eq(1).all()
        for categoria in original[col].unique():
            esperado = original[col].eq(categoria).to_numpy(dtype=bool)
            observado = codificado[f"oh_{col}__{categoria}"].to_numpy(dtype=bool)
            assert np.array_equal(observado, esperado)
    esperadas = {f"oh_{col}__{valor}" for col in columnas for valor in original[col].unique()}
    assert set(indicadores) == esperadas, "Esquema de indicadores inesperado."
    return {"estado": "OK", "indicadores": len(indicadores), "filas": len(codificado)}
