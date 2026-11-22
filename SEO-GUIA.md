# Plan SEO local – Anthox PTY (Ciudad de Panamá)

Objetivo: aparecer en el **“Map Pack” de Google Maps** (los 3 primeros resultados con mapa) y en el top orgánico para búsquedas como *fumigación Panamá*, *control de plagas Panamá*, *fumigadora cerca de mí*, *fumigación de comején*.

---

## 1. Lo que ya incluye el sitio web

| Elemento | Dónde | Para qué sirve |
|---|---|---|
| Título y meta descripción con “Fumigación en Panamá” | `index.html` | Palabra clave principal + CTR en Google |
| Datos estructurados `LocalBusiness` (NAP, horario, zonas, servicios) | `index.html` | Google entiende que eres un negocio local en Ciudad de Panamá |
| Datos estructurados `FAQPage`, `BlogPosting`, `BreadcrumbList` | Inicio y blog | Resultados enriquecidos y respuestas en IA de Google |
| Lista de 21 corregimientos/zonas atendidas | Sección Contacto | Relevancia local por barrio |
| 5 artículos de blog con temas de Panamá | `/blog/` | Tráfico informativo + autoridad temática |
| `sitemap.xml` y `robots.txt` | raíz | Indexación rápida |
| Metas geo (`geo.region PA-8`, coordenadas) e `hreflang` implícito `es-PA` | `<head>` | Señales de localización |
| Sitio estático, liviano, adaptado a móvil | todo | Core Web Vitals (factor de ranking) |
| Clics a WhatsApp medibles (`whatsapp_click`, `generate_lead`) | `js/main.js` | Medir conversiones en GA4 / Google Ads |

---

## 2. Antes de publicar (obligatorio)

1. **Dominio:** el sitio usa `https://www.anthoxpty.com` como ejemplo. Si tu dominio es otro, reemplázalo en `index.html`, `tools/build_blog.py` y `robots.txt`, y ejecuta `python3 tools/build_blog.py`.
2. **Dirección:** si tienes oficina física, agrega `streetAddress` y `postalCode` en el JSON-LD de `index.html` **exactamente igual** que en Google Business Profile.
3. **Confirma las promesas comerciales** del sitio: 15 % de descuento (barra superior), 90 días de garantía, horario Lun–Sáb 7 am–7 pm y los precios base del cotizador (`js/main.js`, objeto `PRICES`).
4. **Redes sociales:** reemplaza los `href="#"` de Instagram/Facebook/TikTok en el footer y agrégalas al arreglo `sameAs` del JSON-LD.
5. **Hosting gratis recomendado:** Netlify, Cloudflare Pages o GitHub Pages (sube la carpeta tal cual).

---

## 3. Google Business Profile (el factor #1 para Google Maps)

Crea/verifica tu perfil en **business.google.com**:

- **Nombre:** “Anthox PTY Control de Plagas” (nombre real del negocio; no rellenar con palabras clave, Google lo penaliza).
- **Categoría principal:** *Servicio de control de plagas*. Secundarias: *Servicio de control de termitas*, *Servicio de desinfección*, *Servicio de eliminación de roedores* (si aparecen).
- **Tipo:** “Negocio de servicio a domicilio” → define **área de servicio**: Ciudad de Panamá, San Miguelito, Arraiján, La Chorrera, Panamá Pacífico (máx. 20).
- **NAP idéntico en todas partes:** Nombre · Teléfono `+507 6761-9763` · Sitio web.
- **Horario**, **botón de WhatsApp/mensajes** y **enlace de citas** → `https://wa.me/50767619763`.
- **Servicios:** carga cada servicio con descripción (residencial, comercial, restaurantes, comején, roedores, mosquitos, chinches, desinfección).
- **Fotos:** mínimo 15 al inicio (logo, técnicos con uniforme, vehículo rotulado, equipos, antes/después). Sube 2–3 fotos nuevas **cada semana**. Fotos tomadas en Panamá con el celular (geolocalizadas) ayudan.
- **Publicaciones (Posts):** 1 por semana — ofertas, consejos (reutiliza los artículos del blog), temporada de dengue, etc.
- **Preguntas y respuestas:** publica tú mismo las FAQ del sitio.

### Reseñas (el factor que más mueve el ranking en Maps)
- Meta: **10 reseñas el primer mes, 50 en 6 meses**.
- Después de cada servicio, envía por WhatsApp el enlace corto de reseña de tu perfil (“Pedir reseñas” en el panel).
- Pide al cliente que mencione **el servicio y su zona** (“fumigaron mi apartamento en Costa del Este”) – esto refuerza la relevancia local.
- **Responde todas** las reseñas en menos de 48 h, usando palabras clave de forma natural.
- Nunca compres reseñas ni ofrezcas descuentos a cambio: Google puede suspender el perfil.

---

## 4. Citaciones y directorios locales (NAP consistente)

Regístrate con exactamente el mismo nombre, teléfono y web en:
Páginas Amarillas Panamá, Encuentra24 (servicios), Apple Business Connect (Apple Maps), Bing Places, Waze for Cities/Local Ads, Facebook Business, Instagram (cuenta de empresa con ubicación), TikTok Business, Yelp, Foursquare, directorios de cámaras de comercio y de PH/administradoras de propiedades.

---

## 5. Contenido – calendario para seguir creciendo

Publica **2 artículos al mes** (usa `tools/posts.py` + `python3 tools/build_blog.py`). Ideas con buen volumen en Panamá:

1. Chinches de cama en hoteles y Airbnb en Panamá
2. Alacranes en Panamá: cuáles son peligrosos y cómo evitarlos
3. Fumigación para restaurantes: requisitos para inspecciones del MINSA
4. Hormigas en la cocina: cómo eliminar la colonia
5. Murciélagos en techos: cómo sacarlos de forma segura
6. Fumigación antes de mudarte a un apartamento nuevo
7. Páginas por zona (*Fumigación en Costa del Este*, *Fumigación en San Miguelito*, *Fumigación en Arraiján*…) con contenido único de cada zona — muy efectivas para SEO local.
8. Páginas por servicio (*/fumigacion-de-comejen*, */control-de-roedores*…) para competir por cada palabra clave.

---

## 6. Técnico y medición

- Da de alta el sitio en **Google Search Console** y envía `sitemap.xml`.
- Instala **Google Analytics 4** (o Tag Manager) — el sitio ya envía los eventos `whatsapp_click` y `generate_lead`.
- Revisa **PageSpeed Insights** (meta: 90+ en móvil).
- Consigue **enlaces locales**: alianzas con administradoras de PH, inmobiliarias, ferreterías, blogs de mudanzas y notas en medios locales.

---

## 7. Palabras clave objetivo

| Prioridad | Palabra clave |
|---|---|
| Alta | fumigación panamá · control de plagas panamá · fumigadora en panamá · fumigación cerca de mí |
| Alta | fumigación de comején panamá · exterminador de cucarachas panamá |
| Media | control de roedores panamá · fumigación de chinches · fumigación de restaurantes panamá |
| Media | fumigación de mosquitos / dengue panamá · desinfección de oficinas panamá |
| Local | fumigación + [Costa del Este, San Francisco, Condado del Rey, San Miguelito, Arraiján, La Chorrera…] |
