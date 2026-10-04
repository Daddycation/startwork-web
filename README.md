# startwork-web

Produktseite von [StartWork](https://apps.apple.com/app/id6813155367) unter
<https://startwork.iamnotadev.xyz>, ausgeliefert über GitHub Pages.

- Texte: `werkzeug/texte.py` (eine Sprache je Block, gleiche Schlüssel)
- Bauen: `python3 werkzeug/bauen.py` schreibt die HTML-Seiten, `sitemap.xml`,
  `robots.txt` und `llms.txt`
- Bilder: entstehen im App-Repo mit `node werkstatt/webseite-bilder.mjs <ziel>/assets`
  aus den Store-Bildern

Keine Cookies, kein Tracking, keine Inhalte von fremden Servern.

## Suchmaschinen

Nach Änderungen die Adressen bei Bing und den anderen IndexNow-Suchmaschinen melden
(Schlüsseldatei `4f5413f9cc449f3e2305e1bc31b4a347.txt` liegt im Wurzelverzeichnis):

```
curl -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json' \
  -d '{"host":"startwork.iamnotadev.xyz","key":"4f5413f9cc449f3e2305e1bc31b4a347","urlList":["https://startwork.iamnotadev.xyz/"]}'
```

Google: Search Console, Domain-Property `iamnotadev.xyz`, Sitemap `sitemap.xml`.
