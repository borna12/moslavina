(function () {
  "use strict";

  var PAGES = [
    { id: "gora", href: "gora.html", label: "Gora" },
    { id: "zivi-svijet", href: "zivi-svijet.html", label: "Živi svijet" },
    { id: "povijest", href: "povijest.html", label: "Povijest" },
    { id: "staza", href: "staza.html", label: "Staza" },
    { id: "igre", href: "igre.html", label: "Igre" },
    { id: "izvori", href: "izvori.html", label: "Izvori" }
  ];

  var LOGO = '<svg class="brand__mark" viewBox="0 0 44 44" fill="none" aria-hidden="true">' +
    '<circle cx="22" cy="22" r="21" stroke="currentColor" stroke-opacity=".5"/>' +
    '<path d="M6 31.5c4.2-1.1 6.6-4.9 9.3-8.6 2.1-2.9 4.2-5.1 6.7-5.1 2.6 0 4.1 2.4 5.8 5.2 2.1 3.5 4.4 6.8 8.2 7.9" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>' +
    '<path d="M6 35.5c5.1-1 8.2-3.4 11.2-6.9M24 31.5c2.1-1.4 3.8-3.3 5.4-5.4M32 30.4c2.2 1.4 4.5 2.3 7 2.7" stroke="currentColor" stroke-opacity=".55" stroke-width="1.4" stroke-linecap="round"/>' +
    '<circle cx="22" cy="11.5" r="2.2" fill="#d9a441"/>' +
    '</svg>';

  function headerHTML(active, ROOT) {
    var links = PAGES.map(function (p) {
      var cur = p.id === active ? ' aria-current="page"' : "";
      return '<a href="' + ROOT + p.href + '"' + cur + '>' + p.label + "</a>";
    }).join("");
    return '<div class="wrap header-inner">' +
      '<a class="brand" href="' + ROOT + 'index.html" aria-label="Moslavina — edukativni portal, početna">' +
      LOGO +
      '<span class="brand__text"><span class="brand__name">Moslavina</span>' +
      '<span class="brand__sub">edukativni portal</span></span></a>' +
      '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Meni</button>' +
      '<nav class="site-nav" id="site-nav" aria-label="Glavna navigacija">' + links + "</nav>" +
      "</div>";
  }

  function footerHTML(ROOT) {
    return '<div class="wrap">' +
      '<div class="footer-grid">' +
      '<div class="footer-brand">' +
      '<span class="brand__name" style="font-family:var(--serif);font-size:1.25rem">Moslavina</span>' +
      '<p>Edukativni portal o Moslavačkoj gori: geologiji, šumi i njezinim stanovnicima, pavlinskom samostanu i poučnoj stazi Crkveni jarak. Uči, istražuj i igraj se.</p>' +
      "</div>" +
      '<div><h4>Istraži</h4><a href="' + ROOT + 'gora.html">Gora između ploča</a><a href="' + ROOT + 'zivi-svijet.html">Živi svijet</a><a href="' + ROOT + 'povijest.html">Povijest</a><a href="' + ROOT + 'staza.html">Staza Crkveni jarak</a></div>' +
      '<div><h4>Igraj se</h4><a href="' + ROOT + 'igre.html">Sve igre</a><a href="' + ROOT + 'igre/kviz.html?k=stijene">Kviz: stijene</a><a href="' + ROOT + 'igre/kviz.html?k=biljke">Kviz: biljke</a><a href="' + ROOT + 'krizaljka.html">Križaljka</a><a href="' + ROOT + 'izvori.html">Izvori i literatura</a></div>' +
      "</div>" +
      '<div class="footer-bottom"><span>© <span id="year"></span> Edukativni portal Moslavina</span>' +
      '<span>Izrađeno za učenje i istraživanje · Regionalni park Moslavačka gora</span></div>' +
      "</div>";
  }

  function mount() {
    var page = document.body.getAttribute("data-page") || "";
    var ROOT = document.body.getAttribute("data-root") || "";
    var header = document.querySelector("[data-site-header]");
    var footer = document.querySelector("[data-site-footer]");
    if (header) header.innerHTML = headerHTML(page, ROOT);
    if (footer) footer.innerHTML = footerHTML(ROOT);

    var year = document.getElementById("year");
    if (year) year.textContent = new Date().getFullYear();

    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");
    if (toggle && nav) {
      toggle.addEventListener("click", function () {
        var open = nav.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", String(open));
        toggle.textContent = open ? "Zatvori" : "Meni";
      });
      nav.addEventListener("click", function (e) {
        if (e.target.tagName === "A") {
          nav.classList.remove("is-open");
          toggle.setAttribute("aria-expanded", "false");
          toggle.textContent = "Meni";
        }
      });
    }

    var reveals = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && reveals.length) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add("is-in");
            io.unobserve(en.target);
          }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
      reveals.forEach(function (el) { io.observe(el); });
    } else {
      reveals.forEach(function (el) { el.classList.add("is-in"); });
    }
  }

  // ---- shared progress (best scores) ----
  var KEY = "moslavina.progress.v1";

  function readProgress() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (err) { return {}; }
  }

  function saveProgress(data) {
    try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (err) { /* ignore */ }
  }

  function recordScore(id, score, total) {
    var data = readProgress();
    var prev = data[id];
    if (!prev || score > prev.score) {
      data[id] = { score: score, total: total, at: new Date().toISOString() };
      saveProgress(data);
    }
    return data;
  }

  // normalize Croatian diacritics for comparisons
  function fold(s) {
    return String(s).toUpperCase()
      .replace(/Č/g, "C").replace(/Ć/g, "C").replace(/Ž/g, "Z")
      .replace(/Š/g, "S").replace(/Đ/g, "D");
  }

  window.Moslavina = {
    pages: PAGES,
    readProgress: readProgress,
    recordScore: recordScore,
    fold: fold
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
