# Guía de lectura JSON simplificada — FIFA Mobile 18 (V5.0.0)

Esta guía ofrece una orientación de lectura para las exportaciones JSON de V5.0.0. La versión actual integra cartas base, eventos/programas, estadísticas oficiales y *Skill Boosts* procedentes de RenderZ, según la procedencia declarada por el responsable del proyecto.

## Cartas base

La estructura V5 documenta:

- `total_stats`: sección/campo asociado al conjunto de estadísticas de la carta.
- `goalkeeping`: bloque que siempre está presente en la estructura, incluso cuando el jugador no es portero. Lee el valor del propio registro en lugar de asumir que siempre contiene estadísticas aplicables.
- `skill_boost`: información del refuerzo de habilidad asociado al jugador/carta, según las claves del JSON real.
- Campos de identidad y carta: ID, nombre, posición, OVR, club, rareza, fondo y temporada, de acuerdo con el registro.

Las claves internas completas pueden variar entre exportaciones. Verifica el JSON de la distribución antes de crear integraciones.

## Cartas de eventos

Los eventos tienen una estructura distinta. El nivel superior identificado en la documentación es:

```json
{
  "has_meta": {
    "metadata": {},
    "players": []
  }
}
```

La colección documentada anteriormente contiene 6.571 registros de eventos, con `SKILL_BOOST` y 30 estadísticas por registro. No asumas que las claves de eventos son idénticas a las de la base de cartas base.

## Procedencia

Según el responsable del proyecto, las estadísticas oficiales y los *Skill Boosts* oficiales se consultan desde RenderZ. El inventario técnico también indica 13.620 valores del motor y 265 registros de guía para la cobertura de estadísticas base. Consulta los metadatos y referencias del registro para conocer el contexto de cada valor.

## Ejemplo de lectura

La documentación V5 menciona como caso de consulta una carta `CR` con ID `1736`. Utiliza ese registro como referencia y comprueba sus claves reales antes de automatizar la lectura.

## Formatos y archivos relacionados

- `fifa_mobile_18_base_completa.json` — JSON de cartas base.
- `fifa_mobile_18_base_completa.csv` y `.txt` — exportaciones tabular y texto.
- `fifa_mobile_18_eventos.json` — JSON de eventos.
- `fifa_mobile_18_eventos.csv` y `.txt` — exportaciones tabular y texto de eventos.
- `README_JSON.md` — descripción detallada de estructuras.
- `README_EVENTOS.md` — catálogo y datos de eventos.
- `README_ICONOS.md` — iconos y recursos gráficos.
- `NOTICE.md` — fuentes y derechos de terceros.
