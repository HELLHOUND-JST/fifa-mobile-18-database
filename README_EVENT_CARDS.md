# Cartas de eventos — FIFA Mobile 18 (V4.0.0)

La V4.0.0 incorpora una colección independiente de cartas de eventos de FIFA Mobile 18 — Season 2. Incluye datos de cartas, atributos y *skill boosts*, imágenes individuales de jugadores, cartas completas, iconos de programas y recursos gráficos adicionales.

## Resumen de la colección

| Recurso | Cantidad / detalle |
|---|---:|
| Registros de la base de eventos | **6.571 filas** |
| Catálogo de refuerzos de habilidad | **37 nombres** |
| Cartas completas de eventos | **6.483 PNG** |
| PNG individuales de jugadores de eventos | **6.570 PNG** |
| Iconos/logotipos de programas | **92** |
| Dimensiones de cartas completas | **256 × 256 píxeles** |
| Variante de PNG individual documentada | **Action Shot únicamente** |

Las cantidades corresponden a recursos diferentes. No debe suponerse que cada fila tenga necesariamente una carta completa, un PNG individual y un icono asociado.

## Archivos de datos

La base de eventos se distribuye en tres formatos:

- `fifa_mobile_18_eventos.csv`
- `fifa_mobile_18_eventos.json`
- `fifa_mobile_18_eventos.txt`

La copia documentada contiene **6.571 filas**. Cada registro incluye el campo `SKILL_BOOST` y **30 estadísticas**. Por separado, el proyecto define un catálogo de **37 nombres de refuerzos de habilidad** (`skill_boosts`). Los 37 nombres son etiquetas de refuerzo, no estadísticas adicionales. Consulta los encabezados del CSV o las claves del JSON para conocer los nombres y tipos exactos de los 30 campos estadísticos.

## Catálogo de 37 refuerzos de habilidad

La lista `skill_boosts` proporcionada para el proyecto contiene **37 nombres**. Se conserva la escritura exacta del listado recibido, incluidos los términos `aggresion` y `long shoots`; no se han traducido ni normalizado.

- `composed`
- `counter`
- `gk diving`
- `captain`
- `generalist`
- `aggresion`
- `shooting`
- `acceleration`
- `physical`
- `holding`
- `passing`
- `defending`
- `strength`
- `awareness`
- `long passing`
- `tackling`
- `short passing`
- `marking`
- `speed`
- `ball control`
- `set pieces`
- `balanced`
- `reactions`
- `crossing`
- `long shoots`
- `handling`
- `pace`
- `dribbling`
- `positioning`
- `heading`
- `shot power`
- `agility`
- `finishing`
- `gk positioning`
- `reflexes`
- `gk generalist`
- `second striker`

Estos 37 elementos representan nombres de *skill boosts*. No deben sumarse a las 30 estadísticas de la base de eventos ni interpretarse como 37 atributos numéricos. El campo `SKILL_BOOST` de cada registro debe leerse según el valor almacenado en la exportación correspondiente.

## Recursos gráficos de eventos

### Cartas completas: `events_cards/`

- **6.483 cartas completas**.
- Formato PNG.
- Resolución **256 × 256 píxeles**.
- Corresponden a composiciones completas de cartas de eventos.

### Imágenes individuales de jugadores: `events_png/`

- **6.570 PNG** de jugadores asociados a cartas de eventos.
- La colección contiene únicamente la variante **Action Shot**.
- Estas imágenes individuales no son las composiciones completas de las cartas.

### Iconos y logotipos de programas: `events_logos/`

- **92 iconos/logotipos** de programas.
- No se encontraron en el CDN los recursos identificados como `17_FAV` y `17_SBC_PLAYER`; por esa razón no aparecen entre los 92 recursos disponibles.

## Manifiestos

La colección incluye:

- `events_manifest.csv`
- `events_manifest.json`

Utiliza los manifiestos para revisar los registros de recursos y las relaciones que contienen. Los nombres de columnas y claves deben tomarse de los propios archivos, ya que el resumen de subida no enumera su esquema.

## Recursos compartidos y adicionales

La V4.0.0 añade recursos para componer o identificar cartas de eventos:

- **931 recursos nuevos** en `assets_cards/backgrounds/`, incluidos fondos de World Cup y de eventos.
- **47 recursos nuevos** en `assets_cards/clubs/`.
- `data/cache_eventos.jsonl`: caché de trabajo de la colección de eventos.
- `_guide_by_fifa_id.py`: utilidad auxiliar relacionada con la consulta por FIFA ID.

Los fondos, escudos e iconos se mantienen en carpetas de recursos compartidas del proyecto. No se debe asumir que todos los recursos de esas carpetas pertenecen exclusivamente a la colección de eventos.

## Herramientas incluidas

La actualización incorpora estos scripts:

| Script | Función indicada por el nombre y el resumen de actualización |
|---|---|
| `extract_eventos_fifa18.py` | Extracción de datos de cartas de eventos. |
| `generate_events_assets.py` | Generación/preparación de recursos gráficos de eventos. |
| `generate_skill_boost.py` | Generación de información relacionada con *skill boosts*. |
| `reconcile_guide.py` | Conciliación de datos o referencias de guía. |
| `inspect_event_assets.py` | Inspección de recursos gráficos de eventos. |
| `_guide_by_fifa_id.py` | Utilidad auxiliar de consulta por FIFA ID. |

Para conocer argumentos, opciones y requisitos precisos, consulta la ayuda (`--help`) y el código de cada script. No se infieren aquí parámetros que no fueron incluidos en el registro de actualización.

## Relación con las cartas base

Las cartas base y las cartas de eventos son conjuntos separados:

| Colección | Datos y recursos |
|---|---|
| Cartas base | Base de cartas base, *skill boosts*, estadísticas revisadas, PNG individuales de jugadores y cartas completas. |
| Cartas de eventos | `fifa_mobile_18_eventos.*`, PNG individuales Action Shot, cartas completas, logos de programas y recursos adicionales de clubes/fondos. |

No asumas que ambas colecciones comparten identificadores, campos, reglas de rareza, esquemas JSON, manifiestos o estructuras de carpetas.

## Uso desde otros proyectos

1. Lee `fifa_mobile_18_eventos.csv` o `.json` para consultar los registros de eventos.
2. Usa `events_manifest.csv` o `events_manifest.json` para inspeccionar los recursos gráficos documentados.
3. Distingue entre `events_png/` (jugador individual) y `events_cards/` (carta completa).
4. Comprueba las rutas y claves reales antes de construir integraciones; no supongas que son idénticas a las carpetas de cartas base.

## Git LFS

La actualización reportó **11.242 objetos LFS** y aproximadamente **513 MB transferidos** durante la subida. Para obtener el contenido real de archivos grandes al clonar el repositorio, instala y configura Git LFS.

## Consideraciones y propiedad intelectual

Esta colección forma parte de un proyecto independiente y no oficial. No está afiliada, patrocinada ni respaldada por EA, EA SPORTS, FIFA, RenderZ, SoFIFA ni FIFAMobileGuide.

Los logotipos de eventos, escudos de clubes, imágenes de jugadores, diseños de cartas y otros elementos visuales pueden pertenecer a EA, sus licenciantes u otros titulares. La atribución no concede permiso para copiar, publicar o redistribuir esos materiales. Consulta [`NOTICE.md`](NOTICE.md) y verifica las autorizaciones necesarias antes de reutilizarlos.
