# FIFA Mobile 18 — Base de cartas, estadísticas, eventos e imágenes (Season 2)

**Versión del proyecto: 4.0.0**  
**Documentación actualizada: 10 de noviembre de 2026**

Proyecto independiente y no oficial dedicado a recopilar, organizar y consultar información de **FIFA Mobile 18 — Season 2**. Reúne tres bases de datos (cartas base, cartas de eventos y cartas Icono/Prime Icon/WC Icon) con estadísticas, *skill boosts*, imágenes individuales de jugadores y composiciones PNG de cartas completas, además de fondos, escudos de clubes y logotipos de programas.

> [!NOTE]
> Este proyecto no está afiliado, patrocinado ni respaldado por Electronic Arts, EA SPORTS, FIFA, RenderZ, SoFIFA ni FIFAMobileGuide. Los nombres se utilizan únicamente para identificar el juego y las referencias consultadas.

> [!IMPORTANT]
> El contenido se ofrece como material de referencia comunitario. No constituye una publicación oficial de EA ni una certificación de que cada dato, estadística, imagen o composición coincida exactamente con el juego. Puede contener omisiones, diferencias o errores. La atribución a una fuente no concede permiso para copiar o redistribuir sus materiales. Consulta [`NOTICE.md`](NOTICE.md) antes de publicar o reutilizar cualquier contenido.

## Evolución del proyecto

- **1.0.0 — Base inicial:** recopilación de información de las cartas base y exportaciones en distintos formatos.
- **2.0.0 — Estadísticas:** ampliación de la base con atributos principales, estadísticas detalladas y campos específicos para porteros.
- **3.0.0 — Recursos gráficos de cartas base:** incorporación de PNG individuales de jugadores y PNG de cartas base completas, junto con manifiestos y herramientas.
- **4.0.0 — Datos reales del motor:** estadísticas y *skill boosts* **reales del motor FIFA Mobile 18** (feed de datos del propio juego, capturado carta a carta); publicación de las bases de eventos y de Iconos, sus imágenes y cartas completas; campo `total_stats`.

## Novedades de la versión 4.0.0

### Cartas base

- Se amplía la información de las cartas base con **skill boosts**. Se documenta un catálogo de **37 nombres de refuerzos de habilidad**; la lista completa está en [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md).
- Las estadísticas son los **valores reales del motor** (rango superior a 99, hasta ~160), no valores generados ni de consola. Ejemplo máximo: `Bale 87` conserva el Heading 866 de la guía.
- Las **265 cartas** con fichas originales de fifamobileguide.com conservan sus valores exactos de la guía (intocables).
- Se añade una exportación de la base completa en CSV, JSON y TXT: `fifa_mobile_18_base_completa.csv`, `fifa_mobile_18_base_completa.json` y `fifa_mobile_18_base_completa.txt`.
- Se añade el campo `total_stats` (suma del motor de los 24 atributos detallados).
- Se conserva la colección de imágenes y cartas completas de V3.0.0.

### Cartas de eventos

- Nueva base independiente: **6.571 filas** en `fifa_mobile_18_eventos.csv`, `.json` y `.txt`.
- La información incluye `SKILL_BOOST` real (del motor) y estadísticas reales; el registro alcanza valores superiores a 99 (máximo **140**, Bonucci 100 OVR).
- Se incorporan **6.483 cartas completas de eventos** de 256 × 256 píxeles en `events_cards/`.
- Se incorporan **6.570 PNG** de jugadores de eventos en `events_png/` (variante Action Shot únicamente).
- **92 iconos/logotipos** de programas en `events_logos/`. No se encontraron en el CDN los recursos `17_FAV` y `17_SBC_PLAYER`.
- Se añaden los manifiestos `events_manifest.csv` y `events_manifest.json`.
- Se incorporan recursos gráficos adicionales: **931 fondos** en `assets_cards/backgrounds/` y **47 clubes nuevos** en `assets_cards/clubs/`, incluidos recursos relacionados con World Cup y eventos.

### Cartas Icono (nueva colección)

- Nueva base independiente: **69 cartas** (36 Icon, 16 Prime Icon, 17 WC Icon) en `fifa_mobile_18_iconos.csv`, `.json` y `.txt`.
- **Stats reales del motor** (máxima 120) salvo **15 originales de la guía** intocables (Deco 85, Inzaghi 87, Maradona 91, Gullit 86/97, Puyol 86/97, Petit 85, Yashin 89, Okocha 86, Ferdinand 89, van Basten 97, Matthäus 98, Ronaldinho 98, van der Sar 98).
- Información de carrera completa por icono (nombre civil, nacionalidad, año de nacimiento, altura, rol real, clubes, honores) curada a mano.
- Pares Pelé/Ronaldo/Henry en dos posiciones con **el mismo render compartido**, señalados con `shared_render_with`/`related_cards`.
- Se incorporan **66 renders** PNG únicos en `icons_png/`, **69 cartas completas** en `icons_cards/`, **2 logos** en `icons_logos/` y manifiestos `icons_manifest.csv`/`.json`.
- Se añaden recursos nuevos: `backgrounds_WC_ICON_M.png`, `backgrounds_WC_ICON_E.png` (CDN sirve el mismo PNG para ambos) y `assets_cards/clubs/112658.png` (escudo "Icons", también presente en Icon/Prime Icon como club).

### Herramientas y utilidades nuevas

- `extract_eventos_fifa18.py`: extractor de la base de cartas de eventos.
- `generate_events_assets.py`: herramienta para generar/preparar recursos gráficos de eventos.
- `generate_skill_boost.py`: herramienta relacionada con la generación de información de *skill boosts*.
- `reconcile_guide.py`: utilidad de conciliación de referencias.
- `inspect_event_assets.py`: herramienta de inspección de recursos gráficos de eventos.
- `_guide_by_fifa_id.py`: utilidad auxiliar de consulta por FIFA ID.
- `data/cache_eventos.jsonl`: caché de trabajo de la colección de eventos.
- `fetch_mobile_stats.py`: descarga el feed del motor (`__data.json` de RenderZ/SvelteKit) para todos los IDs de las tres bases.
- `devalue.py`: parser del formato SvelteKit usado por el fetch.
- `fix_mobile_stats.py`: sustituye las estadísticas por las del motor (respeta las 280 originales de guía) y añade `total_stats`.
- `generate_iconos.py`, `generate_iconos_assets.py`, `validate_iconos.py`, `cache_iconos_rz.py`, `parse_guide_iconos.py`, `icon_player_info.py`: herramientas de la base Iconos.

## Qué se añadió y qué se conservó

La V4.0.0 incorporó los archivos y recursos nuevos descritos en esta documentación. La base anterior y los PNG originales de jugadores base no se modificaron: la actualización se realizó mediante adiciones y sustituciones internas documentadas (estadísticas reales verificadas por carta).

## Contenido del proyecto

| Archivo o carpeta | Descripción |
|---|---|
| `extract_fifa18.py` | Extractor Python de la base principal de cartas base. |
| `fifa_mobile_18_base.csv` / `.json` / `.txt` | Exportaciones de la base principal de cartas base. |
| `fifa_mobile_18_base_player_stats.csv` / `.json` | Base con atributos principales y detallados **reales del motor** (265 de la guía intocables). |
| `fifa_mobile_18_base_player_stats_SAMPLE.json` | Muestra del esquema JSON estadístico, cuando está incluida. |
| `fifa_mobile_18_base_completa.csv` / `.json` / `.txt` | Exportaciones añadidas en V4.0.0 para la base completa. |
| `fifa_mobile_18_skill_boost_distribucion.txt` | Distribución de *skill boosts* de las cartas base. El catálogo de 37 nombres se documenta en `README_EVENT_CARDS.md`. |
| `players_png/` | PNG individuales de jugadores de cartas base. |
| `players_png_manifest.csv` / `.json` | Manifiestos de las imágenes individuales de cartas base. |
| `download_player_png.py` | Descargador de imágenes individuales de cartas base. |
| `cards_full/` | Composiciones PNG de cartas base completas. |
| `cards_full_manifest.csv` / `.json` | Manifiestos de las cartas base completas. |
| `generate_full_cards.py` | Generador de cartas base completas. |
| `fifa_mobile_18_eventos.csv` / `.json` / `.txt` | Base de datos de eventos, con 6.571 filas y `SKILL_BOOST` real más estadísticas reales. |
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
| `data/cache_mobile_stats.jsonl` | Caché de las estadísticas reales del motor (20.525 registros). |
| `data/cache_iconos_rz.jsonl` / `data/guide_iconos.json` / `iconos_list.json` | Cachés y catálogo de la base Iconos. |
| `assets_cards/backgrounds/` | Recursos de fondos; en V4.0.0 se añadieron 931 recursos, incluidos fondos de World Cup y eventos. |
| `assets_cards/clubs/` | Recursos de clubes; en V4.0.0 se añadieron 47 recursos y el escudo `112658` de Icono. |
| `assets_cards/backgrounds/backgrounds_WC_ICON_M.png` / `_E.png` | Fondos de WC Icons (el CDN sirve el mismo PNG para ambos). |
| `assets_cards/` | Recursos gráficos auxiliares utilizados en la composición de cartas. |
| `fonts/` | Fuentes auxiliares documentadas para la composición de cartas base, si están incluidas en la distribución. |
| `organize_json.py` / `clean_json.py` | Utilidades de organización y simplificación JSON. |
| `fifa_mobile_18_iconos.csv` / `.json` / `.txt` | Base de Iconos: 69 cartas con identidad completa y stats reales. |
| `fifa_mobile_18_skill_boost_iconos.txt` | Distribución de *skill boosts* de Iconos. |
| `icons_png/` | 66 renders PNG únicos (3 pares Pelé/Ronaldo/Henry comparten render). |
| `icons_logos/` | `program_17_ICONS.png` (Icon) y `program_17_WCICON.png` (WC Icon); Prime Icons no muestran icono de programa en RenderZ. |
| `icons_cards/` | 69 cartas completas de Iconos, organizadas por rareza. |
| `icons_manifest.csv` / `.json` | Manifiestos de los assets de Iconos (69 filas, todas `ok`). |
| `generate_iconos.py` / `generate_iconos_assets.py` / `validate_iconos.py` / `cache_iconos_rz.py` / `parse_guide_iconos.py` / `icon_player_info.py` | Herramientas de la base Iconos y su validación. |
| `fetch_mobile_stats.py` / `devalue.py` / `fix_mobile_stats.py` | Descarga del feed del motor, parser SvelteKit y sustitución ordenada de stats. |
| `cache_iconos_rz.py` | Caché de páginas de iconos en RenderZ. |
| `README.md` | Este archivo. Presentación, estructura y novedades V4.0.0. |
| `README_JSON.md` | Documentación de datos estadísticos y *skill boosts*. |
| `README_JSON_CLEAN.md` | Guía del JSON simplificado de cartas base. |
| `README_PNG.md` | Documentación de PNG individuales de jugadores base y eventos. |
| `README_CARDS_FULL.md` | Documentación de cartas completas base y eventos. |
| `README_EVENT_CARDS.md` | Guía de la base y recursos gráficos de eventos. |
| `README_EVENTOS.md` | Documentación de la base de eventos (estadísticas). |
| `README_ICONOS.md` | Documentación de la base de Iconos. |
| `NOTICE.md` | Atribuciones, marcas, derechos de terceros y avisos legales. |
| `LEEME.txt` | Guía rápida en español. |

## Cifras documentadas de la V4.0.0

| Colección o recurso | Cantidad documentada |
|---|---:|
| Base de cartas base (V3.0.0) | 13.885 |
| PNG individuales de jugadores base (V3.0.0) | 13.885 |
| Cartas base completas PNG (V3.0.0) | 13.885 |
| Cartas base con stats de la guía (intocables) | 265 |
| Cartas base con stats del motor | 13.620 |
| Filas de la base de eventos | 6.571 |
| Cartas completas de eventos PNG | 6.483 |
| PNG individuales de jugadores de eventos (Action Shot) | 6.570 |
| Iconos/logotipos de programas | 92 |
| Recursos nuevos de fondos | 931 |
| Recursos nuevos de clubes | 47 |
| Cartas Icono (Icon + Prime Icon + WC Icon) | 69 (36 + 16 + 17) |
| Renders únicos de `icons_png/` | 66 |
| Cartas completas `icons_cards/` | 69/69 |
| Iconos con stats de la guía (intocables) | 15 |
| Iconos con stats del motor | 54 |

Estos recuentos describen la subida de V4.0.0. Las cantidades de filas de datos, PNG individuales, cartas completas y logos representan tipos de recursos distintos; no deben interpretarse como un conjunto con correspondencia uno a uno. Para las colecciones de versiones anteriores, consulta los manifiestos correspondientes.

### Recursos de eventos no encontrados

Los iconos de programa `17_FAV` y `17_SBC_PLAYER` no se encontraron en el CDN durante la recopilación indicada; por eso no forman parte de los 92 iconos disponibles. Esta observación describe el resultado de esa consulta y no demuestra que los recursos no puedan existir en otra fuente.

### Distribución por rareza (Cartas Icono)

| Rareza | Cartas |
|---|---:|
| Icon | 36 |
| Prime Icon | 16 |
| WC Icon | 17 |
| **Total** | **69** |

## Estadísticas y *skill boosts*

Las cartas base de V4.0.0 incorporan *skill boosts* reales y estadísticas reales del motor FIFA Mobile 18; el objetivo es ofrecer valores exactos del juego, sin generación propia ni límite de consola.

- **Estadísticas reales, rango mobile:** 1.708 cartas de eventos superan 99 (máximo **140**, Bonucci 100 OVR); 41 cartas Icono superan 99 (máximo **120**); 265 base conservan la guía.
- **Revisión dirigida:** en la V4.0.0 las estadísticas se sustituyeron por los valores reales del motor (vía `fetch_mobile_stats.py` y `fix_mobile_stats.py`); la regla de originales intocables de la guía se respeta (Bale 87 con Heading 866, Deco 85 con su ficha de la guía, etc.).
- `total_stats` = suma del motor de los 24 detallados; presente en CSV y JSON de las tres bases.
- **Skill boosts:** en la base, 13.620 provienen del motor y 265 de la guía; en eventos, 6.571 del motor; en iconos, 54 del motor y 15 de la guía. La distribución está en `fifa_mobile_18_skill_boost_distribucion.txt` y `fifa_mobile_18_skill_boost_iconos.txt`.
- El catálogo **37 nombres de refuerzos de habilidad** está en [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md); no son 37 estadísticas.
- Los 279/280 originales de guía coinciden con los códigos del motor (la excepción documentada es Khedira 80 CM, `179846`: guía "long shoots" vs motor `long passing`).
- La vista del juego muestra los atributos afectados por el boost con +13 % aplicado; esta base los expone **sin boost**; el boost está como campo `skill_boost` aparte.
- No todas las cartas base superan 99 — las de niveles bajos/medios (OVR ≤ 91) simplemente no contienen ningún atributo por encima de 99 en el juego real; es un hecho de datos, no de limitación.

## Recursos gráficos

- **Jugadores base:** `players_png/` conserva la colección individual documentada en V3.0.0.
- **Cartas base completas:** `cards_full/` conserva la colección de cartas base completas documentada en V3.0.0.
- **Jugadores de eventos:** `events_png/` contiene 6.570 PNG, únicamente de tipo Action Shot.
- **Cartas de eventos completas:** `events_cards/` contiene 6.483 PNG de 256 × 256 píxeles.
- **Logotipos de eventos:** `events_logos/` contiene 92 iconos/logotipos de programas.
- **Cartas Icono completas:** `icons_cards/` contiene 69 PNG de 256 × 256 píxeles, con fondo LR5 (Icon/Prime) y `backgrounds_WC_ICON_M/E` (WC Icon), render de jugador, escudo o bandera en el slot club, y tipografías Knul.
- **Renders Icono:** `icons_png/` contiene 66 renders únicos (tres pares Pelé/Ronaldo/Henry comparten render).
- **Logotipos de iconos:** `icons_logos/` contiene `program_17_ICONS.png` (Icon) y `program_17_WCICON.png` (WC Icon).
- **Fondos y clubes:** en `assets_cards/backgrounds/` se añadieron fondos de World Cup/eventos y las variantes WC Icon; en `assets_cards/clubs/` se añadieron 47 recursos y el escudo `112658`.

Consulta [`README_PNG.md`](README_PNG.md), [`README_CARDS_FULL.md`](README_CARDS_FULL.md), [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md), [`README_EVENTOS.md`](README_EVENTOS.md) y [`README_ICONOS.md`](README_ICONOS.md) para detalles adicionales.

## Manifiestos

- `events_manifest.csv`
- `events_manifest.json`
- `icons_manifest.csv`
- `icons_manifest.json`

Los manifiestos permiten inventariar los recursos de cada colección. Revisa sus encabezados y registros para conocer los campos exactos. Para la base se mantienen `players_png_manifest.csv`/`.json` y `cards_full_manifest.csv`/`.json`.

## Herramientas de eventos y de iconos

Los scripts incorporados en V4.0.0 son:

```text
extract_eventos_fifa18.py
generate_events_assets.py
generate_skill_boost.py
reconcile_guide.py
inspect_event_assets.py
_guide_by_fifa_id.py
fetch_mobile_stats.py
devalue.py
fix_mobile_stats.py
generate_iconos.py
generate_iconos_assets.py
validate_iconos.py
cache_iconos_rz.py
parse_guide_iconos.py
icon_player_info.py
```

Para conocer sus argumentos, opciones y requisitos exactos, consulta la ayuda de cada script o su código. No se documentan comandos con parámetros no confirmados.

## Git LFS y archivos grandes

La actualización compartida indica que la subida de Git LFS finalizó correctamente con **11.242 objetos** y aproximadamente **513 MB transferidos**. La colección utiliza Git LFS para almacenar archivos grandes. Para clonar o descargar el repositorio y obtener el contenido real de esos recursos, instala y configura Git LFS antes de recuperar los objetos LFS.

En la subida de la V4.0.0 con estadísticas reales y la base Iconos se transfirieron 139/139 objetos LFS (8,1 MB).

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

### Aplicar las estadísticas reales y regenerar las bases

```bash
python fetch_mobile_stats.py 10     # ~20.500 IDs, ~41.000 peticiones
python fix_mobile_stats.py          # sustituye stats (respeta las 280 de la guía)
python generate_skill_boost.py      # regenera base completa con boosts reales
python generate_iconos.py && python validate_iconos.py
python generate_iconos_assets.py    # compone las 69 cartas de Iconos
```

Para las herramientas de eventos e Iconos, consulta `--help` en los scripts correspondientes. No se asume que tengan los mismos parámetros que las herramientas de cartas base.

## Requisitos y consideraciones

- Python **3.10 o superior** era la versión recomendada para las herramientas documentadas en versiones anteriores. Comprueba los requisitos específicos de cada script.
- Algunas herramientas requieren conexión a Internet para realizar consultas o descargas.
- Se necesita espacio suficiente para bases, cachés, imágenes, fondos, escudos, logotipos y cartas completas.
- Los CSV pueden utilizar `;` como delimitador; confirma el separador del archivo antes de importarlo.
- Los datos pueden contener omisiones o errores; las fuentes externas pueden cambiar, limitar el acceso o dejar de estar disponibles.
- Las estadísticas y *skill boosts* se ofrecen como información de referencia y no constituyen una certificación oficial de EA.
- Las cartas base y las cartas de eventos son colecciones distintas. No mezcles sus manifiestos ni asumas que comparten esquema, identificadores o rutas.
- Los iconos tienen reglas propias (escudo o bandera según rareza, icono de programa según `Icon`/`WC Icon`, y renders compartidos en posiciones dobles); consulta [`README_ICONOS.md`](README_ICONOS.md).
- Dar crédito no concede derechos para redistribuir archivos de terceros. Revisa [`NOTICE.md`](NOTICE.md) y confirma los permisos necesarios antes de publicar datos o recursos gráficos.

## Créditos y propiedad intelectual

Se reconocen **RenderZ**, **SoFIFA** y **FIFAMobileGuide** como referencias consultadas en el trabajo documentado de recopilación y organización. En la V4.0.0, el propio feed de datos del juego capturado vía RenderZ se utilizó para obtener las estadísticas reales y los *skill boosts* de las tres bases; FIFAMobileGuide se conserva como fuente de los 280 originales conservados; SoFIFA sigue como referencia histórica de consola. Los recursos gráficos, tipográficos, logotipos, nombres de eventos y materiales de juego pueden pertenecer a EA, sus licenciantes u otros titulares.

Los nombres **FIFA**, **EA**, **EA SPORTS**, **FIFA Mobile**, **RenderZ**, **SoFIFA** y **FIFAMobileGuide** pertenecen o están asociados a sus respectivos titulares. Este proyecto no reclama la propiedad de sus marcas, sitios, bases de datos, imágenes, fuentes tipográficas, logotipos ni materiales protegidos.

Dar crédito no implica afiliación ni concede derechos de reproducción o redistribución. Este repositorio no incluye una licencia abierta general para el conjunto de código y datos. Consulta [`NOTICE.md`](NOTICE.md) antes de copiar, publicar o distribuir cualquier archivo.

## Contribuciones

Las correcciones, mejoras de documentación y propuestas para los scripts pueden plantearse mediante *Issues* o *Pull Requests*. No contribuyas con imágenes, logotipos, fuentes, archivos del juego ni materiales de terceros que no tengas derecho a compartir.

---

**Aviso:** proyecto comunitario independiente, ofrecido tal como está y sin garantía de exactitud, integridad o disponibilidad. Para información sobre marcas, fuentes y permisos, consulta [`NOTICE.md`](NOTICE.md).
