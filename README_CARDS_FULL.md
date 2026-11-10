# Cartas completas PNG — FIFA Mobile 18 Base, eventos e Iconos (V4.0.0)

Este documento describe las composiciones PNG de cartas completas de FIFA Mobile 18 — Season 2. La colección comprende cartas base (documentadas desde V3.0.0), cartas completas de eventos (V4.0.0) y cartas completas de Iconos (V4.0.0). Las tres colecciones son composiciones generadas a partir de recursos; no son capturas oficiales ni archivos publicados por EA.

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

## Cartas completas de Iconos

La V4.0.0 incorpora la colección de Iconos en:

- Carpeta: `icons_cards/` (agrupada por rareza: `Icon/`, `Prime_Icon/`, `WC_Icon/`).
- Cantidad: **69 cartas completas** (36 Icon, 16 Prime Icon, 17 WC Icon).
- Formato: PNG.
- Dimensiones: **256 × 256 píxeles**.
- Renders del jugador: `icons_png/` (66 archivos únicos; tres pares Pelé/Ronaldo/Henry comparten render).
- Logos de programa: `icons_logos/program_17_ICONS.png` (solo Icon) y `icons_logos/program_17_WCICON.png` (solo WC Icon). Prime Icons no muestran icono de programa en RenderZ.
- Escudo en el slot del club: Icon/Prime Icon usan `assets_cards/clubs/112658.png`; WC Icons usan la bandera del país (201354, 201318, 201335, 201337, 201357, 201362, 201369, 201370, 201386, 201393, 201411).
- Fondos: `backgrounds_LR5.png` (Icon/Prime) y `backgrounds_WC_ICON_E.png` / `backgrounds_WC_ICON_M.png` (WC Icon).
- Manifiestos de iconos: `icons_manifest.csv` y `icons_manifest.json` (69 filas, todas `ok`).

## Recursos utilizados y añadidos en V4.0.0

El proyecto utiliza recursos gráficos y tipográficos descritos en la documentación de cartas base y amplía los recursos para cartas de eventos y de Iconos:

- **Fondos:** se añadieron **931 recursos** en `assets_cards/backgrounds/`, incluidos fondos de World Cup, eventos y las variantes `backgrounds_WC_ICON_M/E` para los WC Iconos (el CDN sirve el mismo PNG para ambos nombres).
- **Clubes:** se añadieron **47 recursos** en `assets_cards/clubs/`, más el escudo `112658` (Icon).
- **Logos de programas:** `events_logos/` contiene **92 iconos/logotipos**. Los recursos `17_FAV` y `17_SBC_PLAYER` no se encontraron en el CDN durante la recopilación.
- **Jugadores de eventos:** `events_png/` contiene **6.570 PNG**, únicamente de variante Action Shot.
- **Jugadores Iconos:** `icons_png/` contiene **66 renders** (3 pares compartidos).

La V3.0.0 documentaba tipografías Knul Medium/Regular, fondos, imágenes individuales y escudos de clubes para la composición de cartas base. Los derechos y permisos aplicables a los componentes originales se explican en [`NOTICE.md`](NOTICE.md).

## Composición de las cartas base

Las cartas base se generan programáticamente a partir de recursos gráficos y una referencia de distribución visual. No son capturas de pantalla de una sesión autenticada de RenderZ ni una afirmación de que sean archivos oficiales publicados por EA.

La documentación de la colección base describe:

- **Tipografía:** Knul Medium y Knul Regular para los textos de la carta.
- **Fondos:** recursos de la colección `backgrounds_18/` y recursos auxiliares bajo `assets_cards/backgrounds/`, según la versión.
- **Imagen del jugador:** recursos individuales de `players_png/`.
- **Escudos de clubes:** recursos de `assets_cards/clubs/`.
- **Distribución visual:** referencia del diseño de carta de RenderZ.

## Composición de las cartas de eventos

Las cartas de eventos se generan con el mismo esquema: fondo de la carta del programa (según el `background_code`), render del jugador (Action Shot), escudo del club o, si no hay escudo, icono del programa en el slot, y textos con Knul Medium/Regular. Las **88 `card_error`** corresponden a cartas de programas para las que RenderZ no ofrecía escudo/fondo/render utilizados.

## Composición de las cartas Icono

Las cartas Icono se generan con el mismo esquema: fondo (LR5 o WC_ICON_*), render del jugador, escudo/bandera según la rareza, texto OVR/pos/nombre con Knul, comprimido horizontalmente si el nombre supera 130 px, y nombre centrado verticalmente siguiendo la regla del 66.5 % + 12 px.

## Manifiestos

Para la colección base:

- `cards_full_manifest.csv`
- `cards_full_manifest.json`

Para la colección de eventos:

- `events_manifest.csv`
- `events_manifest.json`

Para la colección de Iconos:

- `icons_manifest.csv`
- `icons_manifest.json`

Consulta los encabezados y claves reales de cada manifiesto para conocer sus campos y las relaciones que contienen. No se debe asumir que los tres pares comparten el mismo esquema.

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

## Herramientas de eventos y de Iconos

La V4.0.0 incorpora `generate_events_assets.py` e `inspect_event_assets.py` para el flujo de recursos de eventos. El resumen de actualización no proporciona argumentos de línea de comandos concretos para estos scripts; consulta su `--help` y el código antes de ejecutarlos.

Para los Iconos, la V4.0.0 incorpora `generate_iconos.py` (genera CSV/TXT/JSON con estadísticas reales), `generate_iconos_assets.py` (descarga renders, fondos, logos de programa y clubes/banderas, y compone las 69 cartas completas) y `validate_iconos.py` (validación automática).

## Relación con las imágenes individuales

- `players_png/`: imágenes individuales de jugadores de cartas base.
- `events_png/`: 6.570 imágenes individuales de jugadores de eventos; solo Action Shot.
- `icons_png/`: 66 renders de cartas Icono.
- `cards_full/`: cartas base completas.
- `events_cards/`: 6.483 cartas completas de eventos.
- `icons_cards/`: 69 cartas completas de Iconos.

Las imágenes individuales de jugadores no equivalen a composiciones de cartas completas. Consulta [`README_PNG.md`](README_PNG.md), [`README_EVENT_CARDS.md`](README_EVENT_CARDS.md) y [`README_ICONOS.md`](README_ICONOS.md).

## Git LFS

La subida V4.0.0 de eventos reportó **11.242 objetos LFS** y aproximadamente **513 MB transferidos**. En la subida de la V4.0.0 con estadísticas reales y la base Iconos, se transfirieron 139/139 objetos LFS (8,1 MB). Para obtener los PNG y otros archivos grandes en una copia local del repositorio, instala y configura Git LFS.

## Consideraciones

- Las composiciones son resultados generados mediante herramientas del proyecto a partir de recursos y referencias gráficas; no deben describirse como capturas oficiales ni como publicaciones oficiales de EA.
- Las fuentes, imágenes de jugadores, fondos, escudos de clubes, logotipos de eventos y otros elementos visuales pueden estar sujetos a derechos de terceros.
- La referencia al diseño de RenderZ no implica que RenderZ haya creado, aprobado o respaldado estas composiciones.
- Dar crédito no concede permiso para publicar o redistribuir materiales protegidos. Revisa [`NOTICE.md`](NOTICE.md) y verifica las autorizaciones necesarias antes de distribuir imágenes o recursos.
