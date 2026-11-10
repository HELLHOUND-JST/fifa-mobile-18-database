# FIFA Mobile 18 — Base de cartas de Eventos (Season 2)

**Versión del proyecto: 4.0.0**  
**Archivo principal:** `fifa_mobile_18_eventos.csv`  
**Registros:** 6.571 cartas de eventos

La copia documentada contiene **6.571 filas**. El catálogo de **37 nombres de refuerzos de habilidad** está separado (ver [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md)); no son 37 estadísticas. La lista de boosts asignados a estas cartas coincide con los códigos reales del motor.

Este documento presenta la base dedicada de las **cartas de programas/eventos** de FIFA Mobile 18 — Season 2 (los IDs de 6 dígitos ≥ 500.000), separada de la base principal de cartas base siguiendo la exclusión automática aplicada durante la extracción.

## Alcance

- Incluidas todas las cartas con IDs de 6 dígitos del rango de eventos (≥ 500.000): eventos semanales, Golden Ticket, World League promo horarios, etc.
- Excluidas quedan las cartas base de < 500.000 (base principal) y las cartas de WC Icon, que se documentan en [`README_ICONOS.md`](README_ICONOS.md).
- Las estadísticas fueron reemplazadas por los **valores reales del motor FIFA Mobile 18** (feed del juego capturado por carta a carta).
- Los skill boosts son los reales asignados por el motor a cada carta (mapeados a los 37 oficiales).

## Archivos

| Archivo | Contenido |
|---|---|
| `fifa_mobile_18_eventos.csv` | 6.571 filas. Delimitador `;`. 54 columnas (+ `total_stats`). |
| `fifa_mobile_18_eventos.txt` | Vista de texto plano con ASCII puro. |
| `fifa_mobile_18_eventos.json` | JSON organizado: `{metadata, players[]}` con identidad, carta, stats reales y boost. |
| `events_manifest.csv` / `.json` | Inventario de assets: 6.483 compuestas (`ok`, 98.7 %), 88 `card_error` (assets WC no disponibles en RenderZ para todas las cartas). |
| `events_png/` | PNG individuales de los jugadores (organizados por programa). |
| `events_logos/` | Logos de programa descargados. |
| `events_cards/` | Cartas completas 256×256. |
| `extract_eventos_fifa18.py` | Extractor original de la base de eventos. |
| `generate_events_assets.py` / `inspect_event_assets.py` | Generador de assets. |

## Estructura

Cada fila mantiene la identidad de la carta, la referencia de programa, las stats detalladas y el skill boost. Los campos principales son:

- `fifa_id`, `page_name`, `title_name`, `short_name`, `full_name`, `full_name_original`
- `position_mobile`, `ovr_mobile`, `club_id`, `club_name`, `background_code`, `rarity`
- `sofifa_age`, `nationality`, `season`, `renderz_url`
- `skill_boost` (real, del motor o guía — todas vienen del motor)
- `event_name`, `event_id`, `event_detail`, `program_icon`, `action_variant`, `event_resolved_name`, `event_confidence`
- `pace … handling` (6 primarias: `pace/shooting/passing/agility/defending/physical`; 24 detallados)
- `total_stats` — suma del motor de los 24 atributos detallados. Añadido en 4.0.0.

## Estadísticas reales

- Todos los valores provienen del motor de FIFA Mobile 18 (feed de datos oficial del juego vía RenderZ, `__data.json`).
- 1.708 cartas superan los 99; el valor máximo encontrado es **140** (Bonucci 100 OVR, 603695).
- Los detalles completos se exponen sin tope console: 0–160 aprox.
- `stats_source` en JSON: `renderz_mobile_original` para el 100 % de las cartas (no hay originales de guía con ficha propia dentro de este subconjunto).

Distribución de boosts: véase `skill_boosts` en `metadata` del JSON (coincidencia 1 a 1 con los códigos del motor).

## Imágenes y cartas completas

- Todas las cartas componen 256×256 con fondo, render de jugador, escudo y tipografías Knul Medium/Regular (misma disposición que la base).
- 6.483 (`ok`) generadas; 88 (`card_error`) no se pudieron componer por falta de assets jugables en RenderZ para su club/fondo/ícono.

## Criterios

- Las estadísticas son del motor, son **sin boost**; la vista del juego muestra +13 % adicional sobre los atributos afectados por el skill boost.
- Los CSV utilizan `;` como delimitador; los TXT están libres de caracteres no ASCII (nombres saneados); el JSON conserva campos UTF-8.
- Dar crédito no implica afiliación ni concede permiso para redistribuir; consulta [`NOTICE.md`](NOTICE.md).
