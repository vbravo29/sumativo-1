"""Pruebas del aporte algorítmico: oráculo manual, equivalencia y recursividad."""
from pathlib import Path
import sys
import unittest
from functools import partial

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.analisis import (
    tabla_proporciones, tabla_proporciones_iterativa,
    tabla_proporciones_recursiva, tabla_proporciones_agrupada,
)
from src.datos import ContratoEsquema, LectorCSV
from src.pipeline import LimpiadorLicitaciones

ALTERNATIVAS = (
    tabla_proporciones_iterativa,
    partial(tabla_proporciones_recursiva, bloque_base=1),
    partial(tabla_proporciones_recursiva, bloque_base=3),
    partial(tabla_proporciones_recursiva, bloque_base=256),
    tabla_proporciones_agrupada,
)


def muestra():
    return pd.DataFrame({
        "Grupo": ["A", "A", "A", "B", "C", "D", "E"],
        "EstadoLicitacion": ["Adjudicada"] * 6 + ["Revocada"],
        "ResultadoOferta": ["Ganadora", "Ganadora", "Perdedora", None,
                            "Perdedora", "Ganadora", "Ganadora"],
    })


class PruebasAlgoritmos(unittest.TestCase):
    def comprobar(self, entrada, grupo="Grupo", estado="Adjudicada"):
        original = entrada.copy(deep=True)
        referencia = tabla_proporciones(entrada, grupo, estado)
        for funcion in ALTERNATIVAS:
            with self.subTest(funcion=str(funcion), filas=len(entrada), estado=estado):
                resultado = funcion(entrada, grupo, estado)
                pd.testing.assert_frame_equal(resultado, referencia)
                pd.testing.assert_frame_equal(entrada, original)
                for col in ("Ganadora", "Perdedora", "Sin resultado válido", "All"):
                    self.assertEqual(resultado.loc["All", col], resultado.drop(index="All")[col].sum())
        return referencia

    def test_oraculo_manual_y_totales(self):
        tabla = self.comprobar(muestra())
        self.assertEqual(tabla.loc["A", "All"], 3)
        self.assertEqual(tabla.loc["A", "% Ganadora"], 66.67)
        self.assertEqual(tabla.loc["All", "All"], 5)
        self.assertEqual(tabla.loc["All", "% Ganadora"], 60)
        self.assertEqual(tabla.loc["B", "Sin resultado válido"], 1)
        self.assertTrue(pd.isna(tabla.loc["B", "% Ganadora"]))
        self.assertEqual(tabla.loc["C", "% Ganadora"], 0)
        self.assertEqual(tabla.loc["D", "% Ganadora"], 100)
        self.assertNotIn("E", tabla.index)

    def test_vacio_filtro_sin_filas_y_otro_estado(self):
        self.comprobar(muestra().iloc[:0])
        self.comprobar(muestra(), estado="Desierta")
        self.comprobar(muestra(), estado="Revocada")

    def test_faltantes_resultados_e_indices_duplicados(self):
        datos = muestra()
        datos["ResultadoOferta"] = pd.Series([pd.NA, "Otro", None, np.nan, "Ganadora", "Perdedora", "Ganadora"], dtype="string")
        datos.index = [1] * len(datos)
        self.comprobar(datos)

    def test_grupo_faltante_y_categoria_reservada(self):
        for valor in (None, "All"):
            datos = muestra()
            datos.loc[0, "Grupo"] = valor
            for funcion in (tabla_proporciones, *ALTERNATIVAS):
                with self.subTest(valor=valor, funcion=str(funcion)):
                    with self.assertRaises(ValueError):
                        funcion(datos, "Grupo")
        # Un faltante fuera del estado seleccionado no invalida los grupos usados.
        datos = muestra()
        datos.loc[6, "Grupo"] = None
        self.comprobar(datos)

    def test_columnas_ausentes(self):
        for col in ("Grupo", "ResultadoOferta", "EstadoLicitacion"):
            for funcion in ALTERNATIVAS:
                with self.assertRaises(KeyError):
                    funcion(muestra().drop(columns=col), "Grupo")
            # F2 usa acceso por atributo en ResultadoOferta; conservar esa interfaz.
            error = AttributeError if col == "ResultadoOferta" else KeyError
            with self.assertRaises(error):
                tabla_proporciones(muestra().drop(columns=col), "Grupo")

    def test_bloques_invalidos(self):
        for bloque in (0, -1, 1.5, True, "2", None):
            with self.subTest(bloque=bloque), self.assertRaises(ValueError):
                tabla_proporciones_recursiva(muestra(), "Grupo", bloque_base=bloque)

    def test_particiones_aleatorias_reproducibles(self):
        rng = np.random.default_rng(2026)
        for n in (1, 2, 17, 257, 1025):
            datos = pd.DataFrame({
                "Grupo": rng.choice(["A", "B", "C"], n),
                "EstadoLicitacion": rng.choice(["Adjudicada", "Desierta"], n),
                "ResultadoOferta": rng.choice(["Ganadora", "Perdedora", "Otro", None], n),
            })
            self.comprobar(datos)

    def test_dataset_real_ambas_agrupaciones(self):
        ruta = RAIZ / "data/raw/licitaciones_salud_marzo_2026.csv"
        datos = LectorCSV(ContratoEsquema(("TamanoProveedor", "TipoLicitacion"))).leer(ruta)
        limpio = LimpiadorLicitaciones().limpiar(datos)
        for grupo in ("TamanoProveedor", "TipoLicitacion"):
            self.comprobar(limpio, grupo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
