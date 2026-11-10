# FIFA Mobile 18 — Complete Database, Cards, Statistics & Assets (Season 2)

**Project release:** `v5.0.0`  
**Documentation:** 10 November 2026

FIFA Mobile 18 Database V5.0.0 reúne en un único proyecto la información de las cartas base, cartas de eventos y programas, estadísticas de jugadores, *Skill Boosts* y colecciones gráficas asociadas a FIFA Mobile 18 — Season 2. El objetivo de esta versión es ofrecer una referencia integral del catálogo conservado por el proyecto, con datos consultables y recursos organizados mediante manifiestos.

> [!NOTE]
> Proyecto comunitario, independiente y no oficial. No está afiliado, patrocinado ni respaldado por Electronic Arts (EA), EA SPORTS, FIFA, RenderZ, SoFIFA ni FIFAMobileGuide.

> [!IMPORTANT]
> Según la información del proyecto, las estadísticas oficiales del juego y los *Skill Boosts* se obtuvieron de RenderZ. Esto describe la procedencia de los datos, no una afiliación con RenderZ ni una autorización para redistribuir su contenido. Los nombres, imágenes, logotipos, fuentes, fondos y demás recursos de terceros siguen sujetos a los derechos y condiciones de sus titulares. Consulta [`NOTICE.md`](NOTICE.md).

## Evolución del proyecto

- **1.0.0 — Base inicial:** recopilación de información de las cartas base y exportaciones en distintos formatos.
- **2.0.0 — Estadísticas:** ampliación con atributos principales, estadísticas detalladas y campos específicos para porteros.
- **3.0.0 — Recursos gráficos base:** PNG individuales de jugadores y composiciones PNG de cartas base completas.
- **4.0.0 — Eventos y Skill Boosts:** base de cartas de eventos, estadísticas revisadas, *Skill Boosts*, PNG de eventos, cartas completas, logos y recursos gráficos adicionales.
- **5.0.0 — Integración integral:** consolidación de cartas base, cartas de eventos/programas, iconos y recursos gráficos; incorporación de estadísticas oficiales y *Skill Boosts* oficiales procedentes de RenderZ, además de herramientas y esquemas JSON actualizados.

## Novedades de V5.0.0

### 1. Datos de cartas base y estadísticas oficiales

- La colección base documentada conserva **13.885 cartas**.
- La actualización de estadísticas se describe con un desglose de **13.620 registros del motor + 265 registros de guía**, que suma 13.885. Este desglose se mantiene tal como aparece en el resumen de actualización; no implica que ambas procedencias sean idénticas.
- Según el responsable del proyecto, las estadísticas oficiales del juego y los *Skill Boosts* se obtienen de **RenderZ**.
- Se incorpora `fetch_mobile_stats.py` para obtener estadísticas de cartas móviles.
- Se incorpora `fix_mobile_stats.py` para corregir o completar registros estadísticos.
- El JSON actualizado incluye `total_stats` y mantiene el bloque `goalkeeping` presente en cada registro.
- Se documentan las fuentes de datos y se amplían los ejemplos de consulta.

### 2. Cartas de eventos y programas

La colección de eventos documentada en la actualización anterior incluye:

- **6.571 registros** en la base de eventos (`fifa_mobile_18_eventos.*`).
- Campo `SKILL_BOOST` y **30 estadísticas** por registro, según el inventario V4.
- **6.570 PNG individuales** de jugadores de eventos, variante Action Shot.
- **6.483 cartas completas** de eventos en PNG de 256 × 256.
- **92 logos** de eventos/programas en `events_logos/`; los recursos `17_FAV` y `17_SBC_PLAYER` no se encontraron en el CDN en la revisión documentada.

V5 presenta estas colecciones como parte del catálogo integrado de cartas base, eventos y programas. Los recuentos de filas, PNG individuales y cartas completas corresponden a tipos de recurso distintos y no deben sumarse como si fueran registros equivalentes.

### 3. Colecciones de iconos

La captura de cambios de documentación identifica estas colecciones adicionales:

| Carpeta | Inventario comunicado |
|---|---:|
| `icons_png/` | 66 renders PNG |
| `icons_cards/` | 69 de 69 recursos/casos documentados |

También se documentan los recursos de iconos y escudos del inventario, incluido el identificador/recurso de escudo `112658`, el fondo `WC_ICON` y un fondo asociado a estadísticas reales. Consulta [`README_ICONOS.md`](README_ICONOS.md) y verifica los manifiestos para conocer nombres, relaciones y rutas precisas.

### 4. Recursos gráficos de cartas

Se conservan y organizan los recursos gráficos ya descritos en V3/V4:

- `players_png/`: imágenes individuales de jugadores de cartas base (**13.885**).
- `cards_full/`: cartas base completas (**13.885**).
- `events_png/`: PNG individuales de jugadores de eventos (**6.570**, Action Shot).
- `events_cards/`: cartas completas de eventos (**6.483**).
- `events_logos/`: logos de programas/eventos (**92**, según inventario V4).
- `icons_png/`: 66 renders PNG.
- `icons_cards/`: 69 de 69 elementos documentados.
- `assets_cards/backgrounds/`: incluye los **931 recursos adicionales** reportados en V4, fondos World Cup y eventos.
- `assets_cards/clubs/`: incluye los **47 recursos de clubes adicionales** reportados en V4 y el recurso/identificador de escudo `112658` mencionado en el inventario posterior.
- `fonts/`, `backgrounds_18/` y otros recursos auxiliares utilizados para componer cartas.

Las cantidades de iconos y recursos se documentan según los inventarios comunicados. Para conocer el contenido exacto de cada colección, deben consultarse sus manifiestos y carpetas.

### 5. Herramientas de V5

Nuevas herramientas indicadas para esta versión:

| Script | Función documentada |
|---|---|
| `fetch_mobile_stats.py` | Obtención de estadísticas de cartas móviles. |
| `fix_mobile_stats.py` | Revisión, corrección o completado de estadísticas móviles. |
| `generate_iconos_assets.py` | Generación/preparación de recursos gráficos de iconos. |

Se mantienen las herramientas de versiones anteriores, entre ellas `extract_fifa18.py`, `extract_eventos_fifa18.py`, `download_player_png.py`, `generate_full_cards.py`, `generate_events_assets.py`, `generate_skill_boost.py`, `reconcile_guide.py`, `inspect_event_assets.py`, `organize_json.py` y `clean_json.py`, cuando estén presentes en la distribución.

No se inventan argumentos de ejecución para las nuevas herramientas. Consulta `python nombre_del_script.py --help` y el código correspondiente antes de ejecutarlas.

## Archivos y carpetas principales

| Archivo o carpeta | Descripción |
|---|---|
| `fifa_mobile_18_base_completa.csv/.json/.txt` | Exportaciones de la base completa de cartas base. |
| `fifa_mobile_18_base_player_stats.csv/.json` | Exportaciones estadísticas de cartas base usadas en versiones anteriores. |
| `fifa_mobile_18_eventos.csv/.json/.txt` | Base de cartas de eventos y programas. |
| `fifa_mobile_18_skill_boost_distribucion.txt` | Distribución de *Skill Boosts* documentada en V4. |
| `players_png/` | Imágenes individuales de jugadores base. |
| `cards_full/` | Composiciones completas de cartas base. |
| `events_png/` | Imágenes individuales de jugadores de eventos. |
| `events_cards/` | Composiciones completas de cartas de eventos. |
| `events_logos/` | Logos de eventos/programas. |
| `icons_png/` | Renders PNG de iconos. |
| `icons_cards/` | Recursos gráficos de iconos en formato de carta/tarjeta según el inventario. |
| `players_png_manifest.csv/.json` | Manifiestos de imágenes individuales de jugadores base. |
| `cards_full_manifest.csv/.json` | Manifiestos de cartas base completas. |
| `events_manifest.csv/.json` | Manifiestos de recursos de eventos. |
| `assets_cards/backgrounds/` | Fondos de cartas, eventos y World Cup. |
| `assets_cards/clubs/` | Escudos/logos de clubes. |
| `fonts/` | Recursos tipográficos auxiliares de la composición. |
| `data/cache_eventos.jsonl` | Caché de datos de eventos. |
| `fetch_mobile_stats.py` | Obtención de estadísticas móviles. |
| `fix_mobile_stats.py` | Corrección/completado de estadísticas móviles. |
| `generate_iconos_assets.py` | Generación/preparación de iconos. |
| `README_JSON.md` | Esquema JSON de la base y los datos estadísticos. |
| `README_JSON_CLEAN.md` | Guía de la exportación JSON simplificada. |
| `README_PNG.md` | Colecciones PNG individuales. |
| `README_CARDS_FULL.md` | Cartas completas base y de eventos. |
| `README_EVENTOS.md` | Base y recursos de eventos. |
| `README_ICONOS.md` | Colección de iconos, logos y recursos asociados. |
| `NOTICE.md` | Atribuciones, marcas y avisos legales. |
| `LEEME.txt` | Resumen rápido en español. |

La presencia y el nombre exacto de cada archivo pueden variar entre paquetes de distribución; utiliza el inventario del commit o Release correspondiente como referencia definitiva.

## Resumen de cantidades documentadas

| Colección | Cantidad comunicada |
|---|---:|
| Cartas base | 13.885 |
| Estadísticas base: motor + guía | 13.620 + 265 = 13.885 |
| PNG individuales base | 13.885 |
| Cartas base completas | 13.885 |
| Registros de eventos/programas | 6.571 |
| PNG individuales de eventos | 6.570 |
| Cartas completas de eventos | 6.483 |
| Logos de eventos/programas | 92 |
| `icons_png/` | 66 renders |
| `icons_cards/` | 69 de 69 |
| Fondos adicionales reportados en V4 | 931 |
| Recursos nuevos de clubes reportados en V4 | 47 |

Las cifras proceden de los inventarios y resúmenes compartidos durante el desarrollo. No representan una auditoría independiente de cada archivo. Para determinar disponibilidad individual y correspondencias, consulta los manifiestos del Release.

## Estructura JSON

### Base de cartas base

La documentación de V5 identifica el campo `total_stats` y un bloque `goalkeeping` siempre presente. Consulta [`README_JSON.md`](README_JSON.md) para las claves y ejemplos correspondientes a la versión actual.

### Base de eventos

La documentación de cambios describe un objeto superior `has_meta` con las secciones `metadata` y `players`. No debe asumirse que el JSON de eventos comparte el mismo esquema que el JSON de cartas base.

### Ejemplos identificados

- La documentación de lectura menciona un ejemplo de carta `CR` con ID `1736`.
- La estructura de eventos utiliza `has_meta` con `metadata` y `players`.

Los ejemplos son ilustrativos; los tipos, nombres y valores definitivos deben comprobarse en los JSON distribuidos.

## Git LFS y distribución

El proyecto contiene grandes colecciones de PNG y otros recursos binarios gestionados mediante Git LFS. Instala Git LFS antes de clonar o descargar una copia completa que deba recuperar los objetos LFS. Una descarga ZIP automática de GitHub puede no comportarse igual que un `git clone` con LFS correctamente instalado.

Los recuentos de objetos y MB transferidos son específicos de cada subida/commit. No deben reutilizarse cifras históricas de V4 como si fueran el inventario actualizado de V5.

## Fuentes, exactitud y derechos

Según el responsable del proyecto, RenderZ es la fuente de las estadísticas oficiales del juego y de los *Skill Boosts*. La documentación reconoce además referencias históricas y auxiliares, incluidas FIFAMobileGuide y SoFIFA, según corresponda a cada conjunto de datos.

Que ciertos valores correspondan a estadísticas oficiales del juego no convierte el repositorio en un producto oficial de EA ni significa que EA lo respalde. Las marcas, imágenes, escudos, fondos, iconos, tipografías, diseños y bases de datos de terceros siguen sujetos a sus respectivos derechos y condiciones. La atribución no equivale a autorización de redistribución. Consulta [`NOTICE.md`](NOTICE.md) antes de reutilizar o publicar los archivos.

---

**Proyecto comunitario independiente.** Los inventarios describen la copia documentada y pueden variar entre actualizaciones. Se recomienda validar los archivos y manifiestos del Release que se vaya a utilizar.
