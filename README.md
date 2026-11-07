# FIFA Mobile 18 — Base de cartas, estadísticas e imágenes (Season 2)

**Versión del proyecto: 3.0.0**  
**Documentación actualizada: 6 de noviembre de 2026**

Proyecto independiente y no oficial para recopilar, organizar y consultar información de las cartas base de **FIFA Mobile 18 — Season 2**. La colección reúne datos de jugadores y cartas, atributos principales y detallados, imágenes individuales de los jugadores y composiciones PNG de las cartas base completas.

> [!NOTE]
> Este proyecto no está afiliado, patrocinado ni respaldado por Electronic Arts, EA SPORTS, FIFA, RenderZ, SoFIFA ni FIFAMobileGuide. Los nombres se utilizan únicamente para identificar el juego y las referencias consultadas.
>
> [!IMPORTANT]
> El contenido se ofrece como material de referencia comunitario. No constituye una publicación oficial de EA ni una certificación de que cada dato o imagen coincida exactamente con el juego. Puede contener omisiones, diferencias o errores. La atribución a una fuente no concede permiso para copiar o redistribuir sus materiales. Consulta [`NOTICE.md`](NOTICE.md) antes de publicar o reutilizar cualquier contenido.

## Evolución del proyecto

- **1.0.0 — Base inicial:** recopilación de información de las cartas base y exportaciones en distintos formatos.
- **2.0.0 — Estadísticas:** ampliación de la base con atributos principales, estadísticas detalladas y campos específicos para porteros.
- **3.0.0 — Recursos gráficos:** incorporación de PNG individuales de jugadores y PNG de cartas base completas, junto con manifiestos y herramientas para descargarlos o generarlos.

## Novedades de la versión 3.0.0

- Se incorpora la colección `players_png/` con **13.885 imágenes PNG individuales** de los jugadores de las cartas base. Son imágenes del jugador, sin el fondo, el escudo del club ni el marco completo de la carta.
- Se incorpora `cards_full/` con **13.885 composiciones PNG de cartas base completas** a 256 × 256 píxeles.
- Se añaden manifiestos CSV y JSON para inventariar ambas colecciones gráficas.
- Se añade `download_player_png.py` para descargar las imágenes individuales y mantener una caché reanudable.
- Se añade `generate_full_cards.py` para componer las cartas completas utilizando los recursos gráficos disponibles.
- Se amplía la documentación con [`README_PNG.md`](README_PNG.md) y [`README_CARDS_FULL.md`](README_CARDS_FULL.md).

## Contenido del repositorio

| Archivo o carpeta | Descripción |
|---|---|
| `extract_fifa18.py` | Extractor Python de la base principal de cartas. Mantiene cachés y genera las exportaciones principales. |
| `fifa_mobile_18_base.csv` | Base principal de cartas, con una fila por carta base. Delimitador `;`. |
| `fifa_mobile_18_base.json` | Base principal en JSON, con campos UTF-8 adicionales. |
| `fifa_mobile_18_base.txt` | Vista de texto plano de la base principal. |
| `fifa_mobile_18_base_player_stats.csv` | Base ampliada con datos de carta, atributos principales y atributos detallados. Delimitador `;`. |
| `fifa_mobile_18_base_player_stats.json` | Base ampliada en JSON, organizada por jugador, carta y estadísticas. |
| `fifa_mobile_18_base_player_stats_SAMPLE.json` | Muestra reducida del esquema JSON estadístico. |
| `missing_in_renderz.csv` | IDs para los que no se obtuvo una ficha base durante la extracción incluida. |
| `programs_excluded.csv` | IDs detectados como cartas de programas/eventos y excluidos de la base principal. |
| `muestra_prueba_300.csv` / `muestra_prueba_300.txt` | Muestra reducida para inspección rápida de la base principal. |
| `players_png/` | Imágenes PNG individuales de los jugadores, organizadas por rareza. |
| `players_png_manifest.csv` / `.json` | Manifiestos de la colección de imágenes individuales. |
| `download_player_png.py` | Descargador de imágenes individuales desde las referencias/CDN configuradas. |
| `cards_full/` | Composiciones PNG de las cartas base completas, organizadas por rareza. |
| `cards_full_manifest.csv` / `.json` | Manifiestos de las cartas completas generadas. |
| `generate_full_cards.py` | Generador de composiciones de cartas completas a partir de los recursos gráficos. |
| `assets_cards/` | Recursos gráficos auxiliares utilizados por el generador; incluye los logotipos de clubes documentados en `assets_cards/clubs/`. |
| `fonts/` | Archivos tipográficos auxiliares utilizados por el generador de cartas, cuando están incluidos en la distribución. |
| `backgrounds_18/` | Recursos de fondos de cartas utilizados por el generador, cuando están incluidos en la distribución. |
| `data/cache_sofifa_list.json` | Caché de la lista de referencia consultada en SoFIFA. |
| `data/cache_renderz.jsonl` | Caché de consultas de fichas RenderZ. |
| `data/cache_guide_stats.jsonl` | Caché de referencia utilizada durante el trabajo de recopilación de atributos. |
| `data/cache_png_downloads.jsonl` | Caché reanudable de descargas de PNG individuales. |
| `data/manual_overrides.json` | Correcciones manuales persistentes para el extractor principal. |
| `data/progress.json` | Contadores y fecha de la última ejecución registrada por el extractor. |
| `organize_json.py` / `clean_json.py` | Utilidades de organización y simplificación de los datos JSON. |
| `README_JSON.md` | Documentación de la estructura del JSON estadístico. |
| `README_JSON_CLEAN.md` | Guía rápida para consultar la estructura JSON simplificada. |
| `README_PNG.md` | Documentación de las imágenes PNG individuales de jugadores. |
| `README_CARDS_FULL.md` | Documentación de las composiciones PNG de cartas completas. |
| `NOTICE.md` | Atribuciones, marcas, derechos de terceros y avisos legales. |
| `LEEME.txt` | Guía rápida complementaria en español. |

> La tabla describe los elementos documentados para el proyecto. La presencia de un archivo o carpeta concreta depende de los contenidos incluidos en cada distribución del repositorio.

## Cifras de la copia documentada

Los siguientes valores describen la colección documentada en esta versión. Pueden cambiar si se regeneran o actualizan los archivos.

| Elemento | Registros / archivos |
|---|---:|
| Base principal (`fifa_mobile_18_base.csv`) | 13.885 |
| Base con estadísticas (`fifa_mobile_18_base_player_stats.csv`) | 13.885 |
| Imágenes individuales (`players_png/`) | 13.885 |
| Cartas completas (`cards_full/`) | 13.885 |
| IDs sin ficha obtenida (`missing_in_renderz.csv`) | 4.048 |
| IDs de programas/eventos excluidos (`programs_excluded.csv`) | 6.571 |
| Jugadores en la caché de lista SoFIFA | 17.933 |

La colección de imágenes individuales ocupa aproximadamente **128,8 MB** según el manifiesto de documentación de la versión. No se proporciona un tamaño total de la colección de cartas completas porque puede variar según los recursos y la compresión de los PNG.

### Distribución por rareza

| Rareza | PNG individuales | Cartas completas |
|---|---:|---:|
| Master Rare | 1 | 1 |
| Epic Rare | 285 | 285 |
| Gold Rare | 3.656 | 3.656 |
| Silver Rare | 7.752 | 7.752 |
| Bronze Rare | 2.191 | 2.191 |
| **Total** | **13.885** | **13.885** |

## Base de datos y estadísticas

La base principal se centra en **cartas base** y relaciona identificadores de jugadores con la información de sus cartas. La exportación estadística añade:

- **Atributos principales:** seis valores generales para jugadores de campo y seis campos adaptados a la estructura de porteros.
- **Atributos detallados:** velocidad, aceleración, fuerza, control, regate, cabezazo, finalización, potencia de tiro, posicionamiento, defensa, pase y otros campos asociados.
- **Datos de portero:** `gk_diving`, `gk_positioning`, `reflexes` y `handling`; en posiciones a las que no aplica, el bloque correspondiente aparece como `null` en el JSON.

Consulta [`README_JSON.md`](README_JSON.md) y [`README_JSON_CLEAN.md`](README_JSON_CLEAN.md) para conocer las claves y estructuras exactas.

## Imágenes PNG individuales de jugadores

La carpeta `players_png/` contiene una imagen del jugador correspondiente a cada registro de la base de cartas. No incluye el fondo, el escudo del club ni el marco completo de la carta.

- Ruta: `players_png/{rareza}/p{fifa_id}*.png`.
- Dimensiones documentadas: **256 × 256 píxeles**.
- Cantidad documentada: **13.885 PNG**.
- Los nombres de archivo siguen el nombre encontrado en el CDN; algunos incluyen sufijos como `_AS` o `_AS2`.
- Los manifiestos `players_png_manifest.csv` y `players_png_manifest.json` registran los datos de cada descarga.

Consulta [`README_PNG.md`](README_PNG.md) para conocer el esquema del manifiesto y las opciones del descargador.

## Cartas base completas en PNG

La carpeta `cards_full/` contiene una composición gráfica de cada carta base:

- Ruta: `cards_full/{rareza}/card_{fifa_id}.png`.
- Dimensiones documentadas: **256 × 256 píxeles**.
- Cantidad documentada: **13.885 PNG**.
- Las composiciones combinan recursos gráficos de jugador, fondo, club y tipografía, siguiendo una referencia de distribución visual de la carta.
- Los manifiestos `cards_full_manifest.csv` y `cards_full_manifest.json` inventarían los resultados.

Estas imágenes se generaron mediante composición programática de recursos; no son capturas de pantalla de una sesión autenticada de RenderZ ni una declaración de que sean archivos oficiales publicados por EA. Consulta [`README_CARDS_FULL.md`](README_CARDS_FULL.md) para conocer los recursos y el proceso.

## Campos de la base principal

| Campo | Significado |
|---|---|
| `fifa_id` | Identificador del jugador utilizado para relacionar referencias. |
| `short_name`, `full_name` | Nombre corto y nombre completo. |
| `position_mobile` | Posición de la carta en FIFA Mobile. |
| `ovr_mobile` | Media general de la carta móvil. |
| `club_id`, `club_name` | Identificador y nombre del club. |
| `background_code`, `rarity` | Código de fondo y categoría de rareza. |
| `sofifa_overall`, `sofifa_potential` | Media y potencial de la referencia histórica de FIFA 18 para consola. |
| `sofifa_age`, `sofifa_position` | Edad y posición de la referencia de consola. |
| `nationality` | Nacionalidad registrada en la referencia. |
| `renderz_url`, `sofifa_url` | Enlaces a las fichas consultadas. |
| `season` | Temporada asociada al registro. |

### Códigos de rareza

| Código | Categoría |
|---|---|
| `BR` | Bronze Rare |
| `SR` | Silver Rare |
| `GR` | Gold Rare |
| `ER` | Epic Rare |
| `MR` | Master Rare |
| `CR` | Common Rare |
| `BC` | Bronze Common |
| `SC` | Silver Common |
| `GC` | Gold Common |

## Requisitos

- Python **3.10 o superior** recomendado.
- Conexión a Internet para realizar nuevas consultas o descargas mediante los scripts correspondientes.
- Las dependencias concretas pueden variar según el script y la distribución. Consulta la ayuda (`--help`) de cada herramienta y los archivos de requisitos si están incluidos.
- Espacio de almacenamiento suficiente para las bases, cachés, recursos auxiliares e imágenes PNG. La distribución gráfica completa puede ocupar bastante más que los archivos de documentación.

## Uso de las herramientas

Ejecuta los comandos desde la carpeta raíz del repositorio, donde se encuentran los scripts.

### Extractor de la base principal

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

El extractor consulta los IDs configurados, guarda respuestas en caché y genera las exportaciones de la base principal. Las opciones disponibles se pueden consultar con `--help`.

### Descargar PNG individuales de jugadores

```bash
python download_player_png.py --test
python download_player_png.py --workers 12
python download_player_png.py --fast --limit 100
python download_player_png.py --only-ids 20801,158023
python download_player_png.py --export-only
python download_player_png.py --help
```

El descargador utiliza una caché reanudable en `data/cache_png_downloads.jsonl`. Sin opciones de sobrescritura, puede omitir imágenes ya descargadas. Consulta [`README_PNG.md`](README_PNG.md) antes de ejecutar una descarga completa.

### Generar cartas completas

```bash
python generate_full_cards.py --test
python generate_full_cards.py --workers 8
python generate_full_cards.py --workers 8 --overwrite
python generate_full_cards.py --only-ids 20801,158023
python generate_full_cards.py --help
```

La generación es reanudable: según la documentación de la herramienta, sin `--overwrite` se omiten los archivos ya generados. Consulta [`README_CARDS_FULL.md`](README_CARDS_FULL.md) para revisar los recursos de entrada y las opciones.

## Criterios y limitaciones

- La base principal está enfocada en **cartas base**, no en todas las versiones especiales o promocionales de cada jugador.
- Los IDs detectados como cartas de programas/eventos se registran por separado y no se agregan como filas de la base principal.
- Los campos de FIFA Mobile y los de la referencia histórica FIFA 18 para consola pertenecen a contextos de juego distintos; sus medias, posiciones y otros valores pueden no coincidir.
- Los archivos CSV/TXT utilizan nombres normalizados para facilitar su lectura. El JSON principal conserva campos UTF-8 adicionales.
- En la tabla estadística, las celdas vacías pueden corresponder a atributos que no aplican a una posición. En JSON, `null` indica un campo no aplicable o no disponible en esa estructura.
- Las imágenes PNG corresponden a los recursos y composiciones descritos en sus manifiestos y documentos específicos. La disponibilidad futura de las URLs externas no está garantizada.
- Los datos pueden contener omisiones o errores y las fuentes externas pueden cambiar, limitar el acceso o dejar de estar disponibles.
- Los errores `404` o los fallos de conexión no demuestran por sí solos que un jugador nunca haya existido en el juego.
- Los CSV utilizan `;` como delimitador. Al importarlos en una hoja de cálculo, selecciona ese separador si las columnas no se dividen automáticamente.
- Dar crédito no concede derechos para redistribuir archivos de terceros. Revisa `NOTICE.md` y confirma los permisos antes de publicar datos, imágenes, fuentes tipográficas o recursos gráficos.

## Créditos y propiedad intelectual

Se reconocen **RenderZ**, **SoFIFA** y **FIFAMobileGuide** como referencias consultadas durante el trabajo de recopilación y organización. Los recursos gráficos y tipográficos utilizados por las herramientas también pueden estar sujetos a derechos de EA y de otros titulares.

Los nombres **FIFA**, **EA**, **EA SPORTS**, **FIFA Mobile**, **RenderZ**, **SoFIFA** y **FIFAMobileGuide** pertenecen o están asociados a sus respectivos titulares. Este proyecto no reclama la propiedad de sus marcas, sitios, bases de datos, fuentes tipográficas, imágenes ni materiales protegidos.

Dar crédito no implica afiliación ni concede derechos de reproducción o redistribución. Este repositorio no incluye una licencia abierta general para el conjunto de código y datos. Consulta [`NOTICE.md`](NOTICE.md) antes de copiar, publicar o distribuir cualquier archivo.

## Contribuciones

Las correcciones, mejoras de documentación y propuestas para los scripts pueden plantearse mediante *Issues* o *Pull Requests*. No contribuyas con imágenes, logotipos, fuentes, archivos del juego ni materiales de terceros que no tengas derecho a compartir.

---

**Aviso:** proyecto comunitario independiente, ofrecido tal como está y sin garantía de exactitud, integridad o disponibilidad. Para información sobre marcas, fuentes y permisos, consulta [`NOTICE.md`](NOTICE.md).
