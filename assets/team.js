// Team-Seite: liest die Team-Vorlage aus dem Link (#v1...). Der Teil hinter
// dem # geht nie an einen Server, und die Seite darf per Content-Security-
// Policy auch selbst nichts senden. Geprueft wird nach denselben Regeln wie
// in der App (vorlageLesen in StartWork/index.html); beim Uebernehmen prueft
// die App ohnehin noch einmal selbst. Ohne Vorlage bleibt nur die Infoseite.
(function () {
  'use strict';
  var MUSTER = /^#v1\.([A-Za-z0-9_-]+)$/;
  var hash = location.hash;
  // Nur "#v1." zaehlt als Vorlage; ein verstuemmelter Rest (etwa vom
  // Messenger angehaengte Zeichen) bekommt die Meldung statt nichts.
  if (hash.indexOf('#v1.') !== 0) return;
  var T = JSON.parse(document.getElementById('team-texte').textContent);
  var $ = function (id) { return document.getElementById(id); };

  // Wer die Sprache wechselt, behaelt die Vorlage.
  if (MUSTER.test(hash)) {
    document.querySelectorAll('.sprachen a').forEach(function (a) {
      a.setAttribute('href', a.getAttribute('href') + hash);
    });
  }

  function lesen(h) {
    var m = MUSTER.exec(h);
    if (!m || h.length > 20000) return null;
    try {
      var s = m[1].replace(/-/g, '+').replace(/_/g, '/');
      while (s.length % 4) s += '=';
      var bytes = Uint8Array.from(atob(s), function (c) { return c.charCodeAt(0); });
      var d = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes));
      if (!d || typeof d !== 'object' || Array.isArray(d) || d.v !== 1) return null;
      var roh = String(d.a || '').trim().replace(/\/+$/, '');
      var u = new URL(roh);
      if (!/^https?:$/.test(u.protocol) || u.username || u.password || u.search || u.hash || roh.length > 300) return null;
      var liste = Array.isArray(d.k) ? d.k : [];
      if (liste.length > 50) return null;
      var kacheln = [];
      for (var i = 0; i < liste.length; i++) {
        var x = liste[i] || {}, schluessel = String(x.i || '').trim().toUpperCase();
        if (!/^[A-Z][A-Z0-9]+-\d+$/.test(schluessel)) return null;
        kacheln.push(schluessel + ' · ' + String(x.l || schluessel).slice(0, 120));
      }
      return {
        adresse: (u.origin + u.pathname).replace(/\/+$/, ''),
        kacheln: kacheln,
        rundung: [1, 5, 15].indexOf(d.r) >= 0 ? d.r : 1,
        ki: d.ki === 0 ? 0 : 1
      };
    } catch (e) {
      return null;
    }
  }

  $('vorlage').hidden = false;
  var v = lesen(hash);
  if (!v) { $('vschlecht').hidden = false; return; }
  $('vgut').hidden = false;
  // Nur textContent: Titel stammen von irgendwem und werden nie zu HTML.
  $('vadresse').textContent = v.adresse;
  var feld = $('vkacheln');
  if (!v.kacheln.length) feld.textContent = '–';
  v.kacheln.forEach(function (z, i) {
    if (i) feld.appendChild(document.createElement('br'));
    feld.appendChild(document.createTextNode(z));
  });
  $('vrundung').textContent = v.rundung > 1 ? T.rundung_min.replace('{n}', v.rundung) : T.rundung_exakt;
  $('vki').textContent = v.ki ? T.ki_an : T.ki_aus;
  $('voeffnen').setAttribute('href', 'startwork://team' + hash);

  var link = $('vlink'), knopf = $('vkopieren');
  link.value = location.href;
  link.addEventListener('focus', function () { link.select(); });
  knopf.addEventListener('click', function () {
    var markieren = function () { link.focus(); link.select(); };
    if (!navigator.clipboard) return markieren();
    navigator.clipboard.writeText(location.href).then(function () {
      knopf.textContent = T.kopiert;
      setTimeout(function () { knopf.textContent = T.kopieren; }, 2000);
    }, markieren);
  });
})();
