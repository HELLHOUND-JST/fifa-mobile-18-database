# Cartas completas PNG — FIFA Mobile 18 Base (V3.0.0)

Este documento describe la colección de composiciones PNG de las cartas base de FIFA Mobile 18 — Season 2.

## Resultado generado

- **13.885 cartas completas** en PNG.
- Dimensiones: **256 × 256 píxeles**.
- Ruta: `cards_full/{rareza}/card_{fifa_id}.png`.
- Cada archivo combina la imagen del jugador, el fondo de rareza, el escudo del club y los textos de la carta.
- Los resultados se inventarían mediante `cards_full_manifest.csv` y `cards_full_manifest.json`.

### Distribución por rareza

| Rareza | Cantidad |
|---|---:|
| Master Rare | 1 |
| Epic Rare | 285 |
| Gold Rare | 3.656 |
| Silver Rare | 7.752 |
| Bronze Rare | 2.191 |
| **Total** | **13.885** |

## Cómo se componen

Las imágenes se generan programáticamente a partir de recursos gráficos y de una referencia de distribución visual de las cartas. No son capturas de pantalla de una sesión autenticada de RenderZ ni una afirmación de que los archivos generados sean imágenes oficiales publicadas por EA.

Los recursos descritos para el proceso son:

- **Tipografía:** archivos Knul Medium y Knul Regular, convertidos a TTF para su uso en la composición. La documentación de la generación identifica estos recursos como procedentes de EA.
- **Fondos:** recursos de `backgrounds_18/`, con códigos como `MR4`, `ER3`, `GR2`, `GR3`, `SR1` y `BR0`.
- **Imagen del jugador:** archivos individuales asociados a los jugadores, disponibles en la colección `players_png/`.
- **Escudos de clubes:** recursos ubicados en `assets_cards/clubs/`; la documentación del proceso registra 613 escudos.
- **Distribución:** referencia del diseño CSS de la carta de jugador de RenderZ para tamaños y posiciones de los elementos.

La composición utiliza un lienzo de 256 × 256 píxeles. La documentación del generador describe las siguientes posiciones de referencia:

| Elemento | Posición / tamaño documentado |
|---|---|
| Fondo e imagen del jugador | Ocupan el lienzo completo, desde `(0, 0)`. |
| Escudo del club | 40 × 40 píxeles, aproximadamente en `(19%, 46%)`. |
| OVR | Aproximadamente `(19,3%, 15%)`, Knul Medium de 42 px, blanco y con sombra. |
| Posición | Aproximadamente `(20%, 34,5%)`, Knul Regular de 18 px, mayúsculas y blanco. |
| Nombre | Centrado, desde el 66,5% de la altura, Knul Medium de 20 px, mayúsculas y ancho máximo de 130 px. |

El nombre puede comprimirse horizontalmente para caber en el espacio previsto; la documentación del generador indica que no se reduce su altura. Estas medidas describen el diseño implementado por el script y pueden variar si la herramienta cambia.

## Estructura de salida

```text
cards_full/
├── Master_Rare/
├── Epic_Rare/
├── Gold_Rare/
├── Silver_Rare/
└── Bronze_Rare/
```

Los archivos siguen este patrón:

```text
cards_full/{rareza}/card_{fifa_id}.png
```

Ejemplo de nombre: `card_20801.png`.

## Manifiestos

La colección incluye:

- `cards_full_manifest.csv`
- `cards_full_manifest.json`

Estos archivos sirven para inventariar los resultados y relacionarlos con los jugadores de la base. Consulta el propio manifiesto para conocer las columnas y valores registrados en la copia concreta.

## Generador

Script: `generate_full_cards.py`.

## Uso

Ejecuta los comandos desde la raíz del repositorio:

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

La generación es reanudable: sin `--overwrite`, la herramienta omite los archivos que ya están generados, según la documentación del script.

## Relación con las imágenes individuales

Las imágenes individuales de los jugadores se encuentran en `players_png/`. Son un recurso de entrada para el proceso de composición, pero no equivalen a la carta completa. Consulta [`README_PNG.md`](README_PNG.md) para conocer su descarga, organización y manifiestos.

## Consideraciones

- Las composiciones son resultados generados por una herramienta del proyecto a partir de recursos y referencias gráficas; no deben describirse como capturas oficiales ni como una publicación oficial de EA.
- La utilización de fuentes, imágenes de jugadores, fondos, escudos y elementos visuales puede estar sujeta a derechos de terceros.
- La referencia al diseño de RenderZ no implica que RenderZ haya creado, aprobado o respaldado estas composiciones.
- Dar crédito no concede permiso para publicar o redistribuir materiales protegidos. Revisa [`NOTICE.md`](NOTICE.md) y verifica las autorizaciones necesarias antes de distribuir las imágenes.
