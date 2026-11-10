# Rechtliches und Danke (wird von build.py eingebunden)
def simple(eyebrow, h1, inner):
    return (f'<section class="phero" aria-labelledby="h1"><div class="wrap narrow" style="padding-top:clamp(24px,5vw,64px)"><p class="eyebrow">{eyebrow}</p><h1 id="h1">{h1}</h1></div></section>\n'
            f'<section class="sec" style="padding-top:0"><div class="wrap narrow legal">{inner}</div></section>')

IMPRESSUM = """
<h2>Betreiber</h2><p>Seenery Agency by James Alves Da Silva<br>Meisenweg 12<br>8600 Dübendorf<br>Schweiz</p>
<h2>Kontakt</h2><p>E-Mail: <a href="mailto:info@seenery.ch">info@seenery.ch</a><br>Telefon: <a href="tel:+41763391398">076 339 13 98</a><br>Instagram: <a href="https://www.instagram.com/seenery.agency/" rel="noopener" target="_blank">@seenery.agency</a></p>
<h2>Haftung</h2><p>Die Inhalte dieser Website wurden sorgfältig erstellt. Für Richtigkeit, Vollständigkeit und Aktualität wird keine Gewähr übernommen. Für Inhalte verlinkter Websites sind ausschliesslich deren Betreiber verantwortlich.</p>
<h2>Bilder</h2><p>Die Bilder auf dieser Website sind Symbolbilder von Unsplash (Unsplash-Lizenz) und zeigen keine Kundenprojekte. Dargestellte Profile, Bewertungen und Antworten sind fiktive Beispiele.</p>"""

DATENSCHUTZ = """
<h2>Verantwortlich</h2><p>Seenery Agency by James Alves Da Silva, Meisenweg 12, 8600 Dübendorf, Schweiz. E-Mail: <a href="mailto:info@seenery.ch">info@seenery.ch</a>.</p>
<h2>Welche Daten ich bearbeite</h2><p>Wenn Sie das Formular für den Sichtbarkeits-Check ausfüllen, bearbeite ich Ihren Namen, den Namen Ihrer Praxis, Ihres Instituts oder Studios, den Ort, Ihre Telefonnummer, Ihre E-Mail-Adresse und, falls angegeben, Ihre Website oder Ihr Google-Profil.</p>
<h2>Wofür</h2><p>Ich nutze diese Angaben nur, um den Sichtbarkeits-Check zu erstellen, Ihnen eine Bestätigung per E-Mail zu senden und Sie dazu zu kontaktieren. Ich verkaufe keine Daten und gebe sie nicht für Werbezwecke an Dritte weiter.</p>
<h2>Hosting und Formular</h2><p>Diese Website wird bei Netlify, Inc. (USA) gehostet. Die Formular-Angaben werden dort gespeichert. Beim Aufruf der Website verarbeitet Netlify technische Daten wie Ihre IP-Adresse, um die Seite auszuliefern.</p>
<h2>Bestätigungs-Mail und Anfragen-Liste</h2><p>Nach dem Absenden werden Ihre Angaben über den Automationsdienst Make (Make.com) weitergeleitet. Damit wird Ihnen automatisch eine Bestätigung von meiner E-Mail-Adresse gesendet (Google Workspace, Google LLC, USA) und Ihre Anfrage in einer internen Liste in Google Sheets gespeichert.</p>
<h2>Schriften</h2><p>Diese Website lädt Schriften von Google Fonts (Google LLC, USA). Dabei wird Ihre IP-Adresse an Google übermittelt.</p>
<h2>Aufbewahrung</h2><p>Ich lösche Ihre Angaben, sobald sie für den Check und die Kontaktaufnahme nicht mehr nötig sind, ausser es entsteht eine Zusammenarbeit oder eine gesetzliche Aufbewahrungspflicht.</p>
<h2>Ihre Rechte</h2><p>Sie können jederzeit Auskunft über Ihre Daten verlangen, sie berichtigen oder löschen lassen. Schreiben Sie mir dazu an <a href="mailto:info@seenery.ch">info@seenery.ch</a>.</p>
<p>Stand: November 2026</p>"""

DANKE = """
<p class="lead" style="margin-top:0">Ihre Anfrage ist angekommen. Eine Bestätigung ist bereits per E-Mail zu Ihnen unterwegs.</p>
<p style="margin-top:18px">Ich schaue mir Ihre Praxis bei Google, ChatGPT und auf Ihrer Website an und rufe Sie innert zwei Werktagen an. Falls Sie die Bestätigung nicht finden, sehen Sie bitte kurz im Spam-Ordner nach.</p>
<div class="btns"><a class="btn btn-deep" href="index.html">Zurück zur Startseite</a><a class="btn btn-line" href="sichtbar-in-chatgpt.html#test">Den 30-Sekunden-Test machen</a></div>"""

def add(PAGES):
    PAGES['impressum.html'] = ('Impressum · Seenery Agency','Impressum von Seenery Agency, James Alves Da Silva, Dübendorf.','impressum.html', simple('Rechtliches','Impressum',IMPRESSUM), 'nocta')
    PAGES['datenschutz.html'] = ('Datenschutzerklärung · Seenery Agency','Datenschutzerklärung von Seenery Agency, Dübendorf.','datenschutz.html', simple('Rechtliches','Datenschutzerklärung',DATENSCHUTZ), 'nocta')
    PAGES['danke.html'] = ('Danke · Seenery Agency','Danke für Ihre Anfrage.','danke.html', simple('Anfrage erhalten','Herzlichen Dank.',DANKE), 'nocta')
