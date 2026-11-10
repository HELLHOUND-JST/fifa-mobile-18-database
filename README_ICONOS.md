# FIFA Mobile 18 — Base de cartas Icono (Season 2)

**Versión del proyecto: 4.0.0**  
**Archivo principal:** `fifa_mobile_18_iconos.csv`  
**Registros:** 69 cartas Icono

Este documento presenta la base dedicada a las **cartas Icono** de FIFA Mobile 18 — Season 2: las variantes **Icon**, **Prime Icon** e **Icon WC** (Copa del Mundo Rusia 2018). El catálogo de **37 nombres de refuerzos de habilidad** está separado (ver [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md)); no son 37 estadísticas.

## Alcance

| Rareza | Cartas | Stats | Boost |
|---|---:|---|---|
| Icon | 36 | 21 motor + 15 guía | 21 motor + 15 guía |
| Prime Icon | 16 | 16 motor | 16 motor |
| WC Icon | 17 | 17 motor | 17 motor |
| **Total** | **69** | motor **54** · guía **15** | motor **54** · guía **15** |

Los 15 originales de la guía (intocables por regla explícita): Deco 85, Puyol 86, Gullit 86, Petit 85, Yashin 89, Maradona 91, Okocha 86, Inzaghi 87, Ferdinand 89, van Basten 97, Matthäus 98, Ronaldinho 98, Puyol 97, van der Sar 98, Gullit 97.

## Archivos

| Archivo | Contenido |
|---|---|
| `fifa_mobile_18_iconos.csv` | 69 filas. Delimitador `;`. |
| `fifa_mobile_18_iconos.txt` | Vista de texto plano con ASCII puro. |
| `fifa_mobile_18_iconos.json` | JSON limpio: `{_readme, metadata, players[]}` con identidad, carta, stats reales y `total_stats`. |
| `fifa_mobile_18_skill_boost_iconos.txt` | Distribución de skill boosts entre los 37 oficiales. |
| `icons_png/` | Renders PNG del jugador (66 archivos únicos, ver abajo). |
| `icons_logos/` | `program_17_ICONS.png` (Icon) y `program_17_WCICON.png` (WC Icon). Prime Icons no muestran icono de programa en RenderZ. |
| `icons_cards/` | Cartas completas 256×256 (69/69), organizadas por rareza. |
| `icons_manifest.csv` / `.json` | Inventario: 69 filas, todas `ok`. |
| `generate_iconos.py` / `generate_iconos_assets.py` / `icon_player_info.py` / `validate_iconos.py` | Herramientas de generación, assets, biografías (Wikipedia curada a mano) y validación. |

## Adquisición de datos

- **Identidad y ficha de carta:** catálogo RenderZ `/18/player/<id>` (leído vía `__data.json`, el feed que carga la app del juego), más fifamobileguide.com para los 15 originales, y conocimiento curado del autor para biografías (`icon_player_info.py`).
- **Estadísticas:** valores reales del motor de FIFA Mobile 18 (feed del juego vía RenderZ `__data.json`), sin ningún valor generado.
- **Skill boosts:** el motor mapeado a los 37 oficiales para 54 cartas; los 15 originales de la guía conservan su boost.
- Los valores son **sin boost**; la vista del juego muestra +13 % adicional sobre los atributos afectados por el skill boost.
- Los valores llegan hasta ~160 en el motor; en esta base el máximo del set es **120** (varias cartas de Pelé 99 / Ronaldinho 98 / etc.; Pelé 99 → total_stats 2317).

## Identidad completa

SoFIFA no cubrió los iconos; por eso cada registro lleva también:

- `name.short`, `name.full`, `name.original` (con tildes, para los 13 nombres con escritura no ASCII)
- `full_name` en la fila (nombre civil completo)
- `birth_year`, `height_m`
- `nationality`, `foot`, `real_position`
- `clubs` (clubes de la carrera), `honors` (trofeos principales de la carrera)

Ejemplos: Ronaldinho (Brasil, 1980), Pelé (Brasil, 1940), Maradona (Argentina, 1960), Lev Yashin (URSS, 1929), Peter Schmeichel (Dinamarca, 1961).

Los honores y clubes son informativos; las fuentes son de dominio público (Wikipedia y fuentes institucionales) y se han redactado, no copiado.

## Tarjeta completa y club

Iconos y Prime Iconos llevan el escudo `112658` ("Icons") en el slot del club; los WC Icons usan la bandera del país en el slot de club y el logo `program_17_WCICON` como icono de programa:

| fifa_id | País (flag) | Jugador |
|---|---|---|
| 603280 | Nigeria (201393) | Okocha 88 |
| 603281 | Portugal (201354) | Rui Costa 89 |
| 603282 | Francia (201335) | Henry 91 |
| 603283 | Alemania (201337) | Klose 88 |
| 603284 | Japón (201411) | Nakata 88 |
| 603285 | Portugal (201354) | Deco 88 |
| 603286 | México (201386) | Hernández 89 |
| 603287 | Argentina (201369) | Maradona 91 |
| 603288 | Inglaterra (201318) | Moore 90 |
| 603289 | Inglaterra (201318) | Lineker 90 |
| 603290 | Brasil (201370) | Nazário 92 |
| 603291 | Brasil (201370) | Pelé 93 |
| 603292 | Rusia (201357) | Yashin 92 |
| 603293 | España (201362) | Puyol 91 |
| 603294 | Brasil (201370) | Ronaldinho 90 |
| 603295 | Alemania (201337) | Matthäus 90 |
| 603296 | Francia (201335) | Blanc 90 |

## Pares de cartas con el mismo render

Tres jugadores reales aparecen como dos cartas con posiciones distintas en Prime Icon, y **ambas cartas comparten el archivo de render idéntico**. Quedan señalados con `shared_render_with` (CSV) / `card.related_cards` (JSON):

| Pareja | Cartas | Render compartido |
|---|---|---|
| Pelé CF/ST | 502262 / 502555 | `p190043_PI1.png` |
| Ronaldo Nazário ST/CF | 502898 / 502901 | `p37576_PI1.png` |
| Thierry Henry ST/LW | 502899 / 502900 | `p1625_PI1.png` |

## Fondos

Iconos y Prime Icon usan `backgrounds_LR5.png`; WC Icons usan `backgrounds_WC_ICON_M.png` / `backgrounds_WC_ICON_E.png` (RenderZ/CDN sirve el mismo PNG para ambos nombres).

## Criterios

- Celdas `pace/shooting/agility/defending` en porteros quedan vacías (como en el resto de las bases); todo lo demás lleva valores del motor o de la guía.
- `total_stats` = suma del motor de los 24 detallados (ejemplo: Pelé 99 → 2317).
- La tarjeta compuesta en `icons_cards/` lleva OVR, posición y nombre con tipografías Knul Medium/Regular; fondo, escudo, bandera y render provienen de los recursos CDN referenciados por RenderZ (no hay capturas ni sesiones autenticadas).
- 3 renders fueron compartidos entre cartas de la misma realidad (ver tabla); el render es único por archivo, no por carta.
- Los CSV utilizan `;` como delimitador; los nombres de TXT están libres de caracteres no ASCII; los JSON conservan UTF-8 en el nombre original.
- Dar crédito no implica afiliación ni concede permiso para redistribuir. Consulta [`NOTICE.md`](NOTICE.md).
