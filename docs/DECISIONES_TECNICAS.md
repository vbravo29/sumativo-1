# Decisiones técnicas: alternativas evaluadas y descartadas

**Curso:** MCDIA500 — Programación para la Ciencia de Datos
**Proyecto:** Análisis de ofertas en licitaciones públicas del sector Salud (marzo de 2026)
**Grupo:** 5 — Víctor Bravo Barrera, Nayadeth Garrido Ibáñez, Mauricio Cid
**Fases cubiertas:** F1, F2 y primer incremento de F3 · **Última actualización:** 22 de septiembre de 2026

## Propósito

El informe técnico documenta **qué** se hizo y **por qué** (sección IV.B). Este registro
complementa esa información dejando constancia de **qué alternativas se evaluaron y por qué se
descartaron**. Una decisión sin alternativa registrada es indistinguible de una omisión.

---

## 1. Entorno y reproducibilidad

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-01 | Entorno virtual `venv` con el stack científico de Python (NumPy, pandas, Jupyter) y dependencias en `requirements.txt` | Conda · Poetry | Elegimos las herramientas vistas en clases porque eran suficientes para el proyecto y todo el equipo ya sabía utilizarlas. Incorporar Conda o Poetry habría agregado una dificultad innecesaria en esta etapa |
| D-02 | Versiones exactas en NumPy y pandas; rangos por versión mayor en el stack Jupyter | `pip freeze` completo · sin versiones | Guardar todas las versiones habría dejado el proyecto demasiado ligado al computador donde se creó. Tampoco convenía dejarlas sin indicar, porque una actualización futura podría hacer que el notebook entregara resultados diferentes |
| D-03 | Ejecución verificada por script con kernel nuevo y aislado, que registra hash y fecha | «Restart & Run All» manual · `papermill` | Ejecutar el notebook manualmente depende de que una persona recuerde todos los pasos y no deja una evidencia clara. `papermill` también permitía automatizarlo, pero significaba instalar otra herramienta cuando el proyecto ya contaba con una que cumplía esa función |

## 2. Datos de origen

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-04 | Versionar el CSV original (68,96 MB) dentro del repositorio | Script de descarga desde el portal · Git LFS | Preferimos conservar exactamente el archivo utilizado por el equipo, ya que el portal puede actualizar su contenido con el tiempo. Automatizar la descarga o incorporar Git LFS habría agregado trabajo sin aportar una ventaja concreta para esta entrega |
| D-05 | Lectura con `sep=";"` y `encoding="latin-1"`, declarados explícitamente | `utf-8` estricto · `errors='replace'` · detección automática | Probamos UTF-8 y el archivo no se leyó correctamente. Reemplazar los caracteres problemáticos podía cambiar nombres sin que lo notáramos, mientras que dejar la detección automática podía producir resultados distintos entre equipos |
| D-06 | Verificación SHA-256 del archivo antes de procesar | Validar por nombre y tamaño · MD5 | Revisar solo el nombre y el tamaño no garantiza que el contenido sea el mismo. Elegimos SHA-256 porque permite comprobar de manera sencilla que todas las personas están trabajando con la misma copia del archivo |
| D-07 | `data/processed/` fuera del control de versiones, con dimensiones y hash publicados | Versionar los derivados (68,16 y 69,17 MB) | Los archivos procesados se pueden volver a generar desde el original. Guardarlos también en Git habría duplicado gran parte del peso del repositorio y dificultado su descarga y revisión |

## 3. Unidad de análisis y limpieza

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-08 | La fila es una oferta por ítem: no se deduplica por `NroLicitacion` | `drop_duplicates(subset='NroLicitacion')` · agregar a nivel de licitación | Una licitación puede tener varios ítems y recibir distintas ofertas. Si dejábamos una sola fila por licitación, se perdía gran parte de la información necesaria para responder la pregunta del proyecto |
| D-09 | Exclusión nominal de las 3 columnas 100 % vacías, con comprobación previa | `dropna(axis=1, how='all')` · umbral por porcentaje | Preferimos indicar de forma expresa cuáles columnas se eliminan para que la decisión sea visible y revisable. Una regla automática podría borrar otras columnas si el archivo cambia, incluso cuando todavía contengan información útil |
| D-10 | Conservar las 7 columnas constantes, incluida `Sector` | Eliminar toda columna sin varianza | Aunque `Sector` tiene el mismo valor en todas las filas, confirma que los datos corresponden efectivamente al sector Salud. Por eso consideramos que seguía siendo útil como parte del contexto del dataset |
| D-11 | Los 7.613 valores de 1900 en `FechaEstimadaEvaluacionOfertas` pasan a `NaT`; las 44.226 filas se conservan | Eliminar las filas · imputar una fecha plausible · dejar el año 1900 | El año 1900 claramente no representaba una fecha real. Eliminar esas filas habría significado perder muchos registros, y reemplazarlas por una fecha inventada habría agregado información que no conocemos |
| D-12 | `errors='coerce'` con guardia que lanza `ValueError` si una fecha con valor queda nula | `coerce` sin comprobación · `errors='raise'` directo | Queríamos que una fecha incorrecta fuera visible y no desapareciera silenciosamente durante la conversión. La comprobación adicional permite saber en qué columna está el problema y cuántos registros deben revisarse |
| D-13 | Normalización de texto limitada a `str.strip()` | Añadir `.lower()` · transliterar acentos · mapear a códigos (LE, LP, LR, L1) | Los datos no mostraron diferencias relevantes de mayúsculas o acentos que justificaran cambios mayores. Limpiar solo los espacios evita modificar innecesariamente los nombres originales de las categorías |
| D-14 | `NoClasificado` (3.410 ofertas) se preserva como quinta categoría | Imputar por la moda · eliminar las filas · convertir a `NaN` · agrupar con `Micro` | `NoClasificado` representa una situación real del archivo y no sabemos a qué tamaño pertenece cada proveedor. Asignarlo a otra categoría o eliminarlo podía cambiar injustificadamente las comparaciones del estudio |
| D-15 | Los NA parciales (22 columnas) no se imputan; se cuantifican y documentan | Imputación por media/moda · eliminar columnas con >50 % de nulos · imputación por modelo | Las columnas necesarias para el análisis principal estaban completas. Por eso no era necesario inventar valores ni eliminar información de otras variables que podrían resultar útiles más adelante |
| D-16 | `plazo_cierre_dias` se calcula solo con `FechaPublicacion` y `FechaCierre` | Incluir `FechaAdjudicacion` · redondear a días enteros | Publicación y cierre estaban disponibles para todos los registros y describían directamente el plazo que queríamos medir. Otras fechas tenían datos faltantes, y redondear habría eliminado las diferencias de horas presentes en el archivo |
| D-17 | No se escalan ni normalizan las variables numéricas | `StandardScaler` / `MinMaxScaler` preventivo | En esta etapa no estamos entrenando un modelo que necesite variables en una escala común. Mantener el plazo expresado en días hace que el resultado sea más fácil de entender y explicar |

## 4. Cálculo de las proporciones

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-18 | El cálculo se restringe a `EstadoLicitacion == "Adjudicada"` | Usar las 44.226 filas sin filtrar · excluir solo los procesos desiertos | En una licitación desierta o revocada no puede existir una oferta ganadora. Incluir esos casos habría reducido los porcentajes de manera artificial, aunque solo se excluyeron 201 filas |
| D-19 | Denominador propio por grupo, con la categoría residual informada aparte | Denominador común global · publicar solo porcentajes | Cada tamaño de proveedor y tipo de licitación tiene una cantidad distinta de ofertas. Calcular el porcentaje dentro de cada grupo permite compararlos de forma más justa y mostrar también cuántos casos respaldan cada resultado |
| D-20 | Los montos quedan fuera del análisis principal | Sumar o promediar montos · convertir a moneda común | El archivo contiene montos en cuatro monedas diferentes. Sumarlos directamente no tendría sentido y convertirlos requeriría elegir tipos de cambio y fechas que no forman parte del alcance definido para este trabajo |

## 5. Codificación de variables nominales

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-21 | One-hot encoding con prefijo `oh_<columna>__`: 12 indicadores, de 74 a 86 columnas | Label/ordinal encoding · ordinal solo para `TamanoProveedor` · target encoding · frequency encoding | Asignar números a las categorías podía dar la impresión de que unas eran mayores o mejores que otras. La codificación elegida representa cada categoría por separado y respeta casos como `NoClasificado`, que no tienen una posición natural |
| D-22 | Se conservan todas las categorías, sin eliminar una de referencia | `drop_first=True` | Todavía no se ha definido un modelo que necesite una categoría de referencia. Mantenerlas todas facilita comprobar que cada registro pertenece exactamente a una categoría y hace el resultado más transparente |
| D-23 | Indicadores `int8` exportados en archivo independiente de 86 columnas | `dtype=bool` · `int64` por omisión · reemplazar el dataset procesado | Los valores 0 y 1 son claros para revisar y ocupan poco espacio con el tipo elegido. Además, guardar la versión codificada por separado evita reemplazar el dataset procesado que ya estaba documentado en el informe |

## 6. Arquitectura del código

| ID | Decisión adoptada | Alternativas descartadas | Motivo del descarte |
| --- | --- | --- | --- |
| D-24 (F2, superada en F3) | 16 funciones en `src/proyecto.py` que devuelven copias; los notebooks configuran, invocan y presentan | Clase con estado · mantener el código en los notebooks · `inplace=True` | En F2 las funciones eran suficientes porque el objetivo principal era limpiar y validar los datos. Esta decisión se mantiene como parte de la historia del proyecto, pero en F3 el profesor solicitó avanzar hacia una organización basada en clases |
| D-25 | Incorporar `ContratoEsquema`, lectores polimórficos, un limpiador con estado encapsulado y un validador compuesto por reglas, conservando las funciones de F1/F2 como adaptadores | Reescribir los notebooks anteriores · crear una clase monolítica para todo el pipeline · eliminar inmediatamente las funciones públicas | Reescribir lo ya entregado podía introducir errores y hacer que F1 y F2 dejaran de funcionar. Mantener las funciones anteriores permite avanzar gradualmente, mientras que separar las tareas en distintas clases hace más claro qué parte lee, cuál limpia y cuál revisa los datos |

---

Repositorio: <https://github.com/vbravo29/sumativo-1> · Las decisiones aquí registradas se
implementan en `src/proyecto.py` y se documentan en el informe técnico, sección IV.B.
