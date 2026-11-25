(function () {
  "use strict";

  var STOPS = [
    {
      id: "1", x: 196, y: 356, label: "Prizemni sloj",
      tag: "PouÄŤna toÄŤka 1",
      title: "Prizemni sloj Ĺˇume",
      text: "<p>NajniĹľi kat Ĺˇume ÄŤine proljetnice, mahovine i paprati. Zakonom su zaĹˇtiÄ‡ene Ĺˇumska ciklama, sitnocvjetni kukurijek, bijela Ĺˇumarica, visibaba i Ĺˇafran.</p><p>Ispod liĹˇÄ‡a Ĺľive stonoga i kopneni rak babura. Stonoga se hrani trulim liĹˇÄ‡em i pomaĹľe u stvaranju tla, a u opasnosti se sklupÄŤa u loptu.</p>"
    },
    {
      id: "2", x: 240, y: 310, label: "Granit",
      tag: "PouÄŤna toÄŤka 2",
      title: "MoslavaÄŤki granit",
      text: "<p>Granit je kisela, intruzivna magmatska stijena. Grade ga kvarc, kiseli plagioklas, mikroklin i biotit, a javljaju se i andaluzit te silimanit.</p><p>MoslavaÄŤki pluton je klinasta ploÄŤa debela 4â€“5 km koja tone prema jugozapadu. Nastao je skruÄ‡ivanjem magme u dubljim dijelovima kore prije oko 83 milijuna godina.</p>"
    },
    {
      id: "3", x: 284, y: 266, label: "Strukture",
      tag: "PouÄŤna toÄŤka 3",
      title: "Strukture Zemljine kore",
      text: "<p>Stijene se pod naprezanjem ponaĹˇaju elastiÄŤno, krto ili plastiÄŤno. Krtim lomom nastaju pukotine i rasjedi, a plastiÄŤnom deformacijom bore i folijacije.</p><p>MoslavaÄŤki kraj ÄŤini pet tektonskih jedinica, a najznaÄŤajnije strukture su MoslavaÄŤka gora i Savska potolina. NajmlaÄ‘i rasjedi pruĹľaju se sjeverâ€“jug.</p>"
    },
    {
      id: "4", x: 330, y: 216, label: "Samostan",
      tag: "PouÄŤna toÄŤka 4",
      title: "Samostan BlaĹľene Djevice Marije",
      text: "<p>U klancu KamenjaÄŤe, pod GariÄ‡-gradom, nalazi se jedan od najstarijih pavlinskih samostana u Hrvatskoj. Prvi pisani spomeni datiraju iz 1257. i 1260. godine.</p><p>Samostan je djelovao do 16. stoljeÄ‡a, kada su ga redovnici zbog osmanske opasnosti napustili i preselili se u Lepoglavu. IstraĹľivanja traju od 2009. godine.</p>"
    },
    {
      id: "5", x: 368, y: 170, label: "Grmlje",
      tag: "PouÄŤna toÄŤka 5",
      title: "Sloj grmlja u Ĺˇumi",
      text: "<p>U sloju grmlja rastu lijeska, brekinja, drijen, kupina te zaĹˇtiÄ‡ene boĹľikovina i veprina. Veprina ima filokladije â€” proĹˇirene stabljike koje izgledaju kao listovi.</p><p>Ovdje obitavaju kuna bjelica, jelenak, srna, divlja svinja, jazavac i mnogi glodavci. Kuna se vjeĹˇto penje po drveÄ‡u i voli zalaziti u naselja.</p>"
    },
    {
      id: "6", x: 400, y: 132, label: "DrveÄ‡e",
      tag: "PouÄŤna toÄŤka 6",
      title: "Sloj drveÄ‡a u Ĺˇumi",
      text: "<p>KroĹˇnje grade bukva, grab, pitomi kesten, hrast kitnjak, hrast luĹľnjak i bagrem. Bukva ima glatku sivu koru, a grab ispucaniju i oĹˇtro nazubljen list.</p><p>Odrasla stabla hrane i sklanjaju ptice pjevice, djetliÄ‡e, Ĺˇojke i grabljivice. Crna Ĺľuna gnijezdi se u dupljama starih hrastova.</p>"
    },
    {
      id: "7", x: 452, y: 164, label: "DrveÄ‡e 2",
      tag: "PouÄŤna toÄŤka 7",
      title: "Mahovina i sjever",
      text: "<p>Na vlaĹľnijoj i hladnijoj, sjevernoj strani debla ima viĹˇe mahovine. Zato je nazivaju prirodnim kompasom â€” ali u gustoj Ĺˇumi bolje je imati i pravi kompas.</p><p>U ovom dijelu Ĺˇume vrijedi zastati i osluĹˇkivati: crna roda i crna Ĺľuna rijetke su, strogo zaĹˇtiÄ‡ene ptice starih Ĺˇuma.</p>"
    },
    {
      id: "8", x: 470, y: 218, label: "Geodinamika",
      tag: "PouÄŤna toÄŤka 8",
      title: "Geodinamika Zemlje",
      text: "<p>Hrvatska se nalazi u seizmiÄŤki aktivnom dijelu Sredozemlja zbog kretanja AfriÄŤke ploÄŤe prema Euroazijskoj. Napetost se prenosi prema Panonskom bazenu.</p><p>Na vrhu Humke nalazi se seizmoloĹˇka postaja. Potresi se mjere magnitudom (Richter) i intenzitetom (MCS), a razlika od jedne magnitude znaÄŤi oko 30 puta viĹˇe energije.</p>"
    },
    {
      short: "H", id: "humka", x: 434, y: 94, label: "Humka", extra: true,
      tag: "Vrh",
      title: "Humka Â· 488 m",
      text: "<p>NajviĹˇi vrh MoslavaÄŤke gore. S vrha se pruĹľa pogled na cijeli kraj, a ovdje je i seizmoloĹˇka postaja.</p><p>Oznaka vrha dio je planinarske infrastrukture; staza se na Humku nastavlja na planinarske putove.</p>"
    },
    {
      short: "V", id: "vis", x: 600, y: 222, label: "Vis", extra: true,
      tag: "Vidikovac",
      title: "Vis Â· 437 m",
      text: "<p>Drugi istaknuti vrh gore, s vidikovcem i pogledom prema okolnim naseljima i ravnicama. Do njega vode planinarski putovi koji se spajaju sa stazom Crkveni jarak.</p>"
    },
    {
      short: "J", id: "jezero", x: 118, y: 432, label: "Jezero", extra: true,
      tag: "Ulaz",
      title: "Jezero MikleuĹˇka",
      text: "<p>Glavni ulaz na stazu je uz jezero MikleuĹˇka i juĹľnije od njega. Jezero je dobar orijentir i mjesto za poÄŤetak ili kraj Ĺˇetnje.</p>"
    },
    {
      short: "S", id: "slap", x: 392, y: 310, label: "Slap", extra: true,
      tag: "OdmoriĹˇte",
      title: "OdmoriĹˇte kod slapa",
      text: "<p>Mjesto za predah uz potok KamenjaÄŤa. Voda neumorno oblikuje kristalno stijenje â€” u sukobu potoka i stijene, na dugi rok pobjeÄ‘uje potok.</p>"
    }
  ];

  var mapStops = document.getElementById("map-stops");
  var list = document.getElementById("stop-list");
  var content = document.getElementById("stop-content");
  if (!mapStops || !content) return;

  STOPS.forEach(function (s) {
    var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", "stop-dot");
    g.setAttribute("data-stop", s.id);
    g.setAttribute("tabindex", "0");
    g.setAttribute("role", "button");
    g.setAttribute("aria-label", s.title);
    g.innerHTML =
      '<circle cx="' + s.x + '" cy="' + s.y + '" r="' + (s.extra ? 13 : 15) + '" fill="' + (s.extra ? "#f0cd8a" : "#f8f4e9") + '" stroke="#b3542f" stroke-width="2.2"/>' +
      '<text x="' + s.x + '" y="' + (s.y + 4.5) + '" text-anchor="middle" font-family="Inter, sans-serif" font-size="' + (s.extra ? 10 : 12) + '" font-weight="700" fill="#173327">' + (s.extra ? s.short : s.id) + "</text>";
    g.addEventListener("click", function () { select(s.id); });
    g.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(s.id); }
    });
    mapStops.appendChild(g);
  });

  STOPS.forEach(function (s) {
    var li = document.createElement("li");
    var b = document.createElement("button");
    b.type = "button";
    b.textContent = s.extra ? s.short : s.id;
    b.setAttribute("aria-label", s.title);
    b.setAttribute("data-list", s.id);
    b.addEventListener("click", function () { select(s.id); });
    li.appendChild(b);
    li.style.listStyle = "none";
    list.appendChild(li);
  });

  function select(id) {
    var s = STOPS.find(function (x) { return x.id === id; }) || STOPS[0];
    content.innerHTML =
      '<span class="stop-info__num">' + (s.extra ? "â—†" : s.id) + "</span>" +
      '<p class="eyebrow" style="margin:.4rem 0 .3rem">' + s.tag + "</p>" +
      "<h3>" + s.title + "</h3>" + s.text;
    document.querySelectorAll(".stop-dot").forEach(function (d) {
      d.classList.toggle("is-active", d.getAttribute("data-stop") === s.id);
    });
    document.querySelectorAll("[data-list]").forEach(function (b) {
      b.classList.toggle("is-active", b.getAttribute("data-list") === s.id);
    });
  }

  select("1");
})();
