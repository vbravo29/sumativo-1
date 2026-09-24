"""Diagnóstico, frecuencias y proporciones."""
import numpy as np
import pandas as pd


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
