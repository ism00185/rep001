#!/usr/bin/env python3
"""Genera el Manual de Marca de Anthox PTY (HTML -> PDF con Playwright).
Uso: python3 build.py && node render.js
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_R = 1434 / 1575   # alto / ancho del logo completo
ISO_R = 795 / 1117     # alto / ancho del isotipo

# ---------------------------------------------------------------- helpers
def img(name, x, y, w, ratio=LOGO_R, extra=""):
    return f'<image href="img/{name}.png" x="{x}" y="{y}" width="{w}" height="{w*ratio:.1f}" preserveAspectRatio="xMidYMid meet" {extra}/>'

def shadow(cx, cy, rx, ry, op=.35):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity="{op}" filter="url(#blur)"/>'

def darker(hexc, f=.78):
    h = hexc.lstrip('#'); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return '#%02x%02x%02x' % (int(r*f), int(g*f), int(b*f))

# ---------------------------------------------------------------- prendas
SWEATER = "M146 34 Q200 62 254 34 L318 56 Q352 68 362 112 L396 368 Q370 382 344 380 L306 178 L304 418 Q200 432 96 418 L94 178 L56 380 Q30 382 4 368 L38 112 Q48 68 82 56 Z"
TEE = "M146 30 Q200 58 254 30 L330 54 Q356 62 366 84 L398 160 L340 186 L310 140 L308 420 Q200 430 92 420 L90 140 L60 186 L2 160 L34 84 Q44 62 70 54 Z"

def fabric(path, color):
    return (f'<path d="{path}" fill="{color}"/>'
            f'<path d="{path}" fill="url(#fabricShade)"/>'
            f'<path d="{path}" fill="#fff" filter="url(#noise)" opacity=".07"/>')

def sweater(color, logo, hood=False, label=""):
    d = darker(color)
    s = f'<svg viewBox="-10 -50 420 500" class="mock">{shadow(200, 432, 170, 14)}'
    if hood:
        s += f'<path d="M128 46 Q112 -34 200 -40 Q288 -34 272 46 Q200 92 128 46 Z" fill="{d}"/>'
    s += fabric(SWEATER, color)
    s += f'<path d="M10 342 L60 354 L56 380 Q30 382 4 368 Z M390 342 L340 354 L344 380 Q370 382 396 368 Z M96 400 Q200 414 304 400 L304 418 Q200 432 96 418 Z" fill="{d}"/>'
    s += '<path d="M10 348 L58 360 M12 356 L57 368 M390 348 L342 360 M98 406 Q200 420 302 406" stroke="#000" stroke-opacity=".12" fill="none"/>'
    s += '<path d="M94 178 Q112 262 100 336 M306 178 Q288 262 300 336 M150 330 Q200 344 250 330" stroke="#000" stroke-opacity=".12" stroke-width="3" fill="none"/>'
    if hood:
        s += f'<path d="M146 36 Q160 -8 200 -10 Q240 -8 254 36 Q200 78 146 36 Z" fill="{darker(color,.5)}"/>'
        s += '<path d="M182 62 Q180 110 176 150 M218 62 Q220 110 224 150" stroke="#f3f3f3" stroke-width="4" stroke-linecap="round" fill="none"/>'
        s += f'<path d="M128 300 L272 300 L292 392 L108 392 Z" fill="none" stroke="{darker(color,.6)}" stroke-width="3" opacity=".7"/>'
        s += img(logo, 148, 168, 104)
    else:
        s += f'<path d="M146 34 Q200 62 254 34 L264 41 Q200 82 136 41 Z" fill="{d}"/>'
        s += img(logo, 145, 98, 110)
    return s + '</svg>'

def tee(color, logo=None, polo=False, back=False, text_color="#fff"):
    d = darker(color)
    s = f'<svg viewBox="-10 -10 420 460" class="mock">{shadow(200, 428, 165, 12)}' + fabric(TEE, color)
    s += f'<path d="M60 186 L2 160 L8 146 L66 172 Z M340 186 L398 160 L392 146 L334 172 Z" fill="{d}"/>'
    s += '<path d="M90 140 Q106 240 96 330 M310 140 Q294 240 304 330" stroke="#000" stroke-opacity=".12" stroke-width="3" fill="none"/>'
    if back:
        s += f'<path d="M146 30 Q200 44 254 30 L262 36 Q200 56 138 36 Z" fill="{d}"/>'
        s += img(logo, 140, 80, 120, ISO_R)
        s += (f'<text x="200" y="228" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="34" fill="{text_color}" letter-spacing="1">ANTHOX</text>'
              f'<text x="200" y="256" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="11" fill="#7cb518" letter-spacing="3">CONTROL DE PLAGAS</text>'
              f'<text x="200" y="300" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="17" fill="{text_color}">+507 6761-9763</text>'
              f'<text x="200" y="322" text-anchor="middle" font-family="Inter" font-size="12" fill="{text_color}" opacity=".8">anthoxpty.com</text>')
    elif polo:
        s += f'<path d="M146 30 L200 72 L166 96 L130 40 Z" fill="{d}"/><path d="M254 30 L200 72 L234 96 L270 40 Z" fill="{d}"/>'
        s += f'<rect x="192" y="66" width="16" height="84" fill="{darker(color,.88)}"/><circle cx="200" cy="92" r="3" fill="#ddd"/><circle cx="200" cy="120" r="3" fill="#ddd"/>'
        s += img(logo, 232, 112, 66)
    else:
        s += f'<path d="M146 30 Q200 58 254 30 L262 36 Q200 74 138 36 Z" fill="{d}"/>'
        s += img(logo, 140, 92, 120)
    return s + '</svg>'

def cap(color, logo, bill=None):
    bill = bill or darker(color, .7)
    crown = "M70 204 Q64 70 200 58 Q336 70 330 204 Z"
    return (f'<svg viewBox="20 30 360 270" class="mock">{shadow(200, 270, 150, 12)}'
            f'<path d="{crown}" fill="{color}"/><path d="{crown}" fill="url(#fabricShade)"/><path d="{crown}" fill="#fff" filter="url(#noise)" opacity=".07"/>'
            '<path d="M200 60 L200 200 M132 74 Q150 140 138 204 M268 74 Q250 140 262 204" stroke="#000" stroke-opacity=".18" stroke-width="2" fill="none"/>'
            f'<circle cx="200" cy="61" r="7" fill="{darker(color,.6)}"/>'
            + img(logo, 145, 104, 110, ISO_R) +
            f'<path d="M52 198 Q200 172 348 198 Q362 240 200 256 Q38 240 52 198 Z" fill="{bill}"/>'
            '<path d="M60 206 Q200 186 340 206" stroke="#fff" stroke-opacity=".18" stroke-width="2" fill="none" stroke-dasharray="4 4"/>'
            '</svg>')

def mug(color, logo, inner, handle=None):
    handle = handle or color
    body = "M60 60 L270 60 L270 262 Q270 282 248 282 L82 282 Q60 282 60 262 Z"
    return (f'<svg viewBox="20 20 340 300" class="mock">{shadow(170, 286, 130, 10, .4)}'
            f'<path d="M262 96 C346 92 346 236 262 232" stroke="{handle}" stroke-width="26" fill="none" stroke-linecap="round"/>'
            '<path d="M262 96 C346 92 346 236 262 232" stroke="url(#cylH)" stroke-width="26" fill="none" stroke-linecap="round"/>'
            f'<path d="{body}" fill="{color}"/>'
            + img(logo, 105, 98, 120) +
            f'<path d="{body}" fill="url(#cyl)"/>'
            f'<ellipse cx="165" cy="60" rx="105" ry="15" fill="{color}"/><ellipse cx="165" cy="61" rx="97" ry="11" fill="{inner}"/>'
            '<ellipse cx="165" cy="63" rx="97" ry="9" fill="url(#rim)"/>'
            '</svg>')

def van():
    body = "M40 250 L40 92 Q40 60 72 60 L520 60 Q556 60 588 92 L676 170 Q722 176 742 202 L754 248 Q754 270 732 270 L60 270 Q40 270 40 250 Z"
    return ('<svg viewBox="0 20 800 340" class="mock">' + shadow(400, 318, 380, 14, .45) +
            f'<path d="{body}" fill="#fbfbfb"/>'
            '<clipPath id="vanclip"><path d="' + body + '"/></clipPath><g clip-path="url(#vanclip)">'
            '<path d="M0 300 L0 196 Q260 250 560 150 L800 150 L800 300 Z" fill="url(#gradBrand)"/>'
            '<path d="M0 196 Q260 250 560 150 L800 150 L800 162 L566 162 Q262 266 0 212 Z" fill="#a5d34a"/>'
            '<path d="M0 60 L800 60 L800 340 L0 340 Z" fill="url(#cylV)"/></g>'
            '<path d="M548 78 Q578 78 596 96 L664 160 L548 160 Z" fill="url(#glass)"/>'
            '<path d="M532 64 L532 266 M686 172 L686 266" stroke="#000" stroke-opacity=".18" stroke-width="2"/>'
            '<rect x="640" y="178" width="22" height="6" rx="3" fill="#bbb"/>'
            '<path d="M736 198 Q748 204 750 220 L736 220 Z" fill="#ffe9a8"/>'
            '<rect x="720" y="248" width="40" height="18" rx="6" fill="#222"/><rect x="30" y="246" width="30" height="20" rx="6" fill="#222"/>'
            + ''.join(f'<circle cx="{x}" cy="272" r="56" fill="#1a1a1a"/><circle cx="{x}" cy="272" r="46" fill="#2b2b2b"/><circle cx="{x}" cy="272" r="24" fill="#9aa3a8"/><circle cx="{x}" cy="272" r="8" fill="#555"/>' for x in (170, 622))
            + img('logo-color', 70, 74, 150) +
            '<text x="240" y="110" font-family="Montserrat" font-weight="900" font-size="25" fill="#141414">FUMIGACIÓN Y</text>'
            '<text x="240" y="140" font-family="Montserrat" font-weight="900" font-size="25" fill="#41781d">CONTROL DE PLAGAS</text>'
            '<text x="242" y="166" font-family="Inter" font-weight="600" font-size="13.5" fill="#555">Hogares · Negocios · Restaurantes</text>'
            '<text x="270" y="244" font-family="Montserrat" font-weight="800" font-size="26" fill="#fff">WhatsApp +507 6761-9763</text>'
            '<text x="580" y="210" font-family="Montserrat" font-weight="700" font-size="15" fill="#fff">anthoxpty.com</text>'
            '</svg>')

def tote():
    bag = "M86 130 L314 130 L332 418 L68 418 Z"
    return (f'<svg viewBox="40 20 320 420" class="mock">{shadow(200, 424, 140, 10)}'
            '<path d="M130 136 Q130 40 200 40 Q270 40 270 136" stroke="#141414" stroke-width="14" fill="none"/>'
            f'<path d="{bag}" fill="#efe7d6"/><path d="{bag}" fill="url(#fabricShade)"/><path d="{bag}" fill="#000" filter="url(#noise)" opacity=".08"/>'
            '<path d="M130 136 L130 160 M270 136 L270 160" stroke="#141414" stroke-width="14"/>'
            + img('logo-color', 120, 190, 160) + '</svg>')

def bottle():
    return ('<svg viewBox="0 0 200 420" class="mock">' + shadow(100, 404, 60, 8) +
            '<rect x="62" y="20" width="76" height="54" rx="12" fill="#141414"/><rect x="70" y="70" width="60" height="12" fill="#2a2a2a"/>'
            '<path d="M58 82 L142 82 Q156 82 156 98 L156 386 Q156 402 140 402 L60 402 Q44 402 44 386 L44 98 Q44 82 58 82 Z" fill="#2f6b16"/>'
            + img('logo-blanco', 58, 180, 84) +
            '<path d="M58 82 L142 82 Q156 82 156 98 L156 386 Q156 402 140 402 L60 402 Q44 402 44 386 L44 98 Q44 82 58 82 Z" fill="url(#cyl)"/>'
            '<text x="100" y="330" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="11" fill="#a5d34a" letter-spacing="2">ANTHOX PTY</text>'
            '</svg>')

# ---------------------------------------------------------------- iconos de plagas (del sitio web)
PESTS = {
 "Cucaracha": '<ellipse cx="32" cy="36" rx="10" ry="16"/><path d="M32 22v28"/><circle cx="32" cy="18" r="5"/><path d="M29 14C24 6 16 4 10 6M35 14c5-8 13-10 19-8M22 30l-10-6M22 37H9M23 44l-10 8M42 30l10-6M42 37h13M41 44l10 8"/>',
 "Roedor": '<path d="M10 40c0-10 9-18 21-18 8 0 13 4 17 8l8 4c2 1 1 4-1 4h-6c-3 5-9 8-18 8H14c-3 0-4-3-4-6z"/><circle cx="42" cy="26" r="5"/><path d="M12 44c-6 2-8 8-4 12M24 46l-2 6M36 46l2 6"/>',
 "Mosquito": '<path d="M32 22l2 22M33 44l1 10"/><circle cx="31" cy="19" r="4"/><path d="M30 16l-8-8M33 26c8-10 18-12 22-8-4 6-12 9-21 10zM31 26c-8-10-18-12-22-8 4 6 12 9 21 10zM33 32l14 8 4 12M32 34l-12 8-4 12"/>',
 "Hormiga": '<circle cx="32" cy="16" r="6"/><ellipse cx="32" cy="29" rx="4.5" ry="6"/><ellipse cx="32" cy="46" rx="9" ry="12"/><path d="M28 12l-6-8M36 12l6-8M28 27l-12-6-4 6M36 27l12-6 4 6M28 33l-10 12v10M36 33l10 12v10"/>',
 "Comején": '<circle cx="32" cy="14" r="6"/><ellipse cx="32" cy="38" rx="9" ry="18"/><path d="M29 9l-4-5M35 9l4-5M24 30h16M23 37h18M24 44h16M24 24l-12-4M40 24l12-4M24 40l-11 8M40 40l11 8"/>',
 "Chinche": '<ellipse cx="32" cy="38" rx="15" ry="16"/><ellipse cx="32" cy="20" rx="7" ry="5"/><path d="M28 16l-5-7M36 16l5-7M18 30l-9-4M46 30l9-4M17 40H7M47 40h10M19 48l-8 7M45 48l8 7"/>',
 "Araña": '<ellipse cx="32" cy="40" rx="9" ry="11"/><circle cx="32" cy="25" r="6"/><path d="M27 23L14 12 6 18M37 23l13-11 8 6M26 27L10 26 4 34M38 27l16-1 6 8M27 30L12 38l-4 10M37 30l15 8 4 10"/>',
 "Polilla": '<path d="M32 20c-6-8-22-12-24-4-2 9 8 18 22 16zM32 20c6-8 22-12 24-4 2 9-8 18-22 16z"/><ellipse cx="32" cy="34" rx="3" ry="14"/><path d="M31 20l-5-8M33 20l5-8"/>',
}
def pest_icon(name, color="#141414"):
    return f'<svg viewBox="0 0 64 64" fill="none" stroke="{color}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{PESTS[name]}</svg>'

# ---------------------------------------------------------------- color
def cmyk(h):
    r, g, b = (int(h[i:i+2], 16)/255 for i in (1, 3, 5)); k = 1-max(r, g, b)
    if k == 1: return "0 · 0 · 0 · 100"
    c, m, y = ((1-x-k)/(1-k) for x in (r, g, b))
    return " · ".join(str(round(v*100)) for v in (c, m, y, k))
def rgb(h): return " · ".join(str(int(h[i:i+2], 16)) for i in (1, 3, 5))

COLORS = [
  ("Verde Anthox", "#41781D", "Pantone 364 C*", "Color principal. Logotipo, titulares, uniformes y vehículos.", "#fff"),
  ("Verde Lima", "#7CB518", "Pantone 376 C*", "Acento de energía. Botones, destacados y degradados.", "#141414"),
  ("Negro Carbón", "#141414", "Pantone Black 6 C*", "Textos, uniformes y fondos premium.", "#fff"),
  ("Verde Profundo", "#1F3D0E", "Pantone 553 C*", "Fondos oscuros de marca y piezas institucionales.", "#fff"),
  ("Lima Claro", "#A5D34A", "Pantone 367 C*", "Detalles sobre fondos oscuros e iconografía.", "#141414"),
  ("Hueso", "#F6F9F1", "—", "Fondo neutro claro para web y papelería.", "#141414"),
]

# ---------------------------------------------------------------- páginas
pages = []
def page(sec, title, body, dark=False, cls=""):
    n = len(pages) + 1
    head = (f'<div class="ph"><span>ANTHOX PTY · MANUAL DE IDENTIDAD</span><span>{sec}</span></div>' if sec else "")
    foot = f'<div class="pf"><span>{title}</span><span>{n:02d}</span></div>' if sec else ""
    mark = '</p></div></div>'
    if body.startswith('<div class="sh">'):
        i = body.index(mark) + len(mark)
        body = body[:i] + '<div class="content">' + body[i:] + '</div>'
        cls += " flex"
    pages.append(f'<section class="page {"dark" if dark else ""} {cls}">{head}{body}{foot}</section>')

def sechead(num, title, sub):
    return f'<div class="sh"><div class="num">{num}</div><div><h2>{title}</h2><p class="sub">{sub}</p></div></div>'

# 1 Portada
page("", "", f'''
<div class="cover-pattern"></div>
<div class="cover">
  <div class="cover-left">
    <div class="eyebrow">Manual de identidad de marca · v1.0</div>
    <h1>Brand<br>Book</h1>
    <p class="lead">Guía oficial para el uso del logotipo, color, tipografía, tono de voz y aplicaciones de <b>Anthox PTY Control de Plagas</b>.</p>
    <div class="cover-meta"><span>Ciudad de Panamá</span><span>2026</span><span>+507 6761-9763</span></div>
  </div>
  <div class="cover-right"><div class="halo"></div><img src="img/logo-negativo.png" alt=""></div>
</div>''', dark=True, cls="cover-page")

# 2 Índice
idx = [("01", "Esencia de marca", "Misión, visión, valores y personalidad"),
       ("02", "Logotipo", "Anatomía, área de protección, versiones y usos incorrectos"),
       ("03", "Color", "Paleta oficial y proporciones"),
       ("04", "Tipografía", "Familias, jerarquías y estilos"),
       ("05", "Elementos gráficos", "Patrón, degradado e iconografía"),
       ("06", "Tono de voz", "Cómo hablamos con nuestros clientes"),
       ("07", "Aplicaciones", "Suéteres, uniformes, tazas, papelería, vehículo, merch y digital")]
page("Índice", "Contenido", f'''
<div class="idx-wrap">
  <div><div class="eyebrow green">Contenido</div><h2 class="big">Todo lo que<br>necesitas para<br>usar la marca<br><span class="g">correctamente.</span></h2></div>
  <ol class="idx">{"".join(f'<li><b>{a}</b><div><strong>{b}</strong><span>{c}</span></div></li>' for a,b,c in idx)}</ol>
</div>''')

# 3 Esencia
page("01 · Esencia", "Esencia de marca", sechead("01", "Esencia de marca", "Quiénes somos y por qué existimos") + '''
<div class="grid3 mt">
  <div class="card"><div class="k">Quiénes somos</div><p>Anthox PTY es una empresa panameña de fumigación y control de plagas con base en Ciudad de Panamá. Protegemos hogares, PH, oficinas, restaurantes e industrias con tratamientos profesionales, seguros y con garantía por escrito.</p></div>
  <div class="card"><div class="k">Misión</div><p>Eliminar y prevenir plagas con soluciones eficaces, seguras para las familias y el ambiente, brindando una atención rápida, puntual y honesta a cada cliente de Panamá.</p></div>
  <div class="card"><div class="k">Visión</div><p>Ser la empresa de control de plagas más recomendada de Panamá, reconocida por su profesionalismo, su tecnología y la confianza que genera en cada servicio.</p></div>
</div>
<div class="promise">
  <div class="eyebrow green">Promesa de marca</div>
  <p class="quote">“Adiós a las plagas.<br><span class="g">Hola a la tranquilidad.</span>”</p>
</div>''')

# 4 Valores + personalidad
vals = [("Confianza", "Garantía por escrito, precios claros y técnicos identificados."),
        ("Seguridad", "Productos de baja toxicidad, seguros para niños y mascotas."),
        ("Puntualidad", "Llegamos a la hora acordada y avisamos por WhatsApp."),
        ("Experiencia", "Técnicos capacitados en manejo integrado de plagas."),
        ("Cercanía", "Somos panameños: conocemos el clima, los barrios y sus plagas.")]
page("01 · Esencia", "Valores y personalidad", sechead("01", "Valores y personalidad", "Lo que nos guía en cada servicio") + f'''
<div class="vals mt">{"".join(f'<div class="val"><div class="vn">{i+1:02d}</div><h3>{a}</h3><p>{b}</p></div>' for i,(a,b) in enumerate(vals))}</div>
<div class="persona">
  <div><div class="k">Si Anthox fuera una persona…</div><p>Sería un técnico experto, uniformado e impecable, que habla claro, explica lo que hace y deja todo limpio. Firme contra las plagas, amable con las personas.</p></div>
  <div class="sliders">
    {"".join(f'<div class="sl"><span>{a}</span><div class="bar"><i style="left:{p}%"></i></div><span>{b}</span></div>' for a,b,p in [("Formal","Cercano",62),("Técnico","Sencillo",58),("Agresivo","Tranquilo",35),("Tradicional","Moderno",78),("Económico","Premium",66)])}
  </div>
</div>''')

# 5 Logotipo principal / anatomía
page("02 · Logotipo", "Logotipo principal", sechead("02", "Logotipo principal", "Nuestra firma visual: siempre igual, siempre reconocible") + '''
<div class="anat">
  <div class="anat-logo"><img src="img/logo-color.png" alt="">
    
  </div>
  <div class="anat-text">
    <div class="li"><b>A</b><div><strong>Isotipo</strong><p>La “A” de Anthox se levanta como el techo de un hogar protegido. A su alrededor, las plagas que combatimos y el técnico en acción, enmarcados en un círculo de protección.</p></div></div>
    <div class="li"><b>B</b><div><strong>Logotipo</strong><p>“ANTHOX” en letras robustas e itálicas que transmiten fuerza y rapidez. La “O” es una mira sobre la hormiga: precisión en cada tratamiento.</p></div></div>
    <div class="li"><b>C</b><div><strong>Descriptor</strong><p>“CONTROL DE PLAGAS” aclara el servicio y refuerza el posicionamiento local junto al sufijo “PTY”.</p></div></div>
    <div class="li"><b>D</b><div><strong>Sello</strong><p>El chevrón inferior cierra la composición como un escudo: protección y garantía.</p></div></div>
  </div>
</div>''')

# 6 Área de protección
page("02 · Logotipo", "Área de protección y tamaños mínimos", sechead("02", "Área de protección", "Espacio libre y tamaños mínimos de reproducción") + '''
<div class="prot">
  <div class="prot-box"><div class="zone"><img src="img/logo-color.png" alt=""></div>
    <span class="x xt">X</span><span class="x xb">X</span><span class="x xl">X</span><span class="x xr">X</span></div>
  <div>
    <p class="body">Alrededor del logotipo debe respetarse un espacio libre equivalente a <b>X</b>, donde X es la altura de la letra “A” de la palabra ANTHOX. Ningún texto, imagen o borde puede invadir esta zona.</p>
    <div class="mins">
      <div><img src="img/logo-color.png" style="width:120px"><span>Impreso: <b>25 mm</b><br>Digital: <b>120 px</b></span></div>
      <div><img src="img/iso-color.png" style="width:70px"><span>Isotipo impreso: <b>12 mm</b><br>Digital: <b>48 px</b></span></div>
    </div>
    <p class="note">Por debajo de 25 mm utiliza el isotipo solo, o una versión monocromática, para conservar la legibilidad de los detalles.</p>
  </div>
</div>''')

# 7 Versiones
vers = [("Principal a color", "logo-color", "#ffffff", "Fondos blancos o claros."),
        ("Negativo", "logo-negativo", "#141414", "Fondos negros o muy oscuros."),
        ("Negativo sobre verde", "logo-negativo", "#1F3D0E", "Fondos verde profundo."),
        ("Monocromático negro", "logo-negro", "#F6F9F1", "Fax, sellos, grabado y prensa B/N."),
        ("Monocromático blanco", "logo-blanco", "#41781D", "Bordado, serigrafía 1 tinta, vinil."),
        ("Isotipo", "iso-color", "#ffffff", "Redes sociales, favicon, gorras, sellos.")]
page("02 · Logotipo", "Versiones del logotipo", sechead("02", "Versiones", "Una versión para cada fondo y técnica de impresión") + f'''
<div class="vers mt">{"".join(f'<div class="ver"><div class="vbox" style="background:{bg}"><img src="img/{f}.png" class="{"iso" if "iso" in f else ""}"></div><strong>{t}</strong><span>{d}</span></div>' for t,f,bg,d in vers)}</div>''')

# 8 Usos incorrectos
bad = [("No deformar", "transform:scaleX(1.45)"), ("No rotar", "transform:rotate(-18deg)"),
       ("No cambiar colores", "filter:hue-rotate(150deg)"), ("No añadir sombras", "filter:drop-shadow(8px 8px 3px rgba(0,0,0,.6))"),
       ("No usar sobre fondos sin contraste", "BG:#4f9a1f"), ("No usar la versión a color sobre negro", "BG:#141414"),
       ("No aplicar transparencias", "opacity:.35"), ("No recortar el logotipo", "CROP")]
def bad_tile(t, st):
    bg = "#fff"; style = st; inner = '<img src="img/logo-color.png" style="{s}">'
    if st.startswith("BG:"): bg = st[3:]; style = ""
    if st == "CROP": style = "width:150%;margin-left:-55%;margin-top:30%"
    return f'<div class="bad"><div class="bbox" style="background:{bg}">{inner.format(s=style)}<i>✕</i></div><span>{t}</span></div>'
page("02 · Logotipo", "Usos incorrectos", sechead("02", "Usos incorrectos", "Proteger el logotipo es proteger la reputación") +
     f'<div class="bads mt">{"".join(bad_tile(t, s) for t,s in bad)}</div>')

# 9 Fondos y convivencia
page("02 · Logotipo", "Fondos permitidos", sechead("02", "Fondos permitidos", "Contraste y legibilidad ante todo") + '''
<div class="bgs mt">
  <div style="background:#fff;border:1px solid #e3e8dc"><img src="img/logo-color.png"><span class="ok">✓ Blanco</span></div>
  <div style="background:#F6F9F1"><img src="img/logo-color.png"><span class="ok">✓ Hueso</span></div>
  <div style="background:#141414"><img src="img/logo-negativo.png"><span class="ok l">✓ Negro carbón</span></div>
  <div style="background:#1F3D0E"><img src="img/logo-negativo.png"><span class="ok l">✓ Verde profundo</span></div>
  <div style="background:linear-gradient(135deg,#2f6b16,#4f9a1f 55%,#7cb518)"><img src="img/logo-blanco.png"><span class="ok l">✓ Degradado de marca (blanco)</span></div>
  <div class="hexbg"><img src="img/logo-negativo.png"><span class="ok l">✓ Patrón hexagonal</span></div>
</div>''')

# 10 Color
page("03 · Color", "Paleta de color", sechead("03", "Paleta de color", "Tomada directamente del logotipo") + f'''
<div class="swatches mt">{"".join(f'<div class="sw" style="background:{h};color:{tc}"><div><strong>{n}</strong><em>{d}</em></div><dl><dt>HEX</dt><dd>{h}</dd><dt>RGB</dt><dd>{rgb(h)}</dd><dt>CMYK</dt><dd>{cmyk(h)}</dd><dt>PMS</dt><dd>{p}</dd></dl></div>' for n,h,p,d,tc in COLORS)}</div>
<div class="prop"><div style="flex:40;background:#41781D">40%</div><div style="flex:25;background:#141414">25%</div><div style="flex:20;background:#F6F9F1;color:#141414">20%</div><div style="flex:10;background:#7CB518;color:#141414">10%</div><div style="flex:5;background:#A5D34A;color:#141414">5</div></div>
<p class="note">Proporción de uso recomendada. *Equivalencias Pantone aproximadas: valida siempre con una prueba de color de tu imprenta. Degradado de marca: #2F6B16 → #4F9A1F → #7CB518 (135°).</p>''')

# 11 Tipografía
page("04 · Tipografía", "Tipografía", sechead("04", "Tipografía", "Dos familias, gratuitas y disponibles en Google Fonts") + '''
<div class="type mt">
  <div class="tf"><div class="k">Principal · Titulares</div><div class="aa mont">Aa</div><h3 class="mont">Montserrat</h3><p class="mont glyphs">ABCDEFGHIJKLMNÑOPQRSTUVWXYZ<br>abcdefghijklmnñopqrstuvwxyz<br>0123456789 ¿?¡!@#$%&</p><div class="weights mont"><span style="font-weight:600">SemiBold</span><span style="font-weight:700">Bold</span><span style="font-weight:800">ExtraBold</span><span style="font-weight:900">Black</span></div></div>
  <div class="tf"><div class="k">Secundaria · Textos</div><div class="aa inter">Aa</div><h3 class="inter">Inter</h3><p class="inter glyphs">ABCDEFGHIJKLMNÑOPQRSTUVWXYZ<br>abcdefghijklmnñopqrstuvwxyz<br>0123456789 ¿?¡!@#$%&</p><div class="weights inter"><span style="font-weight:400">Regular</span><span style="font-weight:500">Medium</span><span style="font-weight:600">SemiBold</span><span style="font-weight:700">Bold</span></div></div>
  <div class="hier">
    <div class="k">Jerarquía</div>
    <div class="h-eb">ETIQUETA · MONTSERRAT 800 · TRACKING 16%</div>
    <div class="h-h1">Adiós a las cucarachas</div>
    <div class="h-h2">Fumigación en Ciudad de Panamá</div>
    <p class="h-p">Texto de párrafo en Inter Regular con interlineado de 1.6. Claro, directo y fácil de leer en pantalla y papel.</p>
    <span class="h-btn">Cotizar por WhatsApp</span>
  </div>
</div>''')

# 12 Elementos gráficos
page("05 · Elementos", "Elementos gráficos", sechead("05", "Elementos gráficos", "Recursos que hacen reconocible la marca sin el logo") + f'''
<div class="els mt">
  <div class="el hexbg tall"><div class="lbl">Patrón hexagonal<small>Inspirado en panales y estructuras: orden y protección. Opacidad 6–12 %.</small></div></div>
  <div class="el grad"><div class="lbl l">Degradado de marca<small>135° · #2F6B16 → #4F9A1F → #7CB518</small></div></div>
  <div class="el swoosh"><svg viewBox="0 0 400 200" preserveAspectRatio="none"><path d="M0 170 Q180 210 400 60 L400 90 Q190 230 0 200Z" fill="#7cb518"/><path d="M0 140 Q200 190 400 30 L400 50 Q200 210 0 160Z" fill="#41781d"/></svg><div class="lbl">Barrido (swoosh)<small>Extraído del isotipo. Ideal para vehículos, banners y portadas.</small></div></div>
  <div class="el icons"><div class="ico-grid">{"".join(f'<div>{pest_icon(n)}<span>{n}</span></div>' for n in PESTS)}</div><div class="lbl">Iconografía de plagas<small>Trazo lineal 2.6 px, puntas redondeadas, negro carbón o blanco.</small></div></div>
</div>''')

# 13 Tono de voz
page("06 · Tono de voz", "Tono de voz", sechead("06", "Tono de voz", "Expertos que hablan claro, con calidez panameña") + '''
<div class="voice mt">
  <div class="vcol"><div class="k">Así hablamos</div>
    <ul class="yes"><li>Claro y directo: “Eliminamos el comején desde la raíz.”</li><li>Tranquilizador: “Es seguro para tus niños y mascotas.”</li><li>Local: “Llegamos rápido a tu corregimiento.”</li><li>Con prueba: “Garantía por escrito.”</li><li>Tuteo respetuoso y emojis con moderación en WhatsApp 🐜✅</li></ul>
  </div>
  <div class="vcol"><div class="k">Así NO hablamos</div>
    <ul class="no"><li>Alarmista: “¡Tu casa está infestada y es peligrosa!”</li><li>Demasiado técnico: “Aplicamos piretroides de síntesis…”</li><li>Promesas falsas: “100 % libre de plagas para siempre.”</li><li>Desordenado: mayúsculas sostenidas, muchos signos ¡¡¡!!!</li></ul>
  </div>
  <div class="chat">
    <div class="chat-h"><img src="img/iso-color.png"><div><b>Anthox PTY</b><span>en línea</span></div></div>
    <div class="msg in">Hola, creo que tengo comején en el closet 😟</div>
    <div class="msg out">¡Hola! Gracias por escribirnos 👋 Envíanos una foto del polvillo y te decimos si es comején. Podemos inspeccionar mañana en la mañana. ¿En qué zona estás?</div>
    <div class="msg in">En Condado del Rey</div>
    <div class="msg out">¡Perfecto, llegamos ahí! Te confirmo hora por aquí ✅</div>
  </div>
</div>
<div class="taglines"><span>Adiós a las plagas.</span><span>Protegemos tu hogar, cuidamos tu familia.</span><span>Expertos en plagas, cerca de ti.</span><span>Panamá libre de plagas.</span></div>''')

# 14 Suéteres
page("07 · Aplicaciones", "Suéteres y hoodies", sechead("07", "Suéteres y hoodies", "Merch y abrigo para el equipo y clientes") + f'''
<div class="stage three mt">
  <figure>{sweater("#18191a", "logo-negativo", hood=True)}<figcaption><b>Hoodie Negro Carbón</b>Logo negativo bordado al frente</figcaption></figure>
  <figure>{sweater("#2f6b16", "logo-blanco")}<figcaption><b>Suéter Verde Anthox</b>Logo blanco · bordado 1 color</figcaption></figure>
  <figure>{sweater("#f1efe9", "logo-color")}<figcaption><b>Suéter Hueso</b>Logo a color · DTF / bordado</figcaption></figure>
</div>
<p class="spec">Especificación: algodón/poliéster 280 g · logo al pecho 9–11 cm de ancho · bordado en hilo blanco, negro y verde Pantone 364 C.</p>''', cls="studio")

# 15 Uniforme técnico
page("07 · Aplicaciones", "Uniforme técnico", sechead("07", "Uniforme técnico", "La imagen del técnico es la imagen de la marca") + f'''
<div class="stage five mt">
  <figure>{tee("#18191a", "logo-negativo", polo=True)}<figcaption><b>Polo · frente</b>Logo 7 cm pecho izquierdo</figcaption></figure>
  <figure>{tee("#18191a", "iso-negativo", back=True)}<figcaption><b>Polo · espalda</b>Isotipo + nombre + WhatsApp</figcaption></figure>
  <figure>{tee("#ffffff", "logo-color")}<figcaption><b>Camiseta promocional</b>Logo a color al centro</figcaption></figure>
  <figure>{cap("#18191a", "iso-negativo", bill="#2f6b16")}<figcaption><b>Gorra técnica</b>Isotipo bordado · visera verde</figcaption></figure>
  <figure><div class="idcard"><div class="idtop"><img src="img/logo-negativo.png"></div><div class="idphoto"></div><b>Nombre Apellido</b><span>Técnico en control de plagas</span><em>ID 0001 · Vence 12/2027</em></div><figcaption><b>Carné técnico</b>CR80 · 54 × 86 mm</figcaption></figure>
</div>
<p class="spec">El técnico debe portar uniforme completo y carné visible en cada servicio: refuerza la confianza del cliente.</p>''', cls="studio")

# 16 Tazas
page("07 · Aplicaciones", "Tazas", sechead("07", "Tazas (mugs)", "Regalo corporativo para clientes y oficina") + f'''
<div class="stage three mt mugs">
  <figure>{mug("#ffffff", "logo-color", "#41781d", "#41781d")}<figcaption><b>Taza blanca bicolor</b>Interior y asa Verde Anthox</figcaption></figure>
  <figure>{mug("#1a1a1a", "logo-negativo", "#7cb518")}<figcaption><b>Taza negra mate</b>Logo negativo · interior lima</figcaption></figure>
  <figure>{mug("#2f6b16", "logo-blanco", "#f4f4f4")}<figcaption><b>Taza Verde Anthox</b>Logo blanco · interior blanco</figcaption></figure>
</div>
<p class="spec">Cerámica 11 oz · sublimación o impresión UV · área del logo 7–8 cm de ancho, centrado en la cara visible para diestros.</p>''', cls="studio")

# 17 Papelería
page("07 · Aplicaciones", "Papelería", sechead("07", "Papelería corporativa", "Tarjetas de presentación y hoja membretada") + '''
<div class="paper mt">
  <div class="cards">
    <div class="bc front"><img src="img/logo-negativo.png"><div class="bc-pattern"></div></div>
    <div class="bc back"><div><b>Nombre Apellido</b><span>Gerente General</span></div>
      <ul><li>📞 +507 6761-9763</li><li>💬 WhatsApp 6761-9763</li><li>🌐 anthoxpty.com</li><li>📍 Ciudad de Panamá</li></ul>
      <img src="img/iso-color.png"><i></i></div>
    <p class="spec">Tarjeta 9 × 5 cm · cartulina 350 g laminado mate · frente con barniz UV selectivo en el logo.</p>
  </div>
  <div class="letter">
    <div class="lh"><img src="img/logo-color.png"><div><b>Anthox PTY Control de Plagas</b><span>Ciudad de Panamá · +507 6761-9763 · anthoxpty.com</span></div></div>
    <div class="ltitle">CONSTANCIA DE FUMIGACIÓN</div>
    <div class="lines">''' + "".join(f'<i style="width:{w}%"></i>' for w in (90, 96, 80, 94, 70, 88, 96, 60)) + '''</div>
    <div class="ltable">''' + "".join('<i></i>' for _ in range(9)) + '''</div>
    <div class="sign"><i></i><span>Técnico responsable</span></div>
    <div class="lf"></div>
  </div>
</div>''', cls="studio")

# 18 Vehículo
page("07 · Aplicaciones", "Vehículo", sechead("07", "Rotulación vehicular", "Una valla publicitaria que recorre Panamá todos los días") + f'''
<div class="vehicle mt">{van()}</div>
<div class="grid3 spec-grid">
  <div><b>Lateral</b><span>Logo a color, servicio principal y WhatsApp en tamaño legible a 20 m (mín. 12 cm de alto en cifras).</span></div>
  <div><b>Material</b><span>Vinil impreso laminado + vinil de corte Verde Anthox (364 C) y Lima (376 C).</span></div>
  <div><b>Posterior</b><span>Isotipo, “¿Plagas? Escríbenos” y número de WhatsApp en blanco sobre verde.</span></div>
</div>''', cls="studio")

# 19 Merch
page("07 · Aplicaciones", "Merchandising", sechead("07", "Merchandising", "Artículos promocionales y señalética de servicio") + f'''
<div class="merch mt">
  <figure>{tote()}<figcaption><b>Tote bag</b>Lona natural · logo a color</figcaption></figure>
  <figure>{bottle()}<figcaption><b>Termo</b>Acero 20 oz · grabado/blanco</figcaption></figure>
  <figure class="stickers"><div class="st-grid">
    <div class="st s2"><span>FUMIGADO POR</span><img src="img/logo-negativo.png"><em>Próximo servicio: ___/___/___</em></div>
    <div class="st-col"><div class="st s1"><img src="img/logo-color.png"></div><div class="st s3"><img src="img/iso-blanco.png"></div></div></div>
    <figcaption><b>Stickers y sello de servicio</b>El sello “Fumigado por” se coloca tras cada visita: recordatorio y publicidad.</figcaption>
  </figure>
  <figure class="hanger"><div class="dh"><i></i><img src="img/logo-negativo.png"><b>¡Estamos fumigando!</b><span>Por favor no ingresar hasta las ____ : ____</span><em>Mascotas y niños fuera del área</em></div><figcaption><b>Aviso de puerta</b>Para PH, oficinas y restaurantes</figcaption></figure>
</div>''', cls="studio")

# 20 Digital
page("07 · Aplicaciones", "Digital", sechead("07", "Presencia digital", "Sitio web, redes sociales y WhatsApp") + '''
<div class="digital mt">
  <div class="devices">
    <div class="laptop"><div class="screen"><img src="img/web-desk.jpg"></div><div class="base"></div></div>
    <div class="phone"><img src="img/web-mob.jpg"></div>
  </div>
  <div class="social">
    <div class="ig ig1"><img src="img/iso-negativo.png"><span class="tagp">TIP</span><b>¿Cucarachas<br>otra vez?</b><small>3 razones por las que regresan</small></div>
    <div class="ig ig2"><img src="img/iso-blanco.png"><b>Temporada<br>de lluvias =<br>mosquitos</b><small>Elimina criaderos cada semana 🦟</small></div>
    <div class="ig ig3"><img src="img/logo-color.png" class="lg"><b>15% OFF</b><small>en tu primer servicio</small><span class="cta">Escríbenos por WhatsApp</span></div>
    <div class="avatar"><div class="av"><img src="img/iso-color.png"></div><div><b>Foto de perfil</b><span>Isotipo sobre blanco, centrado. Usar en WhatsApp Business, Instagram, Facebook, TikTok y Google Business Profile.</span></div></div>
  </div>
</div>''', cls="studio")

# 21 Contraportada
page("", "", '''
<div class="cover-pattern"></div>
<div class="back">
  <img src="img/logo-negativo.png">
  <p>Este manual es una herramienta viva. Ante cualquier duda sobre el uso de la marca, consulta al equipo de Anthox PTY antes de producir una pieza.</p>
  <div class="contact"><span>+507 6761-9763</span><span>anthoxpty.com</span><span>Ciudad de Panamá, Panamá</span></div>
  <small>© 2026 Anthox PTY Control de Plagas · Manual de identidad v1.0</small>
</div>''', dark=True, cls="cover-page")

# ---------------------------------------------------------------- documento
DEFS = '''<svg width="0" height="0" style="position:absolute"><defs>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="3"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 1"/></feComponentTransfer><feComposite in2="SourceGraphic" operator="in"/></filter>
<linearGradient id="fabricShade" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".32"/><stop offset=".18" stop-color="#000" stop-opacity=".06"/><stop offset=".45" stop-color="#fff" stop-opacity=".10"/><stop offset=".7" stop-color="#000" stop-opacity=".04"/><stop offset="1" stop-color="#000" stop-opacity=".34"/></linearGradient>
<linearGradient id="cyl" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".30"/><stop offset=".22" stop-color="#fff" stop-opacity=".38"/><stop offset=".34" stop-color="#fff" stop-opacity=".05"/><stop offset=".8" stop-color="#000" stop-opacity=".08"/><stop offset="1" stop-color="#000" stop-opacity=".38"/></linearGradient>
<linearGradient id="cylH" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".1"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient>
<linearGradient id="cylV" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".25"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".18"/></linearGradient>
<radialGradient id="rim" cx=".5" cy=".2" r=".8"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<linearGradient id="glass" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#6d7f8c"/><stop offset=".5" stop-color="#25313a"/><stop offset="1" stop-color="#11181d"/></linearGradient>
<linearGradient id="gradBrand" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#2f6b16"/><stop offset=".55" stop-color="#4f9a1f"/><stop offset="1" stop-color="#7cb518"/></linearGradient>
</defs></svg>'''

html = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>Anthox PTY – Manual de Marca</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:ital,wght@0,500;0,600;0,700;0,800;0,900;1,800;1,900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="brandbook.css"></head><body>{DEFS}{"".join(pages)}</body></html>'''
open(os.path.join(HERE, "brandbook.html"), "w", encoding="utf-8").write(html)
print(f"OK: {len(pages)} páginas")
