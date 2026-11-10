# Cartas completas PNG — FIFA Mobile 18 Base y eventos (V5.0.0)

Este documento describe las composiciones de cartas completas de cartas base y de eventos/programas.

## 1. Cartas base completas

- Carpeta: `cards_full/`.
- Cantidad documentada: **13.885 cartas**.
- Dimensiones documentadas: **256 × 256 píxeles**.
- Patrón histórico: `cards_full/{rareza}/card_{fifa_id}.png`.
- Manifiestos: `cards_full_manifest.csv` y `cards_full_manifest.json`.
- Composición: imagen del jugador, fondo, escudo del club y textos de carta; consulta los recursos y herramientas reales de la distribución.

La colección se organiza por rareza. Los recuentos históricos documentados fueron: Master Rare 1, Epic Rare 285, Gold Rare 3.656, Silver Rare 7.752 y Bronze Rare 2.191 (total 13.885).

## 2. Cartas completas de eventos

- Carpeta: `events_cards/`.
- Cantidad comunicada: **6.483 cartas completas**.
- Formato: PNG.
- Dimensiones comunicadas: **256 × 256 píxeles**.
- Manifiestos: `events_manifest.csv` y `events_manifest.json`.

La base de eventos documentada contiene 6.571 filas y las colecciones gráficas reportan 6.570 PNG individuales y 6.483 cartas completas. Son inventarios distintos; no se debe inferir una correspondencia uno a uno ni atribuir una causa a las diferencias sin consultar los manifiestos.

## 3. Iconos en formato de carta/tarjeta

- Carpeta: `icons_cards/`.
- Inventario comunicado en los cambios de documentación V5: **69 de 69**.
- La colección se complementa con `icons_png/`, que contiene **66 renders PNG**.
- Consulta [`README_ICONOS.md`](README_ICONOS.md) para detalles de las colecciones, los identificadores y sus relaciones.

## 4. Recursos gráficos relacionados

Los recursos que intervienen en cartas e iconos incluyen:

- `assets_cards/backgrounds/`: fondos de cartas base, eventos y World Cup; V4 reportó 931 recursos añadidos.
- `assets_cards/clubs/`: escudos/logos de clubes; V4 reportó 47 recursos nuevos.
- Recurso/identificador de escudo `112658`, indicado en el inventario de la documentación V5.
- Fondo `WC_ICON` y un fondo asociado a estadísticas reales.
- `fonts/` y `backgrounds_18/`: recursos auxiliares de tipografía y fondos documentados en versiones anteriores.

Comprueba las carpetas y manifiestos reales para conocer los nombres de archivo, rutas y correspondencias exactas.

## 5. Manifiestos

- Base: `cards_full_manifest.csv` y `cards_full_manifest.json`.
- Eventos: `events_manifest.csv` y `events_manifest.json`.
- Iconos: consulta los manifiestos asociados a `icons_png/` e `icons_cards/` en la distribución V5.

No se debe asumir que todos los manifiestos comparten el mismo esquema.

## 6. Herramientas

- `generate_full_cards.py`: generación de cartas base completas.
- `generate_events_assets.py`: preparación/generación de recursos de eventos.
- `generate_iconos_assets.py`: generación/preparación de recursos gráficos de iconos.

Consulta `--help` de cada script para conocer sus argumentos actuales.

## 7. Git LFS

Las colecciones de cartas e iconos incluyen archivos binarios grandes gestionados mediante Git LFS. Instala y configura Git LFS para recuperar los objetos al clonar el repositorio. Los ZIP automáticos pueden no traer todos los objetos LFS de la misma manera que una clonación con Git LFS.

## 8. Consideraciones

Las composiciones son resultados de herramientas y recursos documentados; no deben describirse automáticamente como capturas oficiales ni como imágenes publicadas directamente por EA. Las fuentes, imágenes, fondos, escudos, iconos, cartas y tipografías pueden estar protegidos por derechos de terceros. Consulta `NOTICE.md`; dar crédito no concede permiso de redistribución.
