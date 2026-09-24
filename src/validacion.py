"""Reglas polimórficas y comprobación de codificación."""
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd


class ReglaValidacion(ABC):
    """Interfaz para reglas intercambiables del validador de calidad."""

    @property
    @abstractmethod
    def nombre(self):
        """Identificador legible de la regla."""

    @abstractmethod
    def validar(self, df, filas_esperadas):
        """Lanza ``AssertionError`` cuando el DataFrame incumple la regla."""


class ReglaColumnasVacias(ReglaValidacion):
    nombre = "columnas_vacias_descartadas"

    def validar(self, df, filas_esperadas):
        descartadas = {
            "LicitacionBaseTipo", "ContratoRenovable", "UnidadTiempoRenovacion"
        }
        presentes = {
            c for c in descartadas.intersection(df.columns) if df[c].isna().all()
        }
        assert not presentes, (
            f"Validación fallida: columnas vacías aún presentes: {presentes}"
        )


class ReglaIntegridadFilas(ReglaValidacion):
    nombre = "integridad_filas"

    def validar(self, df, filas_esperadas):
        assert len(df) == filas_esperadas, (
            "Validación fallida: cambió el número de filas."
        )


class ReglaColumnasObligatorias(ReglaValidacion):
    nombre = "columnas_obligatorias"
    columnas = (
        "NroLicitacion", "TipoLicitacion", "TamanoProveedor",
        "ResultadoOferta", "EstadoLicitacion",
    )

    def validar(self, df, filas_esperadas):
        for col in self.columnas:
            assert col in df.columns, (
                f"Validación fallida: falta columna obligatoria '{col}'."
            )
            nulos = df[col].isna().sum()
            assert nulos == 0, (
                f"Validación fallida: '{col}' contiene {nulos} valores nulos."
            )
            assert df[col].astype("string").str.strip().ne("").all(), (
                f"{col}: etiqueta vacía."
            )


class ReglaResultadoOferta(ReglaValidacion):
    nombre = "resultado_oferta"

    def validar(self, df, filas_esperadas):
        valores = set(df["ResultadoOferta"].unique())
        assert valores.issubset({"Ganadora", "Perdedora"}), (
            f"Valores inesperados en ResultadoOferta: {valores}"
        )


class ReglaFechas(ReglaValidacion):
    nombre = "fechas"

    def validar(self, df, filas_esperadas):
        if "FechaEstimadaEvaluacionOfertas" in df.columns:
            n_1900 = (
                df["FechaEstimadaEvaluacionOfertas"]
                .astype(str)
                .str.startswith("1900")
                .sum()
            )
            assert n_1900 == 0, (
                f"Validación fallida: aún quedan {n_1900} fechas de 1900."
            )
        for col in ("FechaPublicacion", "FechaCierre"):
            assert col in df and pd.api.types.is_datetime64_any_dtype(df[col]), (
                f"{col}: fecha requerida."
            )
            assert df[col].notna().all(), (
                f"{col}: fechas faltantes; revisar antes de calcular plazos."
            )


class ReglaVariablesDerivadas(ReglaValidacion):
    nombre = "variables_derivadas"

    def validar(self, df, filas_esperadas):
        assert "oferta_ganadora" in df.columns, (
            "Falta columna derivada 'oferta_ganadora'."
        )
        assert "licitacion_adjudicada" in df.columns, (
            "Falta columna derivada 'licitacion_adjudicada'."
        )
        relaciones = (
            ("oferta_ganadora", "ResultadoOferta", "Ganadora"),
            ("licitacion_adjudicada", "EstadoLicitacion", "Adjudicada"),
        )
        for derivada, fuente, valor in relaciones:
            assert pd.api.types.is_bool_dtype(df[derivada]), (
                f"{derivada}: tipo no booleano."
            )
            assert (
                df[derivada].notna().all()
                and df[derivada].eq(df[fuente].eq(valor)).all()
            ), f"{derivada}: valores incoherentes."
        assert "plazo_cierre_dias" in df.columns, "Falta plazo_cierre_dias."
        esperado = (
            df["FechaCierre"] - df["FechaPublicacion"]
        ).dt.total_seconds() / 86400
        assert pd.api.types.is_numeric_dtype(df["plazo_cierre_dias"]), (
            "Plazo no numérico."
        )
        assert np.allclose(
            df["plazo_cierre_dias"], esperado, rtol=0, atol=1e-9
        ), "Plazo incoherente con fechas."
        assert esperado.ge(0).all(), (
            "Plazo negativo: revisar registros sin eliminarlos automáticamente."
        )


class ValidadorDatasetProcesado:
    """Ejecuta reglas polimórficas y registra cuáles fueron superadas."""

    def __init__(self, reglas=None):
        reglas_predeterminadas = (
            ReglaColumnasVacias(),
            ReglaIntegridadFilas(),
            ReglaColumnasObligatorias(),
            ReglaResultadoOferta(),
            ReglaFechas(),
            ReglaVariablesDerivadas(),
        )
        self._reglas = tuple(reglas or reglas_predeterminadas)
        if not self._reglas:
            raise ValueError("El validador requiere al menos una regla.")
        if not all(isinstance(regla, ReglaValidacion) for regla in self._reglas):
            raise TypeError("Todas las reglas deben heredar de ReglaValidacion.")

    @property
    def reglas(self):
        return self._reglas

    def validar(self, df, filas_esperadas):
        if df.empty:
            raise AssertionError(
                "Validación fallida: el DataFrame procesado está vacío."
            )
        superadas = []
        for regla in self._reglas:
            regla.validar(df, filas_esperadas)
            superadas.append(regla.nombre)
        return {
            "filas_validadas": len(df),
            "columnas_validadas": len(df.columns),
            "reglas_superadas": len(superadas),
            "detalle_reglas": tuple(superadas),
            "estado": "OK",
        }


def validar_dataset_procesado(df, filas_esperadas):
    """Adaptador compatible con F2 que ejecuta el validador orientado a objetos."""
    return ValidadorDatasetProcesado().validar(df, filas_esperadas)


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
