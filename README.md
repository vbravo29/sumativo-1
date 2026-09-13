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

### Ejecutar F1

Abrir `F1/F1_Definición.ipynb` y seleccionar el kernel de `.venv`; usar **Restart Kernel and Run All Cells**. También se puede ejecutar desde la raíz:

```powershell
.\.venv\Scripts\python.exe F1\verificar_f1.py
```

El script crea un kernel nuevo del intérprete invocante, ejecuta todas las celdas y guarda sus salidas en el notebook. Solo si termina correctamente escribe `evidencias/F1_ejecucion.json`. La ejecución requiere el CSV original documentado y no modifica sus datos. El registro JSON identifica la ejecución y la huella del notebook; los resultados de las pruebas están en sus celdas.

F2 sigue pendiente de implementación y no está cubierto por esta verificación.

## Criterios de trabajo con datos

- El CSV original se conserva sin cambios.
- Las conversiones, filtros y columnas excluidas se justifican en el notebook F2.
- Las fechas se convertirán a un tipo temporal para analizar plazos y etapas del proceso.
- Las columnas sin información o con alta proporción de valores faltantes se evaluarán antes de eliminarlas.
- Los resultados derivados se guardarán en `data/processed/`.

## Estado actual

F1 contiene contexto, problema, preguntas, objetivos, alcance, supuestos, variables previstas, herramientas, lectura inicial y pruebas del código. La comprobación del archivo incluye SHA-256, dimensiones y presencia de columnas necesarias. No demuestra todavía que el dataset esté limpio.

Las salidas guardadas del validador del curso indican que el dataset cumple los requisitos mínimos; también muestran columnas vacías que deben tratarse en F2. El [mapa conceptual](docs/mapa_conceptual_f1_f2.drawio) y el [diccionario de las 74 variables](data/DICCIONARIO_VARIABLES.md) están vinculados en F1. Quedan pendientes su revisión por el equipo, el contraste de las definiciones del reporte con ChileCompra, dos fuentes docentes y una fuente académica reciente. F1 incluye dos referencias técnicas oficiales y la fuente del dataset. El informe integrado todavía debe desarrollarse y vincularse con estas evidencias.

Los cambios se incorporarán al historial mediante commits descriptivos de los integrantes que los revisen. La referencia del commit definitivo se añadirá al preparar la entrega.

## Documentación de F1

- [Mapa conceptual editable en draw.io](docs/mapa_conceptual_f1_f2.drawio): representa F1 implementado, F2 pendiente y F3–F4 proyectadas. La sección 9 de F1 vincula sus nodos con archivos y evidencias.
- [Diccionario de variables](data/DICCIONARIO_VARIABLES.md): cubre las 74 columnas y separa observaciones del CSV de definiciones propuestas.

El reporte de marzo contiene publicaciones desde enero de 2026; todos los cierres observados corresponden a marzo. El criterio oficial de selección mensual queda por confirmar. El mapa se elaboró a partir del avance actual y está pendiente de revisión del equipo.
