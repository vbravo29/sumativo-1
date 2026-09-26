# Fase 3 — Algoritmos y programación orientada a objetos

Esta fase compara algoritmos para calcular la proporción de ofertas ganadoras por tamaño de proveedor y tipo de licitación. Utiliza el dataset de F2 y una estructura de clases para la lectura, limpieza y validación de los datos.

El análisis considera ofertas de procesos adjudicados. Cada fila representa una oferta por ítem; los porcentajes se calculan sobre las ofertas con resultado válido de cada grupo.

## Archivos

| Archivo | Contenido |
| --- | --- |
| [F3_Algoritmos.ipynb](F3_Algoritmos.ipynb) | Desarrollo del análisis, ejemplos, pruebas, mediciones y conclusiones. |
| [test_algoritmos.py](test_algoritmos.py) | Pruebas de equivalencia entre algoritmos y casos límite. |
| [test_nucleo_poo.py](test_nucleo_poo.py) | Pruebas de lectura, limpieza y validación mediante clases. |
| [medir_algoritmos.py](medir_algoritmos.py) | Comparación de tiempos de ejecución y memoria. |
| [verificar_algoritmos.py](verificar_algoritmos.py) | Ejecución del notebook en un kernel nuevo y registro del resultado. |
| `fixtures/` | Archivos de ejemplo utilizados en las pruebas de lectura. |

## Organización del código

La implementación se encuentra en `src/`:

| Módulo | Responsabilidad |
| --- | --- |
| [datos.py](../src/datos.py) | Contrato de esquema, lector abstracto, lector CSV, exportación y huellas SHA-256. |
| [preprocesamiento.py](../src/preprocesamiento.py) | Transformación de fechas, categorías y variables derivadas. |
| [pipeline.py](../src/pipeline.py) | Coordinación de la limpieza y registro de su última ejecución. |
| [validacion.py](../src/validacion.py) | Reglas de calidad y validación del dataset. |
| [analisis.py](../src/analisis.py) | Exploración, frecuencias y cálculo de proporciones. |

`LectorCSV` implementa la interfaz de `LectorDatos`. `LimpiadorLicitaciones` conserva un resumen de la limpieza sin modificar el DataFrame de entrada. `ValidadorDatasetProcesado` aplica reglas que comparten la interfaz `ReglaValidacion`.

Los notebooks de F1 y F2 mantienen sus importaciones desde `src/proyecto.py`. Las nuevas alternativas de cálculo se importan desde `src/analisis.py`.

## Ejecución

Se requiere el entorno Python del proyecto, las dependencias de [requirements.txt](../requirements.txt) y el archivo `data/raw/licitaciones_salud_marzo_2026.csv`. La configuración del entorno está descrita en el [README principal](../README.md#preparación-del-entorno).

Ejecutar los siguientes comandos desde la raíz del repositorio, en este orden:

```powershell
# Pruebas de algoritmos y clases
.\.venv\Scripts\python.exe -m unittest F3.test_algoritmos F3.test_nucleo_poo -v

# Mediciones de tiempo y memoria
.\.venv\Scripts\python.exe F3\medir_algoritmos.py

# Ejecución y guardado del notebook
.\.venv\Scripts\python.exe F3\verificar_algoritmos.py
```

Las mediciones se guardan en `evidencias/F3_algoritmos/`: `resumen.csv` contiene las estadísticas y `mediciones.json` incluye las observaciones individuales, los parámetros, las versiones y las huellas de los archivos utilizados.

El verificador guarda las salidas del notebook y genera `evidencias/F3_algoritmos_ejecucion.json`. El notebook comprueba que las mediciones correspondan al dataset y al código actuales. Si cambia `src/analisis.py` o `F3/medir_algoritmos.py`, es necesario repetir las mediciones. También pueden regenerarse desde el notebook con `REGENERAR_MEDICIONES = True`.

## Comparación de algoritmos

Se comparan cuatro implementaciones:

- **Referencia F2:** cálculo original mediante filtros y agrupaciones.
- **Iterativa:** acumulación de conteos por grupo en un diccionario.
- **Recursiva:** división de registros en bloques y combinación de conteos parciales.
- **Agrupada:** cálculo mediante una agrupación por categoría y resultado.

Las pruebas comprueban que las alternativas producen los mismos resultados. La comparación de rendimiento utiliza distintos tamaños de entrada e incluye el filtrado, las conversiones, el conteo y la construcción de la tabla. La lectura del CSV y la limpieza se realizan antes de medir.

En las mediciones guardadas, la variante agrupada obtuvo la menor mediana de tiempo para el dataset completo en ambas variables. Se utiliza en el análisis de F3; la función de F2 conserva su implementación. La interpretación de los tiempos, la complejidad y los límites de la comparación se desarrolla en el notebook.

La memoria se mide por separado con `tracemalloc`. El pico registrado corresponde a las asignaciones rastreadas durante el cálculo, no a la memoria total del proceso.

## Validación y documentación

La ejecución registrada comprende 14 pruebas aprobadas y 24 celdas de código ejecutadas sin errores. El notebook presenta por separado la preparación de datos, los casos de prueba, las proporciones, los tiempos y la memoria, con las explicaciones correspondientes a cada resultado.

- [Decisiones técnicas](../docs/DECISIONES_TECNICAS.md): criterios de implementación y alternativas evaluadas.
- [Análisis de algoritmos](../docs/F3_APORTE_ALGORITMOS.md): sección técnica preparada para el informe.
- [Evidencias de rendimiento](../evidencias/F3_algoritmos/): resultados reproducibles del experimento.

## Pendientes

- Corregir el tratamiento de una lista de reglas vacía en `ValidadorDatasetProcesado`: actualmente activa las reglas predeterminadas.
- Integrar las mediciones de lectura y las actualizaciones de validación.
- Completar el informe grupal y su bibliografía.
