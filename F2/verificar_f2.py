"""Punto de entrada para verificar F2 desde el entorno virtual del proyecto."""
from pathlib import Path
import sys
import json

raiz = Path(__file__).resolve().parents[1]
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))
from src.ejecucion import ejecutar_notebook


def main():
    registro = ejecutar_notebook(raiz, "F2/F2_Preprocesamiento.ipynb",
        "evidencias/F2_ejecucion.json", "F2: exploración, limpieza modular, proporciones, codificación one-hot, validación y exportación")
    print(json.dumps(registro, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
