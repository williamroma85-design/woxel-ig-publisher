# Bowlita Poke — Fornitori magliette, consegna entro ven 4 settembre 2026

Rilevazione: 30 agosto 2026. Dossier: https://claude.ai/code/artifact/fd308c98-c3ca-48de-94ae-387db68fcab9

## Vincoli

- Consegna entro **venerdì 4 settembre 2026**. Oggi è domenica 30/08 → 5 giorni lavorativi (lun 31 → ven 4)
- Ordine unico con **taglie assortite** (blocco)
- Due posizioni di stampa: **petto fronte alto a sinistra** + **retro centrale grande**

## Verdetto

| Ordine | Fornitore | Consegna prevista |
|---|---|---|
| Lun 31 entro 12:00 | **Errebipromo** | mar 1 set — 3 giorni di margine |
| Lun 31 | **Stampaprint** | mer 2 set — il più economico |
| Mar 1 (riapre) | **CityShirt** | gio 3 set — verificare arretrato ferie |

## Confronto (ordinando lun 31 agosto)

| Entro ven 4? | Fornitore | Tempi | Taglie | Costo | Nota |
|---|---|---|---|---|---|
| SÌ · mar 1 | **Errebipromo** | ordine entro 12:00 → spedito stesso giorno → 1 gg lav. | XS–3XL | spedizione sempre gratis, prezzi **IVA esclusa** | Produttore diretto, DTG/DTF/ricamo in casa in Italia. Da 1 a 500 pz. Supporto grafico gratuito. Isole/montagna 2 gg. Sconti fino al 40% oltre 100 pz |
| SÌ · mer 2 | **Stampaprint** | 48h | XS–3XL | da €2 stampa logo | Nessun minimo. Fronte, retro e maniche. Ristampa gratuita se non soddisfatto. Controllo file base gratis / prof. €5 / fix €29,99 |
| SÌ · mar 1–mer 2 | **T-ShirtPersonalizzate** | ordine entro 10:00 → spedito stesso giorno | sì | spedizione gratis >€89 | Opzione "lavorazione 24H" da spuntare al checkout, non automatica |
| SÌ ma rischioso · gio 3 | **CityShirt** | 24–48h, da mar 1 | sì | €8,50/pz a 25–49 + €3–5 retro | Chiuso per ferie fino al 31/08. Confermare la data al telefono prima di pagare |
| FORSE | Stampamaglie (Ravenna) | 24–48h GLS | sì | da configuratore | Piano C |
| FORSE | Teetogo | 24–48h | sì | da €17,90/pz | Spedizione gratis >€30 ma prezzo di partenza alto |
| FORSE, caro | Vistaprint | express a pagamento | sì (editor esplicito) | da €15/pz + express | Quasi il doppio. Piano di emergenza |
| **NO** | Stampasi | 10 gg lavorativi | — | da €2,47/pz | Consegnerebbe ~14 settembre. Da tenere per il riordino |
| **NO** | Printful | POD dall'estero | — | alto/pz | Fuori scopo per consegna a data fissa |

## Blocco a taglie assortite

Funziona su tutti i fornitori della rosa: si carica la grafica **una volta**, poi una griglia con una casella per taglia; il carrello somma in un unico articolo.

- **Lo sconto quantità si calcola sul totale del blocco, non per taglia.** 4 pezzi × 5 taglie = 20 pz allo scaglione dei 20
- Errebipromo: t-shirt uomo XS–3XL, polo uomo S–3XL. **T-shirt donna solo fino a XXL, polo donna solo fino a L** → se servono taglie superiori, usare il modello unisex/uomo per tutti
- Stampaprint: XS–3XL
- **Da verificare al carrello:** che il prezzo unitario mostrato sia quello dello scaglione del totale

## Scheda prodotto

- **Capo:** t-shirt unisex girocollo, 100% cotone 190 g/m². Su Errebipromo: `B&C Collection TU01T` (Express24h). Equivalenti: `B&C #E190`, `Gildan Softstyle 64000`, `Fruit of the Loom Iconic 195`
- **Colore:** nero (cucina) / bianco o colore brand (sala). Evitare grigi mélange
- **Stampa 1 — petto:** fronte alto a sinistra, larghezza **8–10 cm**, ~7–8 cm sotto la cucitura spalla, ~5–6 cm dal centro petto
- **Stampa 2 — retro:** centrale, larghezza **28–30 cm**, bordo superiore ~8–10 cm sotto la cucitura collo. Errebipromo lavora il retro fino a 20×30 cm — verificare se il logo è quadrato o verticale
- **Tecnica:** **DTF** (due posizioni, capo scuro, <50 pz, nessun impianto, tiene i lavaggi meglio del DTG). Serigrafia solo sopra i 50 pz
- **File:** due `.png` distinti, fondo trasparente, 300 dpi a dimensione reale → petto 10 cm = **1181 px**, retro 30 cm = **3543 px**. Il file petto non è il retro rimpicciolito: va semplificato
- **Curva taglie (20 pz):** 2×S · 6×M · 6×L · 4×XL · 2×XXL

**Il retro aggiunge circa il 60–90% al costo di stampa.** Su CityShirt sono €3–5/pz dichiarati.

## Stime di spesa — 20 pz, cotone 190 g, DTF due posizioni

| Fornitore | Stima /pz | Stima 20 pz | Spedizione |
|---|---|---|---|
| Stampaprint | €8–12 | €160–240 | inclusa in 48h |
| Errebipromo | €11–15 + IVA | €220–300 + IVA | sempre gratis |
| CityShirt | €11,50–13,50 | €230–270 | gratis >€49,90 |
| Vistaprint | €18–22 | €360–440 | express a pagamento |

**Solo CityShirt pubblica un listino per scaglione.** Le altre righe sono stime costruite sui prezzi di partenza dichiarati: i configuratori di Errebipromo e Stampaprint calcolano il prezzo in JavaScript e da questo ambiente i loro siti sono bloccati dal proxy di rete. Trattare come ordine di grandezza, non come preventivo.

## Aperto

- **Manca ancora il logo Bowlita** — non nel repo, non su Dropbox. È il collo di bottiglia della scadenza
- Da confermare: curva taglie, colore capo, zona di consegna (Errebipromo 1 gg regioni principali, 2 gg isole/montagna)

## Limite operativo

L'ordine non è eseguibile da questo ambiente: egress bloccato verso i siti dei fornitori, nessun accesso ai configuratori né upload file. L'ordine richiede comunque account e metodo di pagamento del titolare.
