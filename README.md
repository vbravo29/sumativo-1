# Análisis de licitaciones públicas del sector Salud

Proyecto de Programación para la Ciencia de Datos sobre ofertas del sector Salud incluidas en el reporte de ChileCompra de marzo de 2026. Comprende la definición del problema (F1), el preprocesamiento de datos (F2) y la implementación y evaluación de algoritmos con programación orientada a objetos (F3).

**Repositorio:** [github.com/vbravo29/sumativo-1](https://github.com/vbravo29/sumativo-1)

## Objetivo y alcance

El análisis describe cómo varía la proporción de ofertas ganadoras según el tamaño del proveedor y el tipo de licitación. Se restringe a procesos adjudicados y utiliza como denominador las ofertas con resultado válido de cada grupo. Los resultados son descriptivos y no establecen causalidad.

Cada fila representa una **oferta asociada a un ítem de una licitación**. Una licitación puede aparecer en varias filas por sus distintos ítems y proveedores; el número de registros no equivale al número de licitaciones.

## Datos

| Característica | Valor |
| --- | --- |
| Fuente | [Datos Abiertos de ChileCompra](https://datos-abiertos.chilecompra.cl/descargas) |
| Reporte | Sector Salud, marzo de 2026 |
| Archivo | [licitaciones_salud_marzo_2026.csv](data/raw/licitaciones_salud_marzo_2026.csv) |
| Dimensiones | 44.226 filas y 74 columnas |
| Formato | CSV, separador `;`, codificación `latin-1` |
| Tamaño | 68,96 MB |

El archivo contiene datos del proceso de licitación, fechas, organismos compradores, productos, proveedores y resultados de las ofertas. La [documentación de datos](data/README.md) describe la cobertura observada, las huellas de integridad y los archivos derivados. El [diccionario de variables](data/DICCIONARIO_VARIABLES.md) detalla las 74 columnas.

## Estructura del repositorio

| Carpeta | Contenido |
| --- | --- |
| `F1/` | Definición del proyecto y verificación del entorno. |
| `F2/` | Exploración, limpieza, transformación y validación del dataset. |
| `F3/` | Notebook de algoritmos, pruebas, mediciones y verificación de ejecución. |
| `src/` | Clases y funciones de procesamiento y análisis. |
| `data/raw/` | Dataset original versionado. |
| `data/processed/` | CSV derivados generados localmente; excluidos de Git. |
| `docs/` | Informe F1/F2, mapa conceptual, decisiones técnicas y sección de algoritmos para el informe F3. |
| `evidencias/` | Registros de ejecución y resultados de las mediciones. |

## Preparación del entorno

El proyecto se verificó en Windows con Python 3.12.14. Desde la raíz del repositorio, con Python 3.12 instalado:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

[requirements.txt](requirements.txt) contiene las dependencias de F1, F2 y F3. Los notebooks muestran las versiones utilizadas. Ejecutar F1 permite comprobar la instalación y la lectura del dataset.

## Ejecución

Los siguientes comandos se ejecutan desde la raíz del repositorio:

```powershell
# Definición del proyecto y comprobación del entorno
.\.venv\Scripts\python.exe F1\verificar_f1.py

# Preprocesamiento y generación de los CSV derivados
.\.venv\Scripts\python.exe F2\verificar_f2.py

# Pruebas de algoritmos y clases
.\.venv\Scripts\python.exe -m unittest F3.test_algoritmos F3.test_nucleo_poo -v

# Mediciones y ejecución del notebook F3
.\.venv\Scripts\python.exe F3\medir_algoritmos.py
.\.venv\Scripts\python.exe F3\verificar_algoritmos.py
```

Los verificadores ejecutan los notebooks en kernels nuevos, guardan sus salidas y generan registros en `evidencias/`. F2 crea los CSV procesado y codificado en `data/processed/`; estos archivos no se incluyen al clonar el repositorio.

Las [instrucciones de F3](F3/README.md) detallan las pruebas, los archivos de medición y la comprobación de hashes. Si cambia el código de análisis o de medición, es necesario regenerar los resultados antes de ejecutar el notebook F3.

## Preprocesamiento

El CSV original se conserva sin modificaciones y se verifica mediante SHA-256. El procesamiento aplica las siguientes operaciones:

- Exclusión de tres columnas completamente vacías: `LicitacionBaseTipo`, `ContratoRenovable` y `UnidadTiempoRenovacion`.
- Conversión a `NaT` de 7.613 fechas del año 1900 en `FechaEstimadaEvaluacionOfertas`.
- Conversión de las columnas temporales a `datetime64[ns]`.
- Eliminación de espacios en categorías y conservación de `NoClasificado`.
- Cálculo de `oferta_ganadora`, `licitacion_adjudicada` y `plazo_cierre_dias`.

El dataset procesado conserva 44.226 filas y 74 columnas. Una segunda versión incorpora indicadores one-hot de `TipoLicitacion` y `TamanoProveedor`, sin eliminar las categorías originales. Esta codificación es exploratoria; su uso en un modelo requeriría ajustar el codificador con datos de entrenamiento y definir el tratamiento de categorías desconocidas.

Las reglas y sus justificaciones se encuentran en el notebook F2 y en [DECISIONES_TECNICAS.md](docs/DECISIONES_TECNICAS.md). La validación comprueba la consistencia del procesamiento; los plazos se resumen por registro de oferta.

## Organización del código

| Módulo | Responsabilidad |
| --- | --- |
| `src/datos.py` | Contrato de esquema, lectores, exportación y huellas SHA-256. |
| `src/preprocesamiento.py` | Transformaciones de fechas, categorías, variables derivadas y codificación. |
| `src/pipeline.py` | Coordinación de la limpieza mediante `LimpiadorLicitaciones`. |
| `src/validacion.py` | Validación del dataset mediante reglas y comprobación de indicadores. |
| `src/analisis.py` | Exploración, frecuencias y algoritmos de cálculo de proporciones. |
| `src/entorno.py` | Consulta de versiones de dependencias. |
| `src/ejecucion.py` | Ejecución de notebooks y registro de evidencias. |

`src/proyecto.py` mantiene las importaciones utilizadas por F1 y F2. Las alternativas de cálculo de F3 se importan directamente desde `src/analisis.py`.

## Algoritmos de F3

El [notebook F3](F3/F3_Algoritmos.ipynb) compara la referencia de F2 con versiones iterativa, recursiva y agrupada del cálculo de proporciones. Presenta ejemplos, pruebas de equivalencia, complejidad temporal y espacial, mediciones y conclusiones.

La variante agrupada obtuvo la menor mediana de tiempo para el conjunto completo en las mediciones guardadas. La comparación incluye la preparación interna y la salida del cálculo; excluye la lectura y limpieza del dataset. Los resultados y sus límites se explican en el notebook y en la [sección técnica de algoritmos](docs/F3_APORTE_ALGORITMOS.md).

## Documentación

- **Informe F1/F2:** [editable](docs/informe_f1_f2_grupo_5.docx) y [PDF](docs/f1_s01_grupo5.pdf).
- **Mapa conceptual F1:** [PDF](docs/mcdi500_s1_grupo5.pdf) y [archivo draw.io](docs/mcdi500_s1_grupo5.drawio).
- **Datos:** [procedencia y generación](data/README.md) y [diccionario de variables](data/DICCIONARIO_VARIABLES.md).
- **Arquitectura y métodos:** [decisiones técnicas](docs/DECISIONES_TECNICAS.md).
- **F3:** [instrucciones de ejecución](F3/README.md) y [análisis de algoritmos](docs/F3_APORTE_ALGORITMOS.md).

El informe grupal de F3 y la integración de las mediciones de lectura y actualizaciones de validación están pendientes.

## Trabajo con ramas

Los cambios se integran en `desarrollo`. Cada integrante puede crear una rama desde una versión actualizada de `desarrollo` y proponer su integración mediante un pull request.

La versión revisada se incorpora a `main` mediante un pull request, después de ejecutar las pruebas y verificar los notebooks. El flujo de trabajo es: rama individual → `desarrollo` → `main`.
