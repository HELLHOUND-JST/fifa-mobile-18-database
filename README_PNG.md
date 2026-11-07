# PNG de jugadores — FIFA Mobile 18 Base (V3.0.0)

Este documento describe la colección de imágenes PNG individuales de los jugadores asociadas a las cartas base de FIFA Mobile 18 — Season 2.

## Qué contiene la colección

- **13.885 archivos PNG** documentados.
- Dimensiones: **256 × 256 píxeles**.
- Tamaño total aproximado documentado: **128,8 MB**.
- Contiene únicamente la imagen individual del jugador asociada a su carta base. No incluye el fondo de la carta, el escudo del club ni el marco completo.
- Carpeta: `players_png/{rareza}/p{fifa_id}*.png`.

### Distribución por rareza

| Rareza | Cantidad |
|---|---:|
| Master Rare (MR4) | 1 |
| Epic Rare (ER3) | 285 |
| Gold Rare (GR2) | 3.656 |
| Silver Rare (SR1) | 7.752 |
| Bronze Rare (BR0) | 2.191 |
| **Total** | **13.885** |

## Nombres de archivo

Los nombres conservan el nombre de archivo identificado en el CDN. Dependiendo del recurso pueden incluir sufijos:

- `p20801_AS.png`
- `p158023_AS.png`
- `p212218_AS2.png`
- `p235329.png`

Hay registros con variantes de nombre. El descargador contempla alternativas cuando la primera ruta consultada no está disponible; por eso no debe suponerse que todos los archivos siguen un único patrón de sufijo.

## Manifiestos

La colección incluye:

- `players_png_manifest.csv`
- `players_png_manifest.json`

Según la documentación de la herramienta, los manifiestos registran campos como:

- `fifa_id`
- nombre normalizado
- OVR y posición
- rareza
- nombre del archivo
- URL del CDN y URL de referencia
- ruta de destino
- tamaño en bytes
- estado de la descarga

El manifiesto de la copia documentada registra **13.885 resultados correctos**. Este dato describe la ejecución incluida y no garantiza que las fuentes externas sigan disponibles.

## Descargador

Script: `download_player_png.py`.

El modo exacto consulta la ficha del jugador en RenderZ para identificar el nombre de archivo de la imagen y después solicita el recurso correspondiente al CDN configurado. Si la primera variante no está disponible, el proceso prueba alternativas de nombre documentadas por el script.

La caché reanudable se guarda en:

```text
data/cache_png_downloads.jsonl
```

## Uso

Ejecuta los comandos desde la raíz del repositorio:

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

La caché permite reanudar el trabajo y evita repetir descargas ya registradas, salvo que se utilicen opciones que cambien ese comportamiento.

## Uso desde otros proyectos

Las imágenes pueden localizarse por `fifa_id` y rareza usando la ruta registrada en el manifiesto. Se recomienda leer el manifiesto en lugar de construir manualmente el nombre del PNG, ya que algunos recursos utilizan sufijos alternativos.

## Consideraciones

- Esta colección contiene imágenes individuales, no cartas completas.
- Para las composiciones de cartas completas consulta [`README_CARDS_FULL.md`](README_CARDS_FULL.md).
- Los nombres de FIFA Mobile, RenderZ y otros servicios se utilizan para identificar las referencias. La inclusión de URLs o imágenes no implica afiliación ni autorización para redistribuir recursos de terceros.
- Antes de publicar o reutilizar las imágenes, revisa [`NOTICE.md`](NOTICE.md) y las condiciones vigentes de los titulares correspondientes.
