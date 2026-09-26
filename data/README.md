# Procedencia de datos

## Dataset principal

- **Archivo:** `raw/licitaciones_salud_marzo_2026.csv`
- **Fuente:** [Datos Abiertos de ChileCompra](https://datos-abiertos.chilecompra.cl/descargas)
- **Contenido:** reporte seleccionado de marzo de 2026, sector Salud, con licitaciones y ofertas asociadas.
- **Formato de lectura:** CSV, separador `;`, codificación `latin-1`.
- **Dimensión inicial:** 44.226 filas y 74 columnas.
- **Unidad de análisis:** una oferta asociada a un ítem de una licitación. Una licitación puede aparecer en varias filas.
- **Cobertura observada:** `FechaPublicacion` va del 15 de enero al 25 de marzo de 2026 y `FechaCierre` va del 2 al 31 de marzo de 2026. No todas las publicaciones pertenecen a marzo; las fuentes consultadas no explican el criterio exacto usado para conformar este reporte mensual.
- **Tamaño:** 68,96 MB.
- **SHA-256:** `490D9209A10D387011D481B72B7891F26E997974EC2CF9DFC518AA4A08552232`

El archivo original está versionado para reproducir los análisis con la misma copia del dataset. Los demás archivos descargados en `data/raw/` permanecen excluidos de Git.

## Criterios aplicados

- El archivo original se conserva sin modificaciones y se verifica mediante SHA-256.
- Los resultados derivados se generan únicamente en `data/processed/`.
- El notebook F2 documenta las conversiones de fechas, el tratamiento de valores faltantes y las columnas excluidas, junto con su justificación.
- La validación comprueba la conservación de filas, las columnas obligatorias, los resultados de oferta, las fechas y la coherencia de las variables derivadas.

## Diccionario de variables

El diccionario incluye el contraste realizado con el portal oficial y la API. Distingue conceptos respaldados, correspondencias propuestas y controles del archivo. Las fuentes consultadas no especifican las reglas y el año usados para clasificar el tamaño del proveedor, el tratamiento tributario de los montos ni el significado de las fechas de evaluación registradas en 1900. El parámetro `latin-1` se conserva porque esta copia no admite una lectura UTF-8 estricta, aunque el portal anuncia UTF-8 de forma general.

El [diccionario de trabajo](DICCIONARIO_VARIABLES.md) cubre las 74 columnas. Incluye tipos observados, roles propuestos, faltantes y controles previstos. Las definiciones se basan en encabezados y valores y orientaron las reglas de preprocesamiento aplicadas en la Fase 2.

## Dataset procesado (Fase 2)

- **Archivo derivado:** `processed/licitaciones_salud_marzo_2026_procesado.csv`
- **Generación:** El notebook `F2/F2_Preprocesamiento.ipynb` aplica `limpiar_datos_f2()` de `src/pipeline.py` y exporta el resultado con `exportar_datos_procesados()` de `src/datos.py`. Ambas funciones siguen disponibles desde `src/proyecto.py`.
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

F2 añade una versión con one-hot encoding de `TipoLicitacion` y `TamanoProveedor`, conservando las categorías originales y `NoClasificado`. Cada indicador es un entero 0/1; las categorías no reciben un orden artificial. `src/preprocesamiento.py` implementa `codificar_nominales` y el notebook muestra ejemplos y pruebas de correspondencia, conservación de filas y lectura del archivo exportado.

El archivo adicional es `data/processed/licitaciones_salud_marzo_2026_codificado.csv` (ruta desde la raíz). El CSV procesado de 74 columnas sigue siendo la base de las proporciones. La codificación es una preparación exploratoria; un futuro modelo requerirá ajustar su codificador solo con datos de entrenamiento y definir las categorías desconocidas.

## Generación de archivos derivados

Los CSV de `data/processed/` están excluidos del control de versiones. Se generan desde el original al ejecutar F2 y no están incluidos en una copia recién clonada del repositorio.

Desde la raíz, con el entorno configurado según el [README principal](../README.md#preparación-del-entorno):

```powershell
.\.venv\Scripts\python.exe F2\verificar_f2.py
```

La ejecución crea o reemplaza estos archivos:

- `data/processed/licitaciones_salud_marzo_2026_procesado.csv`: dataset limpio de 74 columnas.
- `data/processed/licitaciones_salud_marzo_2026_codificado.csv`: dataset con 12 indicadores adicionales, de 86 columnas.

El notebook registra las dimensiones y huellas SHA-256 de las exportaciones y comprueba los indicadores después de volver a leer el archivo codificado.
