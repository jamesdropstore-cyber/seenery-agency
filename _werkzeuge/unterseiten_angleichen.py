"""Gleicht Impressum, Datenschutz und Danke an die Startseite an (Schriften, Header, Footer)."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
idx = (root/"index.html").read_text(encoding="utf-8")
wm = re.search(r'<span class="wm" aria-hidden="true">.*?<span class="wm-sub">AGENCY</span></span>', idx, re.S).group(0)
footer = re.search(r'<footer class="footer">.*?</footer>', idx, re.S).group(0)
footer = footer.replace('href="#top"', 'href="index.html"').replace('aria-label="Seenery Agency, zum Seitenanfang"', 'aria-label="Seenery Agency, zur Startseite"')
footer = re.sub(r'\s*<button type="button" class="linkbtn" data-cookie-open>Cookie-Hinweis</button>', '', footer)
FONT_OLD = re.compile(r'\s*<link href="https://fonts.googleapis.com/css2\?family=Cormorant[^>]*>')
FONT_NEW = '\n  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500;6..96,600&family=Playfair+Display:wght@500;600&display=swap">'
pages = {"impressum.html": True, "datenschutz.html": True, "danke.html": False}
for name, cta in pages.items():
    p = root/name; s = p.read_text(encoding="utf-8")
    s = FONT_OLD.sub(FONT_NEW, s)
    s = s.replace('<meta name="viewport" content="width=device-width, initial-scale=1">', '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n  <meta name="theme-color" content="#211a15">')
    if name != "danke.html" and 'rel="canonical"' not in s:
        s = s.replace('<link rel="icon"', f'<link rel="canonical" href="https://seenery.ch/{name}">\n  <link rel="icon"', 1)
    btn = '\n    <a class="btn btn-gold" href="index.html#check">Check anfragen</a>' if cta else ''
    header = ('<header class="site-header">\n  <div class="wrap">\n'
              '    <a class="brand" href="index.html" aria-label="Seenery Agency, zur Startseite">\n      ' + wm + '\n    </a>' + btn + '\n  </div>\n</header>')
    s = re.sub(r'<header class="site-header">.*?</header>', header, s, flags=re.S)
    s = s.replace('<p><a href="index.html">← Zurück zur Startseite</a></p>', '<p class="back"><a href="index.html">← Zurück zur Startseite</a></p>')
    s = s.replace('<a class="btn" href="index.html">Zurück zur Startseite</a>', '<a class="btn btn-gold" href="index.html">Zurück zur Startseite</a>')
    if '<footer class="footer">' not in s:
        s = s.replace('</main>\n', '</main>\n\n' + footer + '\n', 1)
    p.write_text(s, encoding="utf-8")
    print(name, "ok")
