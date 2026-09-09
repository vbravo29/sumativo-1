# sumativo-1
Proyecto de la Sumativa 1 — Fases 1 y 2 (UNAB).

**Estado:** estructura inicial. La definición del caso y la incorporación del dataset están pendientes.

## Estructura
- `F1/F1_Definición.ipynb`: definición y comprobación inicial del entorno.
- `F2/F2_Preprocesamiento.ipynb`: guía de obtención, exploración, limpieza y validación.
- `src/`: funciones compartidas.
- `data/raw/` y `data/processed/`: originales y derivados.
- `docs/informe_f1_f2_grupo_5.docx`: versión de trabajo del informe integrado del grupo 5.
- `materiales/`: referencias y planificación locales, excluidas de Git.
- `evidencias/`: salidas de ejecución.
- `requirements.txt`: dependencias iniciales.

## Requisitos
Python 3.14.7 y Git. Comprobar la versión con `py -3.14 --version`. JupyterLab se instala junto con las dependencias.

## Dependencias
| Paquete | Propósito |
| --- | --- |
| numpy | Operaciones numéricas |
| pandas | Lectura y transformación de datos |
| matplotlib | Visualizaciones |
| jupyterlab | Edición y ejecución de notebooks |
| ipykernel | Kernel Python |
| nbformat | Validación de notebooks |
| nbconvert | Ejecución completa y exportación |

Los rangos se declaran en `requirements.txt`. Después de instalar y validar, generar `requirements-lock.txt` para registrar versiones exactas. Todavía no hay un entorno del equipo validado.

Los mínimos de NumPy (2.3.3), pandas (2.3.3) e ipykernel (7.0.1) se eligieron por su soporte para Python 3.14: [NumPy](https://numpy.org/doc/2.3/release/2.3.3-notes.html), [pandas](https://pandas.pydata.org/pandas-docs/stable/whatsnew/v2.3.3.html) e [ipykernel](https://ipykernel.readthedocs.io/en/stable/changelog.html).

## Instalación en Windows — PowerShell
```powershell
# Ejecutar desde la carpeta raíz del repositorio.
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m jupyterlab
```

Si solo existe `python`, verificar su versión y usar `python -m venv .venv`. Los comandos usan el ejecutable del entorno sin necesidad de activarlo.

Abrir F1 y luego F2 con el kernel del entorno y ejecutar todas las celdas. F2 indica los pendientes; su ejecución no verifica un pipeline real.

Para guardar copias ejecutadas y fijar las versiones después de validar:
```powershell
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute "F1/F1_Definición.ipynb" --output-dir evidencias
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute "F2/F2_Preprocesamiento.ipynb" --output-dir evidencias
.\.venv\Scripts\python.exe -m pip freeze | Out-File -Encoding utf8 requirements-lock.txt
.\.venv\Scripts\python.exe --version
```

Registrar en este README el sistema operativo, la versión exacta de Python y el resultado de la validación una vez realizada. Los demás integrantes deben instalar el archivo lock en un entorno limpio y comprobar ejecución.

## Git y datos
Datos y materiales del curso están excluidos por defecto en `.gitignore`. Documentar cómo obtenerlos; decidir su inclusión según licencia, tamaño y restricciones del caso. Cada integrante debe usar su propia identidad Git y commits descriptivos. Revisar `git status` y `git diff` antes de subir.

## Estado y entrega
El informe del grupo 5 está disponible en [docs/informe_f1_f2_grupo_5.docx](docs/informe_f1_f2_grupo_5.docx). Es una versión inicial con la identificación de integrantes; el desarrollo de F1 y F2 está pendiente.

Pendientes: caso, dataset, definición del problema, desarrollo F1/F2 y validación del entorno. La entrega final incluye un informe PDF integrado y evidencias de ejecución de ambas fases.

Registrar la procedencia del dataset en [data/README.md](data/README.md). Conservar los datos originales en `data/raw/` y guardar los derivados en `data/processed/` para mantener la trazabilidad.

Las decisiones sobre limpieza, tipos de datos y transformaciones se documentarán junto al código correspondiente en los notebooks y se resumirán en el informe integrado. Este README concentra la configuración del proyecto, las dependencias y las instrucciones de ejecución.

test
