# Colecciones PNG de jugadores — FIFA Mobile 18 (V5.0.0)

Este documento resume las colecciones de imágenes individuales de jugadores de cartas base y de eventos/programas documentadas para V5.0.0.

## 1. Imágenes individuales de cartas base

- Carpeta: `players_png/`.
- Cantidad documentada: **13.885 PNG**.
- Dimensiones históricas documentadas: **256 × 256 píxeles**.
- Contenido: imagen individual del jugador, sin fondo de carta, escudo ni marco completo.
- Manifiestos: `players_png_manifest.csv` y `players_png_manifest.json`.
- La colección se organiza por rareza. Consulta los manifiestos para localizar el nombre de archivo exacto.

## 2. Imágenes individuales de jugadores de eventos

- Carpeta: `events_png/`.
- Cantidad documentada: **6.570 PNG**.
- Variante documentada en V4: **Action Shot únicamente**.
- Manifiesto de recursos: `events_manifest.csv` y `events_manifest.json`.

La cantidad de PNG individuales no coincide necesariamente con el número de filas de la base de eventos ni con el número de cartas completas.

## 3. Renders PNG de iconos

- Carpeta: `icons_png/`.
- Inventario comunicado para V5: **66 renders PNG**.
- Los iconos se documentan en conjunto con la colección `icons_cards/`.
- Para nombre, programa, destino y correspondencia exactos, consulta `README_ICONOS.md` y los manifiestos incluidos en la distribución.

## 4. Manifiestos y localización

Los manifiestos permiten relacionar IDs, nombres de archivo, colecciones y rutas. No construyas nombres a partir de suposiciones: algunos recursos pueden tener sufijos o convenciones distintas. Usa los campos de ruta del manifiesto real.

## 5. Herramientas

Para la colección de cartas base se documentó `download_player_png.py`. Para los recursos de eventos se documentó `generate_events_assets.py`. Para iconos, la actualización V5 incluye `generate_iconos_assets.py`.

Los argumentos exactos de los scripts se deben comprobar con:

```bash
python download_player_png.py --help
python generate_events_assets.py --help
python generate_iconos_assets.py --help
```

No todos los scripts necesariamente descargan imágenes; algunos preparan o generan composiciones a partir de recursos locales.

## 6. Git LFS

Las colecciones gráficas incluyen archivos grandes gestionados mediante Git LFS. Instala Git LFS para recuperar los objetos binarios al clonar el repositorio. Comprueba que el contenido descargado no sea únicamente un pequeño puntero LFS.

## 7. Consideraciones

- Las imágenes individuales no son lo mismo que las cartas completas.
- `players_png/` corresponde a jugadores de cartas base; `events_png/` corresponde a jugadores de eventos.
- Los renders de `icons_png/` son una colección distinta de los PNG individuales de jugadores.
- Imágenes, nombres, marcas, iconos y recursos CDN pueden estar sujetos a derechos de terceros. Consulta `NOTICE.md` y verifica permisos antes de redistribuirlos.
