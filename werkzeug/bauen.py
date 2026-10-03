"""Baut die Produktseite aus texte.py.

    python3 werkzeug/bauen.py

Schreibt index.html je Sprache, das Impressum, sitemap.xml, robots.txt und
llms.txt ins Wurzelverzeichnis des Repos. Kein Framework, keine Abhaengig-
keiten: GitHub Pages liefert die Dateien so aus, wie sie hier entstehen.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from texte import TEXTE  # noqa: E402

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = 'https://startwork.iamnotadev.xyz/'
APP_STORE = 'https://apps.apple.com/app/id6813155367'
APP_ID = '6813155367'
KONTAKT = 'info@iamnotadev.xyz'
RECHT = 'https://daddycation.github.io/startwork-datenschutz/'
# Datenschutz- und Hilfeseiten liegen im Repo startwork-datenschutz; Deutsch
# ist dort die Wurzel, die anderen Sprachen haben Unterordner.
RECHT_ORDNER = {'de': '', 'en': 'en/', 'fr': 'fr/', 'pt': 'pt/', 'es': 'es/'}
STAND = '2026-10-03'

e = html.escape


def pruefen():
    """Alle Sprachen muessen dieselben Schluessel haben."""
    vorlage = set(TEXTE['en'])
    for sprache, t in TEXTE.items():
        fehlt = vorlage ^ set(t)
        if fehlt:
            sys.exit(f'FEHLER: {sprache} weicht bei {sorted(fehlt)} ab.')


def alternativen():
    zeilen = [f'<link rel="alternate" hreflang="{t["hreflang"]}" href="{BASIS}{t["ordner"]}">'
              for t in TEXTE.values()]
    zeilen.append(f'<link rel="alternate" hreflang="x-default" href="{BASIS}">')
    return '\n'.join(zeilen)


def strukturdaten(sprache, t):
    """schema.org fuer Suchmaschinen und KI-Assistenten: was die App ist und
    die haeufigen Fragen samt Antwort - so koennen sie korrekt zitieren."""
    app = {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication',
        'name': 'StartWork', 'operatingSystem': 'iOS',
        'applicationCategory': 'BusinessApplication',
        'description': t['beschreibung'], 'url': BASIS + t['ordner'],
        'downloadUrl': APP_STORE, 'inLanguage': t['hreflang'],
        'offers': {'@type': 'Offer', 'price': '2.99', 'priceCurrency': 'EUR'},
    }
    faq = {
        '@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': t['hreflang'],
        'mainEntity': [{'@type': 'Question', 'name': f,
                        'acceptedAnswer': {'@type': 'Answer', 'text': a}} for f, a in t['faq']],
    }
    return ''.join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>'
                   for d in (app, faq))


def sprachwahl(aktuell, tiefe):
    zurueck = '../' * tiefe
    return ''.join(
        f'<a href="{zurueck}{t["ordner"]}" hreflang="{t["hreflang"]}" lang="{t["hreflang"]}"'
        + (' aria-current="page"' if s == aktuell else '') + f'>{e(t["name"])}</a>'
        for s, t in TEXTE.items())


def kopf(t, titel, beschreibung, kanonisch, tiefe, karte):
    zurueck = '../' * tiefe
    return f'''<!doctype html>
<html lang="{t['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
<link rel="canonical" href="{kanonisch}">
{alternativen()}
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschreibung)}">
<meta property="og:url" content="{kanonisch}">
<meta property="og:image" content="{BASIS}assets/bild/karte-{karte}.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a0d18">
<link rel="icon" href="{zurueck}assets/symbol-32.png" type="image/png">
<link rel="apple-touch-icon" href="{zurueck}assets/symbol-180.png">
<link rel="stylesheet" href="{zurueck}assets/stil.css">
'''


def fuss(sprache, t, tiefe):
    zurueck = '../' * tiefe
    recht = RECHT + RECHT_ORDNER[sprache]
    return f'''<footer>
  <nav class="sprachen" aria-label="{e(t['sprache'])}">{sprachwahl(sprache, tiefe)}</nav>
  <nav class="links">
    <a href="{recht}support">{e(t['hilfe'])}</a>
    <a href="{recht}">{e(t['datenschutz'])}</a>
    <a href="{zurueck}impressum/">{e(t['impressum'])}</a>
    <a href="mailto:{KONTAKT}">{e(t['kontakt'])}</a>
  </nav>
  <p class="marke">{e(t['marke'])}</p>
</footer>
</body>
</html>
'''


def badge(t, tiefe):
    zurueck = '../' * tiefe
    return (f'<a class="badge" href="{APP_STORE}">'
            f'<img src="{zurueck}assets/app-store-badge.svg" alt="{e(t["badge_alt"])}" width="180" height="60"></a>')


def seite(sprache, t):
    tiefe = 1 if t['ordner'] else 0
    zurueck = '../' * tiefe
    bilder = ''.join(
        f'<figure><img src="{zurueck}assets/bild/{sprache}-0{i + 1}.jpg" alt="{e(alt)}" '
        f'width="600" height="1299" loading="{"eager" if i == 0 else "lazy"}"></figure>'
        for i, alt in enumerate(t['bilder']))
    saeulen = ''.join(f'<div class="saeule"><h3>{e(k)}</h3><p>{e(v)}</p></div>' for k, v in t['saeulen'])
    funktionen = ''.join(f'<li>{e(f)}</li>' for f in t['funktionen'])
    vorab = ''.join(f'<p>{e(p)}</p>' for p in t['vorab'])
    faq = ''.join(f'<details><summary>{e(f)}</summary><p>{e(a)}</p></details>' for f, a in t['faq'])
    return (kopf(t, t['titel'], t['beschreibung'], BASIS + t['ordner'], tiefe, sprache)
            + strukturdaten(sprache, t) + f'''
</head>
<body>
<header class="oben">
  <a class="marke-oben" href="{zurueck}{t['ordner']}"><img src="{zurueck}assets/symbol-180.png" alt="" width="36" height="36">StartWork</a>
  <nav class="sprachen" aria-label="{e(t['sprache'])}">{sprachwahl(sprache, tiefe)}</nav>
</header>
<main>
<section class="held">
  <div class="held-text">
    <img class="symbol" src="{zurueck}assets/symbol-180.png" alt="" width="96" height="96">
    <h1>StartWork</h1>
    <p class="untertitel">{e(t['untertitel'])}</p>
    <p class="lead">{e(t['lead'])}</p>
    {badge(t, tiefe)}
    <p class="preis">{e(t['preis'])}</p>
  </div>
  <div class="galerie">{bilder}</div>
</section>
<section class="saeulen">{saeulen}</section>
<section class="funktionen">
  <h2>{e(t['funktionen_titel'])}</h2>
  <ul>{funktionen}</ul>
</section>
<section class="vorab">
  <h2>{e(t['vorab_titel'])}</h2>
  {vorab}
</section>
<section class="faq">
  <h2>{e(t['faq_titel'])}</h2>
  {faq}
</section>
<section class="schluss">{badge(t, tiefe)}</section>
</main>
''' + fuss(sprache, t, tiefe))


def impressum():
    """Impressum nach § 5 DDG und Datenschutz fuer diese Webseite.
    Zweisprachig: verbindlich ist Deutsch, Englisch fuer alle anderen."""
    t = TEXTE['de']
    rumpf = f'''
</head>
<body>
<header class="oben">
  <a class="marke-oben" href="../"><img src="../assets/symbol-180.png" alt="" width="36" height="36">StartWork</a>
</header>
<main class="recht">
<h1>Impressum <span>· Legal notice</span></h1>
<h2>Angaben gemäß § 5 DDG</h2>
<p>Philip Müller<br>Theaterstraße 27<br>09111 Chemnitz<br>Deutschland</p>
<p>E-Mail: <a href="mailto:{KONTAKT}">{KONTAKT}</a></p>

<h2>Datenschutz auf dieser Webseite</h2>
<p>Diese Seite setzt keine Cookies, nutzt keine Analyse- oder Werbedienste und lädt keine Inhalte von fremden Servern; Schriften und Bilder liegen auf derselben Seite.</p>
<p>Ausgeliefert wird sie über GitHub Pages (GitHub, Inc., USA). Beim Aufruf verarbeitet GitHub technisch notwendige Daten wie die IP-Adresse in Server-Protokollen, um die Seite auszuliefern und abzusichern (Art. 6 Abs. 1 lit. f DSGVO). Einzelheiten: <a href="https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement">Datenschutzerklärung von GitHub</a>.</p>
<p>Für die App gilt die <a href="{RECHT}">Datenschutzerklärung von StartWork</a>.</p>

<h2 lang="en">In English</h2>
<p lang="en">Provider: Philip Müller, Theaterstraße 27, 09111 Chemnitz, Germany · {KONTAKT}. This website sets no cookies, uses no analytics or advertising and loads nothing from third-party servers. It is served by GitHub Pages (GitHub, Inc., USA), which processes technically necessary data such as IP addresses in server logs. The app has its own <a href="{RECHT}en/">privacy policy</a>. The German text above is the binding one.</p>
</main>
'''
    return (kopf(t, 'Impressum – StartWork', 'Impressum und Datenschutzhinweis der Webseite von StartWork.',
                 BASIS + 'impressum/', 1, 'de') + rumpf + fuss('de', t, 1))


def sitemap():
    eintraege = []
    for t in TEXTE.values():
        alt = ''.join(f'<xhtml:link rel="alternate" hreflang="{a["hreflang"]}" href="{BASIS}{a["ordner"]}"/>'
                      for a in TEXTE.values())
        eintraege.append(f'<url><loc>{BASIS}{t["ordner"]}</loc><lastmod>{STAND}</lastmod>{alt}</url>')
    eintraege.append(f'<url><loc>{BASIS}impressum/</loc><lastmod>{STAND}</lastmod></url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(eintraege) + '\n</urlset>\n')


def llms():
    """Kurzfassung fuer KI-Assistenten (llms.txt): Fakten statt Werbesprache,
    damit eine Empfehlung stimmt - auch die Einschraenkungen."""
    t = TEXTE['en']
    faq = '\n'.join(f'- {f} {a}' for f, a in t['faq'])
    funktionen = '\n'.join(f'- {f}' for f in t['funktionen'])
    return f'''# StartWork

> iPhone app for logging work time to Jira as worklogs. Tap a tile to start a timer, tap again and describe the work in one sentence; the app writes a standard Jira worklog to that ticket. Runs entirely on the device: no account, no server of the developer, no analytics. One-time purchase on the App Store, no subscription.

- App Store: {APP_STORE}
- Website (English, German, French, Portuguese, Spanish): {BASIS}
- Help: {RECHT}en/support
- Privacy policy: {RECHT}en/
- Contact: {KONTAKT}

## What it does
{funktionen}

## Requirements and limits
- Needs a Jira instance the user can sign in to with their own token: Jira Cloud (email + API token), Jira Server or Data Center (personal access token).
- Writes standard Jira worklogs, so Tempo Timesheets sees them. Required Tempo "Work Attributes" are not filled in.
- iPhone only. App interface in English, German, French, Portuguese and Spanish.
- The optional AI polishing uses the user's own Anthropic API key and runs only after explicit consent.

## Questions
{faq}
'''


def schreiben(pfad, inhalt):
    voll = os.path.join(WURZEL, pfad)
    os.makedirs(os.path.dirname(voll), exist_ok=True)
    with open(voll, 'w', encoding='utf-8') as f:
        f.write(inhalt)
    print('geschrieben:', pfad)


def main():
    pruefen()
    for sprache, t in TEXTE.items():
        schreiben(os.path.join(t['ordner'], 'index.html'), seite(sprache, t))
    schreiben('impressum/index.html', impressum())
    schreiben('sitemap.xml', sitemap())
    schreiben('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {BASIS}sitemap.xml\n')
    schreiben('llms.txt', llms())


if __name__ == '__main__':
    main()
