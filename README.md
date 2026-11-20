# Landing Fish Atelier — v5 "Carta"

## Aprire la pagina
Doppio clic su `index.html`. In locale funziona tutto tranne l'invio del form, che funziona solo online. Netlify pubblica il sito dal repo GitHub a ogni push (`netlify.toml` copia solo `index.html`, `assets/` e `_headers`).

## Struttura
```
index.html                    generato da tools/genera-index.py
assets/css/style.css          token in :root (colore, scala, spazi, raggi, ombre, motion)
assets/css/incisioni.css      i disegni come maschere incorporate (generato)
assets/js/main.bundle.js      build di src/main.js
assets/img/pack-finestre*.webp il fronte della busta con le finestre trasparenti
assets/img/incisioni/         disegni degli ingredienti, colorati via CSS mask
assets/fonts/                 Instrument Serif tondo e corsivo — OFL
assets/img/foto/              foto approvate (paccheri, tagliolini) in due larghezze
assets/img/decori/            polpi ad acquerello (materiali approvati) e gambero ad acquerello (gambero-acquerello.webp, disegnato da tools/gambero-acquerello/)
src/main.js                   oblò, contatori, palco, nastro, scheda, form
tools/genera-index.py         le 17 referenze in una lista: si cambia lì e si rigenera
tools/genera-incisioni.py     rigenera incisioni.css se cambi o aggiungi un disegno
```

## Modificare
```
npm install
npm run build                  # ricompila main.bundle.js
python3 tools/genera-index.py  # rigenera index.html dalle referenze
```

## Dove intervenire
- **Foto:** la hero usa i paccheri, la tappa Piatto i tagliolini. Segnaposto rimasti (video) marcati con `<!-- SOSTITUIRE -->`.
- **Hero:** `setupHeroScroll()`; durata del blocco `end: '+=160%'`.
- **Palco:** `setupRoute()`; durata `window.innerHeight * 2.6`.
- **Contatori:** attributo `data-conta` (e `data-conta-da` per partire da un altro numero).
- **Form:** Netlify Forms, nome `assaggi`. Campi: nome, azienda, email (obbligatori), messaggio (facoltativo), consenso privacy.
