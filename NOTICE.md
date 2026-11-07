# NOTICE — Atribuciones, derechos de terceros y avisos legales

**Proyecto:** FIFA Mobile 18 — Base de cartas, estadísticas e imágenes (Season 2)  
**Versión documentada:** 3.0.0  
**Última revisión:** 6 de noviembre de 2026

Este documento identifica marcas, plataformas y referencias de terceros mencionadas o consultadas por el proyecto. Es un aviso informativo de atribución; **no constituye asesoría legal, no sustituye las condiciones de cada sitio y no concede licencias ni permisos que sus titulares no hayan otorgado**.

## 1. Proyecto independiente

FIFA Mobile 18 — Base de cartas, estadísticas e imágenes es un proyecto independiente y no oficial. No está afiliado, patrocinado, aprobado ni respaldado por Electronic Arts, EA SPORTS, FIFA, RenderZ, SoFIFA ni FIFAMobileGuide.

Los nombres de empresas, productos, servicios, plataformas y sitios se utilizan para identificar el juego y las referencias consultadas. Este repositorio no reclama propiedad sobre las marcas, bases de datos, interfaces, diseños, fuentes tipográficas, imágenes ni materiales de terceros.

## 2. Electronic Arts / EA SPORTS / FIFA Mobile

**Electronic Arts Inc. (EA)** y sus licenciantes conservan los derechos que les correspondan sobre sus juegos, servicios, software, contenidos y materiales asociados. Los nombres EA, EA SPORTS y FIFA Mobile, así como sus logotipos, gráficos, imágenes, tipografías, elementos audiovisuales y demás materiales protegidos, no se transfieren al autor ni a los usuarios de este repositorio.

La documentación de la V3.0.0 describe el uso de recursos gráficos y tipográficos asociados a FIFA Mobile 18 para producir composiciones PNG de cartas. La generación de una composición nueva no elimina ni transfiere los derechos que puedan existir sobre sus componentes.

El acuerdo de usuario y las políticas de EA establecen condiciones sobre el acceso, uso, copia y distribución de sus servicios y contenidos. La mención de EA o de FIFA Mobile no representa autorización para reproducir o redistribuir materiales del juego.

- Sitio oficial de EA: <https://www.ea.com/>
- Acuerdo de usuario: <https://www.ea.com/legal/user-agreement?isLocalized=true&setLocale=en-gb>
- Política de contenido: <https://help.ea.com/es/articles/security-and-rules/ea-content-policy/>

## 3. FIFA

**FIFA** y sus marcas, emblemas, denominaciones y materiales oficiales pertenecen a la Fédération Internationale de Football Association (FIFA) o a los titulares que correspondan según cada material o licencia.

La mención de FIFA en el nombre del juego, identificadores o documentación no implica autorización para utilizar marcas oficiales, logotipos, emblemas o materiales protegidos.

- Sitio oficial: <https://www.fifa.com/>
- Información sobre marcas y derechos: <https://inside.fifa.com/en/organisation/contact-fifa/legal-branding-and-rights>
- Condiciones de servicio: <https://legal.fifa.com/terms-of-service>

## 4. RenderZ

**RenderZ** se reconoce como una referencia externa consultada para identificar información de cartas de FIFA Mobile 18, como media móvil, posición, club, código de fondo y rareza. También se utilizó como referencia visual para la distribución de elementos de las composiciones de cartas.

La documentación de la colección `players_png/` indica que las imágenes individuales se identificaron mediante fichas de jugadores y se descargaron desde las rutas de CDN correspondientes. La documentación de `cards_full/` indica que sus composiciones siguen una referencia del diseño de carta de RenderZ. Estas menciones no significan que RenderZ haya creado, aprobado o respaldado los archivos generados.

Las condiciones publicadas por RenderZ identifican a **RenderZ ApS** y establecen restricciones sobre el sitio, sus herramientas, software, propiedad intelectual, contenido y su distribución o puesta a disposición de terceros. Por tanto, la atribución incluida en este repositorio **no autoriza** a publicar, redistribuir, sublicenciar o explotar datos, cachés, imágenes, contenido o servicios de RenderZ. Antes de hacer público o redistribuir material obtenido de RenderZ o de sus CDN, el responsable debe revisar las condiciones vigentes y obtener los permisos necesarios. Si no dispone de ellos, debe excluir los materiales afectados de la publicación.

- Sitio de RenderZ: <https://renderz.app/>
- Condiciones de servicio: <https://renderz.app/terms-of-service>

## 5. SoFIFA

**SoFIFA** se reconoce como referencia independiente para consultar información histórica de jugadores relacionada con FIFA 18. En el proyecto se utilizó el conjunto histórico identificado por `r=180084`.

Las marcas, logotipos, imágenes, fichas, contenidos y demás materiales mostrados en SoFIFA corresponden a sus respectivos titulares. Los términos del sitio no deben interpretarse como una autorización general para republicar su base de datos ni reutilizar masivamente sus contenidos.

Este repositorio puede contener una caché de referencia en `data/cache_sofifa_list.json` y exportaciones que incorporan campos consultados en esa plataforma. Antes de hacer públicos o redistribuir esos archivos, el responsable debe revisar los términos vigentes y confirmar que el uso y la distribución están permitidos.

- Sitio de SoFIFA: <https://sofifa.com/>
- Términos de servicio: <https://sofifa.com/help/tos>
- Documentación de API: <https://sofifa.com/document?profile=new>

## 6. FIFAMobileGuide

**Crédito de referencia: FIFAMobileGuide.com.** Se reconoce a FIFAMobileGuide como una referencia consultada durante el trabajo de recopilación y organización de atributos de jugadores para FIFA Mobile 18.

El repositorio no reclama la propiedad de FIFAMobileGuide, de su sitio web, base de datos, textos, diseños ni otros materiales. Los derechos que correspondan sobre esos recursos permanecen con sus respectivos titulares. La atribución se incluye para reconocer la referencia consultada y **no significa que FIFAMobileGuide haya aprobado, patrocinado o participado en este proyecto**.

Las condiciones de uso publicadas por FIFAMobileGuide contienen restricciones sobre el uso público, copia, almacenamiento, venta o publicación de contenido y bases de datos, salvo que exista contrato o autorización expresa por escrito. La atribución incluida aquí no constituye esa autorización.

Antes de publicar o redistribuir datos o materiales que puedan estar sujetos a esas condiciones, el responsable debe obtener autorización expresa por escrito o excluir de la distribución los materiales afectados. **Dar crédito por sí solo no sustituye ese permiso.**

## 7. Imágenes, fuentes tipográficas y composiciones de cartas

La V3.0.0 incorpora dos colecciones gráficas:

- `players_png/`: imágenes PNG individuales de los jugadores, identificadas mediante referencias de fichas y recursos CDN descritos en `README_PNG.md`.
- `cards_full/`: composiciones PNG de cartas completas creadas programáticamente con recursos de jugador, fondos, escudos y tipografía, descritas en `README_CARDS_FULL.md`.

La documentación técnica del generador menciona recursos de fondo, imágenes de jugadores, logotipos de clubes y archivos tipográficos Knul Medium/Regular. Los derechos sobre cada recurso original permanecen con EA, sus licenciantes o el titular que corresponda. La composición, conversión de formato, cambio de tamaño o inclusión en un manifiesto no convierte esos recursos en propiedad del autor del repositorio ni los hace automáticamente redistribuibles.

Los manifiestos CSV/JSON y los nombres de archivo facilitan la identificación de los recursos, pero no constituyen licencias de uso. Antes de publicar o redistribuir imágenes, tipografías, fondos, escudos o cualquier otro recurso gráfico, el responsable debe verificar que cuenta con los permisos necesarios.

## 8. Material original del proyecto

Los scripts, transformaciones, correcciones manuales y textos de documentación desarrollados específicamente para este repositorio pueden ser obra de sus respectivos autores. Esta declaración no reclama propiedad sobre datos, nombres, marcas, fichas, imágenes, fuentes, fondos, escudos, bases de datos ni otros materiales obtenidos o consultados en sitios de terceros.

Este repositorio no incluye una licencia general (`LICENSE`). Por ello, no debe suponerse que el código, los datos o las imágenes pueden copiarse, modificarse o redistribuirse libremente. Si posteriormente se añade una licencia para el código original, su alcance deberá excluir cualquier material de terceros que el mantenedor no tenga derecho a licenciar.

## 9. No afiliación ni respaldo

El uso de nombres de terceros es nominativo y descriptivo. No implica relación comercial, asociación, patrocinio, autorización, colaboración o respaldo por parte de EA, EA SPORTS, FIFA, RenderZ, SoFIFA o FIFAMobileGuide.

## 10. Exactitud, atribución y permisos

Los archivos de este proyecto se proporcionan como material de referencia comunitario, sin garantía de exactitud, integridad o disponibilidad. Los valores no deben interpretarse como una certificación oficial de EA ni como garantía de que coincidan exactamente con una versión concreta del juego. Las composiciones PNG se presentan como resultados generados mediante las herramientas documentadas, no como capturas oficiales ni como archivos publicados oficialmente por EA.

Dar crédito a una fuente no transfiere la propiedad de sus materiales, no elimina restricciones contractuales y no reemplaza una autorización. El responsable de copiar, publicar, adaptar o redistribuir cualquier archivo debe verificar por separado que cuenta con los permisos necesarios y cumplir las condiciones vigentes de cada titular.

Si un titular considera que algún archivo utiliza material sin autorización, puede contactar al mantenedor del repositorio a través de los medios de contacto publicados en su perfil de GitHub para que se revise el material señalado.
