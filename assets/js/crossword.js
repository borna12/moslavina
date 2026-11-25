(function () {
  "use strict";

  var data = window.KRIZALJKA;
  var root = document.getElementById("crossword");
  if (!data || !root) return;

  var rows = data.rows, cols = data.cols;
  var solution = data.grid.map(function (r) { return r.split(""); });
  var inputs = {};
  var cellWords = {};
  var words = [];

  function k(r, c) { return r + ":" + c; }

  // build word objects
  data.across.forEach(function (cl) {
    words.push({ dir: "A", num: cl.num, clue: cl.clue, len: cl.len, cells: [] });
  });
  data.down.forEach(function (cl) {
    words.push({ dir: "D", num: cl.num, clue: cl.clue, len: cl.len, cells: [] });
  });

  // find start cell for each clue and fill cells
  words.forEach(function (w) {
    var start = null;
    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        if (data.nums[r][c] === w.num) {
          if (w.dir === "A" && (c + 1 >= cols || !solution[r][c + 1])) continue;
          if (w.dir === "D" && (r + 1 >= rows || !solution[r + 1][c])) continue;
          start = [r, c];
          break;
        }
      }
      if (start) break;
    }
    if (!start) return;
    for (var i = 0; i < w.len; i++) {
      var rr = start[0] + (w.dir === "D" ? i : 0);
      var cc = start[1] + (w.dir === "A" ? i : 0);
      w.cells.push([rr, cc]);
      var key = k(rr, cc);
      if (!cellWords[key]) cellWords[key] = {};
      cellWords[key][w.dir] = w;
    }
  });

  var table = document.createElement("table");
  table.className = "cross-grid";
  table.setAttribute("role", "grid");
  var tbody = document.createElement("tbody");

  for (var r = 0; r < rows; r++) {
    var tr = document.createElement("tr");
    for (var c = 0; c < cols; c++) {
      var td = document.createElement("td");
      var sol = solution[r][c];
      if (!sol || sol === " ") {
        td.className = "cross-cell cross-cell--block";
      } else {
        td.className = "cross-cell";
        var inp = document.createElement("input");
        inp.type = "text";
        inp.maxLength = 1;
        inp.autocomplete = "off";
        inp.spellcheck = false;
        inp.setAttribute("aria-label", "Redak " + (r + 1) + ", stupac " + (c + 1));
        inp.dataset.r = r;
        inp.dataset.c = c;
        td.appendChild(inp);
        inputs[k(r, c)] = inp;
        if (data.nums[r][c]) {
          var n = document.createElement("span");
          n.className = "num";
          n.textContent = data.nums[r][c];
          td.appendChild(n);
        }
      }
      tr.appendChild(td);
    }
    tbody.appendChild(tr);
  }
  table.appendChild(tbody);

  var active = null; // {word, cellIndex}

  function wordCellsSet(w) {
    var set = {};
    w.cells.forEach(function (rc) { set[k(rc[0], rc[1])] = true; });
    return set;
  }

  function clearHighlight() {
    Object.keys(inputs).forEach(function (key) { inputs[key].classList.remove("is-active"); });
    document.querySelectorAll(".clue-list li").forEach(function (li) { li.classList.remove("is-active"); });
  }

  function highlight() {
    clearHighlight();
    if (!active) return;
    var set = wordCellsSet(active.word);
    Object.keys(set).forEach(function (key) { inputs[key].classList.add("is-active"); });
    var li = document.querySelector('.clue-list li[data-dir="' + active.word.dir + '"][data-num="' + active.word.num + '"]');
    if (li) li.classList.add("is-active");
  }

  function focusCell(r, c, dir) {
    var key = k(r, c);
    var inp = inputs[key];
    if (!inp) return;
    var cw = cellWords[key];
    if (!cw) return;
    var w = cw[dir] || cw.A || cw.D;
    if (!w) return;
    var idx = w.cells.findIndex(function (rc) { return rc[0] === r && rc[1] === c; });
    active = { word: w, cellIndex: idx < 0 ? 0 : idx };
    highlight();
    inp.focus();
    inp.select();
  }

  function currentCell() {
    if (!active) return null;
    return active.word.cells[active.cellIndex];
  }

  function step(delta) {
    if (!active) return;
    var next = active.cellIndex + delta;
    if (next < 0 || next >= active.word.cells.length) return;
    var rc = active.word.cells[next];
    focusCell(rc[0], rc[1], active.word.dir);
  }

  function typeLetter(letter) {
    var cell = currentCell();
    if (!cell) return;
    var inp = inputs[k(cell[0], cell[1])];
    inp.value = letter.toUpperCase();
    inp.classList.remove("is-wrong", "is-right");
    if (active.cellIndex < active.word.cells.length - 1) step(1);
    checkComplete();
  }

  Object.keys(inputs).forEach(function (key) {
    var inp = inputs[key];
    var r = parseInt(inp.dataset.r, 10), c = parseInt(inp.dataset.c, 10);
    inp.addEventListener("focus", function () {
      var cw = cellWords[key];
      var dir = active ? active.word.dir : "A";
      if (!cw[dir]) dir = cw.A ? "A" : "D";
      var w = cw[dir];
      var idx = w.cells.findIndex(function (rc) { return rc[0] === r && rc[1] === c; });
      active = { word: w, cellIndex: idx < 0 ? 0 : idx };
      highlight();
    });
    inp.addEventListener("click", function () {
      if (active && active.word.cells.length > 1) {
        var cw = cellWords[key];
        var hasBoth = cw.A && cw.D;
        if (hasBoth) {
          var other = active.word.dir === "A" ? "D" : "A";
          if (cw[other]) {
            var w = cw[other];
            var idx = w.cells.findIndex(function (rc) { return rc[0] === r && rc[1] === c; });
            active = { word: w, cellIndex: idx };
            highlight();
          }
        }
      }
      inp.select();
    });
    inp.addEventListener("keydown", function (e) {
      if (e.key === "Backspace") {
        if (inp.value) {
          inp.value = "";
          inp.classList.remove("is-wrong", "is-right");
        } else {
          step(-1);
          var cell = currentCell();
          if (cell) {
            var prev = inputs[k(cell[0], cell[1])];
            if (prev) { prev.value = ""; prev.classList.remove("is-wrong", "is-right"); }
          }
        }
        e.preventDefault();
        return;
      }
      if (e.key === "ArrowRight") { e.preventDefault(); moveArrow(r, c, 0, 1); return; }
      if (e.key === "ArrowLeft") { e.preventDefault(); moveArrow(r, c, 0, -1); return; }
      if (e.key === "ArrowDown") { e.preventDefault(); moveArrow(r, c, 1, 0); return; }
      if (e.key === "ArrowUp") { e.preventDefault(); moveArrow(r, c, -1, 0); return; }
      if (e.key === " " || e.key === "Tab") { return; }
      if (e.key.length === 1) {
        e.preventDefault();
        typeLetter(e.key);
        return;
      }
    });
  });

  function moveArrow(r, c, dr, dc) {
    var nr = r + dr, nc = c + dc;
    while (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
      if (inputs[k(nr, nc)]) {
        var currentDir = active ? active.word.dir : "A";
        focusCell(nr, nc, currentDir);
        return;
      }
      nr += dr; nc += dc;
    }
  }

  // build clue lists
  function clueList(items, dir) {
    return '<ol class="clue-list">' + items.map(function (it) {
      return '<li data-dir="' + dir + '" data-num="' + it.num + '"><span class="clue-num">' + it.num + "</span><span>" + it.clue + "</span></li>";
    }).join("") + "</ol>";
  }

  function buildUI() {
    root.innerHTML =
      '<div class="cross-layout">' +
      '<div>' +
      '<div class="cross-scroll" id="cross-grid-wrap"></div>' +
      '<div class="cross-toolbar">' +
      '<button class="btn btn--small" id="cross-check" type="button">Provjeri</button>' +
      '<button class="btn btn--small btn--ghost" id="cross-hint" type="button">Otkrij slovo</button>' +
      '<button class="btn btn--small btn--ghost" id="cross-solve" type="button">Otkrij sve</button>' +
      '<button class="btn btn--small btn--ghost" id="cross-clear" type="button">Obriši</button>' +
      "</div>" +
      '<div class="letter-pad" aria-label="Hrvatska slova">' +
      ["Č", "Ć", "Ž", "Š", "Đ"].map(function (l) { return '<button type="button" data-letter="' + l + '">' + l + "</button>"; }).join("") +
      "</div>" +
      '<p class="cross-status" id="cross-status" aria-live="polite">Odaberi polje i upiši slovo. Klikni na pojam za početak.</p>' +
      '<p class="small muted">Mala pomoć: slova Č, Ć, Ž, Š i Đ možeš upisati i kao C, C, Z, S i D — provjera ih prepoznaje.</p>' +
      "</div>" +
      '<div class="card card--flat">' +
      '<div class="clue-cols">' +
      '<div><h3 style="font-size:1.05rem;margin-bottom:8px">Vodoravno</h3>' + clueList(data.across, "A") + "</div>" +
      '<div><h3 style="font-size:1.05rem;margin-bottom:8px">Okomito</h3>' + clueList(data.down, "D") + "</div>" +
      "</div></div>" +
      "</div>";

    document.getElementById("cross-grid-wrap").appendChild(table);

    document.querySelectorAll(".clue-list li").forEach(function (li) {
      li.addEventListener("click", function () {
        var dir = li.getAttribute("data-dir");
        var num = parseInt(li.getAttribute("data-num"), 10);
        var w = words.find(function (x) { return x.dir === dir && x.num === num; });
        if (!w) return;
        focusCell(w.cells[0][0], w.cells[0][1], dir);
      });
    });

    document.querySelectorAll(".letter-pad button").forEach(function (btn) {
      btn.addEventListener("click", function () { typeLetter(btn.dataset.letter); });
    });

    document.getElementById("cross-check").addEventListener("click", check);
    document.getElementById("cross-hint").addEventListener("click", revealLetter);
    document.getElementById("cross-solve").addEventListener("click", function () {
      if (!confirm("Otkriti cijelu križaljku? Nakon toga se ne računa kao riješena.")) return;
      revealAll();
    });
    document.getElementById("cross-clear").addEventListener("click", function () {
      Object.keys(inputs).forEach(function (key) {
        inputs[key].value = "";
        inputs[key].classList.remove("is-wrong", "is-right", "is-revealed");
      });
      setStatus("Križaljka je obrisana. Kreni ispočetka!");
      clearHighlight();
      active = null;
    });
  }

  function setStatus(t) {
    var el = document.getElementById("cross-status");
    if (el) el.textContent = t;
  }

  function check() {
    var filled = 0, wrongCells = 0, total = 0;
    Object.keys(inputs).forEach(function (key) {
      var inp = inputs[key];
      var r = parseInt(inp.dataset.r, 10), c = parseInt(inp.dataset.c, 10);
      total++;
      if (inp.value) filled++;
      if (inp.value) {
        if (window.Moslavina.fold(inp.value) === window.Moslavina.fold(solution[r][c])) {
          inp.classList.remove("is-wrong");
          inp.classList.add("is-right");
        } else {
          inp.classList.add("is-wrong");
          inp.classList.remove("is-right");
          wrongCells++;
        }
      }
    });
    if (filled === 0) { setStatus("Još nema upisanih slova."); return; }
    if (wrongCells === 0 && filled === total) {
      win();
    } else if (wrongCells === 0) {
      setStatus("Sve upisano je točno — nastavi s preostalim poljima (" + (total - filled) + ").");
    } else {
      setStatus("Ima " + wrongCells + " netočnih slova. Crvena polja treba ispraviti.");
    }
  }

  function revealLetter() {
    var cell = currentCell();
    if (!cell) { setStatus("Prvo odaberi polje u križaljci."); return; }
    var inp = inputs[k(cell[0], cell[1])];
    inp.value = solution[cell[0]][cell[1]];
    inp.classList.remove("is-wrong", "is-right");
    inp.classList.add("is-revealed");
    setStatus("Otkrilo se slovo. Pokušaj ostalo sam.");
    checkComplete(true);
  }

  function revealAll() {
    Object.keys(inputs).forEach(function (key) {
      var inp = inputs[key];
      var r = parseInt(inp.dataset.r, 10), c = parseInt(inp.dataset.c, 10);
      inp.value = solution[r][c];
      inp.classList.add("is-revealed");
      inp.classList.remove("is-wrong", "is-right");
    });
    solved = true;
    setStatus("Cijela je križaljka otkrivena. Prouči rješenje pa je pokušaj riješiti sam.");
  }

  function allCorrect() {
    return Object.keys(inputs).every(function (key) {
      var inp = inputs[key];
      var r = parseInt(inp.dataset.r, 10), c = parseInt(inp.dataset.c, 10);
      return inp.value && window.Moslavina.fold(inp.value) === window.Moslavina.fold(solution[r][c]);
    });
  }

  function checkComplete(silent) {
    if (allCorrect()) win(silent);
  }

  var solved = false;
  function win(silent) {
    if (solved) return;
    solved = true;
    setStatus("Riješeno! Bravo — sva slova su na svom mjestu. 🎉");
    if (window.Moslavina) window.Moslavina.recordScore("krizaljka", 1, 1);
    if (!silent) {
      var el = document.getElementById("cross-status");
      if (el) el.style.fontWeight = "600";
    }
  }

  buildUI();
})();
