# Anthox PTY – Sitio web de control de plagas

Sitio web estático (HTML + CSS + JS, sin dependencias) para **Anthox PTY Control de Plagas**, Ciudad de Panamá.

## Estructura
```
index.html            Página principal (5 secciones: Inicio, Servicios, Plagas, Nosotros, Contacto) + blog destacado
blog/                 Índice del blog + 5 artículos SEO (generados)
css/styles.css        Estilos (paleta del logo: verde bosque, verde lima, negro)
js/main.js            Widget de WhatsApp, cotizador, identificador de plagas, animaciones
assets/img/           Logo y favicons
tools/posts.py        Contenido de los artículos del blog
tools/build_blog.py   Genera blog/*.html y sitemap.xml
sitemap.xml, robots.txt
SEO-GUIA.md           Plan para posicionar en Google Maps y Google
```

## Ver el sitio
Abre `index.html` en el navegador, o: `python3 -m http.server` y visita http://localhost:8000

## Editar
- **WhatsApp / teléfono:** `+507 6761-9763` (`WA_NUMBER` en `js/main.js` y enlaces `wa.me/50767619763`).
- **Precios del cotizador:** objeto `PRICES` y `PEST_EXTRA` en `js/main.js`.
- **Nuevo artículo:** agrega un bloque en `tools/posts.py` y ejecuta `python3 tools/build_blog.py`.
- **Dominio:** reemplaza `https://www.anthoxpty.com` (ver `SEO-GUIA.md`).

## Publicar
Sube la carpeta a Netlify, Cloudflare Pages o GitHub Pages. Después sigue `SEO-GUIA.md`.
