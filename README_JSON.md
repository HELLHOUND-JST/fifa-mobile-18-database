# Estructura JSON — FIFA Mobile 18 Base y eventos (V5.0.0)

Esta guía describe los esquemas JSON identificados en la documentación V5.0.0. La base de cartas base y la base de eventos son estructuras distintas; no deben combinarse suponiendo que comparten las mismas claves.

## 1. JSON de cartas base

La exportación actual incorpora estadísticas y *Skill Boosts* oficiales del juego, obtenidos de RenderZ según la procedencia declarada para el proyecto.

### Campos y estructuras identificados

- `fifa_id`: identificador del jugador/carta.
- `card`: información de la carta, como OVR, posición, club, rareza, fondo y temporada, según el registro.
- `total_stats`: sección/campo de estadísticas totales documentado para V5.
- `goalkeeping`: bloque de portero que **siempre está presente** en la estructura V5. Debe leerse según su contenido; no se debe asumir que su valor es idéntico para jugadores de campo y porteros.
- `skill_boost`: información del refuerzo de habilidad asociado, cuando aparece en la exportación.
- Los metadatos y campos de fuente deben consultarse en el archivo JSON real.

> **Importante:** el resumen de actualización identifica `total_stats` y `goalkeeping` siempre presente, pero no transcribe el esquema completo de cada objeto. Por ello, esta guía no inventa subclaves ni tipos de dato que no estén confirmados en el JSON distribuido.

### Procedencia de las estadísticas

Según el responsable del proyecto, las estadísticas oficiales del juego y los *Skill Boosts* oficiales proceden de RenderZ. El resumen técnico de la base completa indica un desglose de **13.620 registros del motor + 265 registros de guía**. Conserva ese desglose al describir el inventario y consulta los metadatos/fuentes de cada registro para entender su contexto.

### Ejemplo de lectura

La actualización de documentación menciona un ejemplo de lectura para una carta de rareza `CR` con ID `1736`. Úsalo como referencia para localizar un caso en el JSON real; no asumas campos no presentes en ese registro.

## 2. JSON de eventos

La estructura superior documentada para los eventos utiliza `has_meta`, con secciones `metadata` y `players`:

```json
{
  "has_meta": {
    "metadata": {},
    "players": []
  }
}
```

Este fragmento representa únicamente la forma superior documentada. Las claves de cada jugador/carta deben leerse desde `fifa_mobile_18_eventos.json`.

La base de eventos comunicada en V4 contiene **6.571 registros**, con el campo `SKILL_BOOST` y **30 estadísticas**. V5 integra esta colección en el catálogo general. No se debe asumir que comparte el mismo esquema de `total_stats` de la base de cartas base.

## 3. Ejemplo de inspección segura en Python

```python
import json
from pathlib import Path

path = Path("fifa_mobile_18_base_completa.json")
with path.open(encoding="utf-8") as file:
    data = json.load(file)

print("Tipo raíz:", type(data).__name__)
if isinstance(data, dict):
    print("Claves raíz:", list(data.keys()))
    print("Total stats:", data.get("total_stats"))

    players = data.get("players", [])
    print("Jugadores:", len(players) if isinstance(players, list) else "revisar estructura")
```

Para inspeccionar la estructura de eventos:

```python
import json

with open("fifa_mobile_18_eventos.json", encoding="utf-8") as file:
    events = json.load(file)

print("Claves raíz:", list(events.keys()) if isinstance(events, dict) else type(events).__name__)
if isinstance(events, dict):
    print("Claves has_meta:", list(events.get("has_meta", {}).keys()))
```

Adapta los nombres de archivo y las consultas a la copia concreta que descargues.

## 4. Relación con CSV y TXT

Las exportaciones CSV y TXT son útiles para hojas de cálculo y lectura directa. El delimitador CSV puede ser `;` según la exportación; comprueba el encabezado y el separador del archivo real antes de importarlo.

## 5. Archivos relacionados

- `fifa_mobile_18_base_completa.json`: exportación JSON completa de cartas base.
- `fifa_mobile_18_base_completa.csv` / `.txt`: formatos tabular y texto de la base completa.
- `fifa_mobile_18_eventos.json`: exportación JSON de eventos.
- `fifa_mobile_18_eventos.csv` / `.txt`: formatos tabular y texto de eventos.
- `README_JSON_CLEAN.md`: orientación de lectura simplificada.
- `README_EVENTOS.md`: catálogo y campos de eventos.
- `NOTICE.md`: fuentes, atribuciones y avisos de propiedad intelectual.
