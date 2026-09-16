"""Ejecuta F2 en un kernel nuevo del intérprete actual y conserva evidencia."""
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import os
import sys
import asyncio

import nbformat
from nbclient import NotebookClient


def ejecutar_notebook(raiz, notebook_relativo, evidencia_relativa, alcance, timeout=300):
    """Ejecuta un notebook en kernel nuevo y guarda evidencia solo si termina bien."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    raiz = Path(raiz)
    ruta = raiz / notebook_relativo
    notebook = nbformat.read(ruta, as_version=4)
    nbformat.validate(notebook)
    with TemporaryDirectory() as temporal:
        datos_jupyter = Path(temporal)
        kernel = datos_jupyter / "kernels" / "proyecto-verificacion"
        kernel.mkdir(parents=True)
        (kernel / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "Verificación del proyecto", "language": "python"
        }), encoding="utf-8")
        anterior = os.environ.get("JUPYTER_PATH")
        os.environ["JUPYTER_PATH"] = str(datos_jupyter) + (os.pathsep + anterior if anterior else "")
        try:
            entorno_kernel = {**os.environ, "IPYTHONDIR": str(datos_jupyter / "ipython")}
            NotebookClient(notebook, timeout=timeout, kernel_name="proyecto-verificacion",
                           resources={"metadata": {"path": str(ruta.parent)}}).execute(env=entorno_kernel)
        finally:
            if anterior is None:
                os.environ.pop("JUPYTER_PATH", None)
            else:
                os.environ["JUPYTER_PATH"] = anterior
    nbformat.validate(notebook)
    nbformat.write(notebook, ruta)
    evidencia = raiz / evidencia_relativa
    evidencia.parent.mkdir(exist_ok=True)
    registro = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "notebook": notebook_relativo,
        "notebook_sha256": hashlib.sha256(ruta.read_bytes()).hexdigest(),
        "kernel_nuevo": True,
        "celdas_codigo_ejecutadas": sum(c.cell_type == "code" for c in notebook.cells),
        "errores": 0,
        "alcance": alcance,
    }
    evidencia.write_text(json.dumps(registro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return registro
