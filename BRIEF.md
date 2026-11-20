# Fish Atelier — Landing v5 "Carta"

La v4 "Ghiaccio" rifatta con i materiali approvati dal cliente: foto su velluto blu, polpi ad acquerello, gamberi a retino, post "Gambero", "Christmas" e "Paccheri". Stessa struttura, stile del brand.

## Sistema
- **Font:** Instrument Serif, tondo e corsivo, l'unica famiglia. Tondo maiuscolo per nomi ed etichette ("GAMBERO", "PREPARAZIONE:"), corsivo oro per le seconde voci ("dell'Atelier", "in un minuto").
- **Colori campionati dai post:** carta #EFEEDE, blu inchiostro #00314F, oro #8F7C4F (un filo più scuro del #9C8959 dei post, per leggerlo sulla carta), velluto #0A1A27 per le sezioni scure, che è il blu di fondo delle foto.
- **Trama:** carta con una trama puntinata leggerissima su tutta la pagina. Le fasce a retino tra le sezioni sono state tolte (20/11: niente puntini sugli elementi).
- **Pattern:** il marchio "La gamma *dell'Atelier*" con la barra blu sotto, come "i MENÙ dell'Atelier"; la scheda materia prima come il post "Gambero"; le tre voci del prezzo come il menù di Natale, con i polpi ad acquerello.

## Sezioni
1. **Hero:** nel cerchio si vede la foto intera dei paccheri; scorrendo cresce insieme all'oblò fino a tutto schermo e finisce sulla firma "i piatti *dell'Atelier*".
2. **Da dove parte il prezzo (la materia prima):** gambero e polpo disegnati ad acquerello blu, come il polpo dei materiali approvati (20/11: il cliente non vuole i gamberi a puntini). Su desktop la tavola resta ferma a destra e il disegno cambia con la specie, "dipingendosi" da sinistra; su telefono e senza JS i disegni stanno negli articoli. Il gambero ad acquerello è disegnato in codice (`tools/gambero-acquerello/`): se l'illustratore ne fornisce uno, si sostituisce `assets/img/decori/gambero-acquerello.webp`.
3. **Dal pack al piatto:** PACK (la busta) → *Ricetta* (polpo ad acquerello e riga di menù) → PIATTO (foto dei tagliolini).
4. **Video**, 5. **La gamma *dell'Atelier***, 6. **Il prezzo *in tre portate***, 7. **Buyer e form Netlify**, 8. **Footer.**

## Da validare
- Copy proposti da me: titolo hero "Piatti di mare da ristorante, in pochi minuti", "i piatti dell'Atelier", "Il prezzo in tre portate".
- Logo: il marchio verticale approvato (Fish_Atelier_-_Logo_CMYK). Per header scuro e footer ho fatto la versione in negativo (blu → carta, oro schiarito): da far vedere al cliente.
- I testi di gambero e polpo vengono dai materiali approvati; gli abbinamenti specie → referenze li ho dedotti dai nomi della gamma; −18 °C e 17 referenze sono da confermare.
- Manca ancora la foto "in padella" e il video: la tappa 2 usa l'acquerello, il video ha un segnaposto.
- **Dati per referenza (20/11):** la fascia unica "Conservazione / In padella / Referenze / Dal" è stata tolta: ogni card della gamma ha i suoi dati (conservazione, minuti in padella, formato). In padella 5–8 min per i gamberi viene dal post "Gambero"; per le altre referenze è "da definire". Si compilano in `tools/genera-index.py` (dizionario `PADELLA` e formati in `IN_GAMMA`).
