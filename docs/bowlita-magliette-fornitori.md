# Bowlita Poke — Ricerca fornitori magliette personalizzate

Rilevazione: 27 agosto 2026. Dossier visuale: https://claude.ai/code/artifact/fd308c98-c3ca-48de-94ae-387db68fcab9

## Verdetto per fascia di quantità

| Scenario | Fornitore | Prezzo indicativo |
|---|---|---|
| 10–25 pz, subito | **CityShirt** | ~€10/pz (10–24) |
| 50–100 pz, budget | **Stampasi** | da €2,47/pz a 100 |
| Merch da vendere | **Printful** (POD) | nessun minimo, costo/pz alto |

## Confronto completo

| Fornitore | Prezzo indicativo | Minimo | Consegna | Tecniche | Nota |
|---|---|---|---|---|---|
| CityShirt (cityshirt.it, Napoli) | €15 (1pz) · €12 (5–9) · €10 (10–24) · €8,50 (25–49) | 1 pezzo | 24–48h | DTG, serigrafia, ricamo | Bozza gratis. Spedizione gratis >€49,90, altrimenti €5,90. **In ferie fino al 31/08, lavorazione dal 1/09.** |
| Stampaprint (stampaprint.net) | da €1,59–2 | nessuno | 48h | serigrafia, transfer | Controllo file base gratis; "controlla e perfeziona" €29,99 |
| Stampasi (stampasi.it) | da €2,47 a 100 pz | 10/25/50/100 per modello | 10 gg lav. | serigrafia, DTG, transfer, ricamo | Bozza inclusa, spedizione gratis. ~4,5★ / ~700 rec. Trustpilot |
| Teefactory (teefactory.it) | su preventivo | ~10, per modello | su commessa | serigrafia, DTG, DTF, ricamo | Linea HORECA dedicata a ristoranti (t-shirt, polo, camicie) |
| Helloprint (helloprint.com/it-it) | su preventivo | basso | variabile | stampa, ricamo | Categoria "magliette da lavoro", bozza gratuita |
| Camaloon (camaloon.it) | su configuratore | basso | variabile | serigrafia, digitale | Configuratore semplice, ottima assistenza. Prezzi medi |
| Vistaprint (vistaprint.it) | da €15/pz | 1–5 pz | rapida | serigrafia, DTG, ricamo | Il più caro. Piano B |
| Printful (printful.com/it) | alto/pz | nessuno | su ordine | DTG, ricamo | Print on demand + dropshipping, no canone. Solo merch |

**Attenzione ai prezzi civetta:** "da €1,59" e "da €2,47" sono capi promozionali leggeri (130–150 g/m²) al massimo scaglione. Per una t-shirt 180–190 g/m² con logo 1 colore la forbice reale è **€7–11/pz a 25 pezzi** (fornitori IT) e **€13–16/pz** (Vistaprint).

## Tecnica di stampa

- **Serigrafia** — >25 pz, logo 1–2 colori. Impianti €25–50/colore una tantum, poi il €/pz più basso. Più resistente ai lavaggi.
- **DTG** — nessun impianto, ottimo per piccole tirature e loghi multicolore. Sbiadisce prima su capi scuri.
- **DTF** — compromesso: nessun impianto, colori pieni su nero, tenuta migliore del DTG. Ideale 10–30 pz su capo scuro.
- **Ricamo** — il più duraturo. Richiede digitalizzazione una tantum (€20–60), no dettagli <5 mm.

**Consiglio:** due lotti — t-shirt DTF/serigrafia per la cucina, polo con logo ricamato per la sala.

## Scheda prodotto da configurare

- **Capo:** t-shirt unisex girocollo, 100% cotone ring-spun pettinato, 180–190 g/m². Equivalenti: Gildan Softstyle 64000, B&C #E190, Stanley/Stella Creator, Fruit of the Loom Iconic 195
- **Colore:** nero (cucina), bianco o colore brand (sala). Evitare grigi mélange
- **Fronte:** logo cuore sinistro, 8–10 cm di larghezza
- **Retro (opz.):** logo grande centrato alto, 28–30 cm. +€3–5/pz
- **Tecnica:** DTF o serigrafia 1 colore sopra i 25 pz
- **Curva taglie (10 pz):** 1×S · 3×M · 3×L · 2×XL · 1×XXL. +2–3 pz di scorta
- **File:** serigrafia/ricamo → vettoriale .ai/.eps/.pdf/.svg, testi in tracciati, Pantone Solid Coated. DTG/DTF → .png trasparente, 300 dpi a dimensione reale (30×40 cm = 3543×4724 px)

## Regole prima di pagare

1. Pretendere la bozza firmata con misure e posizioni, per iscritto
2. Ordinare un campione singolo prima del lotto se il fornitore è nuovo
3. Lavare il campione 3 volte a 60° prima di confermare

## Aperto

- **Manca il logo Bowlita in vettoriale** — non presente nel repo né su Dropbox
- Da definire: quantità e curva taglie, data di consegna, solo divise o anche merch

## Limite operativo

L'ordine non è eseguibile da questo ambiente: l'egress verso vistaprint.it, stampasi.it, cityshirt.it e printful.com è bloccato dal proxy di rete (lettura delle pagine solo via servizio esterno, nessun accesso ai configuratori né upload file). L'ordine richiede comunque account e metodo di pagamento del titolare.
