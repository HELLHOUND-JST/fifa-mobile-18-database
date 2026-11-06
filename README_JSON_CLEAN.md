# JSON simplificado — FIFA Mobile 18 Base

Archivo: **`fifa_mobile_18_base_player_stats.json`**  
Muestra: **`fifa_mobile_18_base_player_stats_SAMPLE.json`**  
Registros: **13.885 jugadores**

Esta exportación presenta cada jugador en una estructura compacta con identidad, edad, carta y atributos. Se omiten enlaces y campos auxiliares para que sea más sencilla de consultar desde aplicaciones, scripts y herramientas externas.

## Qué contiene

- **Identidad:** `fifa_id` y `name` (`short`, `full`).
- **Edad:** `age`.
- **Carta:** `card` con media, posición, club, rareza, código de fondo y temporada.
- **Estadísticas:** `stats.primary`, `stats.detailed` y `stats.goalkeeping`.
- **Metadatos:** título, versión de exportación, fecha de generación, temporada, cantidad de registros y conteos por rareza y posición.

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
    "goalkeeping": null
  }
}
```

## Cómo interpretar las estadísticas

- `stats.primary`: seis valores principales. En jugadores de campo se usan `pace`, `shooting`, `passing`, `agility`, `defending` y `physical`. En porteros se usan `gk_diving`, `gk_positioning`, `handling`, `reflexes`, `passing` y `physical`.
- `stats.detailed`: veinte atributos para jugadores de campo y dieciséis para porteros. Los campos que no corresponden a una posición se omiten de esa estructura.
- `stats.goalkeeping`: objeto con `gk_diving`, `gk_positioning`, `reflexes` y `handling` para porteros; `null` para las demás posiciones.
- Los valores numéricos son enteros. `null` significa que el bloque no aplica o que el valor no está disponible.

## Ejemplo de consulta

```python
import json

with open("fifa_mobile_18_base_player_stats.json", encoding="utf-8") as file:
    data = json.load(file)

players = data["players"]

# Obtener los jugadores con OVR igual o superior a 85.
elite_players = [
    player for player in players
    if player["card"]["ovr"] >= 85
]

# Buscar un jugador por su FIFA ID.
player = next((p for p in players if p["fifa_id"] == 20801), None)
if player:
    print(player["name"]["full"], player["stats"]["primary"])
```

Para la explicación completa de las claves y tipos de datos, consulta [`README_JSON.md`](README_JSON.md). Para fuentes, atribuciones y avisos sobre derechos de terceros, consulta [`NOTICE.md`](NOTICE.md).
