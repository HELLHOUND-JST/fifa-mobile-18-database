# FIFA Mobile 18 — Base de cartas (Temporada 2)

Proyecto independiente de recopilación y organización de información de **FIFA Mobile 18 — Season 2**. Incluye un extractor en Python, archivos de datos en CSV/JSON/TXT y cachés utilizados para conservar el progreso de las consultas.

> [!IMPORTANT]
> Este repositorio contiene datos y cachés obtenidos de sitios de terceros. **Dar crédito a una fuente no concede permiso para copiar o redistribuir su contenido.** Antes de publicar el repositorio como público, revisa especialmente las condiciones de RenderZ y SoFIFA y confirma que tienes autorización para distribuir los archivos derivados. Consulta [`NOTICE.md`](NOTICE.md). Mantener el repositorio privado tampoco sustituye el cumplimiento de las condiciones aplicables.

> [!NOTE]
> **Proyecto no oficial.** No está afiliado, patrocinado ni respaldado por Electronic Arts (EA), EA SPORTS, FIFA, RenderZ o SoFIFA.

## Objetivo

Construir una base organizada de las **cartas base** de la Temporada 2 de FIFA Mobile 18, relacionando los IDs de jugadores de SoFIFA con las fichas de jugador de RenderZ.

La regla de inclusión es conservar la ficha de RenderZ cuyo ID coincide con el ID del jugador usado como referencia. Las cartas de programas o eventos relacionadas —por ejemplo, IDs de seis cifras a partir de `500000`— se excluyen de la base principal y se registran por separado en `programs_excluded.csv`.

## Fuentes consultadas

- **RenderZ:** datos de la ficha de la carta base, como media móvil, posición, club, código de fondo y rareza. Ejemplo de consulta: [`https://renderz.app/18/player/20801`](https://renderz.app/18/player/20801).
- **SoFIFA:** lista de referencia e información del jugador para el conjunto histórico indicado por `r=180084`. [Abrir la lista FIFA 18 en SoFIFA](https://sofifa.com/?r=180084&set=true).

Las fuentes son independientes entre sí y conservan sus propios derechos, condiciones y políticas. Los enlaces se incluyen para identificar el origen de los datos, no como prueba de autorización para reutilizarlos.

## Contenido del repositorio

| Archivo o carpeta | Descripción |
|---|---|
| `extract_fifa18.py` | Script Python para consultar las fuentes, mantener cachés y generar las exportaciones. |
| `fifa_mobile_18_base.csv` | Base principal: una fila por carta base, con campos simplificados para facilitar su lectura. |
| `fifa_mobile_18_base.json` | Base principal en JSON; conserva campos originales UTF-8 adicionales para nombres, clubes y nacionalidades. |
| `fifa_mobile_18_base.txt` | Vista de texto alineada para consulta rápida. |
| `missing_in_renderz.csv` | IDs de la lista de referencia para los que no se obtuvo una ficha base en RenderZ. |
| `programs_excluded.csv` | IDs de cartas de programas/eventos detectadas y excluidas de la base principal. |
| `muestra_prueba_300.csv` / `muestra_prueba_300.txt` | Archivos de muestra reducida para inspección rápida. |
| `data/cache_sofifa_list.json` | Caché de la lista de jugadores consultada en SoFIFA. |
| `data/cache_renderz.jsonl` | Caché de respuestas de fichas de RenderZ, una entrada JSON por línea. |
| `data/manual_overrides.json` | Correcciones manuales persistentes aplicadas durante la exportación. |
| `data/progress.json` | Contadores y fecha de la última ejecución registrada. |
| `LEEME.txt` | Guía rápida complementaria en español. |
| `NOTICE.md` | Avisos de marcas, derechos y materiales de terceros. |

### Cifras de la copia incluida

Los siguientes valores describen los archivos de datos incluidos en esta versión del proyecto; pueden cambiar al volver a ejecutar el extractor:

- **13.885** registros en `fifa_mobile_18_base.csv`.
- **4.048** IDs registrados en `missing_in_renderz.csv`.
- **6.571** IDs de programas/eventos distintos en `programs_excluded.csv`.
- **17.933** jugadores en la caché de referencia de SoFIFA.

La copia de datos y los contadores incluidos corresponden a una extracción realizada el **5 de noviembre de 2026**. No representan una garantía de disponibilidad, exactitud o vigencia futura de las fuentes.

## Campos de la base principal

| Campo | Significado |
|---|---|
| `fifa_id` | ID usado para identificar al jugador y consultar su ficha base. |
| `short_name`, `full_name` | Nombre corto y nombre completo. |
| `position_mobile` | Posición de la carta en FIFA Mobile. |
| `ovr_mobile` | Media general de la carta móvil. |
| `club_id`, `club_name` | Identificador y nombre del club. |
| `background_code`, `rarity` | Código de fondo y categoría de rareza de la carta. |
| `sofifa_overall`, `sofifa_potential` | Media y potencial de referencia de SoFIFA. |
| `sofifa_age`, `sofifa_position` | Edad y posición según la referencia de SoFIFA. |
| `nationality` | Nacionalidad registrada en la fuente de referencia. |
| `renderz_url`, `sofifa_url` | Enlaces a las fichas de origen. |
| `season` | Temporada asociada al registro. |

### Códigos de rareza

El extractor traduce los prefijos conocidos de `background_code` a estas categorías:

| Código | Categoría |
|---|---|
| `BR` | Bronze Rare |
| `SR` | Silver Rare |
| `GR` | Gold Rare |
| `ER` | Epic Rare |
| `MR` | Master Rare |
| `CR` | Common Rare |
| `BC` | Bronze Common |
| `SC` | Silver Common |
| `GC` | Gold Common |

## Requisitos

- Python **3.10 o superior**.
- Conexión a Internet para consultar las fuentes.
- No requiere instalar paquetes de terceros: el script utiliza módulos de la biblioteca estándar de Python.

## Uso

Ejecuta los comandos desde la carpeta raíz del repositorio, donde se encuentra `extract_fifa18.py`.

### Comprobar el extractor

```bash
python extract_fifa18.py --test
```

Realiza una prueba limitada a los primeros 10 IDs de la lista de SoFIFA.

### Limitar una consulta de prueba

```bash
python extract_fifa18.py --limit 200
```

Limita a 200 los IDs de referencia que se procesan en esa ejecución. El contenido que ya exista en las cachés también puede participar en las exportaciones.

### Ejecutar el proceso completo

```bash
python extract_fifa18.py
```

Consulta los IDs pendientes, guarda las respuestas en caché y genera los archivos de salida. El proceso es reanudable: al ejecutarlo de nuevo reutiliza los registros guardados y continúa con los pendientes.

### Consultar IDs específicos

```bash
python extract_fifa18.py --only-ids 20801,158023,190871
```

Limita las nuevas consultas de RenderZ a los IDs indicados. Las exportaciones pueden seguir incluyendo otros registros presentes en las cachés.

### Regenerar las exportaciones desde las cachés

```bash
python extract_fifa18.py --export-only
```

Reconstruye los archivos de salida sin volver a consultar las páginas. Necesita que existan las cachés requeridas.

### Volver a consultar desde cero

```bash
python extract_fifa18.py --refresh
```

Ignora las cachés existentes para la consulta y vuelve a obtener los datos de las fuentes.

### Ajustar el número de trabajadores

```bash
python extract_fifa18.py --workers 4
```

Permite cambiar el número de consultas concurrentes. Utiliza un ritmo razonable y respeta las condiciones de cada sitio.

### Aplicar correcciones manuales

```bash
python extract_fifa18.py --set-name 20801 "Cristiano Ronaldo"
python extract_fifa18.py --set-ovr 20801 91
python extract_fifa18.py --export-only
```

Las correcciones se guardan en `data/manual_overrides.json` y se aplican en las siguientes exportaciones. También puedes editar ese archivo directamente y después ejecutar `--export-only`.

Para ver todas las opciones disponibles:

```bash
python extract_fifa18.py --help
```

## Criterios y limitaciones

- La base principal pretende contener **cartas base**, no todas las versiones especiales o promocionales de cada jugador.
- Los IDs identificados como cartas de programas/eventos se registran por separado y no se agregan como filas de la base principal.
- Los campos de FIFA Mobile y los de SoFIFA proceden de fuentes y contextos distintos; por ello, sus medias, posiciones y otros valores pueden no coincidir.
- Los archivos CSV/TXT de la copia están normalizados para facilitar su lectura. El JSON conserva valores originales UTF-8 en campos adicionales como `full_name_original`, `short_name_original`, `club_name_original` y `nationality_original`.
- Los datos pueden estar incompletos, cambiar o dejar de estar disponibles. Los estados `404`, errores de conexión y resultados de extracción no garantizan que un jugador no haya existido en el juego.
- Las páginas, interfaces y condiciones de las fuentes pueden cambiar; el extractor puede requerir ajustes para seguir funcionando.
- El separador de los CSV puede depender de la exportación que generó cada archivo. Si una hoja de cálculo no divide las columnas correctamente, importa el archivo y selecciona el delimitador correspondiente.

## Créditos y propiedad intelectual

Los nombres **FIFA**, **EA**, **EA SPORTS**, **FIFA Mobile**, **RenderZ** y **SoFIFA**, así como sus marcas, logotipos, productos y materiales protegidos, pertenecen a sus respectivos titulares. Se mencionan únicamente para identificar el juego y las fuentes consultadas.

La atribución no implica afiliación ni concede derechos de reproducción o redistribución. **No se debe asumir que los archivos de datos, cachés o exportaciones pueden publicarse o reutilizarse libremente.** Lee [`NOTICE.md`](NOTICE.md) antes de copiar o distribuir cualquier parte del repositorio.

Este repositorio no incluye una licencia abierta general para el conjunto de código y datos. No añadas una licencia MIT, Apache u otra licencia al repositorio completo sin separar primero los materiales propios de los materiales de terceros y comprobar que tienes derechos para licenciarlos.

## Contribuciones

Las correcciones, mejoras de documentación y propuestas para el extractor pueden plantearse mediante *Issues* o *Pull Requests*. No contribuyas con imágenes, logos, archivos del juego ni datos de terceros que no tengas derecho a compartir.

---

**Aviso:** este proyecto es una recopilación comunitaria no oficial. La información se ofrece tal como está, sin garantía de exactitud, integridad o disponibilidad. Para conocer los avisos de terceros, consulta [`NOTICE.md`](NOTICE.md).
