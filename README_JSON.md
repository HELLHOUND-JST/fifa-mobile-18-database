# Datos JSON y estadísticas — FIFA Mobile 18 Base, eventos e Iconos (V4.0.0)

Este documento resume los datos estadísticos documentados para las tres bases de datos: cartas base, cartas de eventos y cartas Icono. La V4.0.0 amplía la información de cartas base con *skill boosts* reales del motor y estadísticas revisadas que ofrecen valores reales del juego; las 265 cartas con fichas originales de fifamobileguide.com conservan sus valores de la guía (intocables). La base de Iconos sigue la misma regla (15 originales de guía, 54 del motor).

## 1. Cartas base

La V4.0.0 amplía los datos de cartas base con:

- información de **skill boosts**; el catálogo documentado incluye **37 nombres** (consulta [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md));
- estadísticas reales del motor (sin valores generados);
- exportación completa adicional en CSV, JSON y TXT;
- nuevo campo `total_stats` = suma del motor de los 24 atributos detallados.

### Exportaciones V4.0.0

- `fifa_mobile_18_base_player_stats.csv` / `.json`
- `fifa_mobile_18_base_completa.csv` / `.json` / `.txt`
- `fifa_mobile_18_skill_boost_distribucion.txt`

### Estructura de estadísticas (V4.0.0)

La base de cartas base utiliza las siguientes secciones:

- `fifa_id`: identificador numérico del jugador.
- `name`: nombres `short` y `full`.
- `age`: edad de referencia cuando está disponible.
- `card`: datos de la carta, como `ovr`, `position`, `club_id`, `club`, `rarity`, `background_code` y `season`.
- `stats.primary`: seis atributos principales según la posición. En porteros: `gk_diving`, `gk_positioning`, `handling`, `reflexes`, `passing` y `physical`.
- `stats.detailed`: los **24** atributos del motor, tanto en campo como en porteros (los porteros tienen valores de campo bajos, como en el juego).
- `stats.goalkeeping`: `gk_diving`, `gk_positioning`, `reflexes`, `handling` en **todas** las posiciones (valores reales del motor; bajos en campo, p. ej. `4`, `18`/`22`).
- `total_stats`: suma del motor de los 24 atributos de `stats.detailed`.

En detalle:

`sprint_speed`, `acceleration`, `strength`, `ball_control`, `dribbling`, `heading`, `finishing`, `shot_power`, `long_shot`, `positioning`, `tackling`, `marking`, `aggression`, `composure`, `awareness`, `reactions`, `free_kick`, `short_passing`, `long_passing` y `crossing` (+ los 4 `gk_*`).

Los valores son **sin boost**; la vista del juego muestra +13 % adicional sobre los atributos afectados por el skill boost.<br/> Las 265 cartas con originales de la guía conservan sus valores exactos de la guía (de fifamobileguide.com), que pueden diferir 1–3 puntos respecto del motor.

Las claves exactas añadidas o modificadas en V4.0.0 son las del JSON real; la introspección completa está en este documento y en la muestra incluida en el repositorio.

## 2. Cartas de eventos

La V4.0.0 añade una base independiente en estos formatos:

- `fifa_mobile_18_eventos.csv`
- `fifa_mobile_18_eventos.json`
- `fifa_mobile_18_eventos.txt`

La copia subida contiene **6.571 filas**. Los registros incluyen el campo `SKILL_BOOST` real (del motor) y **30 estadísticas** (6 primarias + 24 detallados) con sus valores reales del motor; el máximo encontrado es **140** (Bonucci 100 OVR). El catálogo `skill_boosts` documenta por separado **37 nombres** de refuerzos de habilidad; no son 37 estadísticas adicionales. La lista exacta está en [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md).

Las estadísticas de la base de eventos son todas del motor, sin originales de guía (ninguna carta de eventos tiene ficha original en fifamobileguide.com).

## 3. Cartas Icono

La V4.0.0 incorpora una base independiente en estos formatos:

- `fifa_mobile_18_iconos.csv`
- `fifa_mobile_18_iconos.txt`
- `fifa_mobile_18_iconos.json`

La copia subida contiene **69 filas** en tres categorías (36 Icon, 16 Prime Icon, 17 WC Icon), con identidad completa, estadísticas, 69 cartas completas en `icons_cards/` y 66 renders únicos en `icons_png/`. Más información en [`README_ICONOS.md`](README_ICONOS.md).

Los skill boosts de iconos son también 1 de los 37 oficiales: 54 del motor y 15 conservados de la guía (intocables). Las 279 de 280 cartas con originales de guía (base e iconos) coinciden con las del motor; la excepción documentada es Khedira 80 CM (`179846`: guía "long shoots" vs motor `long passing`).

## 4. Diferencias entre colecciones

| Colección | Exportaciones | Contenido documentado |
|---|---|---|
| Cartas base | `fifa_mobile_18_base_player_stats.*`, `fifa_mobile_18_base_completa.*` | 13.885 filas, stats reales del motor (265 de guía intocables) |
| Cartas de eventos | `fifa_mobile_18_eventos.csv/.json/.txt` | 6.571 filas, SKILL_BOOST real y stats reales del motor |
| Cartas Icono | `fifa_mobile_18_iconos.csv/.json/.txt` | 69 filas; stats reales (54) o guía (15 intocables) |

Mantén separadas las tres bases al consultar, importar o combinar registros. No se han proporcionado reglas de unión completas ni garantías de que todos los identificadores sean únicos entre colecciones.

## 5. Ejemplo de lectura

### Base JSON de cartas base

```python
import json

with open("fifa_mobile_18_base_player_stats.json", encoding="utf-8") as file:
    database = json.load(file)

players = database.get("players", [])
print("Registros:", len(players))

if players:
    player = players[0]
    print(player.get("name", {}).get("full"))
    print(player.get("card", {}).get("ovr"))
    print(player.get("stats", {}).get("primary"))
    print("total_stats:", player.get("total_stats"))
```

### Base JSON de eventos

```python
import json

with open("fifa_mobile_18_eventos.json", encoding="utf-8") as file:
    events_data = json.load(file)

print(type(events_data).__name__)
if isinstance(events_data, dict):
    print("Claves superiores:", list(events_data.keys()))
    print("Registros:", len(events_data.get("players", [])))
```

### Base JSON de Iconos

```python
import json

with open("fifa_mobile_18_iconos.json", encoding="utf-8") as file:
    icons_data = json.load(file)

players = icons_data.get("players", [])
for p in players:
    print(p.get("fifa_id"), p.get("card", {}).get("ovr"), p.get("skill_boost"), p.get("total_stats"))
```

## 6. Archivos y herramientas relacionados

- `generate_skill_boost.py`: herramienta relacionada con la generación de *skill boosts*.
- `fifa_mobile_18_skill_boost_distribucion.txt`: distribución de *skill boosts* de la base.
- `fifa_mobile_18_skill_boost_iconos.txt`: distribución de *skill boosts* de iconos.
- `fetch_mobile_stats.py`: descarga el feed del motor (`__data.json` de RenderZ/SvelteKit).
- `fix_mobile_stats.py`: sustitución ordenada de estadísticas (respeta las 280 originales de guía).
- `extract_eventos_fifa18.py`: extractor de datos de cartas de eventos.
- `generate_iconos.py`: generador de la base de iconos.
- `data/cache_mobile_stats.jsonl`: caché con los 20.525 registros del motor.
- `data/cache_eventos.jsonl`: caché de trabajo de eventos.
- [`README_JSON_CLEAN.md`](README_JSON_CLEAN.md): guía del JSON simplificado de cartas base.
- [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md): base de datos y recursos de eventos.
- [`README_ICONOS.md`](README_ICONOS.md): base de datos y recursos de Iconos.
- [`NOTICE.md`](NOTICE.md): fuentes, atribuciones y avisos de propiedad intelectual.

La exportación es generada a partir de las fuentes descritas; la correspondencia entre este documento y el archivo subido es exacta en la versión publicada (`1.1-mobile-stats`).
