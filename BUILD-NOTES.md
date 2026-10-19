# Build-Notes – Seenery Agency (16.10.2026)

- 16.10.2026: Rebrand von «Glow & Grow» auf **Seenery Agency**. Landingpage = gleicher Stand wie der Claude-Spiegel (claude.ai Artifact «Seenery Agency») und Claude Design.
- Wortmarke A5 (SEENERY + Funke, AGENCY) in Kopfzeile und Footer, Favicon A1-a (Runde 5).
- Kontakt: info@seenery.ch · 076 339 13 98 · Instagram @seenery.agency
- Regel: Jede Code-Änderung wird gleichzeitig hier (GitHub → Netlify), im Claude-Spiegel und als Datei für Claude Design aktualisiert.

## Offen
- Domain seenery.ch mit Netlify verbinden (DNS bei Hostpoint)
- noindex entfernen, sobald die Seite offiziell live geht
- Impressum/Datenschutz: Anwalt-Prüfung nach den Piloten

## 19.10.2026
- Impressum, Datenschutz, Danke auf Startseiten-Design: Playfair Display + GG Sans (eingebettet in styles.css), Wortmarke-Header, gleicher Footer. Alte Schriften Cormorant/Lora entfernt. Generator: `_werkzeuge/unterseiten_angleichen.py`
- Formular: Danke-Seite als Ziel (`action="/danke.html"`), auf seenery.ch wird jetzt wirklich an Netlify Forms gesendet (vorher nur auf *.netlify.app)
- Canonical-Tags auf Impressum/Datenschutz
