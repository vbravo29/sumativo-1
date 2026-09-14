# Procedencia de datos

## Dataset principal

- **Archivo:** `raw/licitaciones_salud_marzo_2026.csv`
- **Fuente:** [Datos Abiertos de ChileCompra](https://datos-abiertos.chilecompra.cl/descargas)
- **Contenido:** reporte seleccionado de marzo de 2026, sector Salud, con licitaciones y ofertas asociadas.
- **Formato de lectura:** CSV, separador `;`, codificación `latin-1`.
- **Dimensión inicial:** 44.226 filas y 74 columnas.
- **Unidad de análisis:** una oferta asociada a un ítem de una licitación. Una licitación puede aparecer en varias filas.
- **Cobertura observada:** FechaPublicacion va del 15 de enero al 25 de marzo de 2026; FechaCierre va del 2 al 31 de marzo de 2026. No todas las publicaciones pertenecen a marzo. El criterio oficial del reporte mensual requiere confirmación.
- **Tamaño:** 68,96 MB.
- **SHA-256:** `490D9209A10D387011D481B72B7891F26E997974EC2CF9DFC518AA4A08552232`

El archivo se incluye en el repositorio para que el equipo pueda ejecutar los notebooks con los mismos datos. Los demás archivos descargados en `data/raw/` permanecen excluidos de Git.

## Criterios de tratamiento inicial

- Conservar el archivo original sin modificaciones.
- Crear resultados derivados únicamente en `data/processed/`.
- Documentar en el notebook F2 las conversiones de fechas, tratamiento de valores faltantes y columnas excluidas, junto con su justificación.
- Verificar montos, monedas, fechas, estados y duplicados antes de producir el dataset procesado.

## Diccionario de variables

El diccionario incluye el resultado de la validación parcial con el portal oficial y la API. Distingue conceptos respaldados, correspondencias propuestas y controles del archivo. Siguen sin confirmarse las reglas y año de tamaño de proveedor, los impuestos de los montos y la codificación de las fechas de evaluación de 1900. El parámetro latin-1 se conserva porque esta copia no es UTF-8 válida, aunque el portal anuncia UTF-8 de forma general.

El [diccionario de trabajo](DICCIONARIO_VARIABLES.md) cubre las 74 columnas. Incluye tipos observados, roles propuestos, faltantes y controles previstos. Las definiciones se basan en encabezados y valores y orientaron las reglas de preprocesamiento aplicadas en la Fase 2.

## Dataset procesado (Fase 2)

- **Archivo derivado:** `processed/licitaciones_salud_marzo_2026_procesado.csv`
- **Generación:** Producido por la función `limpiar_datos_f2()` de `src/proyecto.py` e implementado en `F2/F2_Preprocesamiento.ipynb`.
- **Dimensiones:** 44.226 filas y 74 columnas (exclusión de 3 columnas vacías y adición de 3 variables derivadas).
- **Transformaciones aplicadas:**
  - Exclusión de `LicitacionBaseTipo`, `ContratoRenovable` y `UnidadTiempoRenovacion` (100% nulas).
  - Fechas anómalas en año 1900 neutralizadas a `NaT` en `FechaEstimadaEvaluacionOfertas`.
  - Columnas temporales convertidas a formato `datetime64[ns]`.
  - Normalización de cadenas de texto y preservación de la categoría `NoClasificado` en `TamanoProveedor`.
  - Variables derivadas: `oferta_ganadora` (bool), `licitacion_adjudicada` (bool) y `plazo_cierre_dias` (float).
- **Tamaño:** 68,16 MB.
- **SHA-256:** `7e835d6725d8c4f9aa64ad97a294dc38fcc341e71373f544c7f6b8ba2ff31dc5`.


## Codificación de variables nominales

F2 añade una versión con one-hot encoding de `TipoLicitacion` y `TamanoProveedor`, conservando las categorías originales y `NoClasificado`. Cada indicador es un entero 0/1; las categorías no reciben un orden artificial. `src/proyecto.py` contiene `codificar_nominales` y el notebook muestra ejemplos y pruebas de correspondencia, conservación de filas y lectura del archivo exportado.

El archivo adicional es `data/processed/licitaciones_salud_marzo_2026_codificado.csv` (ruta desde la raíz). El CSV procesado de 74 columnas sigue siendo la base de las proporciones. La codificación es una preparación exploratoria; un futuro modelo requerirá ajustar su codificador solo con datos de entrenamiento y definir las categorías desconocidas.
