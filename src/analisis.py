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


def _preparar_conteo(df, grupo, estado):
    """Filtra sin mutar y codifica resultados: 0 ganadora, 1 perdedora, 2 otros."""
    datos = df.loc[df["EstadoLicitacion"].eq(estado)]
    if datos[grupo].isna().any():
        raise ValueError(f"{grupo}: resolver faltantes antes de agrupar.")
    categorias = pd.Index(sorted(datos[grupo].unique()), name=grupo)
    if "All" in categorias:
        raise ValueError("La categoría All está reservada para el total.")
    ganadoras = datos["ResultadoOferta"].eq("Ganadora").fillna(False)
    perdedoras = datos["ResultadoOferta"].eq("Perdedora").fillna(False)
    codigos = np.where(ganadoras, 0, np.where(perdedoras, 1, 2))
    return datos[grupo].to_numpy(), codigos, categorias


def _contar_rango(grupos, codigos, inicio, fin):
    """Cuenta un rango sin crear sublistas ni sub-DataFrames."""
    conteos = {}
    for i in range(inicio, fin):
        acumulado = conteos.setdefault(grupos[i], [0, 0, 0])
        acumulado[codigos[i]] += 1
    return conteos


def _tabla_desde_conteos(conteos, categorias):
    """Combina conteos antes de calcular porcentajes; nunca promedia porcentajes."""
    columnas = ["Ganadora", "Perdedora", "Sin resultado válido"]
    tabla = pd.DataFrame(
        [conteos[c] for c in categorias], index=categorias,
        columns=columnas, dtype="int64",
    )
    tabla["All"] = tabla["Ganadora"] + tabla["Perdedora"]
    tabla.loc["All"] = tabla.sum()
    denominador = tabla["All"].replace(0, np.nan)
    for valor in ("Ganadora", "Perdedora"):
        tabla[f"% {valor}"] = (tabla[valor] / denominador * 100).round(2)
    return tabla


def tabla_proporciones_iterativa(df, grupo, estado="Adjudicada"):
    """Acumula conteos por grupo en un recorrido y devuelve el formato de F2."""
    grupos, codigos, categorias = _preparar_conteo(df, grupo, estado)
    conteos = _contar_rango(grupos, codigos, 0, len(grupos))
    return _tabla_desde_conteos(conteos, categorias)


def _contar_dividiendo(grupos, codigos, inicio, fin, bloque_base):
    """Divide rangos, cuenta hojas y combina diccionarios en profundidad."""
    if fin - inicio <= bloque_base:
        return _contar_rango(grupos, codigos, inicio, fin)
    medio = (inicio + fin) // 2
    izquierda = _contar_dividiendo(grupos, codigos, inicio, medio, bloque_base)
    derecha = _contar_dividiendo(grupos, codigos, medio, fin, bloque_base)
    for grupo, valores in derecha.items():
        acumulado = izquierda.setdefault(grupo, [0, 0, 0])
        for i in range(3):
            acumulado[i] += valores[i]
    return izquierda


def tabla_proporciones_recursiva(df, grupo, estado="Adjudicada", bloque_base=256):
    """Divide y combina conteos; la profundidad crece logarítmicamente.

    bloque_base fija cuándo pasar a conteo iterativo. Debe ser entero positivo.
    La preparación y el formato de salida son los mismos de la versión iterativa.
    """
    if isinstance(bloque_base, bool) or not isinstance(bloque_base, (int, np.integer)) or bloque_base < 1:
        raise ValueError("bloque_base debe ser un entero positivo.")
    grupos, codigos, categorias = _preparar_conteo(df, grupo, estado)
    conteos = _contar_dividiendo(grupos, codigos, 0, len(grupos), bloque_base)
    return _tabla_desde_conteos(conteos, categorias)


def tabla_proporciones_agrupada(df, grupo, estado="Adjudicada"):
    """Obtiene los tres conteos mediante una única agrupación de pandas."""
    grupos, codigos, categorias = _preparar_conteo(df, grupo, estado)
    pares = pd.DataFrame({"grupo": grupos, "resultado": codigos})
    matriz = (
        pares.groupby(["grupo", "resultado"], observed=True, sort=False)
        .size().unstack(fill_value=0)
        .reindex(index=categorias, columns=[0, 1, 2], fill_value=0)
    )
    conteos = dict(zip(categorias, matriz.to_numpy().tolist()))
    return _tabla_desde_conteos(conteos, categorias)
