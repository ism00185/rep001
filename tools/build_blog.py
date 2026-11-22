#!/usr/bin/env python3
"""
Generador del blog de Anthox PTY.

Uso:  python3 tools/build_blog.py
Genera blog/index.html, cada artículo en blog/<slug>.html y sitemap.xml.

Para agregar un artículo nuevo: copia un bloque de POSTS (en tools/posts.py),
cambia slug, título, descripción y contenido, y vuelve a ejecutar el script.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from posts import POSTS  # noqa: E402

SITE = "https://www.anthoxpty.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT, "blog")
WA = "50767619763"

ICONS = {
    "drop": '<path d="M12 2c-3 4-6 7-6 11a6 6 0 0 0 12 0c0-4-3-7-6-11z"/><path d="M9 14a3 3 0 0 0 3 3"/>',
    "house": '<path d="M3 21h18M5 21V9l7-5 7 5v12"/><path d="M9 21v-4h6v4"/>',
    "roach": '<ellipse cx="12" cy="14" rx="4" ry="6"/><path d="M12 8V5M8 12H5M8 16l-3 2M16 12h3M16 16l3 2M10 6L7 3M14 6l3-3"/>',
    "rat": '<path d="M3 15c0-4 3-7 8-7 3 0 5 1.5 6.5 3l3 1.5c.8.4.4 1.5-.4 1.5H18c-1 2-3.5 3-7 3H5c-1.2 0-2-1-2-2z"/><path d="M4 16.5c-2 .8-2.5 3-1 4.5"/>',
    "calendar": '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4M8 14h3v3H8z"/>',
}

WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.05 21.5a9.5 9.5 0 0 1-4.84-1.33l-.35-.2-3.6.94.96-3.5-.23-.36A9.48 9.48 0 0 1 2.5 12 '
          '9.52 9.52 0 0 1 12.05 2.5 9.45 9.45 0 0 1 21.5 12a9.5 9.5 0 0 1-9.45 9.5zm8.08-17.6A11.4 11.4 0 0 0 12.05.5 11.46 11.46 0 0 0 2.13 17.67L.5 23.5l5.97-1.57A11.44 11.44 0 0 0 23.5 12c0-3.06-1.19-5.94-3.37-8.1z"/></svg>')


def head(title, desc, canonical, extra_ld, og_type="website"):
    return f"""<!DOCTYPE html>
<html lang="es-PA" data-root="../">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="geo.region" content="PA-8">
  <meta name="geo.placename" content="Ciudad de Panamá">
  <meta name="theme-color" content="#41781d">
  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="es_PA">
  <meta property="og:site_name" content="Anthox PTY Control de Plagas">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/img/anthox-logo.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="../favicon.png">
  <link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/styles.css">
{extra_ld}
</head>
<body>
<div class="progress" aria-hidden="true"></div>
<a class="skip-link" href="#main">Saltar al contenido</a>
<header class="header">
  <div class="container">
    <a class="brand" href="../" aria-label="Anthox PTY – inicio">
      <img src="../assets/img/favicon-512.png" alt="Logo de Anthox PTY Control de Plagas" width="54" height="54">
      <span class="brand-text">ANTH<span>OX</span><small>CONTROL DE PLAGAS</small></span>
    </a>
    <nav class="nav" aria-label="Principal">
      <ul>
        <li><a href="../">Inicio</a></li>
        <li><a href="../#servicios">Servicios</a></li>
        <li><a href="../#plagas">Plagas</a></li>
        <li><a href="../#nosotros">Nosotros</a></li>
        <li><a class="active" href="./">Blog</a></li>
        <li><a href="../#contacto">Contacto</a></li>
        <li><a class="btn btn-primary" href="../#cotizar">Cotizar gratis</a></li>
      </ul>
    </nav>
    <button class="menu-toggle" type="button" aria-label="Abrir menú" aria-expanded="false"><span></span></button>
  </div>
</header>
<main id="main">
"""


FOOTER = """</main>
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="../"><img src="../assets/img/favicon-512.png" alt="Anthox PTY" width="54" height="54" loading="lazy"><span class="brand-text">ANTH<span>OX</span><small>CONTROL DE PLAGAS</small></span></a>
        <p>Fumigación y control de plagas profesional en Ciudad de Panamá. Hogares, negocios e industrias protegidos con garantía.</p>
      </div>
      <div><h4>Servicios</h4><ul><li><a href="../#servicios">Fumigación residencial</a></li><li><a href="../#servicios">Fumigación comercial</a></li><li><a href="../#servicios">Tratamiento de comején</a></li><li><a href="../#servicios">Control de mosquitos</a></li></ul></div>
      <div><h4>Blog</h4><ul>{blog_links}</ul></div>
      <div><h4>Contacto</h4><ul><li>📍 Ciudad de Panamá, Panamá</li><li>📞 <a href="tel:+50767619763">+507 6761-9763</a></li><li>💬 <a href="https://wa.me/50767619763" target="_blank" rel="noopener">WhatsApp</a></li><li>🕖 Lun–Sáb 7:00 am – 7:00 pm</li></ul></div>
    </div>
    <div class="footer-bottom"><span>© <span class="year">2026</span> Anthox PTY Control de Plagas.</span><span>Fumigación en Panamá · Control de plagas en Ciudad de Panamá</span></div>
  </div>
</footer>
<script src="../js/main.js" defer></script>
</body>
</html>
"""


def ld(obj):
    return '  <script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n  </script>"


def publisher():
    return {"@type": "Organization", "name": "Anthox PTY Control de Plagas",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/anthox-logo.jpg"}}


def icon(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">{ICONS[name]}</svg>'


def card(p, i, prefix=""):
    d = " d%d" % (i % 3) if i % 3 else ""
    return (f'<a class="post-card reveal{d}" href="{prefix}{p["slug"]}.html">'
            f'<div class="post-thumb {p["theme"]}">{icon(p["icon"])}</div>'
            f'<div class="post-body"><div class="post-meta"><span>{p["category"]}</span><span>·</span><span>{p["read"]} min</span></div>'
            f'<h3>{html.escape(p["title"])}</h3><p>{html.escape(p["excerpt"])}</p><span class="link-arrow">Leer artículo</span></div></a>')


def footer():
    links = "".join(f'<li><a href="{p["slug"]}.html">{html.escape(p["short"])}</a></li>' for p in POSTS)
    return FOOTER.replace("{blog_links}", links)


def build_post(p):
    url = f"{SITE}/blog/{p['slug']}.html"
    article_ld = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": p["title"], "description": p["description"],
        "datePublished": p["date"], "dateModified": p["date"],
        "inLanguage": "es-PA", "mainEntityOfPage": url,
        "image": f"{SITE}/assets/img/anthox-logo.jpg",
        "author": {"@type": "Organization", "name": "Equipo técnico Anthox PTY", "url": SITE + "/"},
        "publisher": publisher(),
        "about": p["keywords"], "keywords": ", ".join(p["keywords"]),
        "spatialCoverage": {"@type": "Place", "name": "Ciudad de Panamá, Panamá"},
    }
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["short"], "item": url},
        ],
    }
    blocks = [ld(article_ld), ld(crumbs)]
    if p.get("faq"):
        blocks.append(ld({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]],
        }))
    faq_html = ""
    if p.get("faq"):
        faq_html = '<h2 id="preguntas">Preguntas frecuentes</h2><div class="faq" style="margin:0">' + "".join(
            f"<details><summary>{html.escape(q)}</summary><div>{html.escape(a)}</div></details>" for q, a in p["faq"]) + "</div>"
    related = [x for x in POSTS if x["slug"] != p["slug"]][:3]
    toc = "".join(f'<li><a href="#{a}">{html.escape(t)}</a></li>' for a, t in p["toc"])
    wa_msg = html.escape(p["wa"])
    out = head(p["seo_title"], p["description"], url, "\n".join(blocks), og_type="article")
    out += f"""
<section class="article-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Ruta"><a href="../">Inicio</a> › <a href="./">Blog</a> › {html.escape(p["short"])}</nav>
    <span class="eyebrow"><span class="dot"></span> {p["category"]} · {p["read"]} min de lectura</span>
    <h1>{html.escape(p["title"])}</h1>
    <p style="max-width:760px;font-size:1.1rem">{html.escape(p["description"])}</p>
    <p style="font-size:.88rem;color:#9fb88a;margin:0">Por el equipo técnico de Anthox PTY · Publicado el <time datetime="{p["date"]}">{p["date_h"]}</time></p>
  </div>
</section>
<div class="container article-layout">
  <article class="prose">
    <nav class="toc" aria-label="Contenido"><strong>En este artículo</strong><ol>{toc}</ol></nav>
    {p["body"]}
    {faq_html}
    <div class="callout"><strong>¿Necesitas ayuda profesional?</strong><p style="margin:.4em 0 1em">En Anthox PTY atendemos casas, apartamentos y negocios en toda la Ciudad de Panamá y Panamá Oeste. Cotiza gratis y sin compromiso.</p>
      <a class="btn btn-wa" href="#" data-wa="{wa_msg}">{WA_SVG} Escribir por WhatsApp</a></div>
  </article>
  <aside class="sidebar">
    <div class="side-card dark"><h3>Cotización gratis</h3><p style="color:#eef7e1">Respuesta en minutos por WhatsApp. Lunes a sábado, 7 am – 7 pm.</p>
      <a class="btn btn-dark" href="#" data-wa="{wa_msg}" style="width:100%">Cotizar ahora</a>
      <p style="margin:12px 0 0;font-size:.9rem">o llama al <a href="tel:+50767619763" style="color:#fff;font-weight:700">+507 6761-9763</a></p></div>
    <div class="side-card"><h3>Artículos relacionados</h3><ul>{"".join(f'<li><a href="{r["slug"]}.html">{html.escape(r["title"])}</a></li>' for r in related)}</ul></div>
    <div class="side-card"><h3>Servicios</h3><ul><li><a href="../#servicios">Fumigación residencial</a></li><li><a href="../#servicios">Fumigación comercial</a></li><li><a href="../#servicios">Tratamiento de comején</a></li><li><a href="../#estimator">Cotizador en línea</a></li></ul></div>
  </aside>
</div>
<section class="section section-soft" style="padding-top:70px">
  <div class="container">
    <div class="section-head"><span class="kicker">Sigue leyendo</span><h2>Más consejos para Panamá</h2></div>
    <div class="blog-grid">{"".join(card(r, i) for i, r in enumerate(related))}</div>
  </div>
</section>
"""
    out += footer()
    with open(os.path.join(BLOG_DIR, p["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(out)


def build_index():
    url = f"{SITE}/blog/"
    blog_ld = {
        "@context": "https://schema.org", "@type": "Blog", "name": "Blog de control de plagas en Panamá – Anthox PTY",
        "url": url, "inLanguage": "es-PA", "publisher": publisher(),
        "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/blog/{p['slug']}.html", "datePublished": p["date"]} for p in POSTS],
    }
    out = head("Blog de Fumigación y Control de Plagas en Panamá | Anthox PTY",
               "Consejos y guías sobre cucarachas, comején, ratas, mosquitos y dengue en Panamá. Aprende a prevenir plagas en tu casa o negocio con expertos locales.",
               url, ld(blog_ld))
    out += f"""
<section class="article-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Ruta"><a href="../">Inicio</a> › Blog</nav>
    <span class="eyebrow"><span class="dot"></span> Blog Anthox PTY</span>
    <h1>Guías de control de plagas para hogares y negocios en Panamá</h1>
    <p style="max-width:760px;font-size:1.1rem">Información práctica, escrita por técnicos locales, sobre las plagas más comunes en Ciudad de Panamá y cómo prevenirlas en nuestro clima tropical.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="blog-grid">{"".join(card(p, i) for i, p in enumerate(POSTS))}</div>
    <div class="cta-band" style="margin-top:70px">
      <div><h2>¿Prefieres que lo resolvamos por ti?</h2><p>Cotiza tu fumigación en Ciudad de Panamá en minutos.</p></div>
      <a class="btn btn-dark" href="#" data-wa="Hola Anthox PTY, leí su blog y quiero cotizar una fumigación.">Hablar por WhatsApp</a>
    </div>
  </div>
</section>
"""
    out += footer()
    with open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)


def build_sitemap():
    last = max(p["date"] for p in POSTS)
    urls = [(SITE + "/", last, "1.0", "weekly"), (SITE + "/blog/", last, "0.8", "weekly")]
    urls += [(f"{SITE}/blog/{p['slug']}.html", p["date"], "0.7", "monthly") for p in POSTS]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, mod, pr, ch in urls:
        xml.append(f"  <url><loc>{loc}</loc><lastmod>{mod}</lastmod><changefreq>{ch}</changefreq><priority>{pr}</priority></url>")
    xml.append("</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(xml))


if __name__ == "__main__":
    os.makedirs(BLOG_DIR, exist_ok=True)
    for p in POSTS:
        build_post(p)
    build_index()
    build_sitemap()
    print(f"OK: {len(POSTS)} artículos + blog/index.html + sitemap.xml")
