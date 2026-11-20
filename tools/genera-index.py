"""Genera index.html della landing Fish Atelier v5 "Carta" (stile dei post approvati).
Le 17 referenze stanno in una lista qui sotto: si cambia qui e si rigenera."""
import html as H

NOVITA = [
    ("Polpo e patate", "polpo", "#C99A8E"),
    ("Merluzzo alla mediterranea", "pesce", "#E9E1D3"),
    ("Sugo allo scoglio", "cozza", "#B4553C"),
    ("Sugo alle vongole", "vongola", "#D8C9A6"),
    ("Sugo ai crostacei", "scampo", "#C4643F"),
    ("Sugo ai frutti di mare", "canocchia", "#B9583F"),
    ("Calamari ripieni", "calamaro", "#E6D9C2"),
    ("Zuppa", "scorfano", "#C77A45"),
]
IN_GAMMA = [
    ("Code di gambero", "gambero", "#E39A7C", ["2 kg (astuccio)", "750 g"]),
    ("Gamberi interi", "gambero-intero", "#D8826A", ["400 g"]),
    ("Gambero Rosso Sicilia", "gambero", "#C2443A", ["400 g"]),
    ("Insalata di mare in busta", "seppia", "#DCCBB0", ["800 g", "500 g"]),
    ("Insalata con polpo", "polpo", "#CFA79A", ["800 g"]),
    ("Insalata per risotto", "vongola", "#D9C29A", ["800 g"]),
    ("Gamberi sgusciati", "gambero-intero", "#E7A88E", ["500 g"]),
    ("Fette di salmone", "fette", "#EE9A78", ["800 g"]),
    ("Polpo tagliato cotto", "polpo", "#B98C86", ["800 g"]),
]
# minuti in padella per referenza: per i gamberi viene dal post approvato "Gambero" (5–8 minuti),
# per le altre è da definire con il cliente. La conservazione è quella dei surgelati (−18 °C, da confermare).
PADELLA = {"Code di gambero": "5–8", "Gamberi interi": "5–8", "Gambero Rosso Sicilia": "5–8", "Gamberi sgusciati": "5–8"}

LOREM = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod.",
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse.",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa.",
]


def maschera(incisione):
    """Classi del disegno: la maschera vera sta in assets/css/incisioni.css (data URI, funziona anche con doppio clic)."""
    return f"inc inc-{incisione}"


def pack(nome, incisione, tinta, extra_class="", big=False, lazy=True):
    """La busta vera del pack con le finestre trasparenti: dietro c'è la tinta del prodotto e il suo disegno."""
    src = "assets/img/pack-finestre.webp" if big else "assets/img/pack-finestre-600.webp"
    size = "1024" if big else "600"
    loading = ' loading="lazy" decoding="async"' if lazy else ""
    return (
        f'<div class="busta{extra_class}" style="--tinta:{tinta}" '
        f'role="img" aria-label="Pack provvisorio {H.escape(nome)}: il prodotto si vede dalle due finestre">'
        f'<span class="busta-prodotto" aria-hidden="true"><span class="busta-disegno busta-disegno--sx {maschera(incisione)}"></span><span class="busta-disegno busta-disegno--dx {maschera(incisione)}"></span></span>'
        f'<img src="{src}" alt="" width="{size}" height="{size}" draggable="false"{loading}>'
        f'<span class="busta-riflesso" aria-hidden="true"></span></div>'
    )


def scheda(i, nome, incisione, tinta, gruppo, formati):
    formati_txt = ", ".join(formati) if formati else "Formato da definire"
    formati_html = ", ".join(formati) if formati else '<span class="da-definire">da definire</span>'
    minuti = PADELLA.get(nome)
    padella_html = f"{minuti} <em>min</em>" if minuti else '<span class="da-definire">da definire</span>'
    padella_txt = f"{minuti} minuti" if minuti else "Da definire"
    stato = "Novità" if gruppo == "novita" else "Già in gamma"
    slug = nome.lower().replace(" ", "-").replace("à", "a")
    return f'''        <li class="referenza" data-gruppo="{gruppo}">
          <article class="referenza-card" aria-labelledby="ref-{slug}">
            {pack(nome, incisione, tinta, " busta--card")}
            <p class="referenza-stato referenza-stato--{gruppo}">{stato}</p>
            <h3 class="referenza-nome" id="ref-{slug}">{nome}</h3>
            <dl class="referenza-dati">
              <div><dt>Conservazione</dt><dd>−18 <em>°C</em></dd></div>
              <div><dt>In padella</dt><dd>{padella_html}</dd></div>
              <div class="referenza-dati-formato"><dt>Formato</dt><dd>{formati_html}</dd></div>
            </dl>
            <details class="referenza-scheda" data-scheda>
              <summary>Scheda prodotto</summary>
              <dl class="scheda-voci">
                <div><dt>Materia prima</dt><dd>{LOREM[i % 5]}</dd></div>
                <div><dt>Ricetta</dt><dd>{LOREM[(i + 2) % 5]}</dd></div>
                <div><dt>Nel piatto</dt><dd>{LOREM[(i + 4) % 5]}</dd></div>
                <div><dt>Formati</dt><dd>{formati_txt}</dd></div>
                <div><dt>In padella</dt><dd>{padella_txt}</dd></div>
                <div><dt>Conservazione</dt><dd>−18 °C</dd></div>
              </dl>
            </details>
          </article>
        </li>'''


referenze = "\n".join(
    [scheda(k, n, inc, t, "novita", []) for k, (n, inc, t) in enumerate(NOVITA)]
    + [scheda(k + 3, n, inc, t, "gamma", f) for k, (n, inc, t, f) in enumerate(IN_GAMMA)]
)




def foto(nome, alt, cls, sizes, loading="lazy", pos="50% 50%"):
    """Foto approvata in due larghezze."""
    larghezze = {"paccheri": (1100, 1856, 2304), "tagliolini": (800, 1400, 1738)}[nome]
    piccola, grande, altezza = larghezze
    load = ' loading="lazy" decoding="async"' if loading == "lazy" else ' fetchpriority="high"'
    return (f'<img class="{cls}" src="assets/img/foto/{nome}-{grande}.webp" '
            f'srcset="assets/img/foto/{nome}-{piccola}.webp {piccola}w, assets/img/foto/{nome}-{grande}.webp {grande}w" '
            f'sizes="{sizes}" width="{grande}" height="{altezza}" alt="{alt}" style="object-position:{pos}"{load}>')


def decoro(nome, cls, w, h, extra=""):
    return f'<img class="decoro {cls}" src="assets/img/decori/{nome}.webp" alt="" width="{w}" height="{h}" loading="lazy" decoding="async" aria-hidden="true"{extra}>'


page = f'''<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Fish Atelier · Piatti di mare da ristorante, in pochi minuti</title>
  <meta name="description" content="Fish Atelier, la linea premium di piatti di mare surgelati. Materia prima, ricetta e risultato nel piatto. Marca Bologna 2027.">
  <meta name="theme-color" content="#EFEEDE">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='15' fill='%2300314F'/%3E%3Ccircle cx='16' cy='16' r='9' fill='none' stroke='%23C8B482' stroke-width='2'/%3E%3C/svg%3E">
  <link rel="preload" href="assets/fonts/instrument-serif-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/instrument-serif-latin-400-italic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/img/foto/paccheri-1856.webp" as="image" imagesrcset="assets/img/foto/paccheri-1100.webp 1100w, assets/img/foto/paccheri-1856.webp 1856w" imagesizes="100vw">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="assets/css/incisioni.css">
  <script>document.documentElement.classList.add('js')</script>
</head>
<body>

<a class="skip-link" href="#contenuto">Vai al contenuto</a>

<!-- ============ HEADER ============ -->
<header class="site-header" data-header>
  <a class="logo" href="#top" aria-label="Fish Atelier, torna all'inizio">
    <!-- due versioni del marchio: blu sulla carta, chiaro quando l'header passa sulle sezioni scure -->
    <img class="logo-blu" src="assets/img/logo-fa.webp" alt="" width="361" height="488">
    <img class="logo-chiaro" src="assets/img/logo-fa-chiaro.webp" alt="" width="361" height="488">
  </a>
  <nav class="main-nav" aria-label="Sezioni">
    <ul>
      <li><a href="#rotta">Dal pack al piatto</a></li>
      <li><a href="#gamma">La gamma</a></li>
      <li><a href="#buyer">Per i buyer</a></li>
    </ul>
  </nav>
  <a class="btn btn--pieno" href="#buyer">Prenota un assaggio</a>
</header>

<!-- avanzamento verticale: quanto manca alla fine della pagina -->
<div class="rotta-barra" data-progress aria-hidden="true"><span class="rotta-barra-pieno"></span></div>

<main id="contenuto">

  <!-- ============ HERO: l'oblò si apre sulla foto ============ -->
  <section class="hero" id="top" aria-labelledby="hero-title" data-hero>
    <div class="hero-palco" data-hero-palco>
      <h1 class="hero-titolo" id="hero-title">
        <span class="hero-riga hero-riga--1" data-hero-riga>Piatti<br>di mare</span>
        <span class="hero-riga hero-riga--2" data-hero-riga><em>da ristorante,<br>in pochi minuti</em></span>
      </h1>

      <span class="oblo-anello" data-oblo-anello aria-hidden="true"></span>
      <div class="oblo oblo--hero" data-oblo>
        <!-- la foto intera sta nel cerchio e cresce con lui fino a coprire lo schermo -->
        <div class="oblo-scena" data-oblo-scena>{foto("paccheri", "Paccheri con gamberi e datterino: la pasta cade dalla forchetta nel piatto", "oblo-foto", "100vw", loading="eager", pos="50% 50%")}</div>
        <span class="oblo-velo" data-oblo-velo aria-hidden="true"></span>
        <p class="hero-titolo hero-titolo--dentro" aria-hidden="true">
          <span class="hero-riga hero-riga--1" data-hero-riga>Piatti<br>di mare</span>
          <span class="hero-riga hero-riga--2" data-hero-riga><em>da ristorante,<br>in pochi minuti</em></span>
        </p>
        <div class="oblo-firma" data-oblo-firma>
          <p class="firma"><span class="firma-piccolo">i piatti</span><span class="firma-grande">dell'Atelier</span></p>
          <p class="oblo-sotto">Quality seafood experience · dal 1956</p>
        </div>
      </div>

      <div class="hero-piede">
        <p class="hero-lead">Fish Atelier è la linea premium di piatti di mare surgelati, dal 1956: materia prima scelta e ricette complete, dalla busta alla padella.</p>
        <p class="hero-fiera"><span>Marca Bologna 2027</span><span><em>padiglione 00, stand 00</em></span></p>
      </div>
    </div>
  </section>

  <!-- ============ LA MATERIA PRIMA: le due specie disegnate ad acquerello, come tavole naturalistiche ============ -->
  <section class="materia" aria-labelledby="materia-title" data-materia>
    <div class="wrap sezione-testa materia-testa">
      <h2 class="h2" id="materia-title">Da dove parte <em>il prezzo</em></h2>
      <p>Due materie prime che reggono metà della gamma. Per ognuna: come si cucina e in quali referenze la trovate.</p>
    </div>
    <div class="wrap materia-grid">
      <div class="materia-specie">
        <article class="specie" data-specie aria-labelledby="specie-gambero">
          <img class="specie-disegno" src="assets/img/decori/gambero-acquerello.webp" alt="Gambero disegnato ad acquerello blu" width="1400" height="1051" loading="lazy" decoding="async">
          <p class="specie-n"><em>1 di 2</em></p>
          <h3 class="specie-nome" id="specie-gambero">Gambero</h3>
          <dl class="specie-voci">
            <div><dt>Preparazione:</dt><dd>In padella o sulla griglia per 5–8 minuti</dd></div>
            <div><dt>Gusto:</dt><dd>Delicato e raffinato</dd></div>
            <div><dt>Nutrienti:</dt><dd>Proteine e omega 3</dd></div>
          </dl>
          <div class="specie-referenze">
            <p class="etichetta">Nelle referenze:</p>
            <ul><li>Code di gambero</li><li>Gamberi interi</li><li>Gambero Rosso Sicilia</li><li>Gamberi sgusciati</li></ul>
          </div>
        </article>
        <article class="specie" data-specie aria-labelledby="specie-polpo">
          <img class="specie-disegno" src="assets/img/decori/polpo-intero.webp" alt="Polpo disegnato ad acquerello blu" width="687" height="626" loading="lazy" decoding="async">
          <p class="specie-n"><em>2 di 2</em></p>
          <h3 class="specie-nome" id="specie-polpo">Polpo</h3>
          <dl class="specie-voci">
            <div><dt>Antipasto:</dt><dd>Con patate schiacciate, emulsione al limone e prezzemolo fresco</dd></div>
            <div><dt>Alla griglia:</dt><dd>Con purè di ceci, pomodorini confit e olive taggiasche</dd></div>
          </dl>
          <div class="specie-referenze">
            <p class="etichetta">Nelle referenze:</p>
            <ul><li>Polpo e patate <em>novità</em></li><li>Insalata con polpo</li><li>Polpo tagliato cotto</li></ul>
          </div>
        </article>
      </div>
      <!-- su schermi larghi la tavola resta ferma e cambia disegno quando cambia la specie (stesse immagini degli articoli) -->
      <div class="materia-tavola" aria-hidden="true">
        <figure class="tavola-figura" data-tavola-figura>
          <img src="assets/img/decori/gambero-acquerello.webp" alt="" width="1400" height="1051" loading="lazy" decoding="async">
          <figcaption><em>Tav. I</em> Gambero</figcaption>
        </figure>
        <figure class="tavola-figura tavola-figura--polpo" data-tavola-figura>
          <img src="assets/img/decori/polpo-intero.webp" alt="" width="687" height="626" loading="lazy" decoding="async">
          <figcaption><em>Tav. II</em> Polpo</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <!-- ============ DAL PACK AL PIATTO ============ -->
  <section class="rotta tema-scuro" id="rotta" aria-labelledby="rotta-title" data-tema="scuro" data-rotta>
    <div class="rotta-palco">
      <h2 class="visually-hidden" id="rotta-title">Dal pack al piatto</h2>
      <ol class="tappe">
        <li class="tappa" data-tappa>
          <p class="tappa-parola" aria-hidden="true">Pack</p>
          <div class="oblo oblo--tappa">
            <div class="oblo-interno oblo-interno--carta">{pack("Polpo e patate", "polpo", "#C99A8E", " busta--tappa", big=True)}</div>
          </div>
          <div class="tappa-testo">
            <h3 class="tappa-titolo"><span class="tappa-n">1 di 3</span> Si apre la busta</h3>
            <p>Il prodotto si vede dalle finestre: quello che compri è quello che mangi. Lorem ipsum dolor sit amet.</p>
          </div>
        </li>
        <li class="tappa" data-tappa>
          <p class="tappa-parola" aria-hidden="true"><em>Ricetta</em></p>
          <div class="oblo oblo--tappa">
            <div class="oblo-interno oblo-interno--carta oblo-interno--ricetta">
              {decoro("polpo-intero", "ricetta-polpo", 687, 626)}
              <p class="ricetta-menu"><span>Polpo e patate</span><em>olio, limone, prezzemolo</em></p>
            </div>
          </div>
          <div class="tappa-testo">
            <h3 class="tappa-titolo"><span class="tappa-n">2 di 3</span> Pochi minuti in padella</h3>
            <p>Direttamente da surgelato, senza scongelare: la ricetta è già fatta. Consectetur adipiscing elit.</p>
          </div>
        </li>
        <li class="tappa" data-tappa>
          <p class="tappa-parola" aria-hidden="true">Piatto</p>
          <div class="oblo oblo--tappa">
            <div class="oblo-interno">{foto("tagliolini", "Tagliolini al gambero rosso arrotolati sulla forchetta sopra il piatto", "oblo-foto", "(min-width: 861px) 32rem, 70vw", pos="48% 46%")}</div>
          </div>
          <div class="tappa-testo">
            <h3 class="tappa-titolo"><span class="tappa-n">3 di 3</span> Un piatto da ristorante</h3>
            <p>Il risultato che il cliente porta in tavola. Ut enim ad minim veniam, quis nostrud exercitation.</p>
          </div>
        </li>
      </ol>
    </div>
  </section>

  <!-- ============ VIDEO ============ -->
  <section class="video" aria-labelledby="video-title">
    <div class="wrap sezione-testa">
      <h2 class="h2" id="video-title">Dal pack al piatto, <em>in un minuto</em></h2>
      <p>Il video della preparazione: lo stesso che proietteremo allo stand. Lorem ipsum dolor sit amet.</p>
    </div>
    <div class="video-cornice" data-video>
      <!-- SOSTITUIRE con <video controls playsinline poster="..."> -->
      <div class="video-segnaposto" role="img" aria-label="Segnaposto del video Dal pack al piatto">
        {decoro("polpo-spirale", "video-polpo", 556, 900)}
        <span class="video-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.5v13l11-6.5z"/></svg></span>
        <span class="segnaposto">Video: polpo e patate, dal pack al piatto · 60 s</span>
      </div>
    </div>
  </section>

  <!-- ============ LA GAMMA ============ -->
  <section class="gamma" id="gamma" aria-labelledby="gamma-title">
    <div class="wrap gamma-testa">
      <div>
        <h2 class="marchio" id="gamma-title"><span class="marchio-grande">La gamma</span><em class="marchio-piccolo">dell'Atelier</em></h2>
        <p>Diciassette referenze, otto nuove. Per ognuna: da dove viene la materia prima, come è fatta la ricetta, cosa arriva nel piatto.</p>
      </div>
      <div class="filtri" role="group" aria-label="Filtra le referenze" data-filtri hidden>
        <button class="filtro" type="button" data-filtro="tutte" aria-pressed="true">Tutte <span>17</span></button>
        <button class="filtro" type="button" data-filtro="novita" aria-pressed="false">Novità <span>8</span></button>
        <button class="filtro" type="button" data-filtro="gamma" aria-pressed="false">Già in gamma <span>9</span></button>
      </div>
    </div>
    <div class="nastro" data-nastro>
      <ul class="nastro-binario" data-binario tabindex="0" aria-label="Referenze: scorri in orizzontale">
{referenze}
      </ul>
    </div>
    <div class="wrap nastro-comandi" data-comandi hidden>
      <div class="nastro-avanzamento" aria-hidden="true"><span data-nastro-pieno></span></div>
      <button class="freccia" type="button" data-prev aria-label="Referenze precedenti"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
      <button class="freccia" type="button" data-next aria-label="Referenze successive"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
    </div>
    <div class="wrap"><p class="gamma-nota">I pack sono provvisori: dalle finestre si vede il colore del prodotto e il disegno dell'ingrediente, al posto della foto.</p></div>
  </section>

  <!-- scheda aperta da una referenza (con JS); senza JS la scheda si apre dentro la card -->
  <dialog class="scheda" data-dialog aria-labelledby="scheda-titolo">
    <div class="scheda-corpo">
      <div class="scheda-pack" data-scheda-pack></div>
      <div class="scheda-testo">
        <p class="referenza-stato" data-scheda-stato></p>
        <h3 class="scheda-titolo" id="scheda-titolo" data-scheda-titolo></h3>
        <div data-scheda-voci></div>
        <a class="btn btn--pieno" href="#buyer" data-scheda-cta>Chiedi un campione</a>
      </div>
    </div>
    <button class="scheda-chiudi" type="button" data-chiudi aria-label="Chiudi la scheda"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  </dialog>

  <!-- ============ PERCHÉ PREMIUM: impaginato come il menù approvato ============ -->
  <section class="valore" aria-labelledby="valore-title">
    {decoro("tentacolo-ricciolo", "valore-polpo valore-polpo--1", 390, 900, " data-deriva")}
    {decoro("tentacolo-lungo", "valore-polpo valore-polpo--2", 341, 900, " data-deriva")}
    {decoro("polpo-esse", "valore-polpo valore-polpo--3", 563, 837, " data-deriva")}
    <div class="wrap valore-wrap">
      <h2 class="marchio valore-titolo" id="valore-title"><span class="marchio-grande">Il prezzo</span><em class="marchio-piccolo">in tre portate</em></h2>
      <ol class="valore-lista">
        <li class="valore-voce" data-valore>
          <h3 class="valore-parola">Materia prima</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Da dove arriva il pescato e perché è quello e non un altro.</p>
        </li>
        <li class="valore-voce" data-valore>
          <h3 class="valore-parola">Ricetta</h3>
          <p>Sed do eiusmod tempor incididunt ut labore. Gli ingredienti, le dosi e la cottura pensati da chi lavora in cucina.</p>
        </li>
        <li class="valore-voce" data-valore>
          <h3 class="valore-parola">Nel piatto</h3>
          <p>Ut enim ad minim veniam. Quello che il cliente trova a tavola: consistenza, sapore, porzione.</p>
        </li>
      </ol>
    </div>
  </section>

  <!-- ============ BUYER E ASSAGGI ============ -->
  <section class="buyer tema-scuro" id="buyer" aria-labelledby="buyer-title" data-tema="scuro">
    <div class="wrap buyer-grid">
      <div class="buyer-testo">
        <h2 class="h2" id="buyer-title">Venite ad assaggiare <em>a Marca</em></h2>
        <p class="buyer-lead">Allo stand cuciniamo le novità dal vivo. Prenotate un assaggio, uno showcooking o un incontro con il commerciale. Lorem ipsum dolor sit amet.</p>
        <dl class="fiera">
          <div><dt>Quando</dt><dd>00–00 gennaio 2027</dd></div>
          <div><dt>Dove</dt><dd>BolognaFiere, padiglione 00, stand 00</dd></div>
          <div><dt>Showcooking</dt><dd>Polpo e patate, ore 00:00 e 00:00 <span class="nota">da confermare</span></dd></div>
          <div><dt>Referente</dt><dd>Nome Cognome<br><a href="mailto:commerciale@example.com">commerciale@example.com</a><br><a href="tel:+390000000000">+39 000 000 0000</a></dd></div>
        </dl>
        <a class="profilo" href="#" download>
          <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 19h14"/></svg>
          <span><strong>Brand profile Fish Atelier</strong><span>Posizionamento, gamma, formati e novità. PDF, 2 pagine</span></span>
        </a>
      </div>

      <form class="modulo" name="assaggi" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field" novalidate data-form>
        <!-- Netlify Forms: il nome del form e la trappola per i bot -->
        <input type="hidden" name="form-name" value="assaggi">
        <p class="campo-trappola" aria-hidden="true"><label>Non compilare questo campo <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
        <fieldset class="campo">
          <legend>Cosa vi interessa</legend>
          <div class="scelte">
            <label class="scelta"><input type="radio" name="richiesta" value="assaggio" checked><span>Assaggio allo stand</span></label>
            <label class="scelta"><input type="radio" name="richiesta" value="showcooking"><span>Showcooking</span></label>
            <label class="scelta"><input type="radio" name="richiesta" value="incontro"><span>Incontro commerciale</span></label>
            <label class="scelta"><input type="radio" name="richiesta" value="campioni"><span>Listino e campioni</span></label>
          </div>
        </fieldset>
        <div class="modulo-griglia">
          <div class="campo">
            <label for="f-nome">Nome e cognome</label>
            <input id="f-nome" name="nome" type="text" autocomplete="name" required aria-describedby="e-nome">
            <p class="campo-errore" id="e-nome">Inserisci nome e cognome.</p>
          </div>
          <div class="campo">
            <label for="f-insegna">Insegna o azienda</label>
            <input id="f-insegna" name="insegna" type="text" autocomplete="organization" required aria-describedby="e-insegna">
            <p class="campo-errore" id="e-insegna">Inserisci l'insegna o l'azienda.</p>
          </div>
          <div class="campo">
            <label for="f-email">Email</label>
            <input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="e-email">
            <p class="campo-errore" id="e-email">Inserisci un'email valida, per esempio nome@azienda.it.</p>
          </div>
          <div class="campo">
            <label for="f-tel">Telefono <span class="opz">facoltativo</span></label>
            <input id="f-tel" name="telefono" type="tel" autocomplete="tel">
          </div>
          <div class="campo">
            <label for="f-ruolo">Ruolo</label>
            <select id="f-ruolo" name="ruolo">
              <option>Buyer</option>
              <option>Category manager</option>
              <option>Direzione acquisti</option>
              <option>Altro</option>
            </select>
          </div>
          <div class="campo">
            <label for="f-giorno">Giorno preferito <span class="opz">facoltativo</span></label>
            <select id="f-giorno" name="giorno">
              <option value="">Indifferente</option>
              <option>Giorno 1</option>
              <option>Giorno 2</option>
            </select>
          </div>
        </div>
        <div class="campo">
          <label for="f-msg">Messaggio <span class="opz">facoltativo</span></label>
          <textarea id="f-msg" name="messaggio" rows="3"></textarea>
        </div>
        <div class="modulo-piede">
          <div class="campo">
            <label class="spunta" for="f-privacy"><input type="checkbox" name="privacy" id="f-privacy" required aria-describedby="e-privacy"><span>Ho letto l'<a href="#">informativa privacy</a></span></label>
            <p class="campo-errore" id="e-privacy">Per inviare la richiesta serve il consenso all'informativa.</p>
          </div>
          <button class="btn btn--chiaro" type="submit">Invia la prenotazione</button>
        </div>
        <p class="modulo-esito modulo-esito--errore" role="alert" hidden>Invio non riuscito. Riprovate tra poco o scriveteci a commerciale@example.com.</p>
        <p class="modulo-esito" role="status" aria-live="polite" hidden>Prenotazione inviata. Vi confermiamo giorno e orario entro 00 giorni lavorativi.</p>
      </form>
    </div>
  </section>

</main>

<!-- ============ FOOTER ============ -->
<footer class="site-footer tema-scuro" data-tema="scuro">
  <div class="fascia" aria-hidden="true" data-fascia></div>
  <div class="wrap footer-grid">
    <img class="footer-badge" src="assets/img/logo-fa-chiaro.webp" alt="Fish Atelier, Quality Seafood Experience, 1956" width="361" height="488" loading="lazy">
    <p class="footer-claim">Solo i prodotti del mare <em>di alta qualità</em>, sulla tua tavola.</p>
    <ul class="footer-link">
      <li><a href="#">Instagram</a></li>
      <li><a href="#">Facebook</a></li>
      <li><a href="#">Privacy e cookie</a></li>
    </ul>
  </div>
  <div class="wrap footer-legale"><p>Prodotto da Ragione sociale S.p.A., via Lorem Ipsum 00, 00000 Città (XX), P. IVA 00000000000</p></div>
</footer>

<script src="assets/js/main.bundle.js" defer></script>
</body>
</html>
'''

open(__import__("pathlib").Path(__file__).resolve().parent.parent / "index.html", "w").write(page)
print("ok", len(page))
