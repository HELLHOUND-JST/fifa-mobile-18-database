# PNG de jugadores — FIFA Mobile 18 Base, eventos e Iconos (V4.0.0)

Este documento describe las colecciones de imágenes PNG individuales de jugadores asociadas a las cartas de FIFA Mobile 18 — Season 2: cartas base, cartas de eventos y cartas Icono/Prime Icon/WC Icon.

## Colección de cartas base

La colección base documentada en V3.0.0 contiene:

- **13.885 archivos PNG**.
- Dimensiones: **256 × 256 píxeles**.
- Tamaño total aproximado documentado: **128,8 MB**.
- Imagen individual del jugador asociada a su carta base; no incluye el fondo, escudo del club ni marco completo.
- Ruta: `players_png/{rareza}/p{fifa_id}*.png`.

### Distribución por rareza documentada en V3.0.0

| Rareza | Cantidad |
|---|---:|
| Master Rare (MR4) | 1 |
| Epic Rare (ER3) | 285 |
| Gold Rare (GR2) | 3.656 |
| Silver Rare (SR1) | 7.752 |
| Bronze Rare (BR0) | 2.191 |
| **Total** | **13.885** |

Según el registro de actualización V4.0.0, los PNG originales de jugadores base no se modificaron; las novedades descritas para esta versión son adiciones.

## Colección de cartas de eventos

La V4.0.0 incorpora una colección adicional:

- Carpeta: `events_png/`.
- **6.570 archivos PNG** de jugadores asociados a cartas de eventos.
- Variante disponible: **Action Shot únicamente**.
- La colección es independiente de `players_png/`, que contiene las imágenes individuales de jugadores de cartas base.

La variante Action Shot en eventos aplica a **todas** las cartas de la base de eventos (compuestas como cartas completas en `events_cards/`).

## Colección de cartas Icono

La V4.0.0 incorpora la colección de Iconos:

- Carpeta: `icons_png/` (agrupada por rareza: `Icon/`, `Prime_Icon/`, `WC_Icon/`).
- **66 renders PNG únicos** (variante de la carta; nombres originales del CDN).
- Las 69 cartas Icono usan **66 renders**: tres pares de cartas (Pelé 99 CF/ST, Ronaldo Nazário 98 ST/CF, Thierry Henry 98 ST/LW) comparten el mismo archivo de render en RenderZ.
- Subidos con nombre `p{base_fifa_id}{_SUFIJO}.png` (Icons/Prime: sufijos `_IC1`/`PI1`; WC Icon: sin sufijo, ruta `players_18wc/`).
- Los iconos de programa de Icon (`program_17_ICONS.png`) y WC Icon (`program_17_WCICON.png`) están en `icons_logos/`; los Prime Icons no muestran icono de programa en RenderZ.

## Manifiestos

Para PNG individuales de cartas base, la documentación anterior identifica:

- `players_png_manifest.csv`
- `players_png_manifest.json`

Para recursos de eventos se incorpora:

- `events_manifest.csv`
- `events_manifest.json`

Para recursos de Iconos se incorpora:

- `icons_manifest.csv`
- `icons_manifest.json`

Los manifiestos de eventos y de Iconos corresponden a su colección respectiva y pueden incluir información de más de un tipo de recurso. Consulta sus encabezados y claves para identificar las columnas, rutas y relaciones exactas. No se debe asumir que su estructura es igual a la de los manifiestos de la colección base.

## Nombres de archivo de la colección base

Los nombres documentados para la colección base conservan el nombre identificado en el CDN. Algunos ejemplos:

- `p20801_AS.png`
- `p158023_AS.png`
- `p212218_AS2.png`
- `p235329.png`

Hay registros con variantes de nombre. Para localizar imágenes base, se recomienda consultar `players_png_manifest.csv` o `.json` en lugar de construir manualmente el nombre.

## Descargador de la colección base

Script: `download_player_png.py`.

La herramienta documentada consulta la ficha del jugador para identificar el nombre de archivo de la imagen y después solicita el recurso al CDN configurado. La caché reanudable de la colección base es:

```text
data/cache_png_downloads.jsonl
```

## Uso del descargador de cartas base

Ejecuta desde la raíz del repositorio:

```bash
# Prueba limitada
python download_player_png.py --test

# Descarga con 12 trabajadores
python download_player_png.py --workers 12

# Modo rápido con límite de 100 registros
python download_player_png.py --fast --limit 100

# Descargar IDs específicos
python download_player_png.py --only-ids 20801,158023

# Exportar/manifiestos desde la información almacenada
python download_player_png.py --export-only

# Consultar todas las opciones
python download_player_png.py --help
```

Estos comandos se refieren al descargador de imágenes de cartas base. Para los recursos PNG de eventos e Iconos, consulta `generate_events_assets.py` y `generate_iconos_assets.py` y su ayuda; no se asumen opciones no confirmadas.

## Uso desde otros proyectos

- Para imágenes base, relaciona `fifa_id` y ruta mediante `players_png_manifest.csv` o `.json`.
- Para imágenes de eventos, consulta `events_manifest.csv` o `.json` y comprueba qué campos identifican cada PNG.
- Para imágenes de Iconos, consulta `icons_manifest.csv` o `.json`; en particular `player_file` (archivo original del CDN) y `player_png` (ruta local).
- Distingue la imagen individual del jugador de la composición de la carta completa.
- No asumas que los sufijos, nombres o rutas de eventos o Iconos son iguales a los de las cartas base.

## Consideraciones

- La colección base, la colección de eventos y la colección de Iconos son recursos distintos.
- `events_png/` contiene únicamente la variante Action Shot según el registro de V4.0.0.
- Las imágenes, marcas y otros elementos gráficos pueden pertenecer a EA, sus licenciantes, RenderZ u otros titulares.
- La inclusión de URLs, imágenes o logotipos no implica afiliación ni autorización para redistribuir recursos de terceros.
- Antes de publicar o reutilizar imágenes, revisa [`NOTICE.md`](NOTICE.md) y las condiciones vigentes de los titulares correspondientes.
