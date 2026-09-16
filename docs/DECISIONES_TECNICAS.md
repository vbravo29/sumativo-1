# Decisiones técnicas: alternativas evaluadas y descartadas

**Curso:** MCDIA500 — Programación para la Ciencia de Datos
**Proyecto:** Análisis de ofertas en licitaciones públicas del sector Salud (marzo de 2026)
**Grupo:** 5 — Víctor Bravo Barrera, Nayadeth Garrido Ibáñez, Mauricio Cid
**Fases cubiertas:** F1 y F2 · **Última actualización:** 16 de septiembre de 2026

## Propósito

El informe técnico documenta **qué** se hizo y **por qué** (sección IV.B). Este registro
complementa esa información dejando constancia de **qué alternativas se evaluaron y por qué se
descartaron**. Una decisión sin alternativa registrada es indistinguible de una omisión.

---

## 1. Entorno y reproducibilidad

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-01 | Entorno virtual `venv` con el stack científico de Python (NumPy, pandas, Jupyter) y dependencias en `requirements.txt` | Conda · Poetry | El stack es el propio de un entorno científico en ciencia de datos y corresponde al propuesto en clases. Conda y Poetry añadirían herramientas ajenas al material del curso sin resolver ningún problema del proyecto |
| D-02 | Versiones exactas en NumPy y pandas; rangos por versión mayor en el stack Jupyter | `pip freeze` completo · sin versiones | `pip freeze` congela dependencias transitivas propias de Windows y reduce la portabilidad; sin versiones, un cambio mayor de pandas altera la inferencia de tipos y los resultados |
| D-03 | Ejecución verificada por script con kernel nuevo y aislado, que registra hash y fecha | «Restart & Run All» manual · `papermill` | La ejecución manual no deja registro comprobable por terceros; `papermill` añadiría una dependencia para algo que `nbclient` —ya requerido— resuelve |

## 2. Datos de origen

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-04 | Versionar el CSV original (68,96 MB) dentro del repositorio | Script de descarga desde el portal · Git LFS | El archivo es una foto del día de ejecución. Todavía no existe un pipeline de datos automatizado y el desarrollo se está probando de forma spot, por lo que un script de descarga resolvería un problema que aún no se plantea |
| D-05 | Lectura con `sep=";"` y `encoding="latin-1"`, declarados explícitamente | `utf-8` estricto · `errors='replace'` · detección automática | UTF-8 falla sobre esta copia: se verificó, no se supuso. `errors='replace'` corrompería nombres de organismos en silencio y la detección automática no es determinista |
| D-06 | Verificación SHA-256 del archivo antes de procesar | Validar por nombre y tamaño · MD5 | Nombre y tamaño coinciden entre archivos distintos; MD5 está criptográficamente roto sin ahorro relevante |
| D-07 | `data/processed/` fuera del control de versiones, con dimensiones y hash publicados | Versionar los derivados (68,16 y 69,17 MB) | Duplicaría el peso del repositorio con información reconstruible y generaría un diff binario completo en cada reejecución |

## 3. Unidad de análisis y limpieza

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-08 | La fila es una oferta por ítem: no se deduplica por `NroLicitacion` | `drop_duplicates(subset='NroLicitacion')` · agregar a nivel de licitación | Deduplicar reduciría el archivo de 44.226 a 1.864 filas y destruiría la variable de interés; agregar por licitación responde otra pregunta |
| D-09 | Exclusión nominal de las 3 columnas 100 % vacías, con comprobación previa | `dropna(axis=1, how='all')` · umbral por porcentaje | El automático cambia de comportamiento en silencio si el insumo cambia; un umbral descartaría columnas con 72 % de nulos que siguen siendo legítimas |
| D-10 | Conservar las 7 columnas constantes, incluida `Sector` | Eliminar toda columna sin varianza | Que `Sector` sea constante es la prueba del alcance sectorial declarado en el informe. La falta de varianza es criterio de modelado, no de calidad de datos |
| D-11 | Los 7.613 valores de 1900 en `FechaEstimadaEvaluacionOfertas` pasan a `NaT`; las 44.226 filas se conservan | Eliminar las filas · imputar una fecha plausible · dejar el año 1900 | Eliminar descartaría el 17,2 % del archivo por una anomalía en una columna que no participa del análisis; imputar fabricaría datos en un campo de significado desconocido |
| D-12 | `errors='coerce'` con guardia que lanza `ValueError` si una fecha con valor queda nula | `coerce` sin comprobación · `errors='raise'` directo | Sin comprobación, un cambio de formato en el origen se traduce en pérdida silenciosa; `raise` no indica cuántos registros fallaron ni en qué columna |
| D-13 | Normalización de texto limitada a `str.strip()` | Añadir `.lower()` · transliterar acentos · mapear a códigos (LE, LP, LR, L1) | No hay variantes que difieran solo en capitalización; los códigos no son homogéneos en las categorías privadas y el mapeo exigiría supuestos no respaldados por las fuentes |
| D-14 | `NoClasificado` (3.410 ofertas) se preserva como quinta categoría | Imputar por la moda · eliminar las filas · convertir a `NaN` · agrupar con `Micro` | El sesgo caería justo sobre la variable que el estudio compara. Los resultados lo confirman: 53,36 % de ofertas ganadoras, por encima de `Micro` (51,95 %) |
| D-15 | Los NA parciales (22 columnas) no se imputan; se cuantifican y documentan | Imputación por media/moda · eliminar columnas con >50 % de nulos · imputación por modelo | Ninguna columna afectada participa del cálculo de las proporciones y las cinco variables obligatorias están completas |
| D-16 | `plazo_cierre_dias` se calcula solo con `FechaPublicacion` y `FechaCierre` | Incluir `FechaAdjudicacion` · redondear a días enteros | Las demás fechas tienen faltantes y generarían nulos en el derivado; el redondeo pierde información horaria que el archivo sí registra |
| D-17 | No se escalan ni normalizan las variables numéricas | `StandardScaler` / `MinMaxScaler` preventivo | El análisis es de frecuencias y proporciones sobre categóricas; escalar solo haría ilegible `plazo_cierre_dias`, interpretable en días |

## 4. Cálculo de las proporciones

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-18 | El cálculo se restringe a `EstadoLicitacion == "Adjudicada"` | Usar las 44.226 filas sin filtrar · excluir solo los procesos desiertos | En un proceso desierto o revocado ninguna oferta puede ganar: añade denominador sin numerador posible. Descarta 201 filas (0,45 %) |
| D-19 | Denominador propio por grupo, con la categoría residual informada aparte | Denominador común global · publicar solo porcentajes | El denominador global mide composición del mercado, no probabilidad de ganar dentro del estrato; un 50 % sobre 2 ofertas no es comparable con un 62 % sobre 23.590 |
| D-20 | Los montos quedan fuera del análisis principal | Sumar o promediar montos · convertir a moneda común | Sumar cuatro monedas distintas es un error aritmético; convertir exigiría una fuente externa y una fecha de referencia arbitraria |

## 5. Codificación de variables nominales

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-21 | One-hot encoding con prefijo `oh_<columna>__`: 12 indicadores, de 74 a 86 columnas | Label/ordinal encoding · ordinal solo para `TamanoProveedor` · target encoding · frequency encoding | Numerar las categorías introduce un orden inexistente: `NoClasificado` no tiene lugar en la escala de tamaño y los umbrales no están documentados. Target encoding usaría la variable de interés y provocaría fuga |
| D-22 | Se conservan todas las categorías, sin eliminar una de referencia | `drop_first=True` | Eliminar la referencia depende del modelo, que aún no existe, e invalidaría la comprobación de que cada fila activa exactamente un indicador |
| D-23 | Indicadores `int8` exportados en archivo independiente de 86 columnas | `dtype=bool` · `int64` por omisión · reemplazar el dataset procesado | `bool` obligaría a convertir antes de operar e `int64` consume ocho veces más memoria; reemplazar el procesado rompería la correspondencia con las 74 columnas del informe |

## 6. Arquitectura del código

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-24 | 16 funciones en `src/proyecto.py` que devuelven copias; los notebooks configuran, invocan y presentan | Clase con estado · mantener el código en los notebooks · `inplace=True` | Las transformaciones no comparten estado; el código en notebooks impide reutilizarlo entre F1 y F2; `inplace` destruiría el original sobre el que se apoyan las validaciones |

---

Repositorio: <https://github.com/vbravo29/sumativo-1> · Las decisiones aquí registradas se
implementan en `src/proyecto.py` y se documentan en el informe técnico, sección IV.B.
