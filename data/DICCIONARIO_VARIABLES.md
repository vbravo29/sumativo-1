# Diccionario de variables

Este documento describe las 74 columnas del archivo `licitaciones_salud_marzo_2026.csv`, que contiene 44.226 registros. Su propósito es facilitar la lectura de los datos y dejar claras las decisiones que habrá que tomar durante la preparación de F2.

La pregunta del proyecto se centra en **TipoLicitacion**, **TamanoProveedor** y **ResultadoOferta**. Las demás variables permiten identificar los procesos, revisar su contexto y comprobar la calidad de la información.

## Criterios de lectura

Cada fila se interpreta como una oferta asociada a un ítem. Una licitación puede aparecer varias veces, por lo que `NroLicitacion` no identifica una fila única. La clave de cada observación aún debe revisarse.

Las descripciones se basan en los nombres de las columnas, sus valores y la documentación de ChileCompra. El diccionario de la API ayuda a explicar varios conceptos, pero no describe exactamente este reporte. Las dudas concretas se indican al final; las descripciones restantes son interpretaciones de trabajo, no una transcripción de un diccionario oficial.

En las tablas, **tipo** corresponde a la lectura de pandas y **rol** al uso analítico de la variable. Por ejemplo, un código puede estar guardado como número y seguir siendo un identificador. Los faltantes se calcularon con `isna()`; los valores distintos excluyen esos faltantes. Espacios y etiquetas como `NoClasificado` requieren una revisión aparte.

## Variables del archivo

Las columnas mantienen el orden del CSV y se agrupan por tema. Las fechas todavía están almacenadas como texto. Su conversión y las demás transformaciones corresponden a F2.

### Licitación y presupuesto

| Variable | Descripción | Tipo | Rol | Faltantes | % | Distintos |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `NroLicitacion` | Identificador del proceso de licitación | `str` | identificador | 0 | 0,00 | 1.864 |
| `NombreLicitacion` | Nombre del proceso de compra | `str` | texto | 0 | 0,00 | 1.860 |
| `TipoLicitacion` | Tipo de licitación | `str` | nominal | 0 | 0,00 | 7 |
| `Descripcion` | Descripción del objeto de la licitación | `str` | texto | 0 | 0,00 | 1.651 |
| `MonedaLicitacion` | Moneda del monto de la licitación | `str` | nominal | 0 | 0,00 | 4 |
| `MontoEstimadoLicitacion` | Monto estimado del proceso | `float64` | continua | 0 | 0,00 | 1.670 |
| `MontoEstimadoVisible` | Indicador de visibilidad del monto estimado | `str` | binaria | 0 | 0,00 | 2 |
| `BaseEstimacionMontoLicitacion` | Criterio declarado para estimar el monto | `str` | nominal | 323 | 0,73 | 2 |
| `FuenteFinanciamiento` | Fuente de financiamiento declarada | `str` | texto | 19.168 | 43,34 | 365 |
| `JustificacionMontoEstimado` | Texto que justifica la estimación del monto | `str` | texto | 31.911 | 72,15 | 242 |

### Fechas del proceso

| Variable | Descripción | Tipo | Rol | Faltantes | % | Distintos |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `FechaPublicacion` | Fecha y hora de publicación | `str` | temporal | 0 | 0,00 | 1.830 |
| `FechaInicioPreguntas` | Inicio del período de consultas | `str` | temporal | 0 | 0,00 | 1.275 |
| `FechaFinalPreguntas` | Fin del período de consultas | `str` | temporal | 0 | 0,00 | 818 |
| `FechaPublicacionRespuestas` | Publicación de respuestas a consultas | `str` | temporal | 0 | 0,00 | 730 |
| `FechaActoAperturaTecnica` | Fecha del acto de apertura técnica | `str` | temporal | 0 | 0,00 | 735 |
| `FechaActoAperturaEconomica` | Fecha del acto de apertura económica | `str` | temporal | 0 | 0,00 | 737 |
| `FechaCierre` | Cierre de recepción de ofertas registrado | `str` | temporal | 0 | 0,00 | 548 |
| `FechaAdjudicacion` | Fecha de adjudicación registrada | `str` | temporal | 48 | 0,11 | 1.862 |
| `FechaEntregaEnSoporteFisico` | Fecha asociada a entrega de antecedentes físicos | `str` | temporal | 42.193 | 95,40 | 18 |
| `FechaEstimadaEvaluacionOfertas` | Campo asociado al tiempo o fecha estimada de evaluación; significado por confirmar | `str` | temporal por confirmar | 36.613 | 82,79 | 17 |

### Evaluación, adjudicación y condiciones

| Variable | Descripción | Tipo | Rol | Faltantes | % | Distintos |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `UnidadTiempoEvaluacion` | Unidad de tiempo asociada a la evaluación | `str` | nominal | 290 | 0,66 | 3 |
| `EstadoLicitacion` | Estado administrativo del proceso | `str` | nominal | 0 | 0,00 | 4 |
| `ContemplaObrasPublicas` | Indicador de obras públicas en la licitación | `str` | binaria | 4.527 | 10,24 | 2 |
| `LicitacionInformada` | Indicador denominado licitación informada; alcance por confirmar | `str` | binaria | 0 | 0,00 | 1 |
| `LicitacionBaseTipo` | Campo asociado a bases tipo; significado exacto por confirmar | `float64` | por confirmar | 44.226 | 100,00 | 0 |
| `TipoAdjudicacion` | Modalidad de adjudicación registrada | `str` | nominal | 0 | 0,00 | 1 |
| `TipoAprobacionAdjudicacion` | Tipo de documento o mecanismo de aprobación | `str` | nominal | 0 | 0,00 | 4 |
| `NumeroActaAprobacion` | Identificador del acta o documento de aprobación | `str` | identificador | 0 | 0,00 | 1.567 |
| `FechaActaAprobacion` | Fecha del documento de aprobación | `str` | temporal | 0 | 0,00 | 121 |
| `TipoConvocatoria` | Convocatoria abierta o cerrada | `str` | nominal | 0 | 0,00 | 2 |
| `NroEtapasLicitacion` | Número de etapas expresado en etiquetas | `str` | discreta | 0 | 0,00 | 2 |
| `SubContratacion` | Indicador de permiso de subcontratación, según el concepto documentado en la API; correspondencia del CSV por confirmar | `str` | binaria | 0 | 0,00 | 2 |
| `ProhibicionSubContratacion` | Texto de condiciones o restricciones de subcontratación | `str` | texto | 33.844 | 76,53 | 278 |
| `TomaRazonContraloria` | Indicador asociado a toma de razón | `str` | binaria | 1.892 | 4,28 | 2 |
| `PublicidadOfertasTecnicas` | Indicador de publicidad de las ofertas técnicas | `str` | binaria | 1.892 | 4,28 | 2 |
| `RazonPublicidadOfertasTecnicas` | Justificación de publicidad de ofertas técnicas | `str` | texto | 41.568 | 93,99 | 5 |
| `Contrato` | Categoría de formalización contractual | `str` | nominal | 1.892 | 4,28 | 3 |

### Duración y condiciones del contrato

| Variable | Descripción | Tipo | Rol | Faltantes | % | Distintos |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `TiempoDuracionContrato` | Valor de duración del contrato asociado a su unidad | `int64` | discreta | 0 | 0,00 | 40 |
| `UnidadTiempoDuracionContrato` | Unidad de la duración contractual | `str` | nominal | 2.757 | 6,23 | 4 |
| `ContratoRenovable` | Campo sobre renovación contractual; sin valores para contrastar | `float64` | binaria por confirmar | 44.226 | 100,00 | 0 |
| `ValorTiempoRenovacion` | Valor asociado al plazo de renovación | `int64` | discreta | 0 | 0,00 | 1 |
| `UnidadTiempoRenovacion` | Unidad del plazo de renovación; sin valores para contrastar | `float64` | nominal por confirmar | 44.226 | 100,00 | 0 |
| `FechaEstimadaFirmaContrato` | Fecha estimada de firma del contrato | `str` | temporal | 41.857 | 94,64 | 60 |
| `TipoEjecucion` | Modalidad temporal de ejecución contractual | `str` | nominal | 2.757 | 6,23 | 2 |
| `PlazoPagoContrato` | Categoría del plazo de pago contractual | `str` | nominal | 2.757 | 6,23 | 3 |
| `TipoPago` | Medio o combinación de medios de pago | `str` | nominal | 4.527 | 10,24 | 3 |
| `ObservacionContrato` | Observaciones textuales del contrato | `str` | texto | 35.685 | 80,69 | 194 |
| `ExtensionPlazo` | Indicador de extensión del cierre de recepción de ofertas, según el concepto de la API; correspondencia del CSV por confirmar | `str` | binaria | 1.892 | 4,28 | 2 |

### Organismo comprador

| Variable | Descripción | Tipo | Rol | Faltantes | % | Distintos |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `UnidadCompra` | Nombre de la unidad compradora | `str` | nominal | 0 | 0,00 | 215 |
| `UnidadCompraRUT` | RUT registrado para la unidad compradora | `str` | identificador | 0 | 0,00 | 204 |
| `entCode` | Código de entidad; equivalencia exacta por confirmar | `int64` | identificador | 0 | 0,00 | 189 |
| `Institucion` | Nombre de la institución compradora | `str` | nominal | 0 | 0,00 | 187 |
| `Sector` | Sector institucional registrado | `str` | nominal | 0 | 0,00 | 1 |

### Productos e ítems

| Variable | Descripción | Tipo | Rol | Faltantes | % | Distintos |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `RubroN1` | Clasificación de rubro de primer nivel | `str` | nominal | 0 | 0,00 | 52 |
| `RubroN2` | Clasificación de rubro de segundo nivel | `str` | nominal | 0 | 0,00 | 222 |
| `RubroN3` | Clasificación de rubro de tercer nivel | `str` | nominal | 0 | 0,00 | 772 |
| `CodigoProductoONU` | Código de clasificación de producto o servicio | `int64` | identificador categórico | 0 | 0,00 | 2.104 |
| `ONUProducto` | Denominación del producto en la clasificación | `str` | nominal | 0 | 0,00 | 2.099 |
| `NombreItem` | Nombre registrado del ítem | `str` | texto | 0 | 0,00 | 2.099 |
| `DescripcionItem` | Descripción del bien o servicio solicitado | `str` | texto | 12 | 0,03 | 11.965 |
| `UnidadMedida` | Unidad de medida del ítem | `str` | nominal | 0 | 0,00 | 56 |
| `CantidadItem` | Cantidad registrada para el ítem | `float64` | cuantitativa | 0 | 0,00 | 988 |

### Proveedores y ofertas

| Variable | Descripción | Tipo | Rol | Faltantes | % | Distintos |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `Proveedor` | Nombre del proveedor | `str` | nominal | 0 | 0,00 | 2.374 |
| `ProveedorRUT` | RUT del proveedor | `str` | identificador | 0 | 0,00 | 2.376 |
| `ActividadProveedor` | Actividad declarada por el proveedor | `str` | texto | 6.236 | 14,10 | 1.188 |
| `TamanoProveedor` | Tamaño del proveedor según la categoría del archivo | `str` | nominal | 0 | 0,00 | 5 |
| `NombreOferta` | Nombre de la oferta presentada | `str` | texto | 0 | 0,00 | 5.151 |
| `EspecificacionesProveedor` | Descripción técnica o condiciones ofertadas | `str` | texto | 0 | 0,00 | 32.740 |
| `EstadoOferta` | Estado de aceptación o rechazo de la oferta | `str` | nominal | 0 | 0,00 | 2 |
| `CantidadOferta` | Cantidad registrada en la oferta | `float64` | cuantitativa | 0 | 0,00 | 988 |
| `MonedaOferta` | Moneda asociada a los montos de oferta | `str` | nominal | 0 | 0,00 | 4 |
| `MontoNetoOferta` | Monto denominado neto en la oferta; base de cálculo por confirmar | `float64` | continua | 0 | 0,00 | 13.228 |
| `MontoTotalOferta` | Monto denominado total en la oferta; composición por confirmar | `float64` | continua | 0 | 0,00 | 20.277 |
| `ResultadoOferta` | Etiqueta de resultado ganadora o perdedora | `str` | binaria | 0 | 0,00 | 2 |

## Observaciones para preparar los datos

### Cobertura del reporte

Aunque el archivo corresponde al reporte de marzo de 2026, las fechas de publicación van del **15 de enero al 25 de marzo**. Las fechas de cierre sí están entre el **2 y el 31 de marzo**. Por eso se habla de reporte de marzo y no de licitaciones publicadas exclusivamente durante ese mes. Falta confirmar el criterio de selección mensual utilizado por ChileCompra.

`Sector` solo contiene el valor `SALUD`. También hay columnas constantes, como `LicitacionInformada`, `TipoAdjudicacion` y `ValorTiempoRenovacion`; conviene evaluar su utilidad antes del análisis. `LicitacionBaseTipo`, `ContratoRenovable` y `UnidadTiempoRenovacion` están completamente vacías. Si se excluyen en F2, se registrará el motivo.

### Tamaño del proveedor y resultado de la oferta

`TamanoProveedor` contiene Grande, Mediana, Pequeña, Micro y NoClasificado. Esta última categoría aparece en **3.410 filas** y se mantendrá separada. El SII publica tamaños de empresa basados en ventas, pero no se encontró una especificación que confirme el año o las reglas utilizadas en este CSV. No se asignarán rangos de ventas ni un orden numérico a las categorías sin esa información.

`EstadoOferta` distingue aceptación y rechazo; `ResultadoOferta` distingue Ganadora y Perdedora. Además, hay que considerar `EstadoLicitacion`: una licitación cerrada no necesariamente está adjudicada. En el archivo se observaron:

| Estado del proceso | Registros que requieren revisión |
| --- | --- |
| Cerrada | 56 ofertas: una Ganadora y 55 Perdedora |
| Desierta | 138 ofertas |
| Revocada | 7 ofertas |

Estas etiquetas deben revisarse antes de interpretar las ofertas como pérdidas definitivas. La proporción de ganadoras se calculará sobre resultados válidos y se mostrará junto al número de ofertas de cada grupo. Un grupo sin resultados válidos no tendrá una proporción calculada.

### Montos y cantidades

En las **44.226 filas**, `MontoTotalOferta` coincide con `MontoNetoOferta × CantidadOferta`, con tolerancia relativa de 1e-8 y absoluta de 0,01. Esto sugiere que el neto es un importe por unidad y el total corresponde a la línea, pero la comprobación no aclara el tratamiento de impuestos ni las ofertas con condiciones especiales. Ambos campos quedan fuera de la comparación principal mientras se resuelve esa duda; tampoco representan necesariamente pagos realizados.

Los montos deben leerse junto a su moneda. El presupuesto de una licitación puede repetirse en varias ofertas, así que sumar `MontoEstimadoLicitacion` por fila produciría duplicaciones. Su interpretación también depende de `MontoEstimadoVisible`. Las cantidades deben revisarse con `UnidadMedida`; no se supondrá que todas son enteras ni que `CantidadItem` y `CantidadOferta` representan lo mismo.

### Fechas y condiciones del contrato

Los **7.613 valores presentes** en `FechaEstimadaEvaluacionOfertas` pertenecen al año **1900**; los otros 36.613 están vacíos. No se encontró una explicación de esa codificación. Hasta aclararla, el campo no se usará como fecha real ni se convertirá en duración. Las otras fechas se revisarán por formato y coherencia cronológica antes de calcular plazos.

La documentación de la API relaciona `TiempoDuracionContrato` con su unidad, describe `SubContratacion` como permiso para subcontratar y vincula `ExtensionPlazo` con la extensión del cierre de ofertas. Estas referencias orientan la lectura, aunque falta confirmar su equivalencia exacta con el reporte. No se usará `ExtensionPlazo` como una prórroga general del contrato ni se asumirán reglas legales vigentes a partir de la documentación histórica. `Contrato` tiene tres categorías y no debe convertirse directamente en un campo de sí/no; `NroEtapasLicitacion` contiene Una etapa y Dos etapas y puede convertirse con una correspondencia explícita.

### Identificadores y textos

Los RUT, números de acta y códigos de entidad o producto permiten identificar y relacionar registros. Se conservarán como identificadores, aunque pandas haya leído algunos como enteros. En particular, falta confirmar a qué nivel de la organización corresponde `entCode`. `CodigoProductoONU` no se utilizará como una medida numérica.

Los nombres y las descripciones se conservarán para interpretar los registros. En F2 se revisarán diferencias de escritura, categorías y valores vacíos, sin reemplazarlos automáticamente. Los cambios que se apliquen quedarán documentados en el notebook.

## Fuentes consultadas y alcance de la revisión

El portal oficial confirma que el reporte de licitaciones incorpora ofertas y muestra campos como `NroLicitacion`, `MontoTotalOferta` y `ResultadoOferta`. La sección de definiciones explica los estados del proceso. El diccionario de la API respalda el significado general de fechas de publicación y adjudicación, unidades de tiempo y algunas condiciones contractuales; no resuelve todas las columnas del archivo descargado.

Quedan por confirmar el criterio y año de clasificación del proveedor, el tratamiento de impuestos en los montos, las fechas de evaluación de 1900, la selección mensual y la construcción de `ResultadoOferta`. La consulta puede dirigirse al correo de datos abiertos publicado en el portal: datosabiertos@chilecompra.cl.

- ChileCompra. (s. f.). *Descargas*. https://datos-abiertos.chilecompra.cl/descargas
- ChileCompra. (s. f.). *Definiciones*. https://datos-abiertos.chilecompra.cl/datos-abiertos/definiciones
- ChileCompra. (s. f.). *Diccionario de datos: Licitaciones* (pp. 4–5). https://www.chilecompra.cl/wp-content/uploads/2026/03/Documentacion-API-Mercado-Publico-Licitaciones.pdf
- Servicio de Impuestos Internos. (s. f.). *Estadísticas de empresa*. https://www.sii.cl/sobre_el_sii/estadisticas_de_empresas.html

Estas referencias apoyan la lectura de los datos. Las fuentes docentes y la referencia académica del informe se incorporarán por separado.

## Archivo utilizado

El CSV original se conserva en `data/raw/licitaciones_salud_marzo_2026.csv`. Se leyó con pandas 3.0.1, separador `;`, codificación `latin-1` y `low_memory=False`. Aunque el portal anuncia UTF-8, esta copia no supera la lectura UTF-8 estricta. Los recuentos corresponden al archivo original, sin limpieza ni transformaciones.

SHA-256: `490d9209a10d387011d481b72b7891f26e997974ec2cf9dfc518aa4a08552232`.
