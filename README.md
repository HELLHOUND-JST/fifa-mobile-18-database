# FIFA Mobile 18 — Base de cartas y estadísticas (Temporada 2)

**Versión del proyecto: 2.0**  
**Última actualización de esta documentación: 6 de noviembre de 2026**

Proyecto independiente y no oficial dedicado a recopilar, organizar y consultar información de las cartas base de **FIFA Mobile 18 — Season 2**. La versión 2.0 amplía la base original con un conjunto de atributos principales, estadísticas detalladas y valores específicos para porteros, además de exportaciones CSV y JSON.

> [!NOTE]
> Este proyecto no está afiliado, patrocinado ni respaldado por Electronic Arts, EA SPORTS, FIFA, RenderZ, SoFIFA ni FIFAMobileGuide. Los nombres se utilizan únicamente para identificar el juego y las referencias consultadas.

> [!IMPORTANT]
> Los datos se ofrecen como material de referencia comunitario. No constituyen una publicación oficial de EA ni una certificación de que cada valor coincida exactamente con el juego. Pueden existir diferencias, datos incompletos o errores. La atribución a una fuente tampoco concede permiso para copiar o redistribuir sus materiales. Consulta [`NOTICE.md`](NOTICE.md) antes de publicar o reutilizar el contenido.

## Objetivo

Mantener una base estructurada de las **cartas base** de FIFA Mobile 18 Season 2, evitando mezclar en la tabla principal las cartas especiales o de programas. La base relaciona los identificadores de jugadores con los datos de carta y ofrece una segunda exportación enriquecida con atributos principales y detallados.

## Referencias consultadas

- **RenderZ:** referencia para consultar información de las cartas base, como media móvil, posición, club, código de fondo y rareza. Ejemplo de ficha: `https://renderz.app/18/player/20801`.
- **SoFIFA:** referencia histórica para identificar jugadores y consultar información asociada a FIFA 18. Conjunto utilizado: `r=180084`.
- **FIFAMobileGuide:** referencia reconocida en el trabajo de recopilación y organización de atributos de jugadores. Se incluye su crédito en [`NOTICE.md`](NOTICE.md).

Cada plataforma conserva sus propios derechos, condiciones y políticas. La inclusión de una referencia no supone afiliación ni autorización para redistribuir sus contenidos.

## Novedades de la versión 2.0

- Se incorpora `fifa_mobile_18_base_player_stats.csv`, una exportación que combina la información de las cartas con atributos principales y detallados.
- Se incorpora `fifa_mobile_18_base_player_stats.json`, un JSON organizado por jugador, carta y estadísticas.
- Se añade `fifa_mobile_18_base_player_stats_SAMPLE.json` como muestra pequeña del esquema y de la estructura de los registros.
- Se incluyen utilidades de organización y limpieza de datos JSON: `organize_json.py` y `clean_json.py`.
- Se incorpora una caché adicional de referencia para el trabajo de atributos en `data/cache_guide_stats.jsonl`.

## Contenido del repositorio

| Archivo o carpeta | Descripción |
|---|---|
| `extract_fifa18.py` | Extractor Python de la base de cartas. Consulta las referencias configuradas, mantiene cachés y genera las exportaciones principales. |
| `fifa_mobile_18_base.csv` | Base principal de cartas, con una fila por carta base. Delimitador `;`. |
| `fifa_mobile_18_base.json` | Base principal en JSON, con campos adicionales UTF-8 para conservar nombres y textos originales. |
| `fifa_mobile_18_base.txt` | Vista de texto plano de la base principal. |
| `fifa_mobile_18_base_player_stats.csv` | Base ampliada con datos de carta, atributos principales y atributos detallados. Delimitador `;`. |
| `fifa_mobile_18_base_player_stats.json` | Base ampliada en JSON, con secciones para identidad, edad, carta y estadísticas. |
| `fifa_mobile_18_base_player_stats_SAMPLE.json` | Muestra del JSON ampliado con ejemplos y esquema. |
| `missing_in_renderz.csv` | IDs de referencia para los que no se obtuvo una ficha base en RenderZ durante la extracción incluida. |
| `programs_excluded.csv` | IDs detectados como cartas de programas/eventos y excluidos de la base principal. |
| `muestra_prueba_300.csv` / `muestra_prueba_300.txt` | Muestra reducida para inspección rápida de la base principal. |
| `data/cache_sofifa_list.json` | Caché de la lista de referencia consultada en SoFIFA. |
| `data/cache_renderz.jsonl` | Caché de consultas de fichas RenderZ, una entrada JSON por línea. |
| `data/cache_guide_stats.jsonl` | Caché de referencia utilizada durante el trabajo de recopilación de atributos. |
| `data/manual_overrides.json` | Correcciones manuales persistentes para la extracción principal. |
| `data/progress.json` | Contadores y fecha de la última ejecución registrada por el extractor. |
| `organize_json.py` | Utilidad de organización de los datos estadísticos en formato JSON. |
| `clean_json.py` | Utilidad para generar una versión simplificada del JSON estadístico. |
| `analisis_sofifa_mobile.py` | Script auxiliar de análisis de diferencias entre referencias. |
| `check_wayback.py` | Script auxiliar para consultar disponibilidad de capturas históricas mediante Wayback Machine. |
| `README_JSON.md` | Documentación de la estructura del JSON ampliado. |
| `README_JSON_CLEAN.md` | Guía rápida de lectura de la estructura simplificada. |
| `LEEME.txt` | Guía rápida complementaria en español. |
| `NOTICE.md` | Atribuciones, marcas, derechos de terceros y avisos legales. |

## Cifras de la copia incluida

Los siguientes valores describen los archivos distribuidos en esta versión. Pueden cambiar al actualizar o volver a generar las exportaciones.

| Elemento | Registros |
|---|---:|
| Base principal (`fifa_mobile_18_base.csv`) | 13.885 |
| Base con estadísticas (`fifa_mobile_18_base_player_stats.csv`) | 13.885 |
| IDs sin ficha obtenida (`missing_in_renderz.csv`) | 4.048 |
| IDs de programas/eventos excluidos (`programs_excluded.csv`) | 6.571 |
| Jugadores en la caché de lista SoFIFA | 17.933 |

La copia de datos incluida corresponde a una extracción realizada entre el **5 y el 6 de noviembre de 2026**. Estas cifras no garantizan disponibilidad, exactitud ni vigencia futura de las fuentes externas.

## Qué contiene la base estadística

La exportación estadística añade dos grupos de atributos:

- **Atributos principales:** seis valores generales para jugadores de campo y seis valores adaptados a la estructura de porteros.
- **Atributos detallados:** velocidad, aceleración, fuerza, control, regate, cabezazo, finalización, potencia de tiro, posicionamiento, defensa, pase y otros campos asociados. La estructura de porteros utiliza los campos aplicables a esa posición.
- **Datos de portero:** incluye un grupo específico con `gk_diving`, `gk_positioning`, `reflexes` y `handling`; en jugadores que no son porteros este grupo aparece como `null` en el JSON.

Para conocer los nombres exactos de las claves y la estructura de cada registro, consulta [`README_JSON.md`](README_JSON.md) y [`README_JSON_CLEAN.md`](README_JSON_CLEAN.md).

## Campos de la base principal

| Campo | Significado |
|---|---|
| `fifa_id` | Identificador del jugador utilizado para relacionar las referencias. |
| `short_name`, `full_name` | Nombre corto y nombre completo. |
| `position_mobile` | Posición de la carta en FIFA Mobile. |
| `ovr_mobile` | Media general de la carta móvil. |
| `club_id`, `club_name` | Identificador y nombre del club. |
| `background_code`, `rarity` | Código de fondo y categoría de rareza. |
| `sofifa_overall`, `sofifa_potential` | Media y potencial de referencia de FIFA 18 para consola. |
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
- Conexión a Internet para realizar nuevas consultas con el extractor.
- Los scripts principales utilizan módulos de la biblioteca estándar de Python; no requieren instalar paquetes externos para las funciones descritas en esta guía.

## Uso del extractor de la base principal

Ejecuta los comandos desde la carpeta raíz del repositorio, donde se encuentra `extract_fifa18.py`.

### Prueba rápida

```bash
python extract_fifa18.py --test
```

Realiza una prueba limitada a los primeros 10 IDs de la lista de referencia.

### Limitar una consulta

```bash
python extract_fifa18.py --limit 200
```

Limita a 200 los IDs que se procesan en esa ejecución.

### Ejecutar o reanudar el proceso

```bash
python extract_fifa18.py
```

Consulta los IDs pendientes, guarda respuestas en caché y genera los archivos de salida. El proceso puede reanudarse ejecutando el mismo comando otra vez.

### Consultar IDs específicos

```bash
python extract_fifa18.py --only-ids 20801,158023,190871
```

Limita las nuevas consultas a los IDs indicados. Las exportaciones también pueden incluir registros que ya existan en las cachés.

### Regenerar las exportaciones principales desde las cachés

```bash
python extract_fifa18.py --export-only
```

Reconstruye CSV, TXT y JSON de la base principal sin volver a consultar las páginas. Requiere las cachés correspondientes.

### Volver a consultar desde cero

```bash
python extract_fifa18.py --refresh
```

Ignora las cachés existentes durante la consulta y vuelve a obtener la información.

### Cambiar el número de trabajadores

```bash
python extract_fifa18.py --workers 4
```

Permite ajustar el número de consultas concurrentes. Utiliza un ritmo razonable y respeta las condiciones de cada sitio.

### Aplicar correcciones manuales

```bash
python extract_fifa18.py --set-name 20801 "Cristiano Ronaldo"
python extract_fifa18.py --set-ovr 20801 91
python extract_fifa18.py --export-only
```

Las correcciones se guardan en `data/manual_overrides.json` y se aplican en las siguientes exportaciones.

Para ver todas las opciones disponibles:

```bash
python extract_fifa18.py --help
```

## Criterios y limitaciones

- La base principal está enfocada en **cartas base**, no en todas las versiones especiales o promocionales de cada jugador.
- Los IDs detectados como cartas de programas/eventos se registran por separado y no se agregan como filas de la base principal.
- Los campos de FIFA Mobile y los de la referencia FIFA 18 para consola pertenecen a contextos de juego distintos; sus medias, posiciones y otros valores pueden no coincidir.
- Los archivos CSV/TXT utilizan nombres normalizados para facilitar su lectura. El JSON principal conserva campos UTF-8 adicionales para nombres, clubes y nacionalidades.
- En la tabla estadística, las celdas vacías pueden corresponder a atributos que no aplican a una posición. En el JSON, `null` indica un campo no aplicable.
- Los datos pueden contener omisiones o errores y las fuentes externas pueden cambiar, limitar el acceso o dejar de estar disponibles.
- Los errores `404` y los fallos de conexión no demuestran por sí solos que un jugador nunca haya existido en el juego.
- Los scripts `organize_json.py` y `clean_json.py` se incluyen como utilidades del proceso de estructuración. La reproducción íntegra de ese proceso puede requerir archivos intermedios que no forman parte de esta distribución.
- Los CSV utilizan `;` como delimitador. Al importarlos en una hoja de cálculo, selecciona ese separador si las columnas no se dividen automáticamente.

## Créditos y propiedad intelectual

Se reconoce a **FIFAMobileGuide** como referencia consultada durante el trabajo de recopilación y organización de atributos de jugadores. También se reconocen RenderZ y SoFIFA como referencias utilizadas para la información de cartas y jugadores.

Los nombres **FIFA**, **EA**, **EA SPORTS**, **FIFA Mobile**, **RenderZ**, **SoFIFA** y **FIFAMobileGuide** pertenecen o están asociados a sus respectivos titulares. Este proyecto no reclama la propiedad de sus marcas, sitios, bases de datos ni materiales protegidos.

Dar crédito no implica afiliación ni concede derechos de reproducción o redistribución. Revisa [`NOTICE.md`](NOTICE.md) antes de copiar, publicar o distribuir cualquier archivo. Este repositorio no incluye una licencia abierta general para el conjunto de código y datos.

## Contribuciones

Las correcciones, mejoras de documentación y propuestas para los scripts pueden plantearse mediante *Issues* o *Pull Requests*. No contribuyas con imágenes, logotipos, archivos del juego ni materiales de terceros que no tengas derecho a compartir.

---

**Aviso:** proyecto comunitario independiente, ofrecido tal como está y sin garantía de exactitud, integridad o disponibilidad. Para más información sobre marcas, fuentes y permisos, consulta [`NOTICE.md`](NOTICE.md).
