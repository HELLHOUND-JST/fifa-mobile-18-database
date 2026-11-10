# Iconos, logos y recursos gráficos — FIFA Mobile 18 (V5.0.0)

Este documento reúne la información disponible sobre iconos y recursos gráficos auxiliares de cartas base, eventos y programas.

## 1. Colecciones identificadas en V5

| Carpeta | Inventario comunicado | Descripción |
|---|---:|---|
| `icons_png/` | **66 renders** | Renders PNG de iconos. |
| `icons_cards/` | **69 de 69** | Colección de recursos de iconos en formato de carta/tarjeta según el inventario. |
| `events_logos/` | **92** | Logos de eventos/programas reportados en V4. |

Los tres inventarios deben mantenerse separados: no se ha confirmado que representen la misma clase de icono ni que cada elemento tenga una correspondencia uno a uno.

## 2. Recursos específicos mencionados

El resumen de actualización de documentación V5 menciona:

- Recurso/identificador de escudo: `112658`.
- Fondo: `WC_ICON`.
- Un fondo asociado a estadísticas reales.
- La colección `assets_cards/clubs/` y los recursos de fondos `assets_cards/backgrounds/`.

La captura resume estos elementos como parte del inventario de iconos, escudos y fondos. Para rutas y nombres exactos, utiliza el inventario del repositorio y los manifiestos incluidos en el Release.

## 3. Herramienta de generación

V5 identifica el script:

- `generate_iconos_assets.py`

Su cometido documentado es generar/preparar recursos gráficos de iconos. Los argumentos concretos no aparecen en el resumen; consulta:

```bash
python generate_iconos_assets.py --help
```

No ejecutes procesos de sobrescritura o regeneración masiva sin revisar primero las rutas de entrada y salida del script.

## 4. Manifiestos y catálogo

El proyecto documenta manifiestos y un catálogo de enlaces para facilitar la localización de recursos. Consulta los archivos de manifiesto y las tablas con contexto del repositorio para identificar:

- nombre del icono o programa;
- identificador asociado;
- nombre de archivo;
- ruta dentro de la colección;
- tipo de recurso (render PNG, recurso de carta, logo, escudo o fondo);
- estado de disponibilidad.

No se inventan aquí nombres de columnas, URLs o IDs no presentes en los archivos suministrados.

## 5. Git LFS

Los recursos PNG y otros archivos de gran tamaño pueden estar almacenados mediante Git LFS. Instala/configura Git LFS y comprueba que se descarguen los objetos reales, no solamente archivos puntero. El uso de LFS no modifica la titularidad ni los permisos de los recursos.

## 6. Derechos y atribución

Los nombres, iconos, logos de eventos, escudos de clubes, fondos, imágenes, fuentes y otros materiales pueden pertenecer a EA, RenderZ u otros titulares. Los datos oficiales de estadísticas y *Skill Boosts* se atribuyen a RenderZ según la procedencia declarada para el proyecto; ello no implica afiliación o permiso para redistribuir los recursos de esa plataforma. Consulta `NOTICE.md` antes de publicar o reutilizar archivos.
