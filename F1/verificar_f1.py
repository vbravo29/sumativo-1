"""Punto de entrada para verificar F1 desde el entorno virtual del proyecto."""
from pathlib import Path
import sys
import json

raiz = Path(__file__).resolve().parents[1]
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))
from src.ejecucion import ejecutar_notebook


def main():
    registro = ejecutar_notebook(raiz, "F1/F1_Definición.ipynb",
        "evidencias/F1_ejecucion.json", "F1: entorno, lectura inicial e integridad; cuatro pruebas de entrada")
    print(json.dumps(registro, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
