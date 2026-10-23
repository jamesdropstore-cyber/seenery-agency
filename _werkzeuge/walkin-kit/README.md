# Seenery Walk-in-Kit – Kinoflug durch ein Lokal/Studio, vom Scrollen gesteuert

Referenz: The Smash Burger Bear, Dübendorf (Demo V16, 23.10.2026).
Ergebnis: Ein durchgehender Film ohne Schnitt (Arkade → Tür → Raum → Highlight → Theke/Behandlungsplatz).
Scrollen steuert den Film vor und zurück. Handy und Desktop. Am Schluss gibt es ein Finale (z. B. Produkte fallen auf den Tresen).

## Goldene Regeln (James, 22./23.10.)
1. **Handy-Videos der Kundin NIE auf die Website.** Sie sind nur der Grundriss: Wege, Abstände, wo was steht.
2. **Grundriss zuerst schriftlich festhalten**, bevor irgendetwas generiert wird: Was ist hinter der Tür? Wohin geht man (links/rechts)? Welche Wand kommt nach welcher? Wo stehen Möbel, und wie sind sie ausgerichtet? Wo darf man NICHT hin (Küche, Personal)?
3. **Durch Fenster und Türen sieht man nur den echten Raum.** Kein zweites Lokal, keine Theke, kein Kühlschrank, wo keiner ist.
4. **Zwei Schlüsselbilder dürfen nicht mehr als ca. 90° auseinanderliegen.** Sonst erfindet die KI Räume dazwischen. Darum ein Übergangsdetail ins Bild nehmen (z. B. die Lamellen-Ecke).
5. Endbild von Clip n = Startbild von Clip n+1 (gleiche Higgsfield-ID) → ohne Schnitt.
6. Jede Prompt-Zeile endet mit Verboten: «no people, no text, no windows/doors/rooms that are not there».

## Ablauf (ca. 60–80 Higgsfield-Credits pro Betrieb)
1. **Video der Kundin anschauen** → Grundriss als Liste schreiben (Regel 2) und von James bestätigen lassen.
2. **Schlüsselbilder** (gpt_image_2_5, 16:9, quality high, 2k, ca. 2.75 Credits). Referenz 1 = Standbild aus dem Video (Grundriss), Referenz 2 = bereits generiertes Bild (Licht/Look). Typische Folge:
   K0 aussen, ein paar Schritte vor der Tür · K1 Tür offen von aussen (dahinter nur, was wirklich da ist) · K2 erster Blick drinnen · K3 Highlight-Wand · K4 Theke/Empfang (Preistafel lesbar) · K5 Nahaufnahme Tresen/Liege, leer.
3. **Clips** (minimax_h3, 5 s, 2K, 10 Credits). Start = K(n), Ende = K(n+1). Max. 3 gleichzeitig (sonst 429). Wenn ein Preset «IN THE DARK» vorgeschlagen wird → `declined_preset_id` mitsenden.
   Prompt-Muster: «One continuous smooth gimbal shot, no cuts, first-person eye level, slow constant speed. [Bewegung]. [Was man sieht]. [Verbote]. Photorealistic, cinematic.»
4. **Prüfen:** Kontaktbogen pro Clip (`ffmpeg -vf "select='not(mod(n\,12))',scale=400:-1,tile=4x3"`). Jede erfundene Stelle → nur diesen Clip neu machen.
5. **Frames:** `python3 frames.py <clips-ordner> w d0a.mp4 d0b.mp4 …` → gibt Anzahl + Grenzen aus.
6. **tour.json** füllen (siehe Beispiel):
   - `TM` = [Scroll-Einheit, Position im Film 0–1]. Gesamt 7 Einheiten. Clip-Grenzen auf Kapitel legen, ein Halt (gleiche Position zweimal) für die Preistafel.
   - `FX` = Bildausschnitt am Handy (0 = links, 1 = rechts), dorthin, wo das Wichtige ist.
   - `CH` = Startpunkte der 6 Kapitel-Knöpfe. `CAPW` = Ein-/Ausblendfenster der 6 Texte. `HOLD` = Fenster der Menü-/Preiskarte.
7. **Bauen:** `engine.js` ins Template (Platzhalter `/*ENGINE*/`), `build.py` setzt NF/TM/FX/CH/CAPW/HOLD ein und bettet die kleinen Bilder als CSS-Variablen ein.
8. **Testen:** Playwright-Screenshots 390×844 und 1366×800 an 12–15 Scroll-Punkten → Kontaktbogen ansehen.
9. **Veröffentlichen** als Artifact: Seite + `w/*.webp` über `files`. Max. 255 Dateien pro Publish, 511 pro Version → alte Frames per `null` entfernen und in 2–3 Publishes hochladen.

## Technik (engine.js)
- Canvas zeichnet Frame `w/NNN.webp` je nach Scroll und überblendet weich zum nächsten Frame.
- Laden: erst jedes 8. Bild, dann jedes 2., dann alle → läuft sofort. Ladebalken oben rechts.
- Lenis (CDN `lenis@1.1.13`) für weiches Scrollen, mit Rückfall falls es nicht lädt.
- `prefers-reduced-motion`: alles als ruhige Bildfolge.
- Desktop = 16:9 füllend. Handy = Ausschnitt nach `FX`.

## Upload-Weg zu Higgsfield (Proxy blockiert direkten Upload)
Standbilder in den Branch `tmp-frames-bear` von seenery-agency pushen (Commit mit «[skip netlify]») → `media_import_url` mit raw.githubusercontent.com → danach die Dateien wieder löschen.
