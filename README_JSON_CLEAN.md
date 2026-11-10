# JSON simplificado — FIFA Mobile 18 Base (V4.0.0)

Esta guía se refiere al JSON simplificado de **cartas base** documentado en versiones anteriores. En V4.0.0, la información de las cartas base incorpora *skill boosts* y estadísticas revisadas para ofrecer valores más realistas. La nueva base de eventos se distribuye por separado y no debe confundirse con este JSON.

## Estructura documentada anteriormente

La exportación simplificada previa presentaba cada jugador con identidad, edad, carta y atributos:

- **Identidad:** `fifa_id` y `name` (`short`, `full`).
- **Edad:** `age`.
- **Carta:** `card` con media, posición, club, rareza, código de fondo y temporada.
- **Estadísticas:** `stats.primary`, `stats.detailed` y `stats.goalkeeping`.
- **Metadatos:** título, versión interna de exportación, fecha de generación, temporada, cantidad de registros y conteos por rareza y posición.

V4.0.0 añade información de *skill boosts* y presenta estadísticas revisadas. El catálogo del proyecto documenta **37 nombres de refuerzos de habilidad**; consulta [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md) para ver la lista exacta. La ruta y las claves de los nuevos valores deben comprobarse en el JSON V4 de la distribución; no se infieren aquí campos que no han sido especificados.

## Cómo interpretar la estructura anterior

- `stats.primary`: seis valores principales según la posición del jugador.
- `stats.detailed`: atributos detallados para jugadores de campo o porteros.
- `stats.goalkeeping`: bloque de atributos de portero; en la estructura anterior aparecía como `null` para las demás posiciones.
- En la estructura anterior, los valores numéricos se representaban como enteros y `null` indicaba que el campo no aplicaba o no estaba disponible.

Comprueba el JSON V4 antes de asumir que todos los nombres, cantidades de campos y reglas de `null` permanecen sin cambios.

## Ejemplo de consulta de la estructura previa

```python
import json

with open("fifa_mobile_18_base_player_stats.json", encoding="utf-8") as file:
    data = json.load(file)

players = data.get("players", [])

# Buscar un jugador por FIFA ID, usando la estructura anterior.
player = next((p for p in players if p.get("fifa_id") == 20801), None)

if player:
    print(player.get("name", {}).get("full"))
    print(player.get("card", {}).get("ovr"))
    print(player.get("stats", {}).get("primary"))
```

El ejemplo muestra la estructura documentada previamente y debe adaptarse si el JSON V4 cambia sus claves o niveles.

## Base de datos de cartas de eventos

La V4.0.0 incorpora una base independiente:

- `fifa_mobile_18_eventos.csv`
- `fifa_mobile_18_eventos.json`
- `fifa_mobile_18_eventos.txt`

La copia subida contiene **6.571 filas**, con `SKILL_BOOST` y **30 estadísticas**. El catálogo de **37 nombres de refuerzos de habilidad** es independiente de esos 30 campos estadísticos. Esta base de eventos no es el JSON simplificado de cartas base. Consulta [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md) y [`README_JSON.md`](README_JSON.md) para más información.

## Otras exportaciones V4

- `fifa_mobile_18_base_completa.csv`
- `fifa_mobile_18_base_completa.json`
- `fifa_mobile_18_base_completa.txt`
- `fifa_mobile_18_skill_boost_distribucion.txt`

Consulta los archivos directamente para verificar sus columnas, claves y formato.

## Archivos relacionados

- [`README_JSON.md`](README_JSON.md): estructura estadística y notas sobre las exportaciones V4.
- [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md): datos y recursos gráficos de cartas de eventos.
- [`README_PNG.md`](README_PNG.md) y [`README_CARDS_FULL.md`](README_CARDS_FULL.md): colecciones gráficas.
- [`NOTICE.md`](NOTICE.md): fuentes, atribuciones y avisos sobre derechos de terceros.
