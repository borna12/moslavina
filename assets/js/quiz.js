(function () {
  "use strict";

  var root = document.getElementById("quiz");
  if (!root) return;

  var params = new URLSearchParams(location.search);
  var key = params.get("k") || "stijene";
  var data = window.KVIZOVI && window.KVIZOVI[key];
  if (!data) {
    key = "stijene";
    data = window.KVIZOVI[key];
  }

  var questions = data.pitanja.slice();
  var index = 0;
  var score = 0;
  var answered = [];
  var wrong = [];

  document.title = data.naslov + " · Kviz · Moslavina";
  var crumb = document.getElementById("quiz-crumb");
  if (crumb) crumb.textContent = data.naslov;

  var quizName = {
    stijene: "Stijene i geologija",
    biljke: "Biljke moslavačke šume",
    zivotinje: "Životinje u šumi",
    cinjenice: "Zanimljive činjenice"
  };

  function badge(pct) {
    if (pct >= 90) return { t: "Gorski znalac", i: "🏔️" };
    if (pct >= 70) return { t: "Istraživač gore", i: "🧭" };
    if (pct >= 50) return { t: "Mladi čuvar šume", i: "🌿" };
    return { t: "Vrijedi ponoviti", i: "📖" };
  }

  function startScreen() {
    var minutes = Math.max(3, Math.round(questions.length * 0.4));
    root.innerHTML =
      '<div class="quiz-card">' +
      '<p class="eyebrow" style="margin-bottom:.6rem">Kviz · ' + quizName[key] + "</p>" +
      '<h1 style="font-size:clamp(1.8rem,4vw,2.6rem);margin-bottom:.6rem">' + data.naslov + "</h1>" +
      '<p class="lead" style="font-size:1.05rem">' + data.opis + "</p>" +
      '<div class="pill-row" style="margin:22px 0 26px">' +
      '<span class="tag">' + questions.length + " pitanja</span>" +
      '<span class="tag">≈ ' + minutes + " min</span>" +
      '<span class="tag tag--amber">bez vremenskog ograničenja</span>' +
      "</div>" +
      '<button class="btn" id="quiz-start">Počni kviz <span aria-hidden="true">→</span></button>' +
      '<p class="quiz-hint" style="margin-top:16px">Savjet: pitanja možeš prolaziti i tipkovnicom — brojevi 1–4 odabiru odgovor, Enter vodi dalje.</p>' +
      "</div>";
    document.getElementById("quiz-start").addEventListener("click", function () {
      index = 0; score = 0; answered = []; wrong = [];
      renderQuestion();
    });
  }

  function optionLetter(i) {
    return data.mode === "truefalse" ? ["DA", "NE"][i] : String.fromCharCode(65 + i);
  }

  function renderQuestion() {
    var q = questions[index];
    var options = data.mode === "truefalse" ? ["Da, točno je", "Ne, nije točno"] : q.o;
    var letters = data.mode === "truefalse" ? ["✓", "✕"] : ["A", "B", "C", "D"];

    root.innerHTML =
      '<div class="quiz-top"><span>Pitanje ' + (index + 1) + " / " + questions.length + "</span>" +
      '<span>' + score + " " + (score === 1 ? "točan" : "točnih") + " dosad</span></div>" +
      '<div class="quiz-bar"><div class="quiz-bar__fill" style="width:' + ((index / questions.length) * 100) + '%"></div></div>' +
      '<div class="quiz-card">' +
      '<h2 class="quiz-q">' + q.q + "</h2>" +
      '<div class="quiz-options" role="group" aria-label="Odgovori">' +
      options.map(function (opt, i) {
        return '<button class="quiz-option" type="button" data-i="' + i + '">' +
          '<span class="quiz-option__key" aria-hidden="true">' + letters[i] + "</span>" +
          "<span>" + opt + "</span></button>";
      }).join("") +
      "</div>" +
      '<div class="quiz-feedback" id="quiz-feedback" aria-live="polite"></div>' +
      '<div class="quiz-actions"><span class="quiz-hint" id="quiz-hint">Odaberi jedan odgovor.</span>' +
      '<button class="btn" id="quiz-next" disabled>Dalje <span aria-hidden="true">→</span></button></div>' +
      "</div>";

    var buttons = Array.prototype.slice.call(root.querySelectorAll(".quiz-option"));
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () { choose(parseInt(btn.getAttribute("data-i"), 10)); });
    });
    document.getElementById("quiz-next").addEventListener("click", next);
    root.querySelector(".quiz-option").focus();
    document.addEventListener("keydown", onKey);
  }

  function choose(i) {
    var q = questions[index];
    if (answered[index] !== undefined) return;
    answered[index] = i;
    var correct = i === q.a;
    if (correct) score++; else wrong.push({ q: q, chosen: i });
    var buttons = root.querySelectorAll(".quiz-option");
    buttons.forEach(function (btn, bi) {
      btn.disabled = true;
      if (bi === q.a) btn.classList.add("is-correct");
      if (bi === i && !correct) btn.classList.add("is-wrong");
    });
    var fb = document.getElementById("quiz-feedback");
    fb.classList.add("is-visible");
    fb.innerHTML = "<strong>" + (correct ? "Točno!" : "Netočno.") + "</strong>" + q.e;
    document.getElementById("quiz-next").disabled = false;
    document.getElementById("quiz-hint").textContent = "Objašnjenje je iznad — nastavi kad želiš.";
    document.getElementById("quiz-next").focus();
  }

  function next() {
    document.removeEventListener("keydown", onKey);
    if (index < questions.length - 1) {
      index++;
      renderQuestion();
      window.scrollTo({ top: root.getBoundingClientRect().top + window.scrollY - 100, behavior: "smooth" });
    } else {
      showResult();
    }
  }

  function onKey(e) {
    if (e.key === "Enter" && !document.getElementById("quiz-next").disabled) {
      e.preventDefault();
      next();
      return;
    }
    if (e.key >= "1" && e.key <= "9") {
      var n = parseInt(e.key, 10) - 1;
      var opts = root.querySelectorAll(".quiz-option");
      if (opts[n] && !opts[n].disabled) { e.preventDefault(); choose(n); }
    }
    if (data.mode === "truefalse") {
      if (e.key.toLowerCase() === "d" || e.key.toLowerCase() === "t") {
        var o = root.querySelectorAll(".quiz-option");
        if (o[0] && !o[0].disabled) { e.preventDefault(); choose(0); }
      }
      if (e.key.toLowerCase() === "n") {
        var p = root.querySelectorAll(".quiz-option");
        if (p[1] && !p[1].disabled) { e.preventDefault(); choose(1); }
      }
    }
  }

  function showResult() {
    document.removeEventListener("keydown", onKey);
    var pct = Math.round((score / questions.length) * 100);
    var b = badge(pct);
    if (window.Moslavina) window.Moslavina.recordScore("kviz-" + key, score, questions.length);

    var review = "";
    if (wrong.length) {
      review = '<div class="result__review"><h3>Ponovi ovo</h3>' + wrong.map(function (w) {
        var opts = data.mode === "truefalse" ? ["Da", "Ne"] : w.q.o;
        return '<div class="review-item"><b>' + w.q.q + "</b><br>" +
          "Točno: <b>" + opts[w.q.a] + "</b> · Tvoj odgovor: <span class=\"your\">" + opts[w.chosen] + "</span><br>" +
          '<span class="muted">' + w.q.e + "</span></div>";
      }).join("") + "</div>";
    }

    var others = Object.keys(window.KVIZOVI).filter(function (k) { return k !== key; });
    root.innerHTML =
      '<div class="quiz-card">' +
      '<div class="result">' +
      '<p class="eyebrow" style="justify-content:center">Rezultat</p>' +
      '<div class="result__score">' + score + "<span>/" + questions.length + "</span></div>" +
      '<div class="result__badge">' + b.i + " " + b.t + " · " + pct + "%</div>" +
      '<p class="result__msg">' + (pct >= 90 ? "Bravo! Ti bi mogao voditi terensku nastavu po Moslavačkoj gori." :
        pct >= 70 ? "Vrlo dobro! Vrati se na objašnjenja i osvoji sve bodove." :
        pct >= 50 ? "Dobar početak. Prođi stranice o gori i okušaj se ponovno." :
        "Ne brini — gora ima mnogo slojeva. Pročitaj osnove i pokušaj još jednom.") + "</p>" +
      '<div class="hero__actions" style="justify-content:center">' +
      '<button class="btn" id="quiz-again">Igraj ponovno</button>' +
      '<a class="btn btn--ghost" href="../igre.html">Sve igre</a>' +
      "</div>" + review +
      "</div></div>" +
      '<div class="card card--flat" style="margin-top:20px">' +
      '<h3 style="font-size:1.1rem">Sljedeći kviz</h3><div class="pill-row" style="margin-top:10px">' +
      others.map(function (k) {
        return '<a class="tag" style="text-decoration:none" href="kviz.html?k=' + k + '">' + window.KVIZOVI[k].naslov + "</a>";
      }).join("") +
      "</div></div>";

    document.getElementById("quiz-again").addEventListener("click", function () {
      index = 0; score = 0; answered = []; wrong = [];
      renderQuestion();
      window.scrollTo({ top: root.getBoundingClientRect().top + window.scrollY - 100, behavior: "smooth" });
    });
    window.scrollTo({ top: root.getBoundingClientRect().top + window.scrollY - 100, behavior: "smooth" });
  }

  startScreen();
})();
