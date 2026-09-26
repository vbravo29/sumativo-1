"""Compara cálculo de proporciones sobre datos cargados; no mide lectura del CSV."""
import argparse
from datetime import datetime, timezone
from functools import partial
import gc
import json
from pathlib import Path
import platform
import random
import sys
import timeit
import tracemalloc

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.analisis import (
    tabla_proporciones, tabla_proporciones_iterativa,
    tabla_proporciones_recursiva, tabla_proporciones_agrupada,
)
from src.datos import ContratoEsquema, LectorCSV, sha256_archivo
from src.pipeline import LimpiadorLicitaciones
from src.validacion import ValidadorDatasetProcesado


def medir_tiempos(llamadas, repeticiones, numero, azar):
    """Reutiliza un Timer por algoritmo y alterna el orden de cada ronda."""
    temporizadores = {nombre: timeit.Timer(llamada) for nombre, llamada in llamadas.items()}
    tiempos = {nombre: [] for nombre in llamadas}
    orden = list(llamadas)
    for _ in range(repeticiones):
        azar.shuffle(orden)
        for nombre in orden:
            tiempos[nombre].append(temporizadores[nombre].timeit(number=numero) / numero)
    return tiempos


def medir_memoria(llamada, repeticiones=3):
    """Mide picos en ejecuciones independientes de las mediciones de tiempo."""
    picos = []
    for _ in range(repeticiones):
        gc.collect()
        tracemalloc.start()
        try:
            resultado = llamada()
            picos.append(tracemalloc.get_traced_memory()[1])
        finally:
            tracemalloc.stop()
        del resultado
    return picos


def resumir_medicion(nombre, tiempos, picos):
    """Calcula los cuartiles una sola vez y conserva todas las observaciones."""
    valores = np.asarray(tiempos) * 1000
    q25, mediana, q75 = np.percentile(valores, [25, 50, 75])
    return {
        "algoritmo": nombre, "min_ms": float(valores.min()),
        "mediana_ms": float(mediana), "q25_ms": float(q25), "q75_ms": float(q75),
        "pico_trazado_bytes_mediana": float(np.median(picos)),
        "tiempos_ms": valores.tolist(), "picos_trazados_bytes": picos,
    }


def medir_caso(entrada, grupo, funciones, repeticiones, numero, azar):
    """Verifica y mide los algoritmos para una muestra y una variable."""
    referencia = tabla_proporciones(entrada, grupo)
    llamadas = {nombre: partial(fn, entrada, grupo) for nombre, fn in funciones.items()}
    for llamada in llamadas.values():
        pd.testing.assert_frame_equal(llamada(), referencia)  # Verificación y calentamiento.
    tiempos = medir_tiempos(llamadas, repeticiones, numero, azar)
    filas = []
    for nombre, llamada in llamadas.items():
        filas.append({
            "grupo": grupo, "grupos_observados": len(referencia) - 1,
            **resumir_medicion(nombre, tiempos[nombre], medir_memoria(llamada)),
        })
    return filas


def medir(datos, tamanos=(100, 1000, 10000), repeticiones=7, numero=3, semilla=2026, bloque_base=256):
    """Incluye filtro, preparación, conteo y tabla; alterna el orden entre rondas.

    El pico de tracemalloc excluye la entrada ya cargada y no representa RSS.
    Los tiempos se miden sin tracemalloc, con GC desactivado por timeit.
    """
    if repeticiones < 1 or numero < 1 or datos.empty:
        raise ValueError("Se requieren datos y cantidades de ejecución positivas.")
    tamanos = sorted(set([min(int(n), len(datos)) for n in tamanos] + [len(datos)]))
    if tamanos[0] < 1:
        raise ValueError("Los tamaños deben ser positivos.")
    funciones = {
        "referencia_f2": tabla_proporciones,
        "iterativa": tabla_proporciones_iterativa,
        "recursiva": partial(tabla_proporciones_recursiva, bloque_base=bloque_base),
        "agrupada": tabla_proporciones_agrupada,
    }
    permutacion = np.random.default_rng(semilla).permutation(len(datos))
    azar = random.Random(semilla)
    filas = []
    for n in tamanos:
        entrada = datos.iloc[permutacion[:n]].copy()
        contexto = {
            "filas_entrada": n,
            "filas_adjudicadas": int(entrada.EstadoLicitacion.eq("Adjudicada").sum()),
        }
        for grupo in ("TamanoProveedor", "TipoLicitacion"):
            resultados = medir_caso(entrada, grupo, funciones, repeticiones, numero, azar)
            filas.extend({**contexto, **resultado} for resultado in resultados)
    return filas


def ejecutar(salida=None, repeticiones=7, numero=3):
    """Carga mediante las interfaces POO existentes y guarda CSV y metadatos JSON."""
    salida = Path(salida) if salida else RAIZ / "evidencias/F3_algoritmos"
    # Comprobar el destino antes de invertir tiempo en el experimento.
    salida.mkdir(parents=True, exist_ok=True)
    ruta = RAIZ / "data/raw/licitaciones_salud_marzo_2026.csv"
    raw = LectorCSV(ContratoEsquema(("TamanoProveedor", "TipoLicitacion"))).leer(ruta)
    datos = LimpiadorLicitaciones().limpiar(raw)
    ValidadorDatasetProcesado().validar(datos, len(raw))
    filas = medir(datos, repeticiones=repeticiones, numero=numero)
    registro = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "sistema": platform.platform(),
        "procesador": platform.processor(), "pandas": pd.__version__, "numpy": np.__version__,
        "raw_sha256": sha256_archivo(ruta),
        "analisis_sha256": sha256_archivo(RAIZ / "src/analisis.py"),
        "medicion_sha256": sha256_archivo(Path(__file__)),
        "semilla": 2026, "bloque_base": 256,
        "repeticiones": repeticiones, "ejecuciones_por_repeticion": numero,
        "repeticiones_memoria": 3,
        "alcance": "Cálculo completo sobre DataFrame cargado: filtro, conversión, conteos y salida. Excluye lectura, limpieza, muestreo y validación de equivalencia.",
        "memoria": "Pico de asignaciones rastreadas con tracemalloc; entrada preexistente excluida; no es RSS ni garantiza cubrir toda la memoria nativa.",
        "tiempo": "timeit sin tracemalloc; GC desactivado durante cada ronda; orden alternado con semilla. Mínimo como referencia de menor interferencia, mediana y cuartiles describen la sesión.",
        "mediciones": filas,
    }
    (salida / "mediciones.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tabla = pd.DataFrame(filas).drop(columns=["tiempos_ms", "picos_trazados_bytes"])
    tabla.to_csv(salida / "resumen.csv", index=False)
    return tabla


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path)
    parser.add_argument("--repeticiones", type=int, default=7)
    parser.add_argument("--numero", type=int, default=3)
    args = parser.parse_args()
    print(ejecutar(args.salida, args.repeticiones, args.numero).to_string(index=False))
