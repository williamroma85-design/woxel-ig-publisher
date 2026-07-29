# Woxel — sistema visivo dei post Instagram

Tutti i valori qui sono **misurati dagli asset pubblicati** in `new_posts/`
(20 post, 1080 × 1080), non ipotizzati. Se il renderer cambia, rimisura e aggiorna
questo file — la skill vale quanto i numeri che contiene.

## Token

| Token | Hex | RGB | Uso |
| --- | --- | --- | --- |
| `ink` | `#0F1A2E` | 15, 26, 46 | sfondo scuro / testo sul chiaro |
| `bone` | `#F4F4F2` | 244, 244, 242 | sfondo chiaro / testo sullo scuro |
| `ink-70` | `#3C4664` | — | subhead sul chiaro (ink al 70% su bone) |
| `bone-70` | `#BEC3D2` | — | subhead sullo scuro (bone al 70% su ink) |

Contrasto headline/sfondo misurato: **15.8:1** in entrambe le direzioni. I due tint al
70% sono gli unici colori derivati ammessi: stanno sulla retta ink↔bone, non sono un
terzo colore. Nessun altro colore entra nel sistema.

## Griglia (px, canvas 1080 × 1080)

```
y=0    ┌──────────────────────────────────────────┐
       │                                          │  ← aria: 110px
y=110  │  HEADLINE riga 1        cap height 64    │
y=183  │  HEADLINE riga 2        pitch 73         │
y=256  │  HEADLINE riga 3                         │
y=330  │  ────────────────────────────  rule 2px  │  x da 80 a 1000
y=371  │  Subhead riga 1         cap height 26    │
y=414  │  Subhead riga 2         pitch 44         │
y=458  │  Subhead riga 3                          │
       │                                          │
       │        ← zona bassa: oggi vuota →        │
       │                                          │
y=996  │                                    ██ W  │  logo x 940–1040
y=1040 └──────────────────────────────────────────┘  margine 40
        x=80                              x=1000
```

- margine sinistro `80` — headline, riga e subhead condividono lo stesso filo
- la riga orizzontale finisce a `x=1000`, non a `1080`
- il logotipo è l'unico elemento che entra nella fascia `x>1000` / `y>1000`

## Alternanza degli sfondi

Il piano editoriale alterna rigorosamente, post per post: `16` ink, `17` bone, `18` ink…
fino a `35` bone. Dieci scuri, dieci chiari. Nella griglia del profilo l'effetto è una
scacchiera. Quando aggiungi post, continua l'alternanza — `lint_copy.py` segnala due
sfondi uguali consecutivi.

## Stato attuale — cosa non funziona

`audit_post.py` sui 20 post pubblicati: **0 errori, 20 warning**, tutti lo stesso.

Fra la fine del subhead e il logotipo ci sono **da 507 a 630px di canvas vuoto**, cioè
il **47–58% dell'altezza**. Non è respiro: è metà poster che non fa niente. Tutti i
post soffrono dello stesso squilibrio, quindi la griglia del profilo è uniformemente
sbilanciata verso l'alto.

Tre modi per risolverlo, in ordine di preferenza:

1. **Centro ottico** — sposta il blocco headline+riga+subhead in basso di ~200px, così
   l'aria sopra e sotto si equivale. Intervento minimo sul renderer, effetto immediato.
2. **Numerale d'archivio** — il numero del post (`16`…`35`) in grande, allineato in
   basso a sinistra, nel tint al 70%. Dà ritmo alla serie e riempie la zona bassa senza
   aggiungere copy.
3. **Fascia di piede** — banda piena del colore di foreground negli ultimi ~180px, con
   il logo e `woxel.it` in negativo. Chiude il poster e rafforza il brand nel feed.

Non risolverlo ingrandendo la headline: a 4+ righe il carattere condensato perde forza
e la gerarchia si appiattisce.

## Copy — stato attuale

`lint_copy.py` su `editorial_plan_data.json` segnala 3 post su 20:

| Post | Problema | Correzione |
| --- | --- | --- |
| `17-lead-mai-piu-perso` | `MAI PIU’.` — apostrofo al posto dell'accento | `MAI PIÙ.` |
| `19-valore-del-tuo-tempo` | headline senza punto finale | aggiungi il punto |
| `27-caso-studio-avvocato` | riga di 21 caratteri, sfora la colonna | spezza la riga o accorcia |

## Esempio prima/dopo

`35-roi-30-giorni` — headline su 2 righe, subhead su 2, contenuto che finisce a `y=370`,
poi **626px di vuoto**.

Prima: blocco a `y=110`, logo a `y=996`, in mezzo nulla.

Dopo (opzione 1): blocco a `y=300`, contenuto che finisce a `y=560`, aria sopra `300` e
sotto `436` — il poster respira in modo simmetrico e la headline cade nel punto in cui
l'occhio entra nell'immagine quadrata.

## Come verificare

```bash
pip install pillow
python3 .claude/skills/taste/scripts/audit_post.py new_posts/
python3 .claude/skills/taste/scripts/lint_copy.py
```

Entrambi escono con codice 1 se trovano problemi bloccanti, quindi si possono agganciare
a un workflow GitHub Actions se un giorno gli asset verranno generati nel repo.
