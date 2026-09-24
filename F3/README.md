# Fase 3: núcleo algorítmico y POO

## Primer incremento: reorganización del pipeline F2

La retroalimentación docente propuso trasladar las funciones extensas de
`src/proyecto.py` a objetos con responsabilidades delimitadas. El primer incremento
implementa esa mejora sin romper los notebooks de F1 y F2:

- `ContratoEsquema`: contrato inmutable para las columnas mínimas de una fuente.
- `LectorDatos`: interfaz abstracta de lectura.
- `LectorCSV`: implementación concreta que lee y valida el contrato.
- `LimpiadorLicitaciones`: coordina el pipeline y encapsula un resumen de su última
  ejecución; no modifica el DataFrame recibido.
- `ReglaValidacion`: interfaz abstracta para reglas de calidad intercambiables.
- `ValidadorDatasetProcesado`: aplica una colección de reglas polimórficas.

Las funciones `leer_datos_f1`, `limpiar_datos_f2` y
`validar_dataset_procesado` permanecen como adaptadores compatibles. Por ello, este
incremento mejora cohesión, encapsulamiento y extensibilidad, pero conserva la interfaz
utilizada por los entregables anteriores.

## Verificación

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -m unittest F3.test_nucleo_poo -v
```

Las pruebas cubren lectura normal, esquema incompleto, inmutabilidad de la entrada,
estado del limpiador, compatibilidad de los adaptadores, extensión polimórfica del
validador y detección de un plazo incoherente.


## Organización por archivos

Las clases de lectura y el contrato están en `src/datos.py`; el limpiador y su adaptador, en `src/pipeline.py`; las reglas y el validador, en `src/validacion.py`. Las transformaciones auxiliares residen en `src/preprocesamiento.py`. `src/proyecto.py` conserva el acceso compatible a todas las clases y funciones.

El 24 de septiembre se verificó la separación: seis pruebas POO aprobadas, ejecución completa de F1 y F2 en kernels nuevos y coincidencia SHA-256 de los dos CSV generados en una carpeta temporal con los existentes. Los notebooks y sus evidencias JSON anteriores no se reescribieron.

Este incremento todavía no incluye un notebook F3, benchmarks de tiempo y memoria ni una implementación recursiva. En la revisión se detectó además que `ValidadorDatasetProcesado([])` utiliza las reglas predeterminadas en vez de rechazar la lista vacía; se conserva el comportamiento del aporte original y queda pendiente su corrección con una prueba específica.
