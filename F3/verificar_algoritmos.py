"""Ejecuta y guarda el notebook del aporte algorítmico en un kernel nuevo."""
from pathlib import Path
import json
import sys

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.ejecucion import ejecutar_notebook


if __name__ == "__main__":
    registro = ejecutar_notebook(
        RAIZ, "F3/F3_Algoritmos.ipynb", "evidencias/F3_algoritmos_ejecucion.json",
        "Aporte de algoritmos: POO existente, oráculo manual, recursividad, 14 pruebas y mediciones con hashes verificados.",
    )
    print(json.dumps(registro, ensure_ascii=False, indent=2))
