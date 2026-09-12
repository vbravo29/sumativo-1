# Análisis de licitaciones públicas del sector Salud

Proyecto grupal de la Sumativa 1 de Programación para la Ciencia de Datos. El trabajo cubre la definición del problema, la preparación de los datos y la validación inicial del análisis.

## Propósito del proyecto

El proyecto analiza las licitaciones públicas del sector Salud registradas en ChileCompra durante marzo de 2026. El objetivo es describir cómo se distribuyen las ofertas recibidas según el tipo de licitación, institución compradora, rubro, proveedor, monto y resultado de la oferta.

La pregunta general que guiará el trabajo es: ¿qué características presentan las ofertas de las licitaciones del sector Salud y cómo se relacionan con su resultado?

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

El proyecto usa Python 3.14.7. Cuando `requirements.txt` esté disponible en la rama de trabajo, instalar las dependencias desde la raíz del repositorio con:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

Los notebooks deben ejecutarse con el kernel asociado a `.venv`.

## Criterios de trabajo con datos

- El CSV original se conserva sin cambios.
- Las conversiones, filtros y columnas excluidas se justifican en el notebook F2.
- Las fechas se convertirán a un tipo temporal para analizar plazos y etapas del proceso.
- Las columnas sin información o con alta proporción de valores faltantes se evaluarán antes de eliminarlas.
- Los resultados derivados se guardarán en `data/processed/`.

## Estado actual

El dataset fue validado y cumple los requisitos mínimos del curso: tiene suficientes filas y columnas, combina variables numéricas, categóricas y temporales, y no presenta filas duplicadas exactas. El siguiente paso es completar la definición del problema, los objetivos y las preguntas de análisis en F1.
