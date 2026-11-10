# Datos JSON y estadísticas — FIFA Mobile 18 Base y eventos (V4.0.0)

Este documento resume los datos estadísticos documentados para las cartas base y los datos incluidos en la nueva base de cartas de eventos.

## 1. Cartas base

La V4.0.0 amplía los datos de cartas base con:

- información de **skill boosts**; el catálogo documentado incluye **37 nombres** (consulta [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md));
- estadísticas revisadas para ofrecer valores más realistas;
- exportación completa adicional en CSV, JSON y TXT.

La documentación de versiones anteriores describía el archivo estadístico `fifa_mobile_18_base_player_stats.json`, una muestra `fifa_mobile_18_base_player_stats_SAMPLE.json` y una estructura por jugador con identidad, edad, carta y estadísticas. Las claves exactas añadidas o modificadas en V4 deben comprobarse en la exportación real.

### Exportaciones completas añadidas en V4.0.0

- `fifa_mobile_18_base_completa.csv`
- `fifa_mobile_18_base_completa.json`
- `fifa_mobile_18_base_completa.txt`
- `fifa_mobile_18_skill_boost_distribucion.txt`

El nombre identifica una exportación de la base completa; consulta los propios archivos para ver columnas, claves, orden y contenido detallado.

### Estructura de estadísticas documentada en versiones anteriores

La base de cartas base utilizaba las siguientes secciones:

- `fifa_id`: identificador numérico del jugador.
- `name`: nombres `short` y `full`.
- `age`: edad de referencia cuando está disponible.
- `card`: datos de la carta, como `ovr`, `position`, `club_id`, `club`, `rarity`, `background_code` y `season`.
- `stats.primary`: seis atributos principales según la posición.
- `stats.detailed`: atributos detallados de jugadores de campo o porteros.
- `stats.goalkeeping`: valores de portero (`gk_diving`, `gk_positioning`, `reflexes` y `handling`) en la estructura anterior.

Los ejemplos y campos descritos en esa sección representan el esquema documentado previamente; no se debe asumir que el JSON V4 conserva todas las claves exactamente igual.

## 2. Cartas de eventos

La V4.0.0 añade una base independiente en estos formatos:

- `fifa_mobile_18_eventos.csv`
- `fifa_mobile_18_eventos.json`
- `fifa_mobile_18_eventos.txt`

La copia subida contiene **6.571 filas**. Los registros incluyen el campo `SKILL_BOOST` y **30 estadísticas**. El catálogo `skill_boosts` documenta por separado **37 nombres de refuerzos de habilidad**; no son 37 estadísticas adicionales. La lista exacta está en [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md).

La documentación de esta versión no enumera aquí los nombres individuales de las 30 estadísticas ni las claves JSON. Para integraciones, consulta los encabezados de `fifa_mobile_18_eventos.csv` y las claves de `fifa_mobile_18_eventos.json` directamente. No supongas que el esquema de eventos replica el de la base de cartas base.

## 3. Diferencias entre colecciones

| Colección | Exportaciones | Contenido documentado |
|---|---|---|
| Cartas base | `fifa_mobile_18_base_player_stats.*`, `fifa_mobile_18_base_completa.*` | Datos y estadísticas de cartas base; V4 añade *skill boosts* y estadísticas revisadas. |
| Cartas de eventos | `fifa_mobile_18_eventos.csv/.json/.txt` | 6.571 filas, `SKILL_BOOST` y 30 estadísticas; catálogo separado de 37 nombres de refuerzos. |

Mantén separadas ambas bases al consultar, importar o combinar registros. No se han proporcionado reglas de unión completas ni garantías de que todos los identificadores sean únicos entre colecciones.

## 4. Ejemplos de lectura

### Base JSON de cartas base (estructura previa documentada)

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
```

Este ejemplo corresponde a la estructura documentada anteriormente. Si el archivo V4 utiliza claves diferentes o adicionales, adapta la consulta al contenido real.

### Base JSON de eventos

```python
import json

with open("fifa_mobile_18_eventos.json", encoding="utf-8") as file:
    events_data = json.load(file)

# Inspecciona el nivel superior antes de recorrer los registros.
print(type(events_data).__name__)
if isinstance(events_data, dict):
    print("Claves superiores:", list(events_data.keys()))
elif isinstance(events_data, list):
    print("Registros:", len(events_data))
```

El ejemplo evita asumir una estructura de raíz que no está especificada en el resumen de actualización.

## 5. Archivos y herramientas relacionados

- `generate_skill_boost.py`: herramienta relacionada con la generación de *skill boosts*.
- `fifa_mobile_18_skill_boost_distribucion.txt`: distribución de *skill boosts*.
- `extract_eventos_fifa18.py`: extractor de datos de cartas de eventos.
- `data/cache_eventos.jsonl`: caché de trabajo de eventos.
- [`README_JSON_CLEAN.md`](README_JSON_CLEAN.md): guía del JSON simplificado de cartas base.
- [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md): base de datos y recursos de eventos.
- [`NOTICE.md`](NOTICE.md): fuentes, atribuciones y avisos de propiedad intelectual.
