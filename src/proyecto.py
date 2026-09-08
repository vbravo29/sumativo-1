"""Utilidades iniciales; pipeline del caso pendiente."""
from importlib.metadata import version

def versiones_entorno():
    """Registra versiones; falla si falta una dependencia requerida."""
    paquetes = ("numpy", "pandas", "matplotlib", "jupyterlab", "ipykernel",
                "nbformat", "nbconvert")
    return {nombre: version(nombre) for nombre in paquetes}

