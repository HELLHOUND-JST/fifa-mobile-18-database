# Base de cartas de eventos y programas — FIFA Mobile 18 (V5.0.0)

Este documento describe la colección de cartas de eventos/programas y los recursos relacionados incorporados al proyecto.

## 1. Base de datos

Archivos documentados:

- `fifa_mobile_18_eventos.csv`
- `fifa_mobile_18_eventos.json`
- `fifa_mobile_18_eventos.txt`

Inventario comunicado para la colección V4 que se conserva en V5:

- **6.571 filas** de eventos.
- Campo `SKILL_BOOST`.
- **30 estadísticas** por registro, según el resumen de la versión anterior.

La base de eventos es independiente de la base de cartas base. No se debe asumir que comparten los mismos IDs, estructura JSON, claves, contextos de estadísticas o manifiestos.

## 2. Estructura JSON

La documentación de V5 identifica un objeto superior `has_meta` con las secciones `metadata` y `players`:

```json
{
  "has_meta": {
    "metadata": {},
    "players": []
  }
}
```

Este ejemplo solo representa la estructura superior. Consulta `fifa_mobile_18_eventos.json` para obtener las claves reales de cada carta y jugador.

## 3. Estadísticas y Skill Boosts

Según el responsable del proyecto, las estadísticas oficiales del juego y los *Skill Boosts* oficiales se obtienen de RenderZ. Los registros de eventos documentados incluyen `SKILL_BOOST` y 30 estadísticas. La base de eventos no debe confundirse con el catálogo de 37 nombres de *Skill Boost* descrito en versiones anteriores: esos 37 elementos son nombres/etiquetas de refuerzo, no estadísticas adicionales.

Los campos exactos, los tipos y la interpretación deben verificarse en los encabezados del CSV o las claves del JSON distribuidos.

## 4. Recursos gráficos

- `events_png/`: **6.570 PNG** individuales de jugadores de eventos; la variante documentada anteriormente es Action Shot.
- `events_cards/`: **6.483 cartas completas** de eventos en PNG de 256 × 256.
- `events_logos/`: **92 logos** de eventos/programas, según el inventario V4.
- `assets_cards/backgrounds/`: fondos de eventos y World Cup; V4 informó 931 recursos añadidos en esta carpeta compartida.
- `assets_cards/clubs/`: V4 informó 47 recursos nuevos de clubes.

Los recursos `17_FAV` y `17_SBC_PLAYER` no se encontraron en el CDN durante la consulta documentada en V4; esa observación no demuestra que no puedan existir en otra fuente.

## 5. Manifiestos

La colección utiliza:

- `events_manifest.csv`
- `events_manifest.json`

Consulta sus encabezados y claves para identificar los campos que enlazan registros, imágenes individuales, cartas completas y logos. No asumas que todos los tipos de recursos aparecen asociados uno a uno.

## 6. Herramientas conocidas

- `extract_eventos_fifa18.py`: extracción de datos de eventos.
- `generate_events_assets.py`: preparación/generación de recursos gráficos de eventos.
- `generate_skill_boost.py`: herramienta de procesamiento de *Skill Boosts*.
- `reconcile_guide.py`: conciliación de referencias.
- `inspect_event_assets.py`: inspección de recursos gráficos de eventos.
- `_guide_by_fifa_id.py`: herramienta auxiliar por FIFA ID.

Consulta los scripts y su `--help` para conocer opciones vigentes; no se asumen argumentos no documentados.

## 7. Uso recomendado

1. Consulta `fifa_mobile_18_eventos.csv` o `.json` para localizar la carta.
2. Utiliza `events_manifest.csv` o `.json` para localizar los recursos visuales.
3. Distingue PNG individuales (`events_png/`) de cartas completas (`events_cards/`).
4. Consulta `README_ICONOS.md` para logos e iconos de programas.
5. Comprueba la fuente y el contexto de cada dato antes de reutilizarlo.

## 8. Git LFS y derechos

Los recursos grandes se gestionan parcialmente mediante Git LFS. Instala Git LFS para recuperar los objetos al clonar. Las cartas, imágenes, logos, escudos, fondos y datos pueden estar sujetos a derechos y condiciones de terceros. Consulta `NOTICE.md`; la atribución no equivale a permiso para redistribuir.
