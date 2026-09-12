# Procedencia de datos

## Dataset principal

- **Archivo:** `raw/licitaciones_salud_marzo_2026.csv`
- **Fuente:** [Datos Abiertos de ChileCompra](https://datos-abiertos.chilecompra.cl/descargas)
- **Contenido:** licitaciones del sector Salud publicadas durante marzo de 2026 y sus ofertas asociadas.
- **Formato de lectura:** CSV, separador `;`, codificación `latin-1`.
- **Dimensión inicial:** 44.226 filas y 74 columnas.
- **Unidad de análisis:** una oferta asociada a un ítem de una licitación. Una licitación puede aparecer en varias filas.
- **Cobertura de publicación:** marzo de 2026. Las fechas de los procesos pueden abarcar desde enero hasta meses posteriores, según sus etapas administrativas.
- **Tamaño:** 68,96 MB.
- **SHA-256:** `490D9209A10D387011D481B72B7891F26E997974EC2CF9DFC518AA4A08552232`

El archivo se incluye en el repositorio para que el equipo pueda ejecutar los notebooks con los mismos datos. Los demás archivos descargados en `data/raw/` permanecen excluidos de Git.

## Criterios de tratamiento inicial

- Conservar el archivo original sin modificaciones.
- Crear resultados derivados únicamente en `data/processed/`.
- Documentar en el notebook F2 las conversiones de fechas, tratamiento de valores faltantes y columnas excluidas, junto con su justificación.
- Verificar montos, monedas, fechas, estados y duplicados antes de producir el dataset procesado.
