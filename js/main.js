/* =========================================================
   ANTHOX PTY — Interactividad del sitio
   ========================================================= */
(function () {
  "use strict";

  // ---- Configuración del negocio (editar aquí) ----
  var WA_NUMBER = "50767619763"; // +507 6761-9763
  var BRAND = "Anthox PTY";

  function waLink(text) {
    return "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(text);
  }
  function openWA(text) {
    window.open(waLink(text), "_blank", "noopener");
    // Evento para Google Analytics 4 / Tag Manager si está instalado
    if (window.gtag) window.gtag("event", "whatsapp_click", { event_category: "contacto" });
    if (window.dataLayer) window.dataLayer.push({ event: "whatsapp_click" });
  }
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // ---- Header con sombra al hacer scroll + barra de progreso ----
  var header = $(".header");
  var progress = $(".progress");
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("scrolled", y > 10);
    if (progress) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (h > 0 ? (y / h) * 100 : 0) + "%";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // ---- Menú móvil ----
  var toggle = $(".menu-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    $$(".nav a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("menu-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // ---- Enlace activo según la sección visible ----
  var navLinks = $$('.nav a[href^="#"]');
  if (navLinks.length && "IntersectionObserver" in window) {
    var secObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          navLinks.forEach(function (a) { a.classList.toggle("active", a.getAttribute("href") === "#" + e.target.id); });
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    navLinks.forEach(function (a) { var s = $(a.getAttribute("href")); if (s) secObs.observe(s); });
  }

  // ---- Aparición al hacer scroll ----
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window) {
    var rObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); rObs.unobserve(e.target); } });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { rObs.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  // ---- Contadores animados ----
  var counters = $$("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    var cObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, end = parseFloat(el.dataset.count), suf = el.dataset.suffix || "", t0 = null, dur = 1600;
        function tick(t) {
          if (!t0) t0 = t;
          var p = Math.min((t - t0) / dur, 1), v = Math.floor(end * (1 - Math.pow(1 - p, 3)));
          el.textContent = v + suf;
          if (p < 1) requestAnimationFrame(tick); else el.textContent = end + suf;
        }
        requestAnimationFrame(tick);
        cObs.unobserve(el);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { cObs.observe(c); });
  }

  // ---- Texto rotativo en el hero ----
  var typed = $(".typed");
  if (typed) {
    var words = JSON.parse(typed.dataset.words || "[]"), wi = 0, ci = 0, del = false;
    (function type() {
      var w = words[wi] || "";
      typed.textContent = w.slice(0, ci);
      if (!del && ci < w.length) ci++;
      else if (del && ci > 0) ci--;
      else if (!del) { del = true; return setTimeout(type, 1600); }
      else { del = false; wi = (wi + 1) % words.length; }
      setTimeout(type, del ? 45 : 85);
    })();
  }

  // ---- Pestañas de servicios ----
  $$(".tab").forEach(function (tab) {
    tab.addEventListener("click", function () {
      var f = tab.dataset.filter;
      $$(".tab").forEach(function (t) { t.setAttribute("aria-selected", t === tab ? "true" : "false"); });
      $$(".service-card").forEach(function (c) {
        var show = f === "all" || (c.dataset.cat || "").indexOf(f) > -1;
        c.classList.toggle("hide", !show);
      });
    });
  });

  // ---- Tarjetas de plagas: voltear con toque (móvil) ----
  $$(".pest").forEach(function (p) {
    p.addEventListener("click", function (ev) {
      if (ev.target.closest("a")) return;
      p.classList.toggle("flipped");
    });
  });

  // ---- Identificador de plagas ----
  var quizData = {
    excremento: { t: "Posibles roedores o cucarachas", d: "Excremento en forma de grano de arroz (ratón/rata) o puntos negros tipo pimienta (cucaracha). Recomendamos inspección y control de roedores con estaciones cebadoras y sellado de accesos." },
    polvo: { t: "Posible comején (termitas)", d: "El polvillo tipo aserrín o “cagarruta” junto a muebles y marcos es una señal típica del comején de madera seca, muy común en Panamá. Requiere tratamiento localizado o de barrera." },
    picaduras: { t: "Posibles chinches de cama o pulgas", d: "Picaduras en fila o en grupos al despertar suelen ser chinches. Si hay mascotas y picaduras en tobillos, pueden ser pulgas. Ambas requieren tratamiento profesional en varias visitas." },
    zumbido: { t: "Mosquitos (Aedes aegypti)", d: "En temporada lluviosa los criaderos se multiplican. Hacemos nebulización, tratamiento larvicida y eliminación de criaderos para reducir el riesgo de dengue." },
    filas: { t: "Hormigas", d: "Filas de hormigas hacia la cocina indican un nido cercano. Usamos geles cebo que la colonia lleva al nido para eliminarla desde la raíz." },
    ropa: { t: "Polillas o pececillos de plata", d: "Agujeros en ropa, libros o papeles apuntan a polillas o pececillos de plata, favorecidos por la humedad. Tratamos closets y áreas de almacenamiento." }
  };
  $$(".quiz-opt").forEach(function (opt) {
    opt.addEventListener("click", function () {
      $$(".quiz-opt").forEach(function (o) { o.classList.toggle("selected", o === opt); });
      var r = quizData[opt.dataset.key], box = $(".quiz-result");
      if (!r || !box) return;
      box.innerHTML = "<strong>" + r.t + "</strong><p style='margin:.4em 0 .8em'>" + r.d + "</p>" +
        "<button class='btn btn-wa' type='button' data-wa='Hola " + BRAND + ", creo que tengo " + r.t.toLowerCase() + ". ¿Pueden hacer una inspección?'>" +
        waIcon() + " Consultar por WhatsApp</button>";
      box.classList.add("show");
    });
  });

  // ---- Cotizador estimado ----
  // Precios base de REFERENCIA en USD (ajústalos a tu tarifa real).
  var est = $("#estimator");
  if (est) {
    var PRICES = { // [base, por m² adicional sobre 60 m²]
      residencial: [45, 0.35],
      comercial: [75, 0.45],
      restaurante: [90, 0.5]
    };
    var PEST_EXTRA = { general: 0, cucarachas: 0, roedores: 25, comejen: 60, chinches: 70, mosquitos: 15 };
    var state = { tipo: "residencial", plaga: "general", m2: 80 };
    var range = $("#m2", est), m2Out = $("#m2-out", est), total = $("#est-total", est);

    function calc() {
      var p = PRICES[state.tipo], extra = Math.max(0, state.m2 - 60) * p[1];
      var low = Math.round(p[0] + extra + PEST_EXTRA[state.plaga]);
      var high = Math.round(low * 1.35);
      total.textContent = "$" + low + " – $" + high;
      m2Out.textContent = state.m2 + " m²";
      var pct = ((state.m2 - range.min) / (range.max - range.min)) * 100;
      range.style.setProperty("--p", pct + "%");
      return { low: low, high: high };
    }
    $$(".chip", est).forEach(function (chip) {
      chip.addEventListener("click", function () {
        var g = chip.dataset.group;
        $$('.chip[data-group="' + g + '"]', est).forEach(function (c) { c.classList.toggle("on", c === chip); });
        state[g] = chip.dataset.value;
        calc();
      });
    });
    range.addEventListener("input", function () { state.m2 = +range.value; calc(); });
    $("#est-send", est).addEventListener("click", function () {
      var r = calc();
      openWA("Hola " + BRAND + ", quiero una cotización:\n• Tipo: " + state.tipo + "\n• Plaga: " + state.plaga +
        "\n• Área aprox.: " + state.m2 + " m²\n• Estimado web: $" + r.low + " – $" + r.high);
    });
    calc();
  }

  // ---- Formularios → WhatsApp ----
  $$("form[data-wa-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fd = new FormData(form), lines = ["Hola " + BRAND + ", solicito una cotización:"];
      fd.forEach(function (v, k) { if (String(v).trim()) lines.push("• " + k + ": " + v); });
      openWA(lines.join("\n"));
      if (window.dataLayer) window.dataLayer.push({ event: "generate_lead" });
    });
  });

  // ---- Cualquier botón con data-wa abre WhatsApp ----
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-wa]");
    if (b) { e.preventDefault(); openWA(b.getAttribute("data-wa")); }
  });

  // ---- Widget flotante de WhatsApp ----
  function waIcon() {
    return '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.75-.86-2.02-.96-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.25-.46-2.38-1.47-.88-.79-1.47-1.76-1.65-2.05-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.23 1.36.2 1.87.12.57-.09 1.75-.72 2-1.41.25-.69.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35zM12.05 21.5h-.01a9.5 9.5 0 0 1-4.84-1.33l-.35-.2-3.6.94.96-3.5-.23-.36A9.48 9.48 0 0 1 2.5 12C2.5 6.76 6.77 2.5 12.05 2.5a9.45 9.45 0 0 1 9.45 9.5c0 5.24-4.27 9.5-9.45 9.5zm8.08-17.6A11.4 11.4 0 0 0 12.05.5C5.73.5.6 5.63.6 11.95c0 2.02.53 3.99 1.53 5.72L.5 23.5l5.97-1.57a11.44 11.44 0 0 0 5.47 1.4h.01c6.31 0 11.45-5.14 11.45-11.46 0-3.06-1.19-5.94-3.35-8.1z"/></svg>';
  }
  var rootPath = document.documentElement.dataset.root || "";
  var w = document.createElement("div");
  w.className = "wa-widget";
  w.innerHTML =
    '<div class="wa-panel" role="dialog" aria-label="Chat de WhatsApp con ' + BRAND + '">' +
      '<div class="wa-head"><img src="' + rootPath + 'assets/img/favicon-512.png" alt="" width="44" height="44">' +
        '<div><strong>' + BRAND + '</strong><span>En línea · responde en minutos</span></div>' +
        '<button class="wa-close" type="button" aria-label="Cerrar chat">×</button></div>' +
      '<div class="wa-body"><div class="wa-msg">¡Hola! 👋 Somos <b>Anthox PTY</b>, control de plagas en Ciudad de Panamá.<time>ahora</time></div>' +
        '<div class="wa-msg">¿Qué plaga te está dando problemas? Cotiza gratis por aquí. 🐜🪳🐀<time>ahora</time></div></div>' +
      '<div class="wa-quick">' +
        '<button type="button" data-wa="Hola, quiero cotizar una fumigación para mi casa/apartamento.">🏠 Fumigar mi casa</button>' +
        '<button type="button" data-wa="Hola, necesito fumigación para mi negocio / local comercial.">🏢 Para mi negocio</button>' +
        '<button type="button" data-wa="Hola, creo que tengo comején (termitas). ¿Pueden inspeccionar?">🪵 Comején</button>' +
        '<button type="button" data-wa="Hola, necesito atención urgente por una plaga.">⚡ Urgente</button>' +
      '</div>' +
      '<form class="wa-input"><label class="sr-only" for="wa-text">Escribe tu mensaje</label>' +
        '<input id="wa-text" type="text" placeholder="Escribe tu mensaje…" autocomplete="off">' +
        '<button type="submit" aria-label="Enviar por WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg></button></form>' +
    '</div>' +
    '<button class="wa-fab" type="button" aria-label="Abrir chat de WhatsApp">' + waIcon() + '<span class="wa-badge">1</span></button>';
  document.body.appendChild(w);

  var fab = $(".wa-fab", w), badge = $(".wa-badge", w);
  function setOpen(o) { w.classList.toggle("open", o); if (o && badge) badge.remove(); if (o) setTimeout(function () { var i = $("#wa-text"); if (i && window.innerWidth > 640) i.focus(); }, 250); }
  fab.addEventListener("click", function () { setOpen(!w.classList.contains("open")); });
  $(".wa-close", w).addEventListener("click", function () { setOpen(false); });
  $(".wa-input", w).addEventListener("submit", function (e) {
    e.preventDefault();
    var v = $("#wa-text").value.trim();
    openWA(v || "Hola " + BRAND + ", quiero información sobre sus servicios de fumigación.");
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });

  // Año en el footer
  $$(".year").forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
