"""Transformaciones reutilizables del dataset."""
import pandas as pd


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
