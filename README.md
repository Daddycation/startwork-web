# startwork-web

Produktseite von [StartWork](https://apps.apple.com/app/id6813155367) unter
<https://startwork.iamnotadev.xyz>, ausgeliefert über GitHub Pages.

- Texte: `werkzeug/texte.py` (eine Sprache je Block, gleiche Schlüssel)
- Bauen: `python3 werkzeug/bauen.py` schreibt die HTML-Seiten, `sitemap.xml`,
  `robots.txt` und `llms.txt`
- Bilder: entstehen im App-Repo mit `node werkstatt/webseite-bilder.mjs <ziel>/assets`
  aus den Store-Bildern

Keine Cookies, kein Tracking, keine Inhalte von fremden Servern.

## Team-Seite

`{sprache}/team/` (Englisch: `/team/`) erklärt StartWork im Team und die
Verteilung per Geräteverwaltung. Die App teilt Team-Vorlagen als Link auf
diese Seite (`…/team/#v1.<Vorlage>`); `assets/team.js` liest den Teil hinter
dem `#` nur im Browser und zeigt Zusammenfassung und „In StartWork öffnen“.
Eine Content-Security-Policy verbietet der Seite jede Verbindung nach außen.

- Texte: `werkzeug/team_texte.py` – Knopfnamen wörtlich wie in der App
- Bis App-Version 1.3 im Store ist, steht `TEAM_OEFFENTLICH = False` in
  `werkzeug/bauen.py`: Seite auf `noindex`, nicht in Sitemap, Fußzeile und
  `llms.txt`. Am Freigabetag auf `True` setzen, neu bauen, die fünf Adressen
  per IndexNow melden.

## Suchmaschinen

Nach Änderungen die Adressen bei Bing und den anderen IndexNow-Suchmaschinen melden
(Schlüsseldatei `4f5413f9cc449f3e2305e1bc31b4a347.txt` liegt im Wurzelverzeichnis):

```
curl -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json' \
  -d '{"host":"startwork.iamnotadev.xyz","key":"4f5413f9cc449f3e2305e1bc31b4a347","urlList":["https://startwork.iamnotadev.xyz/"]}'
```

Google: Search Console, Domain-Property `iamnotadev.xyz`, Sitemap `sitemap.xml`.
