#!/usr/bin/env python3
"""seenery.ch v3 · Multi-Page. python3 build.py artifact|repo
artifact: Vorschau (index ohne Doctype, Farbwelt-Umschalter). repo: saubere Dateien für Netlify."""
import sys, os, shutil, json
MODE = sys.argv[1] if len(sys.argv) > 1 else 'repo'
OUT = 'out' if MODE == 'artifact' else 'out-repo'
FONTS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts.css')).read()
GF = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap">'
SP = '<path d="M0 -10 C1 -3 3 -1 10 0 C3 1 1 3 0 10 C-1 3 -3 1 -10 0 C-3 -1 -1 -3 0 -10Z"/>'
WM = f'<span class="wm" aria-hidden="true"><span class="wm-name">SEENERY<svg class="wm-spark" viewBox="-10 -10 20 20">{SP}</svg></span><span class="wm-sub">AGENCY</span></span>'
TEL = '<a href="tel:+41763391398">076 339 13 98</a>'
MAIL = '<a href="mailto:info@seenery.ch">info@seenery.ch</a>'

LEIST = [
 ('website-mit-online-termin.html','Website mit Online-Termin','Eigenes Design, eine Seite pro Behandlung','termin','W'),
 ('google-unternehmensprofil.html','Google-Unternehmensprofil','Gefunden werden, wo «in der Nähe» gesucht wird','gprofil','G'),
 ('google-bewertungen.html','Google-Bewertungen','Mehr echte Stimmen nach jedem Termin','bewertung','★'),
 ('seo-zuerich.html','SEO für Zürich','Bei Google für Ihre Behandlungen gefunden werden','zuerich','S'),
 ('sichtbar-in-chatgpt.html','Sichtbar in ChatGPT','Damit KI-Assistenten Sie kennen und nennen können','ai-chat','AI'),
 ('monatsbericht.html','Monatsbericht','Jeden Monat klare Zahlen statt Bauchgefühl','bericht','%'),
]
FUER = [
 ('aesthetikpraxen.html','Ästhetikpraxen','Ärztliche Kompetenz, online sichtbar gemacht','laser','Ä'),
 ('laser-kosmetikinstitute.html','Laser- & Kosmetikinstitute','Viele Behandlungen, für jede eine klare Seite','laser-handstueck','L'),
 ('lash-brow-nails-studios.html','Lash-, Brow- & Nail-Studios','Für Studios mit Team: Online-Buchung statt DM-Chaos','lash','B'),
]
ALL_LEIST = [x[0] for x in LEIST] + ['leistungen.html']
ALL_FUER = [x[0] for x in FUER]

def esc(s): return s.replace('"','&quot;')

# ---------------- Bausteine ----------------
def header(cur):
    def dd(label, items, key, allhref, alltext, curset):
        links = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}><span class="ico" aria-hidden="true">{ic}</span><span><b>{t}</b><small>{d}</small></span></a>' for h,t,d,_,ic in items)
        if allhref: links += f'<a class="all" href="{allhref}">{alltext} →</a>'
        c = ' cur' if cur in curset else ''
        return f'<div class="dd{c}" data-dd><button type="button" aria-expanded="false" aria-controls="dd-{key}">{label}</button><div class="dd-menu" id="dd-{key}">{links}</div></div>'
    ac = lambda h: ' aria-current="page"' if h == cur else ''
    m_l = ''.join(f'<a href="{h}">{t}</a>' for h,t,*_ in LEIST)
    m_f = ''.join(f'<a href="{h}">{t}</a>' for h,t,*_ in FUER)
    return f'''<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="hd">
  <div class="wrap hd-in">
    <a class="brand" href="index.html" aria-label="Seenery Agency, Startseite">{WM}</a>
    <nav class="nav" aria-label="Hauptnavigation">
      {dd('Leistungen',LEIST,'leist','leistungen.html','Alle Leistungen im Überblick',ALL_LEIST)}
      {dd('Für wen',FUER,'fuer',None,'',ALL_FUER)}
      <a href="website-arten.html"{ac('website-arten.html')}>Website-Arten</a>
      <a href="ablauf.html"{ac('ablauf.html')}>Ablauf</a>
      <a href="ueber-mich.html"{ac('ueber-mich.html')}>Über mich</a>
      <a href="kontakt.html"{ac('kontakt.html')}>Kontakt</a>
    </nav>
    <div class="hd-cta">
      <a class="btn btn-deep btn-sm" href="sichtbarkeits-check.html">Gratis-Check</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">Menü</button>
    </div>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Menü mobil">
    <p class="grp">Leistungen</p><a href="leistungen.html">Alle Leistungen</a>{m_l}
    <p class="grp">Für wen</p>{m_f}
    <p class="grp">Mehr</p><a href="website-arten.html">Website-Arten</a><a href="ablauf.html">Ablauf</a><a href="ueber-mich.html">Über mich</a><a href="faq.html">Häufige Fragen</a><a href="kontakt.html">Kontakt</a>
    <a class="btn btn-deep" href="sichtbarkeits-check.html">Gratis Sichtbarkeits-Check</a>
</nav>'''

def footer():
    l = ''.join(f'<li><a href="{h}">{t}</a></li>' for h,t,*_ in LEIST)
    f = ''.join(f'<li><a href="{h}">{t}</a></li>' for h,t,*_ in FUER)
    return f'''<footer class="ft">
  <div class="wrap">
    <div class="ft-in">
      <div><a class="brand" href="index.html" aria-label="Seenery Agency, Startseite" style="color:inherit">{WM}</a>
        <p style="font-family:var(--serif);font-size:22px;color:var(--on-deep);margin-top:20px">Gesehen. Gebucht. Gewachsen.</p><p>Website, Google-Profil, Bewertungen und Sichtbarkeit in ChatGPT für Ästhetikpraxen, Institute und Studios. Aus Zürich, für die ganze Schweiz.</p>
        <p style="margin-top:12px">{MAIL}<br>{TEL}</p></div>
      <div><h4>Leistungen</h4><ul><li><a href="leistungen.html">Überblick</a></li>{l}</ul></div>
      <div><h4>Für wen</h4><ul>{f}</ul><h4 style="margin-top:26px">Seenery</h4><ul><li><a href="ueber-mich.html">Über mich</a></li><li><a href="ablauf.html">Ablauf</a></li><li><a href="website-arten.html">Website-Arten</a></li></ul></div>
      <div><h4>Kontakt</h4><ul><li><a href="sichtbarkeits-check.html">Gratis Sichtbarkeits-Check</a></li><li><a href="kontakt.html">Kontakt</a></li><li><a href="faq.html">Häufige Fragen</a></li><li><a href="https://www.instagram.com/seenery.agency/" rel="noopener" target="_blank">Instagram</a></li></ul></div>
    </div>
    <div class="ft-bot"><span>© 2026 Seenery Agency · James Alves Da Silva · Dübendorf</span><span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></span></div>
  </div>
</footer>'''

def crumbs(items):
    lis = '<li><a href="index.html">Start</a></li>' + ''.join((f'<li><a href="{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>') for t,h in items)
    return f'<nav class="crumbs" aria-label="Brotkrumen"><ol>{lis}</ol></nav>'

def page_hero(cr, eyebrow, h1a, h1b, lead, img, alt, cap=None, pills=None, btns=True, fig=None):
    p = ''.join(f'<span>{x}</span>' for x in (pills or []))
    pills_html = f'<div class="pills">{p}</div>' if pills else ''
    b = '<div class="btns"><a class="btn btn-deep" href="sichtbarkeits-check.html">Gratis-Check anfragen <span aria-hidden="true">→</span></a><a class="btn btn-line" href="#mehr">Mehr erfahren</a></div>' if btns else ''
    figure = fig or f'<figure class="ph-fig"><img src="img/{img}.webp" alt="{esc(alt)}" width="1600" height="1067" fetchpriority="high">{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>'
    return f'''<section class="phero" aria-labelledby="h1">
  <div class="wrap">
    {crumbs(cr)}
    <div class="ph-grid">
      <div class="ph-copy"><p class="eyebrow">{eyebrow}</p><h1 id="h1">{h1a}<span class="l2">{h1b}</span></h1><p class="lead">{lead}</p>{pills_html}{b}</div>
      {figure}
    </div>
  </div>
</section><span id="mehr"></span>'''

def split(eyebrow, h2, paras, img, alt, rev=False, extra='', hid=None):
    body = ''.join(f'<p>{x}</p>' for x in paras)
    i = hid or ('s-' + img)
    return f'''<div class="split{' rev' if rev else ''}">
  <div class="sp-copy"><p class="eyebrow">{eyebrow}</p><h2 id="{i}">{h2}</h2><div class="body">{body}</div>{extra}</div>
  <figure class="sp-fig"><img src="img/{img}.webp" alt="{esc(alt)}" width="1600" height="1067" loading="lazy"></figure>
</div>'''

def split_mock(eyebrow, h2, paras, mock, rev=False, extra='', hid='s-mock'):
    body = ''.join(f'<p>{x}</p>' for x in paras)
    return f'''<div class="split{' rev' if rev else ''}" style="align-items:center">
  <div class="sp-copy"><p class="eyebrow">{eyebrow}</p><h2 id="{hid}">{h2}</h2><div class="body">{body}</div>{extra}</div>
  <div>{mock}</div>
</div>'''

def gallery(items, label):
    figs = ''.join(f'<figure><img src="img/{im}.webp" alt="{esc(alt)}" width="1600" height="1067" loading="lazy" style="object-position:{pos}"><figcaption>{cap}</figcaption></figure>' for im,alt,cap,pos in items)
    return f'<div class="gallery{" g4" if len(items)==4 else ""}" role="group" aria-label="{label}">{figs}</div>'

def checks(items):
    return '<ul class="checks">' + ''.join(f'<li><div><b>{a}</b><span>{b}</span></div></li>' for a,b in items) + '</ul>'

def faq(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q,a in items) + '</div>'

def head(eyebrow, h2, lead=None, hid='h', center=True):
    l = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<div class="head{" center narrow" if center else ""}"><p class="eyebrow">{eyebrow}</p><h2 id="{hid}">{h2}</h2>{l}</div>'

def cta(title='Wie sichtbar ist Ihre Praxis heute?', text='Ich prüfe Google, ChatGPT und Ihre Website und zeige Ihnen das Ergebnis persönlich. Kostenlos und unverbindlich.'):
    return f'''<section class="cta" aria-labelledby="cta-t"><div class="wrap"><div class="cta-in">
  <div><p class="eyebrow" style="color:var(--acc-soft)">Gratis Sichtbarkeits-Check</p><h2 id="cta-t">{title}</h2><p>{text}</p></div>
  <div class="cta-side"><a class="btn btn-acc" href="sichtbarkeits-check.html">Check anfragen <span aria-hidden="true">→</span></a><div class="direct"><span>Lieber direkt?</span>{TEL}{MAIL}</div></div>
</div></div></section>'''

def related(skip, kind='leist'):
    src = LEIST if kind == 'leist' else FUER
    items = [x for x in src if x[0] != skip][:3] if kind=='leist' else [x for x in src if x[0] != skip]
    cards = ''.join(f'<a class="card text" href="{h}"><div class="cb"><span class="num">{"Leistung" if kind=="leist" else "Für"}</span><h3>{t}</h3><p>{d}</p><span class="go">Mehr erfahren →</span></div></a>' for h,t,d,*_ in items)
    g = 'grid3' if len(items) == 3 else 'grid2'
    return f'<div class="{g}">{cards}</div>'

def steps():
    return '''<ol class="steps">
  <li><h3>Check</h3><p>Ich prüfe Google, ChatGPT und Ihre Website. Mit Screenshots als Ausgangswert.</p></li>
  <li><h3>Gespräch</h3><p>Wir besprechen das Ergebnis, Ihre Ziele und welche Behandlungen mehr gefunden werden sollen.</p></li>
  <li><h3>Entwurf</h3><p>Sie sehen Ihren Entwurf nach wenigen Tagen. Ihre Wünsche fliessen direkt ein.</p></li>
  <li><h3>Live</h3><p>Website und Google-Profil gehen online, in der Regel innert 14 Arbeitstagen ab vollständigen Unterlagen.</p></li>
  <li><h3>Jeden Monat</h3><p>Beiträge, Bewertungen, Pflege und ein Monatsbericht, der direkt an Sie geht.</p></li>
</ol>'''

PROMPT_BOX = lambda pid: f'''<div class="test-box">
  <p class="step">Öffnen Sie ChatGPT und fragen Sie:</p>
  <p class="prompt" id="{pid}">Welche Praxis empfiehlst du für Faltenbehandlung in Zürich?</p>
  <div class="test-row"><button type="button" class="btn btn-light btn-sm" data-copy="{pid}">Frage kopieren</button><span class="copy-ok" role="status" aria-live="polite"></span></div>
  <p class="test-note">Ersetzen Sie «Faltenbehandlung» durch Ihre wichtigste Behandlung und «Zürich» durch Ihren Ort. Wird Ihre Praxis genannt? Ich mache den Test gerne für Sie, mit Screenshot.</p>
</div>'''

# ---------------- Mockups ----------------
def mock_frame(url, inner, note='Beispiel-Darstellung'):
    return f'<div class="mock" role="img" aria-label="{note}"><div class="mock-h" aria-hidden="true"><i></i><i></i><i></i><span>{url}</span></div><div class="mock-b" aria-hidden="true">{inner}</div></div><p class="mock-note">{note}</p>'

MOCK_BOOKING = mock_frame('ihre-praxis.ch/termin', '''<div class="bk-row"><b>Hautanalyse &amp; Beratung</b><small>45 Min.</small></div>
<div class="bk-row"><span>Do, 12. März</span><small>Dr. med. Beispiel</small></div>
<div class="slots"><span class="x">08:30</span><span>09:15</span><span class="on">10:00</span><span>11:30</span><span>13:45</span><span class="x">14:30</span><span>16:00</span><span>17:15</span></div>
<div style="margin-top:16px;background:var(--deep);color:var(--on-deep);border-radius:99px;padding:12px;text-align:center;font-weight:600;font-size:15px">Termin anfragen</div>''', 'Beispiel: Online-Termin auf der eigenen Website')

MOCK_GPROFILE = mock_frame('google.ch/maps', '''<div class="gp"><div class="ttl">Ihre Praxis Zürich</div>
<div class="g-stars" style="font-size:14px">★★★★★ <small>4,9 · Ästhetische Medizin</small></div>
<div class="row"><span class="p">Termin buchen</span><span>Route</span><span>Anrufen</span><span>Website</span></div>
<div class="photos"><i></i><i></i><i></i></div>
<div class="info"><span>📍 Bahnhofstrasse, Zürich</span><span>🕘 Heute geöffnet bis 18:30</span><span>☎ 044 000 00 00</span></div>
<div class="post"><b>Beitrag · vor 3 Tagen</b>Neu bei uns: Hautanalyse mit ausführlicher Beratung. Termine online.</div></div>''', 'Beispiel: vollständiges Google-Profil mit Beitrag (fiktive Angaben)')

MOCK_REVIEWS = '''<div class="mock" role="img" aria-label="Beispiel: Bewertungen mit Antwort und QR-Karte"><div class="mock-b" aria-hidden="true">
<div class="rv"><div class="top"><span class="av">S</span><div><b style="font-size:14.5px">Sandra M.</b><div class="st">★★★★★</div></div></div><p>Sehr ruhige Atmosphäre, ich habe mich gut beraten gefühlt. Der Termin ging online in zwei Minuten.</p><div class="reply"><b>Antwort der Inhaberin</b>Herzlichen Dank für Ihre Worte, wir freuen uns auf das nächste Mal.</div></div>
<div class="rv"><div class="top"><span class="av">L</span><div><b style="font-size:14.5px">Laura K.</b><div class="st">★★★★★</div></div></div><p>Pünktlich, freundlich, alles genau erklärt.</p></div>
<div class="qr"><div class="code">''' + ''.join('<i class="o"></i>' if c=='0' else '<i></i>' for c in '1110111101010110111011000100101011101101110010111110111'[:49]) + '''</div><div><b>Wie war Ihr Termin?</b><small>Scannen und direkt bei Google bewerten. Dauert eine Minute.</small></div></div>
</div></div><p class="mock-note">Beispiel-Darstellung, fiktive Bewertungen</p>'''

MOCK_SERP = mock_frame('google.ch/search?q=laser+haarentfernung+zürich', '''<div class="serp-r"><small>Anzeige · beispiel-kette.ch</small><b>Laser Haarentfernung – Jetzt Aktion</b><p>Filialen in der ganzen Schweiz …</p></div>
<div class="serp-r me"><span class="lbl">Ihre Seite</span><small>ihre-praxis.ch › laser-haarentfernung</small><b>Laser-Haarentfernung in Zürich · Ihre Praxis</b><p>Ablauf, Anzahl Sitzungen, Zonen und Termin online. Beratung vor Ort in Zürich.</p></div>
<div class="serp-r"><small>andere-praxis.ch</small><b>Behandlungen · Andere Praxis</b><p>Unsere Behandlungen im Überblick …</p></div>''', 'Beispiel: eine eigene Seite pro Behandlung in den Google-Ergebnissen')

MOCK_CHAT = mock_frame('chatgpt.com', '''<div class="chatui"><div class="msg u">Welche Praxis empfiehlst du für eine Hautanalyse in Zürich?</div>
<div class="msg b">Einige Anlaufstellen in Zürich, die häufig genannt werden:<ol><li><mark>Ihre Praxis</mark>, Ärztin mit Schwerpunkt Hautqualität, Termine online</li><li>Praxis B …</li><li>Institut C …</li></ol></div></div>''', 'Beispiel-Darstellung: So kann eine KI-Antwort aussehen. Eine Nennung kann niemand garantieren.')

def bars(h): return '<div class="bars">' + ''.join(f'<i style="height:{x}%"></i>' for x in h) + '</div>'
MOCK_REPORT = f'''<div class="mock" role="img" aria-label="Aufbau des Monatsberichts"><div class="mock-b" aria-hidden="true">
<div class="rep-h"><b>Monatsbericht</b><small>Aufbau · Verlauf je Monat</small></div>
<div class="rep-row"><span>Terminanfragen über die Website</span>{bars([30,42,40,55,62,70])}</div>
<div class="rep-row"><span>Anrufe und Routen über Google</span>{bars([45,40,52,58,57,66])}</div>
<div class="rep-row"><span>Neue Google-Bewertungen</span>{bars([20,35,30,48,52,60])}</div>
<div class="rep-row"><span>Positionen wichtiger Suchbegriffe</span>{bars([25,30,38,44,50,58])}</div>
<div class="rep-row"><span>ChatGPT-Test mit Screenshot</span><span style="font-size:14px;color:var(--acc-ink);font-weight:600">genannt / nicht genannt</span></div>
</div></div><p class="mock-note">Aufbau des Berichts. Die Balken sind eine Illustration, keine echten Werte.</p>'''

ICON = {
 'maps':'<svg viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 'search':'<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>',
 'ai':'<svg viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/><path d="M8.5 10.5h7"/></svg>',
 'star':'<svg viewBox="0 0 24 24"><path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8-4.3-4.1 5.9-.8z"/></svg>',
 'loop':'<svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 0 1 14-5.3L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5.3L4 15"/><path d="M4 20v-5h5"/></svg>',
}

PAGES = {}
def page(file, title, desc, main, cta_t=None, crumbs_ld=None):
    PAGES[file] = dict(title=title, desc=desc, main=main, cta=cta_t, crumbs=crumbs_ld)

# ================= STARTSEITE =================
STAGE = '''<div class="stage" role="img" aria-label="Beispiel: Praxis-Website auf dem Laptop, Google-Profil auf dem Handy und eine Antwort von ChatGPT, in der die Praxis genannt wird">
  <span class="tag" aria-hidden="true">Beispiel</span>
  <div class="laptop" aria-hidden="true"><div class="lt-screen"><div class="site">
    <div class="site-nav"><b>IHRE PRAXIS</b><span><i></i><i></i><i></i><em>Termin buchen</em></span></div>
    <div class="site-body"><div class="site-copy"><small>Ästhetische Medizin · Zürich</small><strong>Natürlich schön. Ärztlich begleitet.</strong><span></span><span></span><em>Termin online buchen</em></div><div class="site-img" style="background-image:url(img/hero-treat.webp);background-position:45% center"></div></div>
  </div></div><div class="lt-base"></div></div>
  <div class="phone" aria-hidden="true"><div class="ph-screen"><div class="ph-top"></div><div class="g-search">Ästhetik Praxis in der Nähe</div><div class="g-map"></div><div class="g-card"><b>Ihre Praxis</b><div class="g-stars">★★★★★<small>4,9</small></div><div class="g-meta">Ästhetische Medizin · Geöffnet</div><div class="g-btns"><span>Termin</span><span>Route</span></div></div></div></div>
  <div class="chat" aria-hidden="true"><div class="chat-h"><span class="gpt-dot"></span><b>ChatGPT</b><small>Antwort auf eine Frage</small></div><div class="q">Welche Ästhetikpraxis empfiehlst du in Zürich?</div><div class="a"><span>Häufig genannt wird <mark>Ihre Praxis</mark>: ärztlich geführt, viele sehr gute Bewertungen, Termine online buchbar.</span></div></div>
</div>'''

def lcards():
    return ''.join(f'<a class="card" href="{h}"><div class="ph"><img src="img/{im}.webp" alt="" width="1600" height="1067" loading="lazy"></div><div class="cb"><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p><span class="go">Mehr erfahren →</span></div></a>' for i,(h,t,d,im,_) in enumerate(LEIST))
def fcards():
    return ''.join(f'<a class="card" href="{h}"><div class="ph"><img src="img/{im}.webp" alt="" width="1600" height="1067" loading="lazy"></div><div class="cb"><h3>{t}</h3><p>{d}</p><span class="go">Mehr erfahren →</span></div></a>' for h,t,d,im,_ in FUER)

index_main = f'''<section class="hero" aria-labelledby="h1">
  <div class="wrap hero-in">
    <div>
      <p class="eyebrow">Für Ästhetikpraxen, Institute und Studios · Aus Zürich für die Schweiz</p>
      <h1 id="h1">Ihr Ruf ist ausgezeichnet.<span class="l2">Online sieht man davon zu wenig.</span></h1>
      <p class="lead">Patientinnen entscheiden heute bei Google und ChatGPT, bevor sie anrufen. Ich sorge dafür, dass sie Sie dort finden, Ihnen vertrauen und direkt einen Termin anfragen.</p>
      <div class="btns"><a class="btn btn-deep" href="sichtbarkeits-check.html">Gratis Sichtbarkeits-Check <span aria-hidden="true">→</span></a><a class="btn btn-line" href="#test">Der 30-Sekunden-Test</a></div>
      <div class="hero-note"><span>Gesehen. Gebucht. Gewachsen.</span><span>Ein Ansprechpartner</span><span>Keine Ranking-Versprechen</span><span>Monatsbericht mit klaren Zahlen</span></div>
    </div>
    {STAGE}
  </div>
</section>
<div class="strip" aria-label="Leistungen"><div class="wrap"><ul><li>Website mit Online-Termin</li><li>Google-Profil</li><li>Bewertungen</li><li>SEO Zürich</li><li>Sichtbar in ChatGPT</li><li>Monatsbericht</li></ul></div></div>

<section class="sec" aria-labelledby="ins-t"><div class="wrap insights">
  <div class="sticky"><p class="eyebrow">Was wir sehen</p><h2 id="ins-t">Was viele übersehen.</h2><p class="lead">Ich spreche jede Woche mit Praxen und Studios in der Region Zürich. Drei Dinge sehe ich dabei immer wieder.</p><div class="btns"><a class="tlink" href="ueber-mich.html">Wer dahinter steht →</a></div></div>
  <div>
    <div class="ins"><span class="n">01</span><div><h3>Die meisten Praxen haben ein Sichtbarkeitsproblem, kein Qualitätsproblem.</h3><p>Die Arbeit ist hervorragend, die Bewertungen auch. Aber online wirkt die Praxis kleiner, als sie ist. Und wer online klein wirkt, wird nicht angerufen.</p></div></div>
    <div class="ins"><span class="n">02</span><div><h3>Patientinnen entscheiden bei Google und ChatGPT, bevor sie anrufen.</h3><p>Sie vergleichen Sterne, Fotos und Antworten auf ihre Fragen. Den ersten Eindruck bekommt Ihre Praxis heute auf dem Handy, nicht am Empfang.</p></div></div>
    <div class="ins"><span class="n">03</span><div><h3>Eine schöne Website allein bringt noch keine Termine.</h3><p>Termine kommen, wenn Website, Google-Profil, Bewertungen und ChatGPT zusammenspielen. Fehlt ein Teil, verpufft der Rest.</p></div></div>
  </div>
</div></section>

<section class="sec soft" aria-labelledby="src-t"><div class="wrap">
  {head('Mehrere Quellen statt einer','Mehr Kundinnen aus mehreren Quellen.','Viele Praxen leben von Instagram und Empfehlungen. Das ist wertvoll, aber eine einzige Quelle. Ziel ist eine Agenda, die nicht davon abhängt, ob ein Reel gut läuft.','src-t')}
  <div class="flow">
    <div class="src">
      <a href="google-unternehmensprofil.html"><span class="ic">{ICON['maps']}</span><span><b>Google Maps</b><small>«Ästhetik Praxis in meiner Nähe»</small></span></a>
      <a href="seo-zuerich.html"><span class="ic">{ICON['search']}</span><span><b>Google-Suche</b><small>«Laser Haarentfernung Zürich»</small></span></a>
      <a href="sichtbar-in-chatgpt.html"><span class="ic">{ICON['ai']}</span><span><b>ChatGPT &amp; KI</b><small>«Welche Praxis empfiehlst du?»</small></span></a>
      <a href="google-bewertungen.html"><span class="ic">{ICON['star']}</span><span><b>Bewertungen &amp; Empfehlungen</b><small>«Meine Freundin war dort»</small></span></a>
      <div><span class="ic">{ICON['loop']}</span><span><b>Stammkundinnen</b><small>Die wiederkommen, weil sie sich erinnert fühlen</small></span></div>
    </div>
    <div class="flow-mid" aria-hidden="true"></div>
    <div class="agenda"><h3>Ihre Agenda</h3><p>Gefüllt aus mehreren Wegen, nicht aus einem.</p>
      <div class="cal" aria-hidden="true">{''.join('<span class="f"></span>' if c=='f' else ('<span class="h"></span>' if c=='h' else '<span></span>') for c in 'ffhfffhfhffffhfffhff')}</div>
      <div class="cal-l" aria-hidden="true"><span>Mo</span><span>Di</span><span>Mi</span><span>Do</span><span>Fr</span></div>
      <p style="margin-top:16px;font-size:13.5px">Illustration</p></div>
  </div>
</div></section>

<section class="sec" aria-labelledby="cmp-t"><div class="wrap">
  {head('Ein Ansprechpartner','Ein Ansprechpartner statt fünf Anbieter.','Website hier, Google-Profil dort, Bewertungen nebenbei, SEO bei einer Agentur und niemand, der das Ganze sieht. Bei mir läuft alles zusammen.','cmp-t')}
  <div class="compare">
    <div class="cmp before"><h3>So ist es oft</h3><ul>
      <li><span>Webdesigner für die Website<small>danach selten erreichbar</small></span></li>
      <li><span>Google-Profil macht das Team nebenbei<small>Öffnungszeiten veraltet, keine Beiträge</small></span></li>
      <li><span>Bewertungen kommen zufällig<small>wenige, keine Antworten</small></span></li>
      <li><span>SEO-Agentur mit Ticket-System<small>Berichte, die niemand versteht</small></span></li>
      <li><span>ChatGPT? Hat sich noch niemand angeschaut</span></li></ul></div>
    <div class="cmp after"><h3>Mit Seenery</h3><ul>
      <li>Ein Plan für Website, Google, Bewertungen und ChatGPT</li>
      <li>Ein fester Ansprechpartner, direkt erreichbar</li>
      <li>Gleiche Angaben überall, nichts widerspricht sich</li>
      <li>Texte mit Blick auf die Schweizer Werberegeln</li>
      <li>Ein Monatsbericht, der alles zusammen zeigt</li></ul>
      <div class="btns" style="margin-top:24px"><a class="btn btn-light btn-sm" href="leistungen.html">Leistungen ansehen</a></div></div>
  </div>
</div></section>

<section class="sec paper" aria-labelledby="l-t"><div class="wrap">
  <div class="head split"><div><p class="eyebrow">Leistungen</p><h2 id="l-t">Sechs Bausteine, die zusammen wirken.</h2></div><p class="lead">Was davon Ihre Praxis braucht, klären wir im Gespräch. Jede Leistung hat ihre eigene Seite mit allen Details.</p></div>
  <div class="grid3">{lcards()}</div>
</div></section>

<section class="sec deep" id="test" aria-labelledby="test-t"><div class="wrap test">
  <div><p class="eyebrow">Der 30-Sekunden-Test</p><h2 id="test-t">Wird Ihre Praxis in ChatGPT genannt?</h2><p class="lead">Immer mehr Menschen fragen KI-Assistenten nach Empfehlungen. Wer dort nicht vorkommt, wird gar nicht erst verglichen. Probieren Sie es selbst aus.</p><div class="btns"><a class="btn btn-light" href="sichtbar-in-chatgpt.html">Mehr zu ChatGPT-Sichtbarkeit</a></div></div>
  {PROMPT_BOX('prompt-home')}
</div></section>

<section class="sec" aria-labelledby="fw-t"><div class="wrap">
  {head('Für wen','Gebaut für Betriebe, die wachsen wollen.',None,'fw-t')}
  <div class="grid3">{fcards()}</div>
</div></section>

<section class="sec deep" aria-labelledby="hl-t"><div class="wrap">
  <div class="head"><p class="eyebrow">Haltung</p><h2 id="hl-t" style="max-width:20ch">Woran ich glaube.</h2></div>
  <div class="beliefs">
    <div class="belief"><span class="k">Der Kern</span><blockquote>Wir füllen Ihre Agenda mit Neukunden, die bleiben.</blockquote><p>Gefunden werden Sie über Google und ChatGPT. Bleiben werden sie, weil Ihre Arbeit es wert ist.</p></div>
    <div class="belief"><span class="k">Der Massstab</span><blockquote>Marketing muss sich jeden Monat in Zahlen zeigen.</blockquote><p>Darum gibt es jeden Monat einen Bericht, verständlich und im Vergleich zum Start.</p></div>
    <div class="belief"><span class="k">Der Antrieb</span><blockquote>Gute Arbeit verdient es, gefunden zu werden.</blockquote><p>Wer täglich sorgfältig arbeitet, soll nicht hinter lauteren Anbietern verschwinden.</p></div>
  </div>
</div></section>

<section class="sec soft" aria-labelledby="ab-t"><div class="wrap">
  <div class="head split"><div><p class="eyebrow">Ablauf</p><h2 id="ab-t">Vom Check zum fertigen Auftritt.</h2></div><p class="lead">Wenig Aufwand für Sie, klare Schritte, und Sie wissen immer, wo wir stehen. <a class="tlink" href="ablauf.html">Ablauf im Detail →</a></p></div>
  {steps()}
</div></section>

<section class="sec" aria-labelledby="fq-t"><div class="wrap">
  {head('Häufige Fragen','Ehrliche Antworten.',None,'fq-t')}
  {faq([
   ('Gibt es Ranking-Garantien?','Nein. Eine gute Platzierung ist das Ziel, kein Versprechen. Das kann ehrlicherweise niemand garantieren. Dafür sehen Sie jeden Monat klare Zahlen.'),
   ('Was kostet das?','Das hängt davon ab, was Ihre Praxis braucht: neue Website oder Upgrade, wie viele Behandlungen, wie viel laufende Betreuung. Nach dem kostenlosen Check bekommen Sie ein klares Angebot.'),
   ('Wir haben schon eine Website. Brauchen wir eine neue?','Nicht unbedingt. Hat Ihre Website eine gute Basis, machen wir ein Upgrade und konzentrieren uns auf Google, Bewertungen und ChatGPT.'),
   ('Mit wem arbeite ich zusammen?','Immer direkt mit mir, James Alves Da Silva. Kein Ticket-System und keine wechselnden Projektleiter.'),
  ])}
  <div class="btns c"><a class="btn btn-line" href="faq.html">Alle Fragen ansehen</a></div>
</div></section>'''
page('index.html','Seenery Agency · Sichtbar bei Google und ChatGPT für Praxen und Studios in Zürich',
 'Website mit Online-Termin, Google-Profil, Bewertungen, SEO und Sichtbarkeit in ChatGPT für Ästhetikpraxen, Laser- und Kosmetikinstitute und Beauty-Studios in der Region Zürich. Kostenloser Sichtbarkeits-Check.', index_main)

# ================= LEISTUNGEN ÜBERSICHT =================
LROWS = [
 ('Website mit Online-Termin','Ihr Empfang im Internet. Eigenes Design, eine Seite pro Behandlung und ein Termin-Knopf, der auf jedem Handy funktioniert.',['Eigenes Design statt Vorlage','Seite pro Behandlung','Online-Termin eingebunden','Schnell auf dem Handy']),
 ('Google-Unternehmensprofil','Wer «in der Nähe» sucht, sieht zuerst die Karte. Ihr Profil wird vollständig, aktuell und mit regelmässigen Beiträgen lebendig gehalten.',['Alle Behandlungen als Leistungen','Echte Fotos','Google-Beiträge','Termin-Link im Profil']),
 ('Google-Bewertungen','Aus zufriedenen Patientinnen werden sichtbare Empfehlungen, mit einem einfachen System für Ihr Team.',['QR-Karte am Empfang','Link nach dem Termin','Antworten auf Bewertungen','Ohne Zugriff auf Patientendaten']),
 ('SEO für Zürich','Bei Google für genau die Behandlungen gefunden werden, die Sie anbieten, dort wo Ihre Patientinnen wohnen und arbeiten.',['Suchbegriffe Ihrer Region','Saubere Technik','Verzeichnisse wie local.ch','Positionsverlauf']),
 ('Sichtbar in ChatGPT','Klare, überall gleiche Fakten zu Praxis, Team und Behandlungen, damit KI-Assistenten Sie verstehen und nennen können.',['Fakten-Seiten','Strukturierte Daten','Monatlicher ChatGPT-Test','Screenshot mit Datum']),
 ('Monatsbericht','Jeden Monat schwarz auf weiss, was sich bewegt. Verständlich erklärt und im Vergleich zum Start.',['Anfragen und Anrufe','Neue Bewertungen','Positionen bei Google','ChatGPT-Test']),
]
lrows = ''.join(f'''<article class="lrow"><figure class="lr-fig"><img src="img/{LEIST[i][3]}.webp" alt="" width="1600" height="1067" loading="lazy"></figure><div><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p><ul>{''.join(f"<li>{x}</li>" for x in L)}</ul><div class="btns" style="margin-top:22px"><a class="tlink" href="{LEIST[i][0]}">{t}: alle Details →</a></div></div></article>''' for i,(t,d,L) in enumerate(LROWS))
page('leistungen.html','Leistungen: Website, Google-Profil, Bewertungen, SEO und ChatGPT · Seenery Agency',
 'Alle Leistungen von Seenery Agency im Überblick: Website mit Online-Termin, Google-Unternehmensprofil, Google-Bewertungen, SEO für Zürich, Sichtbarkeit in ChatGPT und Monatsbericht.',
 page_hero([('Leistungen',None)],'Leistungen','Alles, was es für mehr Termine braucht.','Aus einer Hand.','Sechs Bausteine, die zusammen wirken. Sie bekommen nicht alles, sondern das, was Ihre Praxis wirklich weiterbringt. Was das ist, zeigt der kostenlose Check.','leistungen','Hautpflegeprodukte auf hellem Untergrund mit Steinen und Zweigen','Bilder: Beispiele, keine Kundenprojekte',pills=['Website','Google','Bewertungen','SEO','ChatGPT','Bericht']) +
 f'''<section class="sec" style="padding-top:0" aria-label="Die sechs Bausteine"><div class="wrap lrows">{lrows}</div></section>
<section class="sec soft" aria-labelledby="ext-t"><div class="wrap">
  {head('Auf Wunsch und später','Was dazukommen kann.','Nicht jede Praxis braucht alles gleichzeitig. Diese Bausteine kommen dazu, wenn die Basis steht.','ext-t')}
  {checks([
   ('Kundenkartei und Reaktivierung','Kundinnen, die länger nicht da waren, bekommen eine persönliche Erinnerung per WhatsApp, SMS oder E-Mail. Bei verschreibungspflichtigen Behandlungen ohne Rabatt, wie es die Werberegeln verlangen.'),
   ('Deutsch und Englisch','Für internationale Patientinnen eine zweite Sprache.'),
   ('Rundgang und Video','Ruhig bewegte Bilder oder ein Rundgang durch Ihre Räume.'),
   ('Ratgeber-Artikel','Antworten auf die Fragen, die Patientinnen vor dem Termin googeln.'),
   ('Fotoshooting, Logo und Werbung','Über erfahrene Partner, abgestimmt auf Ihren Auftritt.'),
   ('Schulung für Ihr Team','Wie man um Bewertungen bittet und das Google-Profil pflegt.'),
  ])}
  <p class="mock-note" style="margin-top:28px">Nicht im Angebot: Webshops und laufende Betreuung von Social-Media-Kanälen. Dafür vermittle ich gerne Partner.</p>
</div></section>''', crumbs_ld=[('Leistungen','leistungen.html')])

# ================= LEISTUNGSSEITEN =================
def leist_page(file, title, desc, hero, intro, items_title, items, mock_block, faqs, ctat=None):
    t = [x for x in LEIST if x[0]==file][0][1]
    main = f'''{hero}
<section class="sec" style="padding-top:0" aria-labelledby="s-intro"><div class="wrap">{intro}</div></section>
<section class="sec soft" aria-labelledby="i-t"><div class="wrap">{head('Was dazugehört',items_title,None,'i-t')}{checks(items)}</div></section>
<section class="sec" aria-labelledby="s-mock"><div class="wrap">{mock_block}</div></section>
<section class="sec paper" aria-labelledby="fq-t"><div class="wrap">{head('Häufige Fragen','Kurz beantwortet.',None,'fq-t')}{faq(faqs)}</div></section>
<section class="sec tight" aria-labelledby="rel-t"><div class="wrap">{head('Weitere Leistungen','Was zusammen wirkt.',None,'rel-t')}{related(file)}</div></section>'''
    page(file, title, desc, main, ctat, crumbs_ld=[('Leistungen','leistungen.html'),(t,file)])

leist_page('website-mit-online-termin.html','Website mit Online-Termin für Praxen und Studios in Zürich · Seenery Agency',
 'Website auf dem Niveau Ihrer Praxis: eigenes Design, eine Seite pro Behandlung, Online-Termin, schnell auf dem Handy und gebaut für Google und ChatGPT.',
 page_hero([('Leistungen','leistungen.html'),('Website mit Online-Termin',None)],'Leistung · Website','Ein Auftritt auf dem Niveau','Ihrer Arbeit.','Kein Baukasten von der Stange. Ihre Website bekommt ein eigenes Gesicht, eine Seite pro Behandlung und einen Termin-Knopf, der auf jedem Handy funktioniert.','termin','Frau tippt auf einem Smartphone und bucht einen Termin','Die meisten Termine werden auf dem Handy angefragt',pills=['Eigenes Design','Seite pro Behandlung','Online-Termin']),
 split_mock('Die Idee','Ihre Website ist Ihr Empfang im Internet.',
   ['Bevor eine Patientin Ihren Empfang betritt, hat sie Ihre Website gesehen. Dort entscheidet sie, ob sie Ihnen vertraut. Darum gestalte ich jede Website so, dass sie zu Ihren Räumen, Ihrem Team und Ihrer Arbeit passt.',
    'Gebaut wird aus bewährten Bausteinen. Deshalb sehen Sie Ihren ersten Entwurf nach wenigen Tagen und nicht erst nach Wochen.'], MOCK_BOOKING, hid='s-intro'),
 'Alles für einen starken Auftritt.',
 [('Eigenes Design','Farben, Schriften und Bildsprache passend zu Ihrer Praxis.'),('Eine Seite pro Behandlung','Ablauf, Dauer, Ausfallzeit, häufige Fragen und Termin-Knopf.'),
  ('Online-Termin','OneDoc, Fresha, Shore oder Ihr bestehendes System, sauber eingebunden.'),('Handy zuerst','Gestaltet für den Daumen, nicht nur für den Bildschirm.'),
  ('Schnelle Ladezeit','Bilder und Technik so optimiert, dass nichts wartet.'),('Gebaut für Google und ChatGPT','Saubere Struktur und klare Fakten zu Praxis und Team.'),
  ('Team und Qualifikationen','Porträts, Schwerpunkte und Ausbildung schaffen Vertrauen.'),('Bewertungen auf der Website','Echte Stimmen aus Google, dort wo entschieden wird.'),
  ('Impressum und Datenschutz','Die Pflichtseiten gehören dazu.'),('Laufende Anpassungen','Neue Behandlung, neue Öffnungszeiten: im vereinbarten Umfang passe ich an.')],
 split('Warum es wirkt','Wer vergleicht, entscheidet in Sekunden.',
   ['Eine Patientin öffnet meist mehrere Praxen nebeneinander. Den Termin bekommt oft die Praxis, deren Auftritt am ruhigsten, klarsten und vertrauenswürdigsten wirkt, und bei der der Termin nur einen Klick entfernt ist.',
    'Darum steht der Termin-Knopf auf jeder Seite an derselben Stelle, und jede Behandlung beantwortet die Fragen, die sonst am Telefon gestellt werden.'],'web-booking','Frau liegt entspannt auf dem Sofa und bucht am Laptop online einen Termin',rev=True,hid='s-mock'),
 [('Wie lange dauert es?','Den ersten Entwurf sehen Sie nach wenigen Tagen. Online ist die Website in der Regel innert 14 Arbeitstagen ab vollständigen Unterlagen.'),
  ('Wer schreibt die Texte?','Ich schreibe die Texte aus Ihren Inhalten und unserem Gespräch. Sie geben fachlich frei.'),
  ('Funktioniert unser Buchungssystem?','In den meisten Fällen ja. Ich prüfe Ihr System im Gespräch und binde es ein. Die Kosten für das Buchungssystem laufen direkt über Sie.'),
  ('Wem gehört die Website?','Design und Texte dürfen Sie nach Bezahlung des Setups auch nach Vertragsende unbeschränkt nutzen. Die Domain läuft auf Ihren Namen.')])

leist_page('google-unternehmensprofil.html','Google-Unternehmensprofil für Praxen und Studios in Zürich · Seenery Agency',
 'Ihr Google-Unternehmensprofil komplett: alle Behandlungen, echte Fotos, Öffnungszeiten, Termin-Link und regelmässige Google-Beiträge für Praxen und Studios in der Region Zürich.',
 page_hero([('Leistungen','leistungen.html'),('Google-Unternehmensprofil',None)],'Leistung · Google-Profil','Gefunden werden,','wo gesucht wird.','Wer «in meiner Nähe» sucht, sieht zuerst Google Maps. Dort entscheiden Sterne, Fotos und ein vollständiges Profil, wer angerufen wird.','gprofil','Hand hält ein Smartphone mit geöffneter Google-Maps-Karte','Gesucht wird auf dem Handy, oft unterwegs',pills=['Profil komplett','Google-Beiträge','Termin-Link']),
 split_mock('Die Idee','Ihr Profil ist oft der erste Kontakt.',
   ['Viele Patientinnen sehen Ihr Google-Profil, bevor sie Ihre Website öffnen. Fehlt die Telefonnummer, stimmen die Öffnungszeiten nicht oder führt der Website-Knopf ins Leere, ist die Patientin schnell bei der nächsten Praxis.',
    'Und auch Google selbst ist auf vollständige, richtige Angaben angewiesen. Fehlen Kategorien und Leistungen oder widersprechen sich Adresse, Telefonnummer und Öffnungszeiten auf verschiedenen Seiten, kann Google Ihre Praxis schlechter einordnen und zeigt sie bei passenden Suchen seltener.',
    'Ich richte Ihr Profil vollständig ein und halte es lebendig, mit regelmässigen Beiträgen und neuen Fotos.'], MOCK_GPROFILE, hid='s-intro'),
 'Ein Profil, das arbeitet.',
 [('Alle Behandlungen als Leistungen','Damit Google weiss, wofür Sie stehen.'),('Kategorien richtig gewählt','Haupt- und Zusatzkategorien passend zu Ihrem Angebot.'),
  ('Telefon, Website und Termin-Link','Alles richtig verknüpft, nichts führt ins Leere.'),('Öffnungszeiten und Feiertage','Immer aktuell, auch über Weihnachten.'),
  ('Echte Fotos','Räume, Team und Atmosphäre statt Symbolbilder.'),('Regelmässige Google-Beiträge','Mit Bild und klarem Bezug zu Ihren Behandlungen.'),
  ('Antworten auf Bewertungen','Professionell und freundlich, von Ihnen freigegeben.'),('Gleiche Angaben in Verzeichnissen','local.ch, search.ch und weitere, ohne Widersprüche.')],
 f'''<div class="center narrow">{head('Warum es wirkt','Die Karte zeigt nur wenige Praxen.','Bei einer Suche in der Nähe zeigt Google zuerst eine kleine Auswahl auf der Karte. Ein vollständiges, aktives Profil mit vielen echten Bewertungen ist die beste Grundlage, um dort aufzutauchen. Garantieren kann das niemand.','s-mock')}</div>''',
 [('Wir haben schon ein Profil. Braucht es das trotzdem?','Meist ja. Oft fehlen Leistungen, Fotos oder Beiträge, oder der Website-Knopf führt auf eine Buchungsplattform statt auf Ihre Seite.'),
  ('Wie oft erscheinen Beiträge?','Das legen wir gemeinsam fest. Mehr Beiträge bedeuten mehr Aktivität im Profil.'),
  ('Wem gehört das Profil?','Ihnen. Ich arbeite mit einem Zugang, den Sie jederzeit entziehen können.')])

leist_page('google-bewertungen.html','Mehr Google-Bewertungen für Praxen und Studios · Seenery Agency',
 'Mehr echte Google-Bewertungen nach jedem Termin und professionelle Antworten, für Praxen, Institute und Studios in der Region Zürich. Ohne Zugriff auf Patientendaten.',
 page_hero([('Leistungen','leistungen.html'),('Google-Bewertungen',None)],'Leistung · Bewertungen','Aus zufriedenen Patientinnen','werden Empfehlungen.','Ihre Patientinnen sind begeistert, aber nur wenige schreiben es auf. Mit einem einfachen System wird nach jedem Termin freundlich um eine ehrliche Bewertung gebeten.','bewertung','Lächelnde Frau sitzt an einem Holztisch und schreibt auf ihrem Smartphone','Eine Bewertung dauert nur eine Minute',pills=['QR-Karte','Link nach dem Termin','Antworten']),
 split_mock('Die Idee','Fünf Sterne sind gut. Viele echte Stimmen sind besser.',
   ['Eine Praxis mit wenigen Bewertungen wirkt neben einer mit vielen kleiner, auch wenn die Qualität gleich ist. Und eine einzelne unfaire Bewertung wiegt schwer, wenn es nur wenige gibt.',
    'Darum richte ich ein Bewertungs-System ein, das Ihr Team ohne Aufwand nutzt. Gefragt werden alle Patientinnen, nicht nur die zufriedenen. So will es Google, und so bleibt es ehrlich.'], MOCK_REVIEWS, hid='s-intro'),
 'So kommen mehr echte Stimmen.',
 [('QR-Karte am Empfang','Scannen und direkt bei Google bewerten.'),('Link nach dem Termin','Ihr Team schickt einen kurzen Link per SMS oder E-Mail.'),
  ('Kurze Anleitung fürs Team','Wann und wie man freundlich fragt.'),('Antworten auf Bewertungen','Professionell, von Ihnen freigegeben und ohne zu bestätigen, dass jemand Patientin ist.'),
  ('Umgang mit unfairen Bewertungen','Ruhige Antwort und Meldung bei Google. Ob Google löscht, entscheidet Google.'),('Kein Zugriff auf Patientendaten','Ihr Team fragt, ich richte das System ein. Das Berufsgeheimnis bleibt bei Ihnen.')],
 f'''<div class="center narrow">{head('Warum es wirkt','Vertrauen entsteht durch Menge und Ehrlichkeit.','Neue Patientinnen lesen Bewertungen, bevor sie anrufen. Viele echte Stimmen und gute Antworten zeigen: Hier wird man ernst genommen.','s-mock')}</div>''',
 [('Dürfen wir Patientinnen um Bewertungen bitten?','Ja, freundlich und ohne Gegenleistung. Belohnungen für Bewertungen sind bei Google nicht erlaubt.'),
  ('Was tun bei einer unfairen Bewertung?','Ruhig und professionell antworten und bei Google melden. Wer mitliest, achtet oft mehr auf Ihre Antwort als auf die Bewertung.'),
  ('Sehen Sie unsere Patientendaten?','Nein. Ihr Team stellt die Frage, ich liefere Karte, Link und Vorlagen.')])

leist_page('seo-zuerich.html','SEO Zürich für Ästhetikpraxen, Institute und Studios · Seenery Agency',
 'Lokale Suchmaschinenoptimierung in Zürich: die richtigen Suchbegriffe, eine Seite pro Behandlung, saubere Technik und gleiche Angaben in Verzeichnissen. Für Praxen, Institute und Studios.',
 page_hero([('Leistungen','leistungen.html'),('SEO für Zürich',None)],'Leistung · SEO Zürich','Gefunden werden, wenn','in Zürich gesucht wird.','Lokale Suchmaschinenoptimierung für Praxen, Institute und Studios: die Suchbegriffe Ihrer Patientinnen, eine Seite pro Behandlung und Technik, die Google versteht.','zuerich','Luftaufnahme der Zürcher Altstadt mit Limmat und Zürichsee','Gesucht wird lokal: in Zürich und Umgebung',pills=['Lokale Suchbegriffe','Seite pro Behandlung','Saubere Technik']),
 split_mock('Die Idee','Eine Seite für alles ist eine Seite für nichts.',
   ['Viele Praxen führen alle Behandlungen auf einer einzigen Seite. Wer aber «Laser Haarentfernung Zürich» sucht, landet bei der Praxis mit der passenden Seite.',
    'Darum bekommt jede wichtige Behandlung eine eigene Seite: was sie bewirkt, wie sie abläuft, wie oft man kommt und was man danach beachtet. Mit Termin-Knopf direkt in Ihr Buchungssystem.'], MOCK_SERP, hid='s-intro'),
 'Was ich jeden Monat tue.',
 [('Suchbegriffe Ihrer Region','Mit Google Trends, Keyword Planner und Search Console finde ich heraus, wonach gesucht wird.'),('Seite pro Behandlung','Inhalte, die echte Fragen vor dem Termin beantworten.'),
  ('Titel und Beschreibungen','Für jede Seite eindeutig, damit sie in den Ergebnissen auffällt.'),('Strukturierte Daten','Praxis, Adresse, Öffnungszeiten und Behandlungen maschinenlesbar.'),
  ('Ladezeit und Technik','Schnell auf dem Handy, sauber verlinkt.'),('Verzeichnisse','Gleiche Angaben auf local.ch, search.ch und weiteren.'),
  ('Search Console','Eingerichtet und überwacht: welche Suchen zu Ihnen führen.'),('Positionsverlauf','Ihre wichtigsten Suchbegriffe im Monatsbericht.')],
 f'''<div class="center narrow">{head('Ehrlich gesagt','Keine Seiten für jede Gemeinde.','Manche Anbieter bauen hundert fast gleiche Seiten für jeden Ort. Google stuft solche Seiten als Spam ein. Ich baue nur Seiten mit echtem Inhalt, die Patientinnen wirklich weiterhelfen.','s-mock')}</div>''',
 [('Wann sieht man Ergebnisse?','Erste Veränderungen können sich nach einigen Wochen zeigen. Gute Platzierungen bei Google brauchen meist mehrere Monate.'),
  ('Gibt es eine Garantie für Platz 1?','Nein. Das kann niemand ehrlich garantieren. Sie sehen dafür jeden Monat, wie sich Ihre Positionen entwickeln.'),
  ('Was ist mit Google Ads?','Bezahlte Anzeigen sind ein eigenes Thema. Auf Wunsch vermittle ich einen Partner, der sie betreut.')])

leist_page('sichtbar-in-chatgpt.html','Sichtbar in ChatGPT: GEO für Praxen und Studios in Zürich · Seenery Agency',
 'Damit ChatGPT und andere KI-Assistenten Ihre Praxis kennen und nennen können: klare Fakten, gleiche Angaben überall und ein monatlicher ChatGPT-Test mit Screenshot.',
 page_hero([('Leistungen','leistungen.html'),('Sichtbar in ChatGPT',None)],'Leistung · ChatGPT & KI','Wenn jemand fragt,','soll Ihr Name fallen können.','Immer mehr Menschen fragen ChatGPT nach einer Praxis. KI-Assistenten nennen oft nur wenige Namen. Ich arbeite daran, dass Ihre Praxis dafür die richtigen Fakten liefert.','ai-chat','Hände tippen auf der Tastatur eines Laptops eine Frage ein','Neue Suche: Fragen statt Suchbegriffe',pills=['Klare Fakten','Gleiche Angaben überall','Monatlicher Test']),
 split_mock('Die Idee','KI-Assistenten empfehlen, was sie verstehen.',
   ['ChatGPT und andere Assistenten stützen sich auf Inhalte im Netz. Je klarer und einheitlicher Ihre Praxis, Ihr Team und Ihre Behandlungen beschrieben sind, desto besser können sie Sie einordnen.',
    'Ob und wann Sie genannt werden, kann niemand garantieren. Darum teste ich jeden Monat mit denselben Fragen und halte das Ergebnis mit Datum und Screenshot fest.'], MOCK_CHAT, hid='s-intro'),
 'Was ich dafür tue.',
 [('Fakten-Seiten','Praxis, Team, Qualifikationen und Behandlungen klar beschrieben.'),('Gleiche Angaben überall','Website, Google-Profil, Verzeichnisse und Social Media stimmen überein.'),
  ('Strukturierte Daten','Damit Maschinen lesen können, wer Sie sind und was Sie anbieten.'),('Antworten auf echte Fragen','Inhalte zu den Fragen, die Patientinnen stellen.'),
  ('Monatlicher ChatGPT-Test','Dieselben Fragen jeden Monat, mit Screenshot.'),('Verlauf im Monatsbericht','Wird Ihre Praxis genannt, und in welchem Zusammenhang.')],
 f'''<div class="test" id="test" style="background:var(--deep);border-radius:28px;padding:clamp(24px,4vw,48px);color:var(--on-deep)"><div><p class="eyebrow" style="color:var(--acc-soft)">Der 30-Sekunden-Test</p><h2 id="s-mock" style="color:var(--on-deep)">Probieren Sie es selbst aus.</h2><p class="lead" style="color:var(--on-deep-2)">Fragen Sie ChatGPT nach Ihrer wichtigsten Behandlung in Ihrem Ort. Kommt Ihre Praxis vor?</p></div>{PROMPT_BOX('prompt-geo')}</div>''',
 [('Was ist der Unterschied zwischen SEO und GEO?','SEO bedeutet: bei Google gefunden werden. GEO bedeutet: von KI-Assistenten wie ChatGPT verstanden und genannt werden. Ich arbeite an beidem.'),
  ('Warum schwanken die ChatGPT-Antworten?','KI-Antworten sind nicht jedes Mal gleich. Darum zählt der Verlauf über mehrere Monate, nicht ein einzelner Test.'),
  ('Gilt das auch für andere KI-Assistenten?','Die Grundlagen sind dieselben: klare, einheitliche Fakten. Getestet wird standardmässig mit ChatGPT.')])

leist_page('monatsbericht.html','Monatsbericht: Ihre Sichtbarkeit in klaren Zahlen · Seenery Agency',
 'Jeden Monat ein verständlicher Bericht: Terminanfragen, Anrufe über Google, neue Bewertungen, Positionen wichtiger Suchbegriffe und der ChatGPT-Test mit Screenshot.',
 page_hero([('Leistungen','leistungen.html'),('Monatsbericht',None)],'Leistung · Monatsbericht','Jeden Monat schwarz auf weiss,','was sich bewegt.','Platz 1 kann niemand ehrlich garantieren. Was Sie bekommen: saubere Arbeit und jeden Monat einen Bericht, der zeigt, was passiert ist. Im Vergleich zum Vormonat und zum Start.','bericht','Laptop, Notizbuch und Kaffeetasse auf einem Holztisch','Kurz, verständlich, jeden Monat',pills=['Anfragen','Bewertungen','Positionen','ChatGPT-Test']),
 split_mock('Die Idee','Zahlen statt Bauchgefühl.',
   ['Viele Praxen wissen nicht, ob sich ihr Marketing lohnt. Der Monatsbericht zeigt es: Wie viele Anfragen kamen über die Website, wie oft wurde über Google angerufen, wie viele Bewertungen sind dazugekommen.',
    'Was genau gemessen werden kann, hängt von Ihrem Buchungssystem und Ihren Zugängen ab. Das klären wir am Anfang.'], MOCK_REPORT, hid='s-intro'),
 'Was im Bericht steht.',
 [('Terminanfragen über die Website','Aus dem Formular oder Ihrem Buchungssystem, soweit messbar.'),('Aufrufe, Anrufe und Routen','Aus der Statistik Ihres Google-Profils.'),
  ('Neue Bewertungen','Anzahl, Durchschnitt und Antworten.'),('Positionen bei Google','Verlauf für Ihre wichtigsten Suchbegriffe.'),
  ('ChatGPT-Test','Dieselben Fragen, mit Screenshot und Datum.'),('Was ich getan habe','Beiträge, Anpassungen und nächste Schritte.')],
 f'''<div class="center narrow">{head('Was nicht drin steht','Keine geschönten Zahlen.','Wenn etwas nicht funktioniert, steht es im Bericht, zusammen mit dem, was ich daran ändere.','s-mock')}</div>''',
 [('Woher kommen die Zahlen?','Aus der Statistik Ihres Google-Profils, der Google Search Console, Ihrem Formular oder Buchungssystem und dem monatlichen ChatGPT-Test.'),
  ('Wie bekomme ich den Bericht?','Einmal im Monat per E-Mail, kurz und verständlich. Gerne besprechen wir ihn auch am Telefon.'),
  ('Ab wann gibt es Vergleichswerte?','Beim Start halte ich den Ausgangswert fest. Ab dem zweiten Bericht sehen Sie die Veränderung.')])

# ================= ZIELGRUPPEN =================
def zg_page(file, title, desc, hero, sit, chips_t, chips, needs, special, faqs, who, ctat, gal=''):
    t = [x for x in FUER if x[0]==file][0][1]
    main = f'''{hero}
<section class="sec" style="padding-top:0" aria-labelledby="sit-t"><div class="wrap">{sit}</div></section>
{gal}
<section class="sec soft" aria-labelledby="ch-t"><div class="wrap">{head('So wird gesucht',chips_t,'Beispiele für Suchanfragen, wie sie Menschen in der Region Zürich eingeben. Für genau diese Momente entstehen Ihre Seiten.','ch-t')}<div class="chips">{''.join(f'<span>{c}</span>' for c in chips)}</div></div></section>
<section class="sec" aria-labelledby="nd-t"><div class="wrap">{head('Was ich für Sie tue','Alles, was es für mehr Termine braucht.',None,'nd-t')}{checks(needs)}</div></section>
{special}
<section class="sec paper" aria-labelledby="fq-t"><div class="wrap">{head('Häufige Fragen',f'Was {who} mich fragen.',None,'fq-t')}{faq(faqs)}</div></section>
<section class="sec tight" aria-labelledby="rel-t"><div class="wrap">{head('Auch interessant','Weitere Bereiche.',None,'rel-t')}{related(file,'fuer')}</div></section>'''
    page(file, title, desc, main, ctat, crumbs_ld=[(t,file)])

zg_page('aesthetikpraxen.html','Website und Google-Sichtbarkeit für Ästhetikpraxen in Zürich · Seenery Agency',
 'Website mit Online-Termin, Google-Profil, Bewertungen und Sichtbarkeit in ChatGPT für ärztliche Ästhetikpraxen in der Region Zürich. Mit Blick auf die Schweizer Werberegeln.',
 page_hero([('Ästhetikpraxen',None)],'Für Ästhetikpraxen','Ärztliche Kompetenz,','online sichtbar gemacht.','Ihre Patientinnen vertrauen Ihrer Erfahrung. Neue Patientinnen sollen diese Erfahrung schon online spüren: bei Google, bei ChatGPT und auf einer Website, die so ruhig und präzise wirkt wie Ihre Behandlungen.','laser','Fachperson in Handschuhen behandelt das Gesicht einer Patientin mit einem Gerät','Symbolbild',pills=['Seite pro Behandlung','Werberegeln im Blick','OneDoc-Anbindung']),
 split('Die Ausgangslage','Ausgezeichnete Bewertungen, aber online zu leise.',
   ['Viele Praxen haben hervorragende Bewertungen, ein starkes Instagram und zufriedene Stammpatientinnen. Trotzdem nennt ChatGPT andere Namen, und bei Google erscheint zuerst die Praxis mit dem vollständigeren Profil.',
    'Dazu kommt: Werbung für ästhetische Medizin hat in der Schweiz klare Grenzen. Ich schreibe Ihre Inhalte mit Blick auf diese Regeln. Die fachliche Freigabe bleibt immer bei Ihnen.'],'aesth-2','Hautanalyse des Gesichts unter einer beleuchteten Lupenlampe',rev=True,hid='sit-t'),
 'Wonach Patientinnen suchen',
 ['Faltenbehandlung Zürich','Ästhetische Medizin Zürich','Hautverjüngung','Hautcheck Zürich','Lippenbehandlung Zürich','Narbenbehandlung','Ästhetik Praxis in meiner Nähe','Hautarzt Zürich Termin'],
 [('Eine Seite pro Behandlung','Mit Ablauf, Dauer, Ausfallzeit, häufigen Fragen und Termin-Knopf.'),('Online-Termin mit OneDoc','Ihr bestehendes Buchungssystem wird sauber eingebunden.'),
  ('Ärztinnen und Team sichtbar','Qualifikationen, Schwerpunkte und Porträts schaffen Vertrauen.'),('Google-Profil komplett','Alle Behandlungen, Fotos, Öffnungszeiten und regelmässige Beiträge.'),
  ('Bewertungs-System','Ihr Team bittet nach jedem Termin um eine ehrliche Bewertung.'),('Sichtbarkeit in ChatGPT','Klare Fakten zu Praxis, Team und Behandlungen, monatlich getestet.'),
  ('Deutsch und Englisch','Für internationale Patientinnen auf Wunsch zweisprachig.'),('Monatsbericht','Anfragen, Anrufe, Bewertungen, Positionen und ChatGPT-Test.')],
 f'''<section class="sec deep" aria-labelledby="wr-t"><div class="wrap">
  <div class="head"><p class="eyebrow">Werberegeln</p><h2 id="wr-t" style="max-width:22ch">Sichtbar werden, ohne die Regeln zu verletzen.</h2><p class="lead">Für verschreibungspflichtige Arzneimittel gilt in der Schweiz ein Publikumswerbeverbot. Das betrifft auch beliebte ästhetische Behandlungen. Darum gilt bei mir:</p></div>
  <div class="beliefs">
    <div class="belief"><span class="k">Keine Präparatenamen</span><p>Behandlungen werden beschrieben, Markennamen von Präparaten nicht beworben.</p></div>
    <div class="belief"><span class="k">Keine Vorher-Nachher-Bilder</span><p>Stattdessen Räume, Team, Ablauf und ehrliche Information.</p></div>
    <div class="belief"><span class="k">Keine Rabatte und Heilversprechen</span><p>Auch nicht in Erinnerungen an Patientinnen. Jede Seite geht vor der Veröffentlichung zur Freigabe an Sie.</p></div>
  </div>
  <p style="margin-top:28px;font-size:14.5px">Das ersetzt keine Rechtsberatung. Bei Unsicherheiten empfehle ich, die Inhalte zusätzlich prüfen zu lassen.</p>
</div></section>''',
 [('Dürfen Sie für unsere Behandlungen werben?','Ich verzichte auf Markennamen von Präparaten, auf Vorher-Nachher-Bilder, auf Rabatte und auf Heilversprechen. Jede Seite geht vor der Veröffentlichung zur fachlichen Freigabe an Sie. Eine Rechtsberatung ersetzt das nicht.'),
  ('Arbeiten Sie mit OneDoc?','Ja. Haben Sie bereits OneDoc oder ein anderes Buchungssystem, binde ich es ein. Die Kosten für das Buchungssystem laufen direkt über Sie.'),
  ('Wie gehen Sie mit Bewertungen um, Stichwort Berufsgeheimnis?','Antworten bestätigen nie, dass jemand Patientin ist, und nennen keine Behandlungsdetails. Sie geben jede Antwort frei.'),
  ('Wie viel Zeit braucht das von uns?','Am Anfang etwa ein bis zwei Stunden für Fotos, Freigaben und Zugänge. Danach übernehme ich die laufende Arbeit.')],
 'Praxen','Wie sichtbar ist Ihre Praxis heute?',
 gal=f'''<section class="sec tight" style="padding-top:0" aria-labelledby="g-t"><div class="wrap">{head('Was Patientinnen sehen wollen','Ruhe, Kompetenz, Vertrauen.','Auf Ihrer Website zeigen wir, was Ihre Praxis ausmacht: Beratung, Räume, Team und Sorgfalt. Ohne Vorher-Nachher-Bilder, mit echten Momenten.','g-t')}{gallery([('natural','Natürliches Porträt einer jungen Frau mit klarer Haut','Natürlichkeit','center 30%'),('aesth-5','Weisse Serumflasche mit goldener Pipette auf Marmor','Hautpflege','center'),('aesth-3','Heller Praxisraum mit Lounge und Behandlungskabine','Praxisräume','center'),('c-room3','Eleganter, heller Raum mit weissem Lederstuhl und Spiegel','Ambiente','center')],'Bildbeispiele Ästhetikpraxis')}</div></section>''')

zg_page('laser-kosmetikinstitute.html','Website und Google-Sichtbarkeit für Laser- und Kosmetikinstitute in Zürich · Seenery Agency',
 'Multi-Page-Website mit einer Seite pro Behandlung und Zone, Online-Buchung, Google-Profil und Sichtbarkeit in ChatGPT für Laser- und Kosmetikinstitute in der Region Zürich.',
 page_hero([('Laser- & Kosmetikinstitute',None)],'Für Laser- & Kosmetikinstitute','Viele Behandlungen.','Für jede eine klare Seite.','Laser-Haarentfernung nach Zonen, Gesichtsbehandlungen, Microneedling und vieles mehr: Wer viel anbietet, braucht eine Website, die jede Behandlung einzeln erklärt und buchbar macht. Genau so wird man bei Google gefunden.','laser-handstueck','Laser-Handstück bei der Haarentfernung am Arm einer Kundin','Symbolbild',pills=['Seite pro Behandlung','Zonen und Pakete','Online-Buchung']),
 split_mock('Die Ausgangslage','Ein grosses Angebot, das online klein wirkt.',
   ['Viele Institute führen alle Behandlungen auf einer einzigen Seite. Für Google ist das eine Seite für alles, und damit für keine Suche wirklich stark.',
    'Ich baue für jede Behandlung eine eigene Seite: was sie bewirkt, wie sie abläuft, wie oft man kommt, was man danach beachtet. Mit Termin-Knopf direkt in Ihr Buchungssystem.'], MOCK_SERP, hid='sit-t'),
 'Wonach Kundinnen suchen',
 ['Laser Haarentfernung Zürich','Laser Haarentfernung Beine','Gesichtsbehandlung Zürich','Microneedling Zürich','Kosmetikinstitut Zürich','Kosmetikstudio in meiner Nähe','Hydrafacial Zürich','Laser Haarentfernung Gesicht'],
 [('Eine Seite pro Behandlung und Zone','Damit jede Suche eine passende Antwort findet.'),('Zonen-Übersicht','Kundinnen sehen auf einen Blick, welche Zonen Sie behandeln.'),
  ('Online-Buchung','Fresha, Shore, OneDoc oder Ihr bestehendes System, sauber eingebunden.'),('Ablauf und Pflegehinweise','Vorher, am Termin, nachher: weniger Fragen am Telefon.'),
  ('Google-Profil komplett','Alle Behandlungen als Leistungen, Fotos und regelmässige Beiträge.'),('Bewertungs-System','Mehr echte Stimmen nach jedem Termin.'),
  ('Saisonale Inhalte','Zum Beispiel die Laser-Saison im Herbst und Winter, als Google-Beiträge.'),('Monatsbericht','Anfragen, Anrufe, Bewertungen und Positionen im Überblick.')],
 f'''<section class="sec deep" aria-labelledby="ls-t"><div class="wrap">
  <div class="head"><p class="eyebrow">Gut zu wissen</p><h2 id="ls-t" style="max-width:24ch">Texte, die zu Ihren Qualifikationen passen.</h2><p class="lead">Die Verordnung zum Schutz vor Gefährdungen durch nichtionisierende Strahlung (V-NISSG) regelt, wer welche Laser- und IPL-Behandlung durchführen darf. Ihre Website soll genau das zeigen, was Ihr Team anbieten darf, und die Qualifikationen sichtbar machen.</p></div>
</div></section>''',
 [('Unser Angebot ändert sich oft. Ist das ein Problem?','Nein. Neue Behandlungen bekommen eine eigene Seite, saisonale Angebote laufen über Google-Beiträge.'),
  ('Funktioniert das mit unserem Buchungssystem?','In den meisten Fällen ja. Ich prüfe Ihr System im Gespräch und binde es ein.'),
  ('Brauchen wir neue Fotos?','Echte Fotos von Räumen und Team wirken am stärksten. Ich sage Ihnen, welche Bilder fehlen.')],
 'Institute','Wie sichtbar ist Ihr Institut heute?',
 gal=f'''<section class="sec tight" style="padding-top:0" aria-labelledby="g-t"><div class="wrap">{head('Ihr Angebot, sichtbar gemacht','Jede Behandlung bekommt ihr Bild.','Laser, Gesichtsbehandlungen, Kosmetik: Kundinnen buchen, was sie verstehen. Darum zeigt Ihre Website jede Behandlung mit Bild, Ablauf und Termin-Knopf.','g-t')}{gallery([('laser-beine','Laser-Haarentfernung an den Beinen auf der Behandlungsliege','Zonen: Beine','center'),('laser-2','Laser-Haarentfernung am Arm einer Kundin mit Handstück','Zonen: Arme','center'),('facial','Kosmetikerin trägt eine Gesichtsmaske auf','Gesichtsbehandlung','center'),('device-face','Frau bei einer Lichtbehandlung im Gesicht mit einem modernen Gerät','Lichtbehandlung','center')],'Bildbeispiele Laser- und Kosmetikinstitut')}</div></section>''')

zg_page('lash-brow-nails-studios.html','Website mit Online-Buchung für Lash-, Brow- und Nail-Studios in Zürich · Seenery Agency',
 'Website mit Online-Buchung, Google-Profil und Bewertungs-System für Lash-, Brow-, Nagel- und Kosmetikstudios mit Team in der Region Zürich.',
 page_hero([('Lash-, Brow- & Nail-Studios',None)],'Für Studios mit Team','Ihre Arbeit ist wunderschön.','Ihre Agenda sollte voll sein.','Wimpern, Brauen, Nägel: Ihre Kundinnen lieben Ihre Arbeit. Neue Kundinnen sollen Sie finden und direkt online buchen, statt per DM zu fragen und zu warten.','lash','Lash-Stylistin setzt Wimpernverlängerungen bei einer liegenden Kundin','Symbolbild',pills=['Online-Buchung','Weniger DMs','Mehr Bewertungen']),
 split('Die Ausgangslage','Ausgebucht bei Stammkundinnen, unsichtbar für neue.',
   ['Viele Studios leben von Instagram und Empfehlungen. Termine laufen über DMs, Anrufe zwischen zwei Kundinnen und Nachrichten am Abend. Das kostet Zeit, und neue Kundinnen, die nicht warten wollen, buchen woanders.',
    'Mit einer eigenen Website, Online-Buchung rund um die Uhr und einem starken Google-Profil kommen Anfragen geordnet rein. Ihr Team kann sich auf die Arbeit konzentrieren.'],'nails','Nageldesignerin arbeitet an den Nägeln einer Kundin unter der Lampe',rev=True,hid='sit-t'),
 'Wonach Kundinnen suchen',
 ['Wimpernverlängerung Zürich','Lash Lifting Zürich','Brow Lamination Zürich','Nagelstudio in meiner Nähe','Gel Nägel Zürich','Augenbrauen Zürich','Wimpern auffüllen','Maniküre Zürich'],
 [('Online-Buchung rund um die Uhr','Kundinnen buchen um 23 Uhr auf dem Sofa, ohne DM.'),('Eine Seite pro Behandlung','Neuset, Auffüllen, Lifting, Gel und mehr.'),
  ('Team vorstellen','Jede Stylistin mit Schwerpunkt und Foto.'),('Google-Profil komplett','Leistungen, Fotos und Beiträge.'),
  ('Bewertungs-System','QR-Karte am Platz und Link nach dem Termin.'),('Instagram verbunden','Ihre besten Arbeiten auf der Website, gleiche Bilder, gleiche Sprache.'),
  ('Stammkundinnen zurückholen','Auf Wunsch später: Erinnerung an Kundinnen, die länger nicht da waren.'),('Monatsbericht','Buchungen, Aufrufe, Anrufe und Bewertungen.')],
 f'''<section class="sec" aria-labelledby="bk-t"><div class="wrap">{split_mock('Online-Buchung','Weniger Nachrichten, mehr gebuchte Termine.',['Kundinnen sehen freie Zeiten sofort und buchen selbst. Sie bekommen eine Bestätigung, Ihr Team eine geordnete Agenda.','Wenn Sie bereits Fresha, Treatwell oder ein anderes System nutzen, wird es eingebunden.'],MOCK_BOOKING,rev=True,hid='bk-t')}</div></section>''',
 [('Wir haben schon Fresha oder Treatwell. Passt das?','Ja. Ich binde Ihr System ein, damit Buchungen über Ihre eigene Website laufen.'),
  ('Wir sind ein kleines Team. Lohnt sich das?','Wenn Sie wachsen und neue Kundinnen gewinnen wollen, ja. Was genau sinnvoll ist, zeigt der kostenlose Check.'),
  ('Können Sie unsere Instagram-Bilder nutzen?','Bilder, die Sie selbst auf Instagram zeigen, nutze ich gerne mit Ihrem Einverständnis.')],
 'Studios','Wie sichtbar ist Ihr Studio heute?',
 gal=f'''<section class="sec tight" style="padding-top:0" aria-labelledby="g-t"><div class="wrap">{head('Ihre Arbeit im Mittelpunkt','Lashes, Brows, Nails. Und Ihr Team.','Kundinnen wählen ein Studio nach der Arbeit, die sie sehen. Darum bekommt jede Behandlung eine eigene Seite mit Ihren besten Bildern, und Ihr Team ein Gesicht.','g-t')}{gallery([('lbn-lashlift','Auge mit langen, geschwungenen Wimpern','Lashes','30% center'),('lbn-brow','Augenbrauen werden mit Fadentechnik geformt','Brows','center'),('lbn-nailart','Gepflegte Hände mit nudefarbener Maniküre','Nails','center'),('lbn-happy','Lächelnde Stylistin im Studio vor einem Spiegel','Ihr Team','70% center'),('lbn-salon','Helles, modernes Studio','Ihr Studio','center')],'Bildbeispiele Beauty-Studio')}</div></section>''')

# ================= WEBSITE-ARTEN =================
def wf(kind):
    if kind == 'pages': return '<div class="pg p1"></div><div class="pg p2"></div><div class="pg p3"></div>'
    if kind == 'one': return '<div class="wf"><div class="bar"><i></i><i></i><i></i></div><div class="blk h"></div><span class="btn-m"></span><div class="blk t"></div><div class="blk t2"></div><div class="row"><i></i><i></i><i></i></div></div>'
    if kind == 'hero': return '<div class="wf"><div class="bar"><i></i><i></i><i></i></div><div class="blk im" style="height:70px"></div><div class="blk t"></div><span class="btn-m"></span></div>'
    if kind == 'film': return '<div class="wf"><div class="bar"><i></i><i></i><i></i></div><div class="blk h" style="height:90px"></div></div><span class="play"></span>'
    if kind == 'up': return '<div class="wf" style="transform:rotate(-3deg) translateX(-8%)"><div class="bar"><i></i><i></i><i></i></div><div class="blk t"></div><div class="blk im"></div><div class="row"><i></i><i></i><i></i></div></div><div class="wf" style="position:absolute;width:52%;right:8%;bottom:14%"><div class="bar"><i></i><i></i><i></i></div><div class="blk h" style="height:24px"></div><span class="btn-m"></span></div>'
    return '<div class="wf" style="width:44%"><div class="bar"><i></i><i></i><i></i></div><div class="blk im" style="height:60px"></div><div class="blk t"></div><span class="btn-m" style="width:70%"></span></div>'
TYPES = [
 ('Signature','Multi-Page-Website','pages','Mehrere Seiten mit eigenem Menü, eine Seite pro Behandlung. Am stärksten für Google und ChatGPT.','Ästhetikpraxen und Institute'),
 ('First Look','Website mit bewegtem Einstieg','hero','Das erste Bild bewegt sich ganz ruhig, die Termin-Karte steht gleich daneben. Wirkt sofort hochwertig.','Praxen mit schönen Räumen'),
 ('Cinematic','Rundgang und Video','film','Ein Rundgang durch Ihre Räume beim Scrollen. Patientinnen fühlen sich schon vor dem Termin willkommen.','Premium-Praxen'),
 ('Essential','Booking-first One-Pager','one','Alles auf einer Seite, der Termin-Knopf ganz oben. Schnell online und klar.','Kleinere Teams, schneller Start'),
 ('Upgrade','Ihre Website, stärker','up','Ihre Website ist schön? Dann wird nicht neu gebaut, sondern sichtbar gemacht: Struktur, Google-Profil, Bewertungen und ChatGPT.','Praxen mit guter Basis'),
 ('Kampagne','Microsite','micro','Eine kleine Extra-Seite für eine Eröffnung oder einen neuen Standort, mit eigenem Link für Instagram und Werbung.','Eröffnungen, neue Standorte'),
]
types_html = '<div class="types">' + ''.join(f'<article class="type"><div class="vis" aria-hidden="true">{wf(k)}<span class="lbl">{l}</span></div><div class="tb"><h3>{n}</h3><p>{t}</p><span class="for">Ideal für: {f}</span></div></article>' for l,n,k,t,f in TYPES) + '</div>'
page('website-arten.html','Website-Arten für Praxen und Studios: welche passt zu Ihnen? · Seenery Agency',
 'Multi-Page-Website, bewegter Einstieg, Rundgang mit Video, Booking-first One-Pager, Upgrade oder Microsite: sechs Website-Arten für Praxen, Institute und Studios im Vergleich.',
 page_hero([('Website-Arten',None)],'Website-Arten','Welche Website passt','zu Ihrer Praxis?','Kein Baukasten. Jede Website bekommt ein eigenes Gesicht, gebaut aus Bausteinen, die sich bei anspruchsvollen Praxen bewährt haben. Hier sind die sechs Arten, aus denen wir gemeinsam wählen.','web-design','Handgezeichnete Website-Layouts in Aquarellfarben auf hellem Papier','Vom Entwurf zur fertigen Website',pills=['Sechs Arten','Eigenes Design','Für Google gebaut']) +
 f'''<section class="sec" style="padding-top:0" aria-labelledby="ty-t"><div class="wrap">{head('Die Auswahl','Sechs Arten, ein Ziel: mehr Termine.',None,'ty-t')}{types_html}
 <p class="mock-note" style="margin-top:26px">Welche Art zu Ihnen passt und was sie umfasst, besprechen wir persönlich.</p></div></section>
<section class="sec soft" aria-labelledby="wh-t"><div class="wrap">{head('Bei allen dabei','Was jede Website mitbringt.',None,'wh-t')}{checks([('Online-Termin','Ihr Buchungssystem sauber eingebunden.'),('Handy zuerst','Gestaltet für den Daumen.'),('Schnelle Ladezeit','Optimierte Bilder und schlanke Technik.'),('Gebaut für Google und ChatGPT','Struktur und Daten, die Maschinen lesen können.'),('Impressum und Datenschutz','Die Pflichtseiten gehören dazu.'),('Ihr Eigentum','Domain auf Ihren Namen, Nutzung von Design und Texten auch nach Vertragsende.')])}</div></section>''', crumbs_ld=[('Website-Arten','website-arten.html')])

# ================= ABLAUF =================
page('ablauf.html','Ablauf: vom Gratis-Check zur fertigen Website · Seenery Agency',
 'So läuft die Zusammenarbeit mit Seenery Agency: Sichtbarkeits-Check, Gespräch, Entwurf nach wenigen Tagen, Livegang und monatliche Betreuung mit Bericht.',
 page_hero([('Ablauf',None)],'Ablauf','Klare Schritte.','Wenig Aufwand für Sie.','Vom ersten Check bis zum Monatsbericht wissen Sie immer, wo wir stehen und was als Nächstes kommt. Ihr Aufwand: am Anfang ein bis zwei Stunden, danach kurze Freigaben.','ablauf','Leeres Notizbuch mit Stift und Kaffeebecher auf einem Holzbrett','Gut geplant ist halb gewonnen',pills=['Check','Gespräch','Entwurf','Live','Monatlich']) +
 f'''<section class="sec" style="padding-top:0" aria-labelledby="tl-t"><div class="wrap narrow" style="max-width:900px">{head('Schritt für Schritt','So arbeiten wir zusammen.',None,'tl-t',center=False)}
<ol class="tl">
  <li><div><h3>Gratis Sichtbarkeits-Check</h3><p>Ich prüfe, wie Ihre Praxis heute bei Google, in Google Maps und in ChatGPT erscheint, und schaue mir Ihre Website auf dem Handy an. Mit Screenshots als Ausgangswert.</p><span class="you">Ihr Aufwand: Formular ausfüllen, 2 Minuten</span></div></li>
  <li><div><h3>Gespräch</h3><p>Wir besprechen das Ergebnis, Ihre Ziele und welche Behandlungen mehr gefunden werden sollen. Danach bekommen Sie ein klares Angebot.</p><span class="you">Ihr Aufwand: etwa 30 bis 45 Minuten</span></div></li>
  <li><div><h3>Entwurf</h3><p>Sie sehen Ihren Entwurf nach wenigen Tagen. Ihre Wünsche fliessen direkt ein, bis alles passt.</p><span class="you">Ihr Aufwand: Fotos, Infos und Feedback</span></div></li>
  <li><div><h3>Livegang</h3><p>Website und Google-Profil gehen online, in der Regel innert 14 Arbeitstagen ab vollständigen Unterlagen. Bewertungs-System und Monatsbericht werden eingerichtet.</p><span class="you">Ihr Aufwand: Freigabe</span></div></li>
  <li><div><h3>Jeden Monat</h3><p>Google-Beiträge, Bewertungen, Pflege, ChatGPT-Test und ein Monatsbericht, der direkt an Sie geht.</p><span class="you">Ihr Aufwand: Bericht lesen, kurze Freigaben</span></div></li>
</ol></div></section>
<section class="sec soft" aria-labelledby="nd-t"><div class="wrap">{head('Was ich von Ihnen brauche','Damit es schnell geht.',None,'nd-t')}{checks([('Fotos','Von Räumen, Team und Ihnen. Fehlt etwas, sage ich Ihnen, welche Bilder es braucht.'),('Zugang zum Google-Profil','Als Verwalter, jederzeit entziehbar.'),('Domain und Hosting','Zugang oder Auftrag zur Übernahme.'),('Buchungssystem','Link oder Zugang zu OneDoc, Fresha, Shore oder Ihrem System.'),('Ihre Behandlungen','Liste mit den wichtigsten Infos. Die Texte schreibe ich.'),('Fachliche Freigabe','Bevor etwas online geht.')])}</div></section>''', crumbs_ld=[('Ablauf','ablauf.html')])

# ================= FAQ =================
FAQ_GROUPS = [
 ('Allgemein',[
  ('Gibt es Ranking-Garantien?','Nein. Eine gute Platzierung ist das Ziel, kein Versprechen. Das kann ehrlicherweise niemand garantieren. Dafür sehen Sie jeden Monat klare Zahlen.'),
  ('Was kostet das?','Das hängt davon ab, was Ihre Praxis braucht: neue Website oder Upgrade, wie viele Behandlungen, wie viel laufende Betreuung. Nach dem kostenlosen Check bekommen Sie ein klares Angebot.'),
  ('Für wen ist Seenery gedacht?','Für Ästhetikpraxen, Laser- und Kosmetikinstitute und Beauty-Studios mit Team, die mehr neue Kundinnen und Kunden gewinnen wollen. Der Schwerpunkt liegt in der Region Zürich, gearbeitet wird für die ganze Schweiz.'),
  ('Mit wem arbeite ich zusammen?','Immer direkt mit mir, James Alves Da Silva. Kein Ticket-System und keine wechselnden Projektleiter.')]),
 ('Website',[
  ('Wie schnell geht das?','Ihren ersten Entwurf sehen Sie nach wenigen Tagen. Online ist die Website in der Regel innert 14 Arbeitstagen, sobald Fotos, Texte, Freigaben und Zugänge vollständig da sind.'),
  ('Wir haben schon eine Website. Brauchen wir eine neue?','Nicht unbedingt. Hat Ihre Website eine gute Basis, machen wir ein Upgrade und konzentrieren uns auf Google, Bewertungen und ChatGPT.'),
  ('Gehören uns Domain, Website und Google-Profil?','Ja. Domain und Google-Profil laufen auf Ihren Namen. Design und Texte Ihrer Website dürfen Sie nach Bezahlung des Setups auch nach Vertragsende unbeschränkt nutzen.')]),
 ('Google und ChatGPT',[
  ('Was ist der Unterschied zwischen SEO und GEO?','SEO bedeutet: bei Google gefunden werden. GEO bedeutet: von KI-Assistenten wie ChatGPT verstanden und genannt werden. Ich arbeite an beidem.'),
  ('Wann sieht man Ergebnisse?','Erste Veränderungen können sich nach einigen Wochen zeigen. Gute Platzierungen bei Google brauchen meist mehrere Monate.'),
  ('Dürfen wir um Bewertungen bitten?','Ja, freundlich und ohne Gegenleistung. Belohnungen für Bewertungen sind bei Google nicht erlaubt.')]),
 ('Zusammenarbeit',[
  ('Wie viel Zeit braucht das von uns?','Am Anfang etwa ein bis zwei Stunden für Fotos, Freigaben und Zugänge. Danach übernehme ich die laufende Arbeit.'),
  ('Kommen Sie auch vorbei?','Ja, in der Region Zürich gerne persönlich. In der übrigen Schweiz per Video und Telefon.'),
  ('Was passiert nach dem Gratis-Check?','Sie bekommen sofort eine Bestätigung per E-Mail. Innert zwei Werktagen rufe ich Sie an und wir besprechen das Ergebnis, ohne Verkaufsdruck.')]),
]
faq_html = ''.join(f'<p class="faq-grp">{g}</p>' + faq(items) for g,items in FAQ_GROUPS)
page('faq.html','Häufige Fragen zu Website, Google und ChatGPT · Seenery Agency',
 'Antworten auf häufige Fragen: Ranking-Garantien, Kosten, Dauer, Eigentum an Website und Google-Profil, SEO und GEO, Bewertungen und Zusammenarbeit.',
 page_hero([('Häufige Fragen',None)],'Häufige Fragen','Ehrliche Antworten','auf gute Fragen.','Was Praxen und Studios mich am häufigsten fragen. Ihre Frage ist nicht dabei? Rufen Sie mich an oder schreiben Sie mir.','faq','Rosafarbene Pflegeprodukte und ein Pinsel auf hellem Untergrund','Symbolbild',btns=False) +
 f'<section class="sec" style="padding-top:0" aria-label="Fragen und Antworten"><div class="wrap"><div style="max-width:860px;margin:0 auto">{faq_html}</div></div></section>', crumbs_ld=[('Häufige Fragen','faq.html')])

# ================= ÜBER MICH =================
portrait = '<figure class="portrait"><span class="ini" aria-hidden="true">JA</span><figcaption><b>James Alves Da Silva</b>Gründer · Dübendorf<br><small>Porträt folgt</small></figcaption></figure>'
page('ueber-mich.html','Über mich · James Alves Da Silva · Seenery Agency',
 'James Alves Da Silva, Gründer von Seenery Agency in Dübendorf: ein fester Ansprechpartner für Website, Google-Profil, Bewertungen und Sichtbarkeit in ChatGPT.',
 page_hero([('Über mich',None)],'Über mich','Ein Ansprechpartner.','Kein Agentur-Apparat.','Ich bin James Alves Da Silva, Gründer von Seenery Agency in Dübendorf. Ich arbeite mit Praxen und Studios, die nicht lauter, sondern besser gefunden werden wollen.',None,None,fig=portrait) +
 f'''<section class="sec" style="padding-top:0" aria-labelledby="st-t"><div class="wrap narrow" style="max-width:820px">
  <p class="eyebrow">Meine Geschichte</p><h2 id="st-t">Warum es Seenery gibt.</h2>
  <div style="margin-top:22px;color:var(--muted);font-size:18px"><p>Ich habe Menschen als Personal Trainer begleitet und dabei gemerkt, was mich antreibt: anderen zu helfen, ihr Bestes zu zeigen. Heute mache ich das für Praxen und Studios in der Region Zürich.</p>
  <p>Gelernt habe ich Industriemechanik, danach habe ich im Verkauf gearbeitet. Daher kommt mein Anspruch an Präzision, und ich weiss, dass gutes Zuhören jedem Verkauf vorausgeht.</p>
  <p>Ich baue selbst ein Unternehmen auf und weiss, wie sich Wachstum anfühlt. Genau das wünsche ich mir für meine Kundinnen: mehr Menschen, die ihre Arbeit erleben, ein Team, das wachsen kann, und eine Agenda, die Wochen im Voraus gefüllt ist.</p></div>
  <blockquote class="quote"><p>«Wenn eine Praxis wächst, wächst ihr Team, und mehr Menschen finden zu der Behandlung, die sie suchen.»</p><cite>James Alves Da Silva</cite></blockquote>
</div></section>
<section class="sec soft" aria-labelledby="hw-t"><div class="wrap">{head('Wie ich arbeite','Drei Dinge, auf die Sie zählen können.',None,'hw-t')}
<div class="grid3">
  <div class="card text"><div class="cb"><span class="num">Ehrlich</span><h3>Klare Zahlen statt Garantien</h3><p>Keine Ranking-Garantien. Dafür jeden Monat ein Bericht und offene Worte, wenn etwas nicht funktioniert.</p></div></div>
  <div class="card text"><div class="cb"><span class="num">Schnell</span><h3>Entwurf in Tagen</h3><p>Dank bewährter Bausteine sehen Sie Ihren Entwurf nach wenigen Tagen.</p></div></div>
  <div class="card text"><div class="cb"><span class="num">Persönlich</span><h3>Direkt erreichbar</h3><p>Sie sprechen immer mit mir. Per Telefon, Mail oder persönlich bei Ihnen in der Praxis.</p></div></div>
</div></div></section>
<section class="sec" aria-labelledby="fa-t"><div class="wrap">{head('Kurz und knapp','Seenery in Stichworten.',None,'fa-t')}
<div class="facts"><div class="fact"><b>Dübendorf</b><span>Sitz, nahe Zürich</span></div><div class="fact"><b>Ganze Schweiz</b><span>Region Zürich auch persönlich vor Ort</span></div><div class="fact"><b>1 Ansprechpartner</b><span>Von Check bis Bericht</span></div><div class="fact"><b>Deutsch &amp; Englisch</b><span>Websites auf Wunsch zweisprachig</span></div></div></div></section>''', crumbs_ld=[('Über mich','ueber-mich.html')])

# ================= CHECK & KONTAKT =================
def form(h='Check anfragen', sub='Dauert 2 Minuten. Sie erhalten sofort eine Bestätigung per E-Mail.'):
    return f'''<form class="form" name="sichtbarkeits-check" method="POST" action="/danke.html" data-netlify="true" netlify-honeypot="firma-website" data-check-form>
  <h2 style="font-size:30px">{h}</h2><p class="sub">{sub}</p>
  <input type="hidden" name="form-name" value="sichtbarkeits-check">
  <p class="hp" aria-hidden="true"><label>Bitte leer lassen<input name="firma-website" tabindex="-1" autocomplete="off"></label></p>
  <div class="field"><label for="f-name">Vorname und Name <span class="req" aria-hidden="true">*</span></label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
  <div class="field"><label for="f-studio">Praxis / Institut / Studio <span class="req" aria-hidden="true">*</span></label><input id="f-studio" name="studio" type="text" autocomplete="organization" required></div>
  <div class="row2">
    <div class="field"><label for="f-ort">Ort <span class="req" aria-hidden="true">*</span></label><input id="f-ort" name="ort" type="text" autocomplete="address-level2" required></div>
    <div class="field"><label for="f-telefon">Telefon <span class="req" aria-hidden="true">*</span></label><input id="f-telefon" name="telefon" type="tel" autocomplete="tel" inputmode="tel" required></div>
  </div>
  <div class="field"><label for="f-email">E-Mail <span class="req" aria-hidden="true">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required></div>
  <div class="field"><label for="f-profil">Website oder Google-Profil <span class="opt">(optional)</span></label><input id="f-profil" name="profil" type="text"></div>
  <p class="consent">* Pflichtfelder. Mit dem Absenden sind Sie einverstanden, dass ich Ihre Angaben für den Check und die Kontaktaufnahme nutze. Mehr in der <a href="datenschutz.html">Datenschutzerklärung</a>.</p>
  <button class="btn btn-deep" type="submit">Kostenlosen Check anfragen <span aria-hidden="true">→</span></button>
  <p class="form-msg" role="status" aria-live="polite"></p>
</form>'''

page('sichtbarkeits-check.html','Gratis Sichtbarkeits-Check für Praxen und Studios in Zürich · Seenery Agency',
 'Kostenloser Sichtbarkeits-Check: Wie erscheint Ihre Praxis bei Google, in Google Maps und in ChatGPT? Mit Screenshots, persönlich besprochen. Für Praxen und Studios in der Region Zürich.',
 f'''<section class="phero" aria-labelledby="h1"><div class="wrap">{crumbs([('Sichtbarkeits-Check',None)])}
<div class="form-wrap">
  <div>
    <p class="eyebrow">Gratis Sichtbarkeits-Check</p><h1 id="h1">Wie sichtbar ist Ihre Praxis heute?</h1>
    <p class="lead">Ich prüfe, wie Ihre Praxis bei Google, in Google Maps und in ChatGPT erscheint, und zeige Ihnen das Ergebnis persönlich. Kostenlos und unverbindlich.</p>
    <ul class="ok-list">
      <li>Google-Suche für Ihre wichtigsten Behandlungen</li>
      <li>Ihr Google-Profil im Vergleich zu Praxen in der Nähe</li>
      <li>Der ChatGPT-Test: werden Sie genannt?</li>
      <li>Ihre Website auf dem Handy: Ladezeit und Weg zum Termin</li>
      <li>Bewertungen: Anzahl, Schnitt und Antworten</li>
    </ul>
    <figure class="check-fig"><img src="img/kontakt.webp" alt="Laptop, Notizblock, Smartphone und Kaffeetasse auf einem Holztisch" width="1600" height="1067"></figure>
  </div>
  {form()}
</div></div></section>
<section class="sec soft" aria-labelledby="af-t"><div class="wrap">{head('Was danach passiert','Ohne Verkaufsdruck.',None,'af-t')}
<ol class="steps s3"><li><h3>Sofort</h3><p>Sie bekommen eine Bestätigung per E-Mail.</p></li><li><h3>Innert zwei Werktagen</h3><p>Ich rufe Sie an und wir vereinbaren einen Termin.</p></li><li><h3>Im Gespräch</h3><p>Sie sehen das Ergebnis mit Screenshots und entscheiden in Ruhe.</p></li></ol>
</div></section>''', 'nocta', crumbs_ld=[('Sichtbarkeits-Check','sichtbarkeits-check.html')])

page('kontakt.html','Kontakt · Seenery Agency · Dübendorf, Region Zürich',
 'Kontakt zu Seenery Agency: James Alves Da Silva, Dübendorf. Telefon 076 339 13 98, info@seenery.ch. Persönlich in der Region Zürich.',
 f'''<section class="phero" aria-labelledby="h1"><div class="wrap">{crumbs([('Kontakt',None)])}
<div class="form-wrap">
  <div>
    <p class="eyebrow">Kontakt</p><h1 id="h1">Reden wir über Ihre Praxis.</h1>
    <p class="lead">Rufen Sie an, schreiben Sie mir oder fordern Sie direkt den kostenlosen Check an. Ich melde mich innert zwei Werktagen.</p>
    <div class="contact-cards">
      <a href="tel:+41763391398"><span class="ic" aria-hidden="true">☎</span><span><small>Telefon</small><b>076 339 13 98</b></span></a>
      <a href="mailto:info@seenery.ch"><span class="ic" aria-hidden="true">@</span><span><small>E-Mail</small><b>info@seenery.ch</b></span></a>
      <div><span class="ic" aria-hidden="true">⌂</span><span><small>Sitz</small><b>Dübendorf, Region Zürich</b><small>Termine gerne bei Ihnen vor Ort</small></span></div>
      <a href="https://www.instagram.com/seenery.agency/" rel="noopener" target="_blank"><span class="ic" aria-hidden="true">◎</span><span><small>Instagram</small><b>@seenery.agency</b></span></a>
    </div>
  </div>
  {form('Nachricht und Check','Am schnellsten über den Gratis-Check. Sie erhalten sofort eine Bestätigung per E-Mail.')}
</div></div></section>''', 'nocta', crumbs_ld=[('Kontakt','kontakt.html')])

import legal; legal.add(PAGES)
PAGES['404.html']=('Seite nicht gefunden · Seenery Agency','Diese Seite gibt es nicht.','404.html',legal.simple('Fehler 404','Diese Seite gibt es nicht.','<p class="lead" style="margin-top:0">Vielleicht hat sich die Adresse geändert. Hier geht es weiter:</p><div class="btns"><a class="btn btn-deep" href="index.html">Zur Startseite</a><a class="btn btn-line" href="leistungen.html">Leistungen</a><a class="btn btn-line" href="sichtbarkeits-check.html">Gratis-Check</a></div>'),'nocta')
for k in ('impressum.html','datenschutz.html','danke.html','404.html'):
    t,d,_,m,_c = PAGES[k]
    PAGES[k] = dict(title=t, desc=d, main=m, cta='nocta', crumbs=None)

# ---------------- Dokument ----------------
def jsonld(file, p):
    data = []
    if file == 'index.html':
        data.append({"@context":"https://schema.org","@type":"ProfessionalService","name":"Seenery Agency","url":"https://seenery.ch/","email":"info@seenery.ch","telephone":"+41763391398",
          "address":{"@type":"PostalAddress","streetAddress":"Meisenweg 12","postalCode":"8600","addressLocality":"Dübendorf","addressCountry":"CH"},
          "areaServed":"Region Zürich","founder":{"@type":"Person","name":"James Alves Da Silva"},"sameAs":["https://www.instagram.com/seenery.agency/"]})
        data.append({"@context":"https://schema.org","@type":"WebSite","name":"Seenery Agency","url":"https://seenery.ch/"})
    elif p.get('crumbs'):
        items = [{"@type":"ListItem","position":1,"name":"Start","item":"https://seenery.ch/"}]
        for i,(n,h) in enumerate(p['crumbs']):
            items.append({"@type":"ListItem","position":i+2,"name":n,"item":"https://seenery.ch/"+h})
        data.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items})
    return ''.join(f'<script type="application/ld+json">{json.dumps(d,ensure_ascii=False)}</script>' for d in data)

THEME_INIT = "<script>var t='b';try{var s=localStorage.getItem('seenery-theme');if(s==='c')t='c';}catch(e){}var q=(location.search.match(/[?&]t=([bc])/)||[])[1];if(q)t=q;document.documentElement.setAttribute('data-theme',t);</script>"
SWITCH = ('<div class="theme-sw" role="group" aria-label="Farbwelt wählen (nur Vorschau)"><span>Farbwelt wählen</span>'
  '<button type="button" data-t="b"><i style="background:conic-gradient(#0a1220 0 50%,#0a0a0a 0 75%,#d7efff 0)"></i><span style="all:unset">B · Marine Nacht<small>dunkler Hero, Blacktop &amp; Fusion, Gold</small></span></button>'
  '<button type="button" data-t="c"><i style="background:conic-gradient(#13223a 0 50%,#0a0a0a 0 75%,#d7efff 0)"></i><span style="all:unset">C · Marine &amp; Perle<small>hell, kühl, Blacktop &amp; Fusion</small></span></button>'
  '<button type="button" class="x" aria-label="Umschalter einklappen">×</button><button type="button" class="open-sw">Farbwelt</button></div>')

def doc(file, p):
    ct = p.get('cta')
    body = f'''{header(file)}
<main id="inhalt">
{p['main']}
{'' if ct=='nocta' else cta(ct) if ct else cta()}
</main>
{footer()}'''
    hc = f'''<meta name="description" content="{esc(p['desc'])}">
<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_CH">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{GF}
<link rel="stylesheet" href="site.css">
{jsonld(file,p)}'''
    sw = SWITCH if MODE == 'artifact' else ''
    ti = THEME_INIT if MODE == 'artifact' else ''
    if MODE == 'artifact' and file == 'index.html':
        return f'''<meta charset="utf-8">
<title>Seenery Website v3</title>
<meta name="claude:viewport-fit-sides" content="cover">
{ti}
{hc}
{body}
{sw}
<script src="site.js"></script>
'''
    canon = 'https://seenery.ch/' + ('' if file == 'index.html' else file)
    robots = '<meta name="robots" content="noindex">' if file in ('danke.html','404.html') else ''
    return f'''<!doctype html>
<html lang="de-CH" data-theme="{'c' if MODE=='repo' else 'b'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{p['title']}</title>
<link rel="canonical" href="{canon}">
{robots}{ti}
{hc}
</head>
<body>
{body}
{sw}
<script src="site.js"></script>
</body>
</html>
'''

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT,'img'))
for f,p in PAGES.items():
    open(os.path.join(OUT,f),'w').write(doc(f,p))
open(os.path.join(OUT,'site.css'),'w').write(FONTS + '\n' + open('site.css').read())
shutil.copy('site.js', os.path.join(OUT,'site.js'))
for im in os.listdir('img'):
    if im.endswith('.webp') and im not in ('aesth.webp','aesth-hero.webp','arten.webp','c-room1.webp','c-room2.webp','hero-skin.webp','opt-a.webp','opt-b.webp','opt-c.webp','opt-d.webp','lm1.webp','lm2.webp','lm3.webp','chatgpt.webp','serum.webp','opt-b.webp','laser-3.webp','laser-4.webp','laser-5.webp'): shutil.copy(os.path.join('img',im), os.path.join(OUT,'img',im))
shutil.copy('/home/claude/site2/out/favicon.svg', os.path.join(OUT,'favicon.svg'))
urls = ''.join(f'<url><loc>https://seenery.ch/{"" if f=="index.html" else f}</loc></url>' for f in PAGES if f not in ('danke.html','404.html'))
open(os.path.join(OUT,'sitemap.xml'),'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
open(os.path.join(OUT,'robots.txt'),'w').write('User-agent: *\nAllow: /\nSitemap: https://seenery.ch/sitemap.xml\n')
print(MODE, len(PAGES), 'Seiten')
