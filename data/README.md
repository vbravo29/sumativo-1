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

El [diccionario de trabajo](DICCIONARIO_VARIABLES.md) cubre las 74 columnas. Incluye tipos observados, roles propuestos, faltantes y controles previstos. Las definiciones se basan en encabezados y valores y requieren contraste con la documentación del reporte masivo. No se han limpiado ni transformado datos.
