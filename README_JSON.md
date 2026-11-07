# Estructura del JSON — FIFA Mobile 18 Base con estadísticas

**Proyecto:** V3.0.0  
**Archivo principal:** `fifa_mobile_18_base_player_stats.json`  
**Muestra:** `fifa_mobile_18_base_player_stats_SAMPLE.json`  
**Registros de la copia documentada:** 13.885 jugadores

Este documento explica la estructura de la exportación JSON ampliada que acompaña a la base de cartas de FIFA Mobile 18 — Season 2. La V3.0.0 incorpora además colecciones de imágenes PNG, documentadas por separado en [`README_PNG.md`](README_PNG.md) y [`README_CARDS_FULL.md`](README_CARDS_FULL.md).

## Estructura general

El archivo contiene cuatro secciones principales:

```json
{
  "_readme": "Descripción breve del archivo",
  "metadata": {
    "title": "FIFA Mobile 18 (Temporada 2) - Cartas base con estadisticas",
    "version": "1.0-clean",
    "generated_at": "fecha ISO 8601",
    "season": "FIFA Mobile 18 - Season 2",
    "total_cards": 13885,
    "counts_by_rarity": {},
    "counts_by_position": {},
    "how_to_read": {}
  },
  "schema": {},
  "players": [
    {
      "fifa_id": 20801,
      "name": {"short": "Cristiano Ronaldo", "full": "Cristiano Ronaldo"},
      "age": 32,
      "card": {},
      "stats": {}
    }
  ]
}
```

La clave `metadata.version` describe la versión interna de esa exportación JSON; no debe confundirse automáticamente con la versión global del repositorio (`3.0.0`).

## Secciones de cada jugador

### `fifa_id`

Identificador numérico utilizado para reconocer al jugador y relacionar sus registros.

### `name`

- `short`: nombre corto.
- `full`: nombre completo.

Los valores de esta exportación están normalizados para facilitar su uso en herramientas y scripts.

### `age`

Edad registrada en la referencia histórica incluida en la base. Se almacena como número entero cuando está disponible.

### `card`

Información de la carta base:

| Clave | Descripción |
|---|---|
| `ovr` | Media general de la carta móvil. |
| `position` | Posición de la carta (`GK`, `CB`, `ST`, `LW`, etc.). |
| `club_id` | Identificador numérico del club. |
| `club` | Nombre del club. |
| `rarity` | Categoría de rareza. |
| `background_code` | Código de fondo, como `MR4`, `ER3`, `GR2`, `SR1` o `BR0`. |
| `season` | Temporada asociada a la carta. |

### `stats.primary`

Contiene seis atributos principales. Para jugadores de campo se utilizan `pace`, `shooting`, `passing`, `agility`, `defending` y `physical`.

Para porteros se utilizan `gk_diving`, `gk_positioning`, `handling`, `reflexes`, `passing` y `physical`.

### `stats.detailed`

Incluye atributos detallados. La estructura de jugadores de campo contiene 20 campos:

`sprint_speed`, `acceleration`, `strength`, `ball_control`, `dribbling`, `heading`, `finishing`, `shot_power`, `long_shot`, `positioning`, `tackling`, `marking`, `aggression`, `composure`, `awareness`, `reactions`, `free_kick`, `short_passing`, `long_passing` y `crossing`.

Para porteros se utiliza una estructura de 16 campos, sin `finishing`, `shot_power`, `long_shot` ni `positioning`.

### `stats.goalkeeping`

En los porteros contiene un objeto con cuatro valores: `gk_diving`, `gk_positioning`, `reflexes` y `handling`.

En jugadores que no son porteros aparece como `null`, porque ese bloque no aplica a su posición.

## Tipos de datos

- Los identificadores, edades y atributos numéricos se guardan como números, no como cadenas.
- `null` representa un campo que no aplica o un dato no disponible en esa estructura.
- Las claves mantienen nombres consistentes en inglés para facilitar su consulta desde código.
- El archivo utiliza codificación UTF-8.

## Ejemplo de lectura en Python

```python
import json

with open("fifa_mobile_18_base_player_stats.json", encoding="utf-8") as file:
    database = json.load(file)

print("Total de jugadores:", database["metadata"]["total_cards"])

# El archivo está ordenado por media de carta, de mayor a menor.
player = database["players"][0]
print(player["name"]["full"])
print("OVR:", player["card"]["ovr"])
print("Ritmo:", player["stats"]["primary"].get("pace"))

# Porteros con al menos 85 de reflejos.
goalkeepers = [
    player for player in database["players"]
    if player["card"]["position"] == "GK"
    and player["stats"]["goalkeeping"] is not None
    and player["stats"]["goalkeeping"]["reflexes"] is not None
    and player["stats"]["goalkeeping"]["reflexes"] >= 85
]

print("Porteros encontrados:", len(goalkeepers))
```

## Archivos relacionados

- `fifa_mobile_18_base_player_stats.csv`: misma colección en formato tabular para hojas de cálculo y herramientas compatibles con CSV separado por `;`.
- `fifa_mobile_18_base_player_stats_SAMPLE.json`: muestra reducida para revisar la estructura sin cargar el archivo completo.
- `fifa_mobile_18_base.json`: base original de cartas, con campos adicionales de referencia y nombres UTF-8.
- `players_png/`: colección de imágenes individuales de los jugadores. Consulta [`README_PNG.md`](README_PNG.md).
- `cards_full/`: composiciones PNG de cartas completas. Consulta [`README_CARDS_FULL.md`](README_CARDS_FULL.md).

## Nota sobre las exportaciones

El JSON incluido es una exportación ya generada. Los scripts `organize_json.py` y `clean_json.py` forman parte de las utilidades de estructuración, pero la reproducción completa del proceso puede requerir archivos intermedios que no se incluyen en esta distribución.

Para conocer el proyecto completo, sus referencias consultadas y los avisos de propiedad intelectual, consulta [`README.md`](README.md) y [`NOTICE.md`](NOTICE.md).
