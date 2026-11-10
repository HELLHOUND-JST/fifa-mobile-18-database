# PNG de jugadores — FIFA Mobile 18 Base y eventos (V4.0.0)

Este documento describe las colecciones de imágenes PNG individuales de jugadores asociadas a cartas base y cartas de eventos de FIFA Mobile 18 — Season 2.

## Colección de cartas base

La colección documentada en V3.0.0 contiene:

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

## Colección de cartas de eventos (V4.0.0)

La V4.0.0 incorpora una colección adicional:

- Carpeta: `events_png/`.
- **6.570 archivos PNG** de jugadores asociados a cartas de eventos.
- Variante disponible: **Action Shot únicamente**.
- La colección es independiente de `players_png/`, que contiene las imágenes individuales de jugadores de cartas base.

El resumen de actualización no especifica las dimensiones, nombres de archivo o esquema de manifiesto de `events_png/`. Consulta la carpeta y los manifiestos reales antes de asumir esas propiedades.

## Manifiestos

Para PNG individuales de cartas base, la documentación anterior identifica:

- `players_png_manifest.csv`
- `players_png_manifest.json`

Para recursos de eventos se incorpora:

- `events_manifest.csv`
- `events_manifest.json`

El manifiesto de eventos corresponde a la colección de recursos de eventos y puede incluir información de más de un tipo de recurso. Consulta sus encabezados y claves para identificar las columnas, rutas y relaciones exactas. No se debe asumir que su estructura es igual a la de los manifiestos de la colección base.

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

Estos comandos se refieren al descargador de imágenes de cartas base. Para los recursos PNG de eventos, consulta `generate_events_assets.py` y su ayuda; no se asumen opciones no confirmadas.

## Uso desde otros proyectos

- Para imágenes base, relaciona `fifa_id` y ruta mediante `players_png_manifest.csv` o `.json`.
- Para imágenes de eventos, consulta `events_manifest.csv` o `.json` y comprueba qué campos identifican cada PNG.
- Distingue la imagen individual del jugador de la composición de la carta completa.
- No asumas que los sufijos, nombres o rutas de eventos son iguales a los de las cartas base.

## Consideraciones

- La colección base y la colección de eventos son recursos distintos.
- `events_png/` contiene únicamente la variante Action Shot según el registro de V4.0.0.
- Las imágenes, marcas y otros elementos gráficos pueden pertenecer a EA, sus licenciantes, RenderZ u otros titulares.
- La inclusión de URLs, imágenes o logotipos no implica afiliación ni autorización para redistribuir recursos de terceros.
- Antes de publicar o reutilizar imágenes, revisa [`NOTICE.md`](NOTICE.md) y las condiciones vigentes de los titulares correspondientes.
