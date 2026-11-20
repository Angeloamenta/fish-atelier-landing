/* ==========================================================================
   Fish Atelier — Landing v5 "Carta"

   Cosa fa:    l'oblò della hero si apre a tutto schermo sulla foto dei paccheri;
               la scheda del gambero entra come il post approvato; "Dal pack al
               piatto" è un palco con tre oblò che si danno il cambio; la gamma
               è un nastro di pack da trascinare con la scheda in un dialog.
   Perché:     un solo gesto grafico (il cerchio) ripetuto con misura dà
               identità senza effetti sparsi. Ogni movimento porta lo sguardo
               su prodotto, sequenza o contatto.
   Assunzioni: senza JS la pagina è completa (oblò fermo, tappe una sotto
               l'altra, schede apribili nella card). Con "riduci movimento"
               niente smooth scroll, pin o parallasse.
   ========================================================================== */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';
import Lenis from 'lenis';

gsap.registerPlugin(ScrollTrigger, SplitText);

const SELECTORS = {
  header: '[data-header]',
  progress: '[data-progress]',
  darkSections: '[data-tema="scuro"]',
  hero: '[data-hero]',
  heroStage: '[data-hero-palco]',
  heroLines: '[data-hero-riga]',
  porthole: '[data-oblo]',
  portholeRing: '[data-oblo-anello]',
  portholeSignature: '[data-oblo-firma]',
  route: '[data-rotta]',
  stops: '[data-tappa]',
  video: '[data-video]',
  rail: '[data-binario]',
  railControls: '[data-comandi]',
  filters: '[data-filtri]',
  dialog: '[data-dialog]',
  drift: '[data-deriva]',
  valueRows: '[data-valore]',
  band: '[data-fascia]',
  form: '[data-form]',
  splitTitles: 'main .h2',
};

const DURATION = { fast: 0.32, base: 0.6, slow: 1.1 };
const EASE = { out: 'expo.out', inOut: 'power3.inOut', soft: 'power2.out' };

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

let lenis = null;

/* ==========================================================================
   SCROLL MORBIDO — un solo ticker per Lenis e ScrollTrigger
   ========================================================================== */
function setupSmoothScroll() {
  if (reducedMotion) return;
  // allowNestedScroll: il nastro orizzontale della gamma scorre da solo con trackpad e rotella
  lenis = new Lenis({ lerp: 0.1, allowNestedScroll: true });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const id = link.getAttribute('href');
      if (id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      event.preventDefault();
      lenis.scrollTo(target, { offset: id === '#top' ? 0 : -8, duration: 1.4 });
    });
  });
}

/* ==========================================================================
   HEADER E BARRA: chiari sul ghiaccio, ribaltati sulle sezioni scure
   ========================================================================== */
const darkUnderHeader = new Set();
const darkUnderBar = new Set();
let heroIsDark = false;

function applyTheme() {
  const header = document.querySelector(SELECTORS.header);
  const bar = document.querySelector(SELECTORS.progress);
  header?.classList.toggle('is-scuro', heroIsDark || darkUnderHeader.size > 0);
  bar?.classList.toggle('is-scuro', heroIsDark || darkUnderBar.size > 0);
}

function setupHeaderTheme() {
  const header = document.querySelector(SELECTORS.header);
  if (!header) return;
  const headerMiddle = () => header.offsetHeight / 2;

  document.querySelectorAll(SELECTORS.darkSections).forEach((section) => {
    ScrollTrigger.create({
      trigger: section,
      start: () => `top top+=${headerMiddle()}`,
      end: () => `bottom top+=${headerMiddle()}`,
      onToggle: (self) => { self.isActive ? darkUnderHeader.add(section) : darkUnderHeader.delete(section); applyTheme(); },
    });
    ScrollTrigger.create({
      trigger: section, start: 'top center', end: 'bottom center',
      onToggle: (self) => { self.isActive ? darkUnderBar.add(section) : darkUnderBar.delete(section); applyTheme(); },
    });
  });

  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 24);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

function setupProgressBar() {
  const fill = document.querySelector(`${SELECTORS.progress} span`);
  if (!fill) return;
  const setScale = gsap.quickSetter(fill, 'scaleY');
  ScrollTrigger.create({
    start: 0, end: 'max',
    onUpdate: (self) => setScale(self.progress),
  });
}

/* ==========================================================================
   HERO — l'oblò si apre e la pagina passa dal ghiaccio alla notte
   ========================================================================== */
function setHeroDark(dark) {
  if (dark === heroIsDark) return;
  heroIsDark = dark;
  applyTheme();
}

function portholeStartRadius() {
  const ring = document.querySelector(SELECTORS.portholeRing);
  // l'anello è largo 2r + 1.75rem: da lì ricavo il raggio vero, qualunque sia il breakpoint
  const remPx = parseFloat(getComputedStyle(document.documentElement).fontSize);
  return (ring.offsetWidth - 1.75 * remPx) / 2;
}

// scala iniziale della foto: larga quanto il cerchio (un filo di più), così si vede tutta la composizione
function photoStartScale() {
  const scene = document.querySelector('[data-oblo-scena]');
  if (!scene) return 1;
  return Math.min(1, (portholeStartRadius() * 2.1) / scene.offsetWidth);
}

function portholeCoverRadius() {
  // metà della diagonale dello schermo: il cerchio copre tutto
  return Math.hypot(window.innerWidth, window.innerHeight) / 2 + 2;
}

function setPhotoStartScale() {
  const scene = document.querySelector('[data-oblo-scena]');
  if (!scene) return;
  const apply = () => scene.style.setProperty('--foto-s', String(photoStartScale()));
  apply();
  window.addEventListener('resize', () => { if (window.scrollY < 10) apply(); });
}

function playHeroEntrance() {
  if (reducedMotion) return;
  gsap.timeline({ defaults: { ease: EASE.out } })
    .from(SELECTORS.porthole, { '--k': 0, duration: DURATION.slow * 1.2, ease: EASE.inOut })
    .from(SELECTORS.portholeRing, { scale: 0.6, autoAlpha: 0, duration: DURATION.slow }, 0.25)
    // l'ingresso usa proprietà diverse da quelle dello scroll (yPercent e l'opacità del contenitore):
    // così lo scroll registra come partenza lo stato finale e, tornando in cima, il titolo ricompare
    .from('.hero-titolo', { autoAlpha: 0, duration: DURATION.slow }, 0.35)
    .from('.hero-riga--1', { yPercent: 40, duration: DURATION.slow }, 0.35)
    .from('.hero-riga--2', { yPercent: 40, duration: DURATION.slow }, 0.45)
    .from('.hero-piede > *', { y: 16, autoAlpha: 0, duration: DURATION.base, stagger: 0.08, ease: EASE.soft }, 0.7);
}

function setupHeroScroll() {
  const hero = document.querySelector(SELECTORS.hero);
  const porthole = document.querySelector(SELECTORS.porthole);
  if (!hero || !porthole || reducedMotion) return;

  const scene = porthole.querySelector('[data-oblo-scena]');
  const veil = porthole.querySelector('[data-oblo-velo]');
  const signature = document.querySelector(SELECTORS.portholeSignature);
  const word = signature.querySelector('.firma-grande');

  const timeline = gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: {
      trigger: hero,
      start: 'top top',
      end: '+=160%',
      pin: SELECTORS.heroStage,
      scrub: 0.8,
      invalidateOnRefresh: true,
      // il cerchio aperto conta come sezione scura solo finché la hero è bloccata
      onUpdate: (self) => setHeroDark(self.isActive && self.progress > 0.42),
      onLeave: () => setHeroDark(false),
      onLeaveBack: () => setHeroDark(false),
    },
  });

  timeline
    .to('.hero-piede', { autoAlpha: 0, y: 20, duration: 0.12 }, 0)
    .fromTo(porthole, { '--r': () => `${portholeStartRadius()}px` }, { '--r': () => `${portholeCoverRadius()}px`, duration: 0.6, ease: 'power2.in' }, 0)
    // fromTo con partenza esplicita: l'anello ha anche un ingresso, e senza questo tornando su resterebbe nascosto
    .fromTo(SELECTORS.portholeRing,
      { scale: 1, autoAlpha: 1 },
      { scale: () => portholeCoverRadius() / portholeStartRadius(), autoAlpha: 0, duration: 0.45, ease: 'power2.in', immediateRender: false }, 0)
    // le due righe del titolo si separano verso i lati mentre il cerchio le attraversa
    .to('.hero-riga--1', { xPercent: -30, duration: 0.6 }, 0)
    .to('.hero-riga--2', { xPercent: 30, duration: 0.6 }, 0)
    .to(SELECTORS.heroLines, { autoAlpha: 0, duration: 0.18 }, 0.42)
    // la foto parte intera dentro il cerchio e cresce con lui fino a coprire lo schermo
    .fromTo(scene, { '--foto-s': () => photoStartScale() }, { '--foto-s': 1, duration: 0.6, ease: 'power2.in' }, 0)
    .to(veil, { opacity: 1, duration: 0.2 }, 0.55)
    // la firma entra come "DEDICATION" di Okains: lettere larghe che si stringono
    .set(signature, { visibility: 'visible' }, 0.62)
    .fromTo(word, { letterSpacing: '0.3em', autoAlpha: 0 }, { letterSpacing: '-0.02em', autoAlpha: 1, duration: 0.3, ease: 'power2.out' }, 0.62)
    .fromTo(['.firma-piccolo', '.oblo-sotto'], { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.2, stagger: 0.05 }, 0.72)
    .to({}, { duration: 0.1 }); // un attimo fermi sulla firma prima di sbloccare
}

/* ==========================================================================
   LA MATERIA PRIMA — la tavola ad acquerello cambia disegno con la specie
   ========================================================================== */
function setupMateria(mm) {
  const section = document.querySelector('[data-materia]');
  if (!section) return;
  const figures = gsap.utils.toArray('[data-tavola-figura]', section);
  const species = gsap.utils.toArray('[data-specie]', section);
  if (figures.length !== species.length) return;

  const showFigure = (activeIndex) => {
    figures.forEach((figure, index) => figure.classList.toggle('is-attiva', index === activeIndex));
  };

  // la tavola ferma accanto alle specie solo su schermi larghi; sotto, i disegni restano negli articoli
  mm.add('(min-width: 861px)', () => {
    section.classList.add('is-tavola');
    showFigure(0);
    const triggers = species.map((item, index) => ScrollTrigger.create({
      trigger: item,
      start: 'top 60%',
      end: 'bottom 40%',
      onToggle: (self) => {
        item.classList.toggle('is-attiva', self.isActive);
        if (self.isActive) showFigure(index);
      },
    }));
    ScrollTrigger.refresh(); // la tavola ha cambiato l'altezza delle specie

    return () => {
      triggers.forEach((trigger) => trigger.kill());
      section.classList.remove('is-tavola');
      species.forEach((item) => item.classList.remove('is-attiva'));
      showFigure(-1);
    };
  });
}

/* ==========================================================================
   DAL PACK AL PIATTO — tre oblò che si danno il cambio
   ========================================================================== */
function setupRoute(mm) {
  const route = document.querySelector(SELECTORS.route);
  if (!route) return;

  mm.add('(min-width: 861px) and (prefers-reduced-motion: no-preference)', () => {
    const stops = gsap.utils.toArray(SELECTORS.stops, route);
    route.classList.add('is-pinned');

    const parts = stops.map((stop) => ({
      word: stop.querySelector('.tappa-parola'),
      inner: stop.querySelector('.oblo-interno'),
      text: stop.querySelector('.tappa-testo'),
    }));

    // stato iniziale: si vede solo la prima tappa
    parts.slice(1).forEach(({ word, inner, text }) => {
      gsap.set(word, { yPercent: 60, autoAlpha: 0 });
      gsap.set(inner, { clipPath: 'circle(0% at 50% 50%)' });
      gsap.set(text, { autoAlpha: 0, y: 24 });
    });

    const timeline = gsap.timeline({
      defaults: { ease: EASE.inOut, duration: 1 },
      scrollTrigger: {
        trigger: route,
        start: 'top top',
        end: () => `+=${window.innerHeight * 2.6}`,
        pin: '.rotta-palco',
        scrub: 0.8,
        invalidateOnRefresh: true,
      },
    });

    timeline.to({}, { duration: 0.4 }); // la prima tappa resta un momento
    for (let index = 1; index < parts.length; index += 1) {
      const previous = parts[index - 1];
      const current = parts[index];
      const label = `tappa-${index}`;
      timeline
        .add(label)
        .to(previous.word, { yPercent: -60, autoAlpha: 0 }, label)
        .to(previous.text, { autoAlpha: 0, y: -24, duration: 0.5 }, label)
        .to(previous.inner, { scale: 0.86 }, label)
        .to(current.inner, { clipPath: 'circle(75% at 50% 50%)' }, label)
        .to(current.word, { yPercent: 0, autoAlpha: 1 }, `${label}+=0.15`)
        .to(current.text, { autoAlpha: 1, y: 0, duration: 0.5 }, `${label}+=0.5`)
        .to({}, { duration: 0.4 });
    }

    return () => route.classList.remove('is-pinned');
  });

  // schermi piccoli: le tappe una sotto l'altra, ogni oblò si apre quando entra
  mm.add('(max-width: 860px) and (prefers-reduced-motion: no-preference)', () => {
    gsap.utils.toArray('.oblo--tappa .oblo-interno', route).forEach((inner) => {
      gsap.from(inner, {
        clipPath: 'circle(0% at 50% 50%)', duration: DURATION.slow * 1.2, ease: EASE.inOut,
        scrollTrigger: { trigger: inner, start: 'top 80%', once: true },
      });
    });
  });
}

/* ==========================================================================
   VIDEO — la cornice si allarga mentre arriva
   ========================================================================== */
function setupVideo() {
  const frame = document.querySelector(SELECTORS.video);
  if (!frame || reducedMotion) return;
  gsap.fromTo(frame,
    { clipPath: 'inset(8% 14% 8% 14% round 999px)' },
    {
      clipPath: 'inset(0% 0% 0% 0% round 16px)', ease: 'none',
      scrollTrigger: { trigger: frame, start: 'top 95%', end: 'center 55%', scrub: 0.6 },
    });
}

/* ==========================================================================
   LA GAMMA — nastro trascinabile, filtri, scheda nel dialog
   ========================================================================== */
function setupRail() {
  const rail = document.querySelector(SELECTORS.rail);
  const controls = document.querySelector(SELECTORS.railControls);
  if (!rail || !controls) return;
  controls.hidden = false;

  const previousButton = controls.querySelector('[data-prev]');
  const nextButton = controls.querySelector('[data-next]');
  const fill = controls.querySelector('[data-nastro-pieno]');

  const updateControls = () => {
    const maxScroll = rail.scrollWidth - rail.clientWidth;
    const visibleShare = rail.clientWidth / rail.scrollWidth;
    const progress = maxScroll > 0 ? rail.scrollLeft / maxScroll : 1;
    fill.style.transform = `scaleX(${visibleShare + (1 - visibleShare) * progress})`;
    previousButton.disabled = rail.scrollLeft < 4;
    nextButton.disabled = rail.scrollLeft > maxScroll - 4;
  };

  const step = (direction) => {
    const card = rail.querySelector('.referenza:not([hidden])');
    const distance = card ? card.offsetWidth * 2 : rail.clientWidth * 0.8;
    rail.scrollBy({ left: direction * distance, behavior: reducedMotion ? 'auto' : 'smooth' });
  };
  previousButton.addEventListener('click', () => step(-1));
  nextButton.addEventListener('click', () => step(1));
  rail.addEventListener('scroll', updateControls, { passive: true });
  window.addEventListener('resize', updateControls);
  updateControls();

  setupRailDrag(rail);
  return updateControls;
}

// trascinamento col mouse (su touch lo scroll nativo basta già)
function setupRailDrag(rail) {
  let startX = 0;
  let startScroll = 0;
  let dragging = false;
  let moved = false;

  rail.addEventListener('pointerdown', (event) => {
    if (event.pointerType !== 'mouse' || event.button !== 0) return;
    dragging = true;
    moved = false;
    startX = event.clientX;
    startScroll = rail.scrollLeft;
  });
  window.addEventListener('pointermove', (event) => {
    if (!dragging) return;
    const delta = event.clientX - startX;
    if (Math.abs(delta) > 6 && !moved) {
      moved = true;
      rail.classList.add('is-trascinando');
    }
    if (moved) rail.scrollLeft = startScroll - delta;
  });
  window.addEventListener('pointerup', () => {
    if (!dragging) return;
    dragging = false;
    rail.classList.remove('is-trascinando');
  });
  // dopo un trascinamento il rilascio non deve aprire la scheda
  rail.addEventListener('click', (event) => {
    if (moved) { event.preventDefault(); event.stopPropagation(); moved = false; }
  }, true);
}

function setupFilters(onChange) {
  const group = document.querySelector(SELECTORS.filters);
  const rail = document.querySelector(SELECTORS.rail);
  if (!group || !rail) return;
  group.hidden = false;

  const buttons = [...group.querySelectorAll('[data-filtro]')];
  const items = [...rail.querySelectorAll('.referenza')];

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      const filter = button.dataset.filtro;
      buttons.forEach((other) => other.setAttribute('aria-pressed', String(other === button)));
      items.forEach((item) => { item.hidden = filter !== 'tutte' && item.dataset.gruppo !== filter; });
      rail.scrollLeft = 0;
      onChange?.();
      if (!reducedMotion) {
        gsap.fromTo(items.filter((item) => !item.hidden),
          { y: 24, autoAlpha: 0 },
          { y: 0, autoAlpha: 1, duration: DURATION.base, ease: EASE.out, stagger: 0.04, clearProps: 'transform,opacity,visibility' });
      }
    });
  });
}

function setupProductDialog() {
  const dialog = document.querySelector(SELECTORS.dialog);
  if (!dialog || typeof dialog.showModal !== 'function') return; // senza dialog resta la scheda dentro la card

  const packSlot = dialog.querySelector('[data-scheda-pack]');
  const statusSlot = dialog.querySelector('[data-scheda-stato]');
  const titleSlot = dialog.querySelector('[data-scheda-titolo]');
  const entriesSlot = dialog.querySelector('[data-scheda-voci]');
  const sampleLink = dialog.querySelector('[data-scheda-cta]');

  document.querySelectorAll('[data-scheda] > summary').forEach((summary) => {
    summary.addEventListener('click', (event) => {
      event.preventDefault();
      const card = summary.closest('.referenza-card');
      const pack = card.querySelector('.busta').cloneNode(true);
      pack.classList.remove('busta--card');
      const image = pack.querySelector('img');
      image.src = 'assets/img/pack-finestre.webp';
      image.removeAttribute('loading');

      packSlot.replaceChildren(pack);
      const status = card.querySelector('.referenza-stato');
      statusSlot.textContent = status.textContent;
      statusSlot.className = status.className;
      titleSlot.textContent = card.querySelector('.referenza-nome').textContent;
      const entries = card.querySelector('.scheda-voci').cloneNode(true);
      entriesSlot.replaceChildren(entries);

      dialog.showModal();
      lenis?.stop();
    });
  });

  dialog.addEventListener('close', () => lenis?.start());
  dialog.querySelector('[data-chiudi]').addEventListener('click', () => dialog.close());
  // clic sul fondo scuro: chiude
  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
  // "Chiedi un campione": chiude, porta al form e preseleziona la richiesta giusta
  sampleLink.addEventListener('click', (event) => {
    event.preventDefault();
    dialog.close();
    const choice = document.querySelector('input[name="richiesta"][value="campioni"]');
    if (choice) choice.checked = true;
    const message = document.querySelector('#f-msg');
    if (message && !message.value) message.value = `Vorrei ricevere un campione di: ${titleSlot.textContent}.`;
    const target = document.querySelector('#buyer');
    if (lenis) lenis.scrollTo(target, { duration: 1.4 });
    else target.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth' });
  });
}

/* ==========================================================================
   PERCHÉ PREMIUM — le parole entrano, i disegni derivano
   ========================================================================== */
function setupValueRows() {
  if (reducedMotion) return;
  gsap.utils.toArray(SELECTORS.valueRows).forEach((row) => {
    gsap.from(row.querySelectorAll('.valore-parola, p'), {
      x: -24, autoAlpha: 0, duration: DURATION.slow, ease: EASE.out, stagger: 0.12,
      scrollTrigger: { trigger: row, start: 'top 80%', once: true },
    });
  });
  gsap.utils.toArray(SELECTORS.drift).forEach((drawing, index) => {
    gsap.fromTo(drawing,
      { yPercent: 12, rotation: index % 2 ? 6 : -6 },
      { yPercent: -12, rotation: index % 2 ? -3 : 3, ease: 'none',
        scrollTrigger: { trigger: drawing.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
}

function setupSplitTitles() {
  if (reducedMotion) return;
  document.querySelectorAll(SELECTORS.splitTitles).forEach((title) => {
    const split = SplitText.create(title, { type: 'lines', mask: 'lines' });
    gsap.from(split.lines, {
      yPercent: 105, duration: DURATION.slow, ease: EASE.out, stagger: 0.08,
      scrollTrigger: { trigger: title, start: 'top 85%', once: true },
    });
  });
}

function setupBand() {
  const band = document.querySelector(SELECTORS.band);
  if (!band || reducedMotion) return;
  // la fascia dei pesci scorre di lato mentre il footer entra
  gsap.fromTo(band, { '--x': '0px' }, {
    '--x': '-320px', ease: 'none',
    scrollTrigger: { trigger: band, start: 'top bottom', end: 'bottom top', scrub: true },
    onUpdate() { band.style.backgroundPositionX = band.style.getPropertyValue('--x'); },
  });
}

/* ==========================================================================
   FORM — validazione e invio a Netlify Forms
   ========================================================================== */
function setupForm() {
  const form = document.querySelector(SELECTORS.form);
  if (!form) return;

  const rules = [
    { input: form.querySelector('#f-nome'), valid: (value) => value.trim().length > 1 },
    { input: form.querySelector('#f-insegna'), valid: (value) => value.trim().length > 1 },
    { input: form.querySelector('#f-email'), valid: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value.trim()) },
    { input: form.querySelector('#f-privacy'), valid: (_value, input) => input.checked },
  ];

  const validate = ({ input, valid }) => {
    const ok = valid(input.value, input);
    input.closest('.campo').classList.toggle('ha-errore', !ok);
    input.setAttribute('aria-invalid', String(!ok));
    return ok;
  };

  rules.forEach((rule) => {
    rule.input.addEventListener('blur', () => { if (rule.input.value || rule.input.type === 'checkbox') validate(rule); });
    rule.input.addEventListener('input', () => { if (rule.input.closest('.ha-errore')) validate(rule); });
    rule.input.addEventListener('change', () => { if (rule.input.closest('.ha-errore')) validate(rule); });
  });

  const submitButton = form.querySelector('button[type="submit"]');
  const errorMessage = form.querySelector('.modulo-esito--errore');
  const successMessage = form.querySelector('.modulo-esito:not(.modulo-esito--errore)');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const results = rules.map(validate);
    if (!results.every(Boolean)) {
      rules[results.indexOf(false)].input.focus();
      return;
    }
    // le richieste arrivano in Netlify > Forms > assaggi
    submitButton.disabled = true;
    errorMessage.hidden = true;
    try {
      const response = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString(),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      successMessage.hidden = false;
      successMessage.focus?.();
    } catch (error) {
      submitButton.disabled = false;
      errorMessage.hidden = false;
    }
  });
}

/* ---------- Avvio ---------- */
function init() {
  const mm = gsap.matchMedia();
  setupSmoothScroll();
  setPhotoStartScale();
  playHeroEntrance();
  setupHeroScroll();
  setupMateria(mm);
  setupRoute(mm);
  setupVideo();
  const updateRail = setupRail();
  setupFilters(updateRail);
  setupProductDialog();
  setupValueRows();
  setupSplitTitles();
  setupBand();
  setupForm();
  // dopo i pin della hero e del palco: così i trigger del tema tengono conto dello spazio aggiunto
  setupHeaderTheme();
  setupProgressBar();

  // i font cambiano le misure: ricalcolo i trigger quando sono pronti
  document.fonts?.ready.then(() => ScrollTrigger.refresh());
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
else init();
