# JSON simplificado — FIFA Mobile 18 Base (V4.0.0)

Esta guía se refiere al JSON simplificado de **cartas base**. En V4.0.0, la información de las cartas base incorpora **skill boosts reales** (13.620 del motor + 265 conservados de la guía) y **estadísticas reales del motor**; las 265 cartas con fichas originales de fifamobileguide.com son intocables. La base de eventos y la base de Iconos se distribuyen por separado y no deben confundirse con este JSON.

## Qué contiene

La exportación simplificada presenta cada jugador con identidad, edad, carta y atributos:

- **Identidad:** `fifa_id` y `name` (`short`, `full`).
- **Edad:** `age`.
- **Carta:** `card` con media, posición, club, rareza, código de fondo y temporada.
- **Estadísticas:** `stats.primary`, `stats.detailed` y `stats.goalkeeping`.
- **Totales:** `total_stats` (suma del motor de los 24 atributos detallados).
- **Metadatos:** título, versión interna de exportación (`1.1-mobile-stats`), fecha de generación, temporada, cantidad de registros, conteos por rareza/posición y `stats_source`.

## Estructura de un registro

```json
{
  "fifa_id": 20801,
  "name": {
    "short": "Cristiano Ronaldo",
    "full": "Cristiano Ronaldo"
  },
  "age": 32,
  "card": {
    "ovr": 90,
    "position": "LW",
    "club_id": 243,
    "club": "Real Madrid",
    "rarity": "Master Rare",
    "background_code": "MR4",
    "season": "Season 2 (FIFA Mobile 18)"
  },
  "total_stats": 1736,
  "stats": {
    "primary": {
      "pace": 93,
      "shooting": 94,
      "passing": 85,
      "agility": 95,
      "defending": 37,
      "physical": 78
    },
    "detailed": {},
    "goalkeeping": {
      "gk_diving": 4,
      "gk_positioning": 21,
      "reflexes": 21,
      "handling": 21
    }
  }
}
```

## Cómo interpretar la estructura

- `stats.primary`: seis valores principales según la posición del jugador. En porteros se usan `gk_diving`, `gk_positioning`, `handling`, `reflexes`, `passing` y `physical`.
- `stats.detailed`: los **24** atributos del motor, tanto en jugadores de campo como en porteros (en porteros los valores de campo son bajos, como en el juego).
- `stats.goalkeeping`: objeto con `gk_diving`, `gk_positioning`, `reflexes`, `handling` presentes en **todas** las posiciones (valores reales del motor; bajos en campo, como en el juego).
- `total_stats`: enteros; suma del motor de los 24 atributos de `stats.detailed`.
- Los valores son **sin boost**; la vista del juego muestra +13 % adicional sobre los atributos afectados por el skill boost.
- Las 265 cartas de la base con fichas originales de la guía conservan sus valores exactos de la guía (que pueden diferir 1–3 puntos del motor).

## Ejemplo de consulta

```python
import json

with open("fifa_mobile_18_base_player_stats.json", encoding="utf-8") as file:
    data = json.load(file)

players = data.get("players", [])

# Buscar un jugador por FIFA ID.
player = next((p for p in players if p.get("fifa_id") == 20801), None)

if player:
    print(player.get("name", {}).get("full"))
    print(player.get("card", {}).get("ovr"))
    print("total_stats:", player.get("total_stats"))
    print(player.get("stats", {}).get("primary"))
```

## Base de datos de cartas de eventos

La V4.0.0 incorpora una base independiente:

- `fifa_mobile_18_eventos.csv`
- `fifa_mobile_18_eventos.json`
- `fifa_mobile_18_eventos.txt`

La copia subida contiene **6.571 filas**, con `SKILL_BOOST` real (del motor) y estadísticas reales del motor (del total 1.708 filas > 99; máximo **140**). Los **37 nombres del catálogo de refuerzos** son etiquetas de refuerzo, no estadísticas. Esta base de eventos no es el JSON simplificado de cartas base. Consulta [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md) y [`README_JSON.md`](README_JSON.md) para más información.

## Base de datos de cartas Icono

La V4.0.0 incorpora una base separada de **69 cartas** (36 Icon, 16 Prime Icon, 17 WC Icon):

- `fifa_mobile_18_iconos.csv`
- `fifa_mobile_18_iconos.json`
- `fifa_mobile_18_iconos.txt`

Stats reales del motor (54) o de la guía original (15 intocables). Consulta [`README_ICONOS.md`](README_ICONOS.md).

## Otras exportaciones V4

- `fifa_mobile_18_base_completa.csv`
- `fifa_mobile_18_base_completa.json`
- `fifa_mobile_18_base_completa.txt`
- `fifa_mobile_18_skill_boost_distribucion.txt`
- `fifa_mobile_18_eventos.*`
- `fifa_mobile_18_iconos.*`

Consulta los archivos directamente para verificar sus columnas, claves y formato.

## Archivos relacionados

- [`README_JSON.md`](README_JSON.md): estructura estadística y notas sobre las exportaciones V4.
- [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md): datos y recursos gráficos de cartas de eventos.
- [`README_EVENTOS.md`](README_EVENTOS.md): documentación estadística de la base de Eventos.
- [`README_ICONOS.md`](README_ICONOS.md): documentación completa de la base de Iconos.
- [`README_PNG.md`](README_PNG.md) y [`README_CARDS_FULL.md`](README_CARDS_FULL.md): colecciones gráficas.
- [`NOTICE.md`](NOTICE.md): fuentes, atribuciones y avisos sobre derechos de terceros.
