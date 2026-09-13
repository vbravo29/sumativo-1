# Análisis de licitaciones públicas del sector Salud

Proyecto grupal de la Sumativa 1 de Programación para la Ciencia de Datos. El trabajo cubre la definición del problema, la preparación de los datos y la validación inicial del análisis.

## Propósito del proyecto

El proyecto analiza las ofertas del archivo de licitaciones públicas del sector Salud de marzo de 2026. El objetivo es describir las diferencias en la proporción de ofertas ganadoras según el tipo de licitación y el tamaño del proveedor, mediante un flujo reproducible y con validación de la calidad de los datos.

La pregunta general es: ¿cómo varía la proporción de ofertas ganadoras según el tipo de licitación y el tamaño del proveedor en el sector Salud durante marzo de 2026? El análisis es descriptivo y no establece causalidad. F1 define el cálculo y sus restricciones; los resultados aún no se han calculado.

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

`requirements.txt` declara las dependencias principales de F1; pip instala sus dependencias internas automáticamente. Las versiones utilizadas se muestran en las salidas del notebook. Cada nueva instalación debe verificarse ejecutando F1 completo. Las librerías de visualización del futuro análisis se incorporarán cuando se implemente F2.

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
- Se neutralizaron las 7.613 fechas centinela del año 1900 en `FechaEstimadaEvaluacionOfertas` convirtiéndolas a `NaT`.
- Las columnas temporales (`FechaPublicacion`, `FechaCierre`, `FechaAdjudicacion`) se convirtieron a `datetime64[ns]`.
- Se preservó explícitamente la categoría `NoClasificado` en `TamanoProveedor` (3.410 ofertas) sin imputaciones artificiales.
- Se calcularon variables derivadas: `oferta_ganadora`, `licitacion_adjudicada` y `plazo_cierre_dias` (promedio 14,38 días).
- El dataset procesado resultante (44.226 filas x 74 columnas) se almacena en `data/processed/licitaciones_salud_marzo_2026_procesado.csv`.

## Estado del proyecto (Fases 1 y 2 Integradas)

El avance consolida los entregables exigidos para la **Sumativa 1**:
- **Fase 1 (Implementada):** Contexto, problema, preguntas de investigación, objetivos F1–F4, alcance, supuestos, contrato de lectura y pruebas unitarias.
- **Fase 2 (Implementada):** Diagnóstico EDA, pipeline modular en `src/proyecto.py`, limpieza justificada, suite de validación (casos normales, límites y excepciones) y exportación trazable.
- **Informe Técnico Formal:** Documento integrado en `docs/informe_f1_f2_grupo_5.docx` y compilado a PDF con índice de contenidos actualizado, tablas estadísticas y referencias bibliográficas en formato APA 7.ª edición.
- **Mapa Conceptual Técnico:** [docs/mapa_conceptual_f1_f2.drawio](docs/mapa_conceptual_f1_f2.drawio) actualizado, reflejando F1 y F2 implementadas y F3–F4 proyectadas.
- **Diccionario de Datos:** [data/DICCIONARIO_VARIABLES.md](data/DICCIONARIO_VARIABLES.md) con las 74 variables agrupadas temáticamente y con observaciones técnicas.

