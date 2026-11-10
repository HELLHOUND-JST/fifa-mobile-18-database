# Cartas completas PNG — FIFA Mobile 18 Base y eventos (V4.0.0)

Este documento describe las composiciones PNG de cartas completas de FIFA Mobile 18 — Season 2. La colección comprende cartas base documentadas desde V3.0.0 y cartas completas de eventos incorporadas en V4.0.0.

## Cartas base

La colección base documentada en V3.0.0 contiene:

- **13.885 cartas completas** en PNG.
- Dimensiones: **256 × 256 píxeles**.
- Ruta documentada: `cards_full/{rareza}/card_{fifa_id}.png`.
- Cada archivo combina la imagen del jugador, fondo, escudo del club y textos de la carta.
- Manifiestos: `cards_full_manifest.csv` y `cards_full_manifest.json`.

### Distribución por rareza documentada en V3.0.0

| Rareza | Cantidad |
|---|---:|
| Master Rare | 1 |
| Epic Rare | 285 |
| Gold Rare | 3.656 |
| Silver Rare | 7.752 |
| Bronze Rare | 2.191 |
| **Total** | **13.885** |

La información anterior describe la colección base de V3.0.0. Según el resumen de la actualización V4.0.0, los recursos base existentes no se modificaron; la V4 añadió recursos de eventos y archivos adicionales.

## Cartas completas de eventos

La V4.0.0 incorpora una colección separada en:

- Carpeta: `events_cards/`.
- Cantidad: **6.483 cartas completas**.
- Formato: PNG.
- Dimensiones: **256 × 256 píxeles**.
- Manifiestos de eventos: `events_manifest.csv` y `events_manifest.json`.

La base de datos de eventos contiene **6.571 filas**, mientras que el conjunto de cartas completas contiene **6.483 PNG**. Son recuentos de recursos diferentes; la diferencia no se interpreta aquí como un error o como una causa específica, porque el resumen de actualización no explica esa relación.

## Recursos utilizados y añadidos en V4.0.0

El proyecto utiliza recursos gráficos y tipográficos descritos en la documentación de cartas base y amplía los recursos para cartas de eventos:

- **Fondos:** se añadieron **931 recursos** en `assets_cards/backgrounds/`, incluidos fondos de World Cup y de eventos.
- **Clubes:** se añadieron **47 recursos** en `assets_cards/clubs/`.
- **Logos de programas:** `events_logos/` contiene **92 iconos/logotipos**. Los recursos `17_FAV` y `17_SBC_PLAYER` no se encontraron en el CDN durante la recopilación.
- **Jugadores de eventos:** `events_png/` contiene **6.570 PNG**, únicamente de variante Action Shot.

La V3.0.0 documentaba tipografías Knul Medium/Regular, fondos, imágenes individuales y escudos de clubes para la composición de cartas base. Los derechos y permisos aplicables a los componentes originales se explican en [`NOTICE.md`](NOTICE.md).

## Composición de las cartas base

Las cartas base se generan programáticamente a partir de recursos gráficos y una referencia de distribución visual. No son capturas de pantalla de una sesión autenticada de RenderZ ni una afirmación de que sean archivos oficiales publicados por EA.

La documentación de la colección base describe:

- **Tipografía:** Knul Medium y Knul Regular para los textos de la carta.
- **Fondos:** recursos de la colección `backgrounds_18/` y recursos auxiliares bajo `assets_cards/backgrounds/`, según la versión.
- **Imagen del jugador:** recursos individuales de `players_png/`.
- **Escudos de clubes:** recursos de `assets_cards/clubs/`.
- **Distribución visual:** referencia del diseño de carta de RenderZ.

La distribución técnica detallada para las cartas base está documentada en las versiones previas de este archivo y en el generador `generate_full_cards.py`.

## Manifiestos

Para la colección base:

- `cards_full_manifest.csv`
- `cards_full_manifest.json`

Para la colección de eventos:

- `events_manifest.csv`
- `events_manifest.json`

Consulta los encabezados y claves reales de cada manifiesto para conocer sus campos y las relaciones que contienen. No se debe asumir que los dos pares de manifiestos comparten el mismo esquema.

## Generador de cartas base

Script: `generate_full_cards.py`.

```bash
# Prueba de generación
python generate_full_cards.py --test

# Generar con 8 trabajadores
python generate_full_cards.py --workers 8

# Sobrescribir los archivos existentes
python generate_full_cards.py --workers 8 --overwrite

# Generar cartas para IDs concretos
python generate_full_cards.py --only-ids 20801,158023

# Consultar las opciones disponibles
python generate_full_cards.py --help
```

Según la documentación de la herramienta, sin `--overwrite` la generación omite los archivos que ya existen.

## Herramientas de eventos

La V4.0.0 incorpora `generate_events_assets.py` e `inspect_event_assets.py` para el flujo de recursos de eventos. El resumen de actualización no proporciona argumentos de línea de comandos concretos para estos scripts; consulta su `--help` y el código antes de ejecutarlos.

## Relación con las imágenes individuales

- `players_png/`: imágenes individuales de jugadores de cartas base.
- `events_png/`: 6.570 imágenes individuales de jugadores de eventos; solo Action Shot.
- `cards_full/`: cartas base completas.
- `events_cards/`: 6.483 cartas completas de eventos.

Las imágenes individuales de jugadores no equivalen a composiciones de cartas completas. Consulta [`README_PNG.md`](README_PNG.md) y [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md).

## Git LFS

La subida V4.0.0 reportó **11.242 objetos LFS** y aproximadamente **513 MB transferidos**. Para obtener los PNG y otros archivos grandes en una copia local del repositorio, instala y configura Git LFS.

## Consideraciones

- Las composiciones son resultados generados mediante herramientas del proyecto a partir de recursos y referencias gráficas; no deben describirse como capturas oficiales ni como publicaciones oficiales de EA.
- Las fuentes, imágenes de jugadores, fondos, escudos de clubes, logotipos de eventos y otros elementos visuales pueden estar sujetos a derechos de terceros.
- La referencia al diseño de RenderZ no implica que RenderZ haya creado, aprobado o respaldado estas composiciones.
- Dar crédito no concede permiso para publicar o redistribuir materiales protegidos. Revisa [`NOTICE.md`](NOTICE.md) y verifica las autorizaciones necesarias antes de distribuir imágenes o recursos.
