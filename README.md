# FIFA Mobile 18 — Base de cartas, estadísticas, eventos e imágenes (Season 2)

**Versión del proyecto: 4.0.0**  
**Documentación actualizada: 10 de noviembre de 2026**

Proyecto independiente y no oficial dedicado a recopilar, organizar y consultar información de **FIFA Mobile 18 — Season 2**. Reúne datos de cartas base y cartas de eventos, estadísticas, *skill boosts*, imágenes individuales de jugadores y composiciones PNG de cartas completas, además de fondos, escudos de clubes y logotipos de eventos.

> [!NOTE]
> Este proyecto no está afiliado, patrocinado ni respaldado por Electronic Arts, EA SPORTS, FIFA, RenderZ, SoFIFA ni FIFAMobileGuide. Los nombres se utilizan únicamente para identificar el juego y las referencias consultadas.

> [!IMPORTANT]
> El contenido se ofrece como material de referencia comunitario. No constituye una publicación oficial de EA ni una certificación de que cada dato, estadística, imagen o composición coincida exactamente con el juego. Puede contener omisiones, diferencias o errores. La atribución a una fuente no concede permiso para copiar o redistribuir sus materiales. Consulta [`NOTICE.md`](NOTICE.md) antes de publicar o reutilizar cualquier contenido.

## Evolución del proyecto

- **1.0.0 — Base inicial:** recopilación de información de las cartas base y exportaciones en distintos formatos.
- **2.0.0 — Estadísticas:** ampliación de la base con atributos principales, estadísticas detalladas y campos específicos para porteros.
- **3.0.0 — Recursos gráficos de cartas base:** incorporación de PNG individuales de jugadores y PNG de cartas base completas, junto con manifiestos y herramientas.
- **4.0.0 — Skill boosts y cartas de eventos:** actualización de las cartas base con *skill boosts* y estadísticas revisadas; incorporación de una base de datos de eventos, sus imágenes individuales, cartas completas, logos y recursos gráficos adicionales.

## Novedades de la versión 4.0.0

### Cartas base

- Se amplía la información de las cartas base con **skill boosts**. Se documenta un catálogo de **37 nombres de refuerzos de habilidad**; la lista completa está en [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md).
- Se revisan las estadísticas para ofrecer valores más realistas.
- Se añade una exportación de la base completa en CSV, JSON y TXT: `fifa_mobile_18_base_completa.csv`, `fifa_mobile_18_base_completa.json` y `fifa_mobile_18_base_completa.txt`.
- Se añade `fifa_mobile_18_skill_boost_distribucion.txt`, con la distribución de *skill boosts*.
- Se conservan las colecciones de imágenes individuales y cartas completas de jugadores base publicadas en V3.0.0.

### Cartas de eventos

- Se incorpora una base independiente con **6.571 filas**: `fifa_mobile_18_eventos.csv`, `fifa_mobile_18_eventos.json` y `fifa_mobile_18_eventos.txt`.
- La información de cada registro incluye `SKILL_BOOST` y **30 estadísticas**. Por separado, el catálogo documentado de refuerzos de habilidad contiene **37 nombres**; no son 37 estadísticas adicionales.
- Se incorporan **6.483 cartas completas de eventos** de 256 × 256 píxeles en `events_cards/`.
- Se incorporan **6.570 PNG de jugadores de eventos** en `events_png/`. Esta colección contiene únicamente la variante **Action Shot**.
- Se añaden **92 iconos/logotipos de programas** en `events_logos/`. No se encontraron en el CDN los recursos `17_FAV` y `17_SBC_PLAYER`.
- Se añaden los manifiestos `events_manifest.csv` y `events_manifest.json`.
- Se incorporan recursos gráficos adicionales: **931 recursos de fondos** en `assets_cards/backgrounds/` y **47 recursos nuevos de clubes** en `assets_cards/clubs/`, incluidos recursos relacionados con World Cup y eventos.

### Herramientas y utilidades nuevas

- `extract_eventos_fifa18.py`: extractor de la base de cartas de eventos.
- `generate_events_assets.py`: herramienta para generar/preparar recursos gráficos de eventos.
- `generate_skill_boost.py`: herramienta relacionada con la generación de información de *skill boosts*.
- `reconcile_guide.py`: utilidad de conciliación de referencias.
- `inspect_event_assets.py`: herramienta de inspección de recursos gráficos de eventos.
- `_guide_by_fifa_id.py`: utilidad auxiliar de consulta por FIFA ID.
- `data/cache_eventos.jsonl`: caché de trabajo de la colección de eventos.

## Qué se añadió y qué se conservó

Según el registro de actualización compartido para el commit `a78158b4`, la subida de V4.0.0 incorporó los archivos y recursos nuevos descritos en esta documentación. La base anterior y los PNG originales de jugadores base no se modificaron: la actualización se realizó mediante adiciones.

## Contenido del proyecto

| Archivo o carpeta | Descripción |
|---|---|
| `extract_fifa18.py` | Extractor Python de la base principal de cartas base. |
| `fifa_mobile_18_base.csv` / `.json` / `.txt` | Exportaciones de la base principal de cartas base. |
| `fifa_mobile_18_base_player_stats.csv` / `.json` | Base de cartas base con atributos y estadísticas. |
| `fifa_mobile_18_base_player_stats_SAMPLE.json` | Muestra del esquema JSON estadístico, cuando está incluida. |
| `fifa_mobile_18_base_completa.csv` / `.json` / `.txt` | Exportaciones añadidas en V4.0.0 para la base completa. |
| `fifa_mobile_18_skill_boost_distribucion.txt` | Distribución de *skill boosts* de las cartas base. El catálogo de 37 nombres se documenta en `README_EVENT_CARDS.md`. |
| `players_png/` | PNG individuales de jugadores de cartas base. |
| `players_png_manifest.csv` / `.json` | Manifiestos de las imágenes individuales de cartas base. |
| `download_player_png.py` | Descargador de imágenes individuales de cartas base. |
| `cards_full/` | Composiciones PNG de cartas base completas. |
| `cards_full_manifest.csv` / `.json` | Manifiestos de las cartas base completas. |
| `generate_full_cards.py` | Generador de cartas base completas. |
| `fifa_mobile_18_eventos.csv` / `.json` / `.txt` | Base de datos de eventos, con 6.571 filas y `SKILL_BOOST` más 30 estadísticas. |
| `events_cards/` | 6.483 composiciones PNG de cartas completas de eventos (256 × 256). |
| `events_png/` | 6.570 PNG individuales de jugadores de eventos; solo variante Action Shot. |
| `events_logos/` | 92 iconos/logotipos de programas; `17_FAV` y `17_SBC_PLAYER` no se encontraron en el CDN. |
| `events_manifest.csv` / `.json` | Manifiestos de los recursos de eventos. |
| `extract_eventos_fifa18.py` | Extractor de la base de datos de eventos. |
| `generate_events_assets.py` | Herramienta de generación/preparación de recursos de eventos. |
| `generate_skill_boost.py` | Herramienta relacionada con la generación de *skill boosts*. |
| `reconcile_guide.py` | Utilidad para conciliar referencias. |
| `inspect_event_assets.py` | Herramienta para inspeccionar recursos de eventos. |
| `_guide_by_fifa_id.py` | Utilidad auxiliar de consulta por FIFA ID. |
| `data/cache_eventos.jsonl` | Caché de datos de la colección de eventos. |
| `assets_cards/backgrounds/` | Recursos de fondos; en V4.0.0 se añadieron 931 recursos, incluidos fondos de World Cup y eventos. |
| `assets_cards/clubs/` | Recursos de clubes; en V4.0.0 se añadieron 47 recursos. |
| `assets_cards/` | Recursos gráficos auxiliares utilizados en la composición de cartas. |
| `fonts/` | Fuentes auxiliares documentadas para la composición de cartas base, si están incluidas en la distribución. |
| `backgrounds_18/` | Fondos de cartas base, si están incluidos en la distribución. |
| `organize_json.py` / `clean_json.py` | Utilidades de organización y simplificación JSON. |
| `README_JSON.md` | Documentación de datos estadísticos y *skill boosts*. |
| `README_JSON_CLEAN.md` | Guía del JSON simplificado de cartas base. |
| `README_PNG.md` | Documentación de PNG individuales de jugadores base y eventos. |
| `README_CARDS_FULL.md` | Documentación de cartas completas base y eventos. |
| `README_EVENT_CARDS.md` | Guía de la base y recursos gráficos de eventos. |
| `NOTICE.md` | Atribuciones, marcas, derechos de terceros y avisos legales. |
| `LEEME.txt` | Guía rápida en español. |

## Cifras documentadas de la V4.0.0

| Colección o recurso | Cantidad documentada |
|---|---:|
| Base de cartas base (copia documentada en V3.0.0) | 13.885 |
| PNG individuales de jugadores base (copia documentada en V3.0.0) | 13.885 |
| Cartas base completas PNG (copia documentada en V3.0.0) | 13.885 |
| Filas de la base de eventos | 6.571 |
| Cartas completas de eventos PNG | 6.483 |
| PNG individuales de jugadores de eventos (Action Shot) | 6.570 |
| Iconos/logotipos de programas | 92 |
| Recursos nuevos de fondos | 931 |
| Recursos nuevos de clubes | 47 |

Estos recuentos describen la subida de V4.0.0 comunicada para el commit `a78158b4`. Las cantidades de filas de datos, PNG individuales, cartas completas y logos representan tipos de recursos distintos; no deben interpretarse como un conjunto con correspondencia uno a uno. Para las colecciones de versiones anteriores, consulta los manifiestos correspondientes.

### Recursos de eventos no encontrados

Los iconos de programa `17_FAV` y `17_SBC_PLAYER` no se encontraron en el CDN durante la recopilación indicada. Por eso no forman parte de los 92 iconos disponibles. Esta observación describe el resultado de esa consulta y no demuestra que los recursos no puedan existir en otra fuente.

## Estadísticas y *skill boosts*

Las cartas base de V4.0.0 incorporan *skill boosts* y estadísticas revisadas con el objetivo de ofrecer valores más realistas. La distribución de *skill boosts* se resume en `fifa_mobile_18_skill_boost_distribucion.txt`.

La base de eventos se distribuye en CSV, JSON y TXT y contiene 6.571 filas con `SKILL_BOOST` y 30 estadísticas. El proyecto documenta además un catálogo de **37 nombres de refuerzos de habilidad**; estos nombres no deben confundirse con las 30 estadísticas. Consulta [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md) para ver el catálogo completo y los archivos de datos para comprobar las columnas o claves exactas.

## Recursos gráficos

- **Jugadores base:** `players_png/` conserva la colección individual documentada en V3.0.0.
- **Cartas base completas:** `cards_full/` conserva la colección de cartas base completas documentada en V3.0.0.
- **Jugadores de eventos:** `events_png/` contiene 6.570 PNG, únicamente de tipo Action Shot.
- **Cartas de eventos completas:** `events_cards/` contiene 6.483 PNG de 256 × 256 píxeles.
- **Logotipos de eventos:** `events_logos/` contiene 92 iconos/logotipos de programas.
- **Fondos y clubes:** en `assets_cards/backgrounds/` se añadieron 931 recursos y en `assets_cards/clubs/`, 47 recursos nuevos.

Consulta [`README_PNG.md`](README_PNG.md), [`README_CARDS_FULL.md`](README_CARDS_FULL.md) y [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md) para detalles adicionales.

## Manifiestos

- `events_manifest.csv`
- `events_manifest.json`

Los manifiestos de eventos permiten inventariar los recursos de esa colección. Revisa sus encabezados y registros para conocer los campos exactos y las relaciones que proporciona cada uno. Para los recursos base se mantienen `players_png_manifest.csv`/`.json` y `cards_full_manifest.csv`/`.json`.

## Herramientas de eventos

Los scripts incorporados en V4.0.0 son:

```text
extract_eventos_fifa18.py
generate_events_assets.py
generate_skill_boost.py
reconcile_guide.py
inspect_event_assets.py
_guide_by_fifa_id.py
```

Para conocer sus argumentos, opciones y requisitos exactos, consulta la ayuda de cada script o su código. No se documentan comandos con parámetros no confirmados.

## Git LFS y archivos grandes

La actualización compartida indica que la subida de Git LFS finalizó correctamente con **11.242 objetos** y aproximadamente **513 MB transferidos**. La colección utiliza Git LFS para almacenar archivos grandes. Para clonar o descargar el repositorio y obtener el contenido real de esos recursos, instala y configura Git LFS antes de recuperar los objetos LFS.

El resumen de la subida también muestra una advertencia remota `GH010` relacionada con una muestra aleatoria de 10.000 objetos; según el registro compartido, la advertencia no impidió completar la subida.

## Uso de herramientas de cartas base

Ejecuta desde la raíz del repositorio. Estos comandos corresponden a las herramientas documentadas para la base y recursos base en versiones anteriores; consulta `--help` antes de ejecutar procesos completos.

### Extractor principal

```bash
python extract_fifa18.py --test
python extract_fifa18.py --limit 200
python extract_fifa18.py
python extract_fifa18.py --only-ids 20801,158023,190871
python extract_fifa18.py --export-only
python extract_fifa18.py --refresh
python extract_fifa18.py --workers 4
python extract_fifa18.py --help
```

### PNG individuales de cartas base

```bash
python download_player_png.py --test
python download_player_png.py --workers 12
python download_player_png.py --fast --limit 100
python download_player_png.py --only-ids 20801,158023
python download_player_png.py --export-only
python download_player_png.py --help
```

### Cartas base completas

```bash
python generate_full_cards.py --test
python generate_full_cards.py --workers 8
python generate_full_cards.py --workers 8 --overwrite
python generate_full_cards.py --only-ids 20801,158023
python generate_full_cards.py --help
```

Para las herramientas de eventos, consulta `--help` en los scripts correspondientes. No se asume que tengan los mismos parámetros que las herramientas de cartas base.

## Requisitos y consideraciones

- Python **3.10 o superior** era la versión recomendada para las herramientas documentadas en versiones anteriores. Comprueba los requisitos específicos de cada script.
- Algunas herramientas requieren conexión a Internet para realizar consultas o descargas.
- Se necesita espacio suficiente para bases, cachés, imágenes, fondos, escudos, logotipos y cartas completas.
- Los CSV pueden utilizar `;` como delimitador; confirma el separador del archivo antes de importarlo.
- Los datos pueden contener omisiones o errores; las fuentes externas pueden cambiar, limitar el acceso o dejar de estar disponibles.
- Las estadísticas y *skill boosts* se ofrecen como información de referencia y no constituyen una certificación oficial de EA.
- Las cartas base y las cartas de eventos son colecciones distintas. No mezcles sus manifiestos ni asumas que comparten esquema, identificadores o rutas.
- Dar crédito no concede derechos para redistribuir archivos de terceros. Revisa [`NOTICE.md`](NOTICE.md) y confirma los permisos necesarios antes de publicar datos o recursos gráficos.

## Créditos y propiedad intelectual

Se reconocen **RenderZ**, **SoFIFA** y **FIFAMobileGuide** como referencias consultadas en el trabajo documentado de recopilación y organización. Los recursos gráficos, tipográficos, logotipos, nombres de eventos y materiales de juego pueden pertenecer a EA, sus licenciantes u otros titulares.

Los nombres **FIFA**, **EA**, **EA SPORTS**, **FIFA Mobile**, **RenderZ**, **SoFIFA** y **FIFAMobileGuide** pertenecen o están asociados a sus respectivos titulares. Este proyecto no reclama la propiedad de sus marcas, sitios, bases de datos, imágenes, fuentes tipográficas, logotipos ni materiales protegidos.

Dar crédito no implica afiliación ni concede derechos de reproducción o redistribución. Este repositorio no incluye una licencia abierta general para el conjunto de código y datos. Consulta [`NOTICE.md`](NOTICE.md) antes de copiar, publicar o distribuir cualquier archivo.

## Contribuciones

Las correcciones, mejoras de documentación y propuestas para los scripts pueden plantearse mediante *Issues* o *Pull Requests*. No contribuyas con imágenes, logotipos, fuentes, archivos del juego ni materiales de terceros que no tengas derecho a compartir.

---

**Aviso:** proyecto comunitario independiente, ofrecido tal como está y sin garantía de exactitud, integridad o disponibilidad. Para información sobre marcas, fuentes y permisos, consulta [`NOTICE.md`](NOTICE.md).
