# Análisis de licitaciones públicas del sector Salud

Proyecto grupal de la Sumativa 1 de Programación para la Ciencia de Datos. El trabajo cubre la definición del problema, la preparación de los datos y la validación inicial del análisis.

## Propósito del proyecto

El proyecto analiza las ofertas del archivo de licitaciones públicas del sector Salud de marzo de 2026. El objetivo es describir las diferencias en la proporción de ofertas ganadoras según el tipo de licitación y el tamaño del proveedor, mediante un flujo reproducible y con validación de la calidad de los datos.

La pregunta general es: ¿cómo varía la proporción de ofertas ganadoras según el tipo de licitación y el tamaño del proveedor en el sector Salud durante marzo de 2026? El análisis es descriptivo y no establece causalidad. F1 define el cálculo y sus restricciones; F2 incluye resultados descriptivos preliminares, restringidos a procesos adjudicados.

## Qué representa la información

ChileCompra es la plataforma mediante la cual organismos públicos publican necesidades de compra y reciben ofertas de proveedores. Una licitación puede incluir uno o más productos o servicios, y para cada ítem pueden participar varios proveedores.

Cada fila del archivo corresponde a una **oferta asociada a un ítem de una licitación**. Por eso una misma licitación puede aparecer en varias filas: puede tener distintos ítems y varias ofertas para cada uno. No se debe interpretar cada fila como una licitación única.

El archivo contiene, entre otros, estos grupos de información:

- Datos de la licitación: identificador, nombre, tipo, estado, moneda y monto estimado.
- Fechas del proceso: publicación, cierre, adjudicación y otras etapas administrativas.
- Información del organismo comprador: institución, unidad de compra y sector.
- Información del bien o servicio: rubro, producto, descripción, unidad de medida y cantidad.
- Información de los proveedores y ofertas: proveedor, tamaño de empresa, monto ofertado, moneda y resultado (`Ganadora` o `Perdedora`).

## Dataset

El dataset principal es [`data/raw/licitaciones_salud_marzo_2026.csv`](data/raw/licitaciones_salud_marzo_2026.csv), obtenido desde [Datos Abiertos de ChileCompra](https://datos-abiertos.chilecompra.cl/descargas).

| Característica | Información |
| --- | --- |
| Cobertura | Sector Salud, reporte de licitaciones de marzo de 2026 |
| Registros | 44.226 ofertas asociadas a licitaciones e ítems |
| Variables | 74 columnas |
| Formato | CSV con separador `;` y codificación `latin-1` |
| Tamaño | 68,96 MB |

El detalle de procedencia, lectura y trazabilidad está en [data/README.md](data/README.md).

## Estructura del repositorio

- `F1/`: notebook de definición del proyecto y configuración del entorno.
- `F2/`: notebook de exploración, limpieza, transformación y validación de datos.
- `data/raw/`: dataset original.
- `data/processed/`: datos generados durante el preprocesamiento.
- `docs/`: informe integrado en desarrollo.
- `evidencias/`: resultados de ejecuciones verificadas.
- `src/`: funciones reutilizables del proyecto.

## Preparación del entorno

La verificación de F1 utiliza un entorno virtual con Python 3.12.14 en Windows. La referencia anterior a Python 3.14.7 no se ha validado en esta revisión. Para reproducir el entorno desde la raíz del repositorio, con Python 3.12 instalado:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

`requirements.txt` declara las dependencias principales de F1 y F2; pip instala sus dependencias internas automáticamente. Las versiones utilizadas se muestran en las salidas del notebook. Cada nueva instalación debe verificarse ejecutando F1 completo. Los gráficos adicionales quedan previstos para F3.

### Ejecución de notebooks

Para reproducir la ejecución completa de cada notebook y regenerar las evidencias técnicas en un kernel nuevo y aislado:

```powershell
# Ejecución verificada de Fase 1 (Definición y entorno)
.\.venv\Scripts\python.exe F1\verificar_f1.py

# Ejecución verificada de Fase 2 (Exploración, preprocesamiento y validación)
.\.venv\Scripts\python.exe F2\verificar_f2.py
```

Cada script inicia un kernel nuevo del entorno virtual, ejecuta todas las celdas secuencialmente, preserva sus salidas en el notebook y emite un registro de trazabilidad en `evidencias/` (`F1_ejecucion.json` y `F2_ejecucion.json`).

## Criterios de trabajo y preprocesamiento (F2)

- El CSV original en `data/raw/` se conserva inmutable con verificación de hash SHA-256.
- Se excluyeron las 3 columnas 100% vacías (`LicitacionBaseTipo`, `ContratoRenovable`, `UnidadTiempoRenovacion`).
- Se neutralizaron las 7.613 fechas anómalas del año 1900 en `FechaEstimadaEvaluacionOfertas` convirtiéndolas a `NaT`.
- Las columnas temporales (`FechaPublicacion`, `FechaCierre`, `FechaAdjudicacion`) se convirtieron a `datetime64[ns]`.
- Se preservó explícitamente la categoría `NoClasificado` en `TamanoProveedor` (3.410 ofertas) sin imputaciones artificiales.
- Se calcularon variables derivadas: `oferta_ganadora`, `licitacion_adjudicada` y `plazo_cierre_dias` (promedio 14,38 días).
- El dataset procesado resultante (44.226 filas x 74 columnas) se almacena en `data/processed/licitaciones_salud_marzo_2026_procesado.csv`.

## Estado del proyecto (Fases 1 y 2 Integradas)

El avance consolida los entregables exigidos para la **Sumativa 1**:
- **Fase 1 (Implementada):** Contexto, problema, preguntas de investigación, objetivos F1–F4, alcance, supuestos, contrato de lectura y pruebas unitarias.
- **Fase 2 (Implementada):** Diagnóstico EDA, pipeline modular en `src/proyecto.py`, limpieza justificada, suite de validación (casos normales, límites y excepciones) y exportación trazable.
- **Informe Técnico Formal:** Documento integrado en `docs/informe_f1_f2_grupo_5.docx` con índice de contenidos actualizado; la exportación definitiva queda pendiente del cierre de las citas docentes, tablas estadísticas y referencias bibliográficas en formato APA 7.ª edición.
- **Mapa conceptual F1:** [PDF de entrega](docs/mcdi500_s1_grupo5.pdf) y [editable en draw.io](docs/mcdi500_s1_grupo5.drawio). Incluye portada y mapa en dos páginas carta; organiza el entorno, la documentación y la colaboración de F1, con continuidad hacia F2–F4.
- **Diccionario de Datos:** [data/DICCIONARIO_VARIABLES.md](data/DICCIONARIO_VARIABLES.md) con las 74 variables agrupadas temáticamente y con observaciones técnicas.


## Pendiente documental
Completar dos materiales docentes verificables y sus citas. El informe incluye un apartado amarillo como recordatorio. La limpieza y sus pruebas no sustituyen una validación estadística ni normativa. Los plazos se resumen por registro de oferta.

## Codificación de variables nominales

F2 añade una versión con one-hot encoding de `TipoLicitacion` y `TamanoProveedor`, conservando las categorías originales y `NoClasificado`. Cada indicador es un entero 0/1; las categorías no reciben un orden artificial. `src/proyecto.py` contiene `codificar_nominales` y el notebook muestra ejemplos y pruebas de correspondencia, conservación de filas y lectura del archivo exportado.

El archivo adicional es `data/processed/licitaciones_salud_marzo_2026_codificado.csv` (ruta desde la raíz). El CSV procesado de 74 columnas sigue siendo la base de las proporciones. La codificación es una preparación exploratoria; un futuro modelo requerirá ajustar su codificador solo con datos de entrenamiento y definir las categorías desconocidas.

## Funciones y responsabilidades

Las celdas configuran entradas, llaman funciones y muestran resultados. Las operaciones repetibles se concentran en `src/proyecto.py`:

| Componente | Función |
| --- | --- |
| Lectura y trazabilidad | `leer_datos_f1`, `sha256_archivo`, `versiones_entorno` |
| Diagnóstico y frecuencias | `resumen_exploracion`, `tablas_frecuencia` |
| Exclusión de columnas vacías | `excluir_columnas_vacias` |
| Fechas y años excluidos por columna | `convertir_fechas` |
| Normalización de categorías | `normalizar_categorias` |
| Indicadores y plazos | `generar_variables_derivadas` |
| Coordinación de limpieza | `limpiar_datos_f2` |
| Comprobación del resultado | `validar_dataset_procesado` |
| Proporciones por cualquier variable de agrupación | `tabla_proporciones` |
| Codificación y comprobación one-hot | `codificar_nominales`, `validar_codificacion` |
| Exportación | `exportar_datos_procesados` |

`src/ejecucion.py` contiene `ejecutar_notebook`, compartida por los verificadores F1 y F2. Las funciones de transformación devuelven copias; las de lectura/exportación tienen rutas explícitas. Las pruebas permanecen visibles en los notebooks. No se encapsulan instrucciones aisladas de presentación ni la configuración mínima necesaria para importar el módulo.
