# woxel-ig-publisher

Publisher automatico per Instagram (account business Woxel). Gira su GitHub Actions.

## Struttura

- `woxel_daily_publish.py` — script principale. Legge il piano editoriale, trova il post
  del giorno, carica l'immagine (catena di fallback GitHub raw → catbox → 0x0 → tmpfiles)
  e pubblica via Instagram Graph API (`graph.instagram.com/v21.0`).
- `refresh_token.py` — rinnova il long-lived token Meta e riscrive il secret
  `WOXEL_META_TOKEN` nel repo tramite GitHub API.
- `editorial_plan_data.json` — piano editoriale (data, immagine, caption, hashtag).
- `new_posts/` — immagini dei post.
- `woxel_publish_log.txt` — log append-only delle pubblicazioni.
- `.github/workflows/publish.yml` — cron Lun/Mar/Gio/Ven 09:00 Europe/Rome.
- `.github/workflows/refresh-token.yml` — refresh periodico del token.

## Segreti

`WOXEL_META_TOKEN`, credenziali GitHub CDN (`WOXEL_CDN_REPO`) e i file
`woxel_token.txt` / `woxel_github.txt` non vanno mai committati (già in `.gitignore`).

## graphify

Questo progetto ha un knowledge graph in `graphify-out/` con god nodes, community
e relazioni cross-file.

Regole:
- Per domande sul codice, esegui prima `graphify query "<domanda>"` quando esiste
  `graphify-out/graph.json`. Usa `graphify path "<A>" "<B>"` per le relazioni e
  `graphify explain "<concetto>"` per concetti puntuali. Restituiscono un sottografo
  mirato, di solito molto più piccolo di `GRAPH_REPORT.md` o di un grep grezzo.
- Se esiste `graphify-out/wiki/index.md`, usalo per la navigazione ampia invece di
  sfogliare i sorgenti.
- Leggi `graphify-out/GRAPH_REPORT.md` solo per una review architetturale ampia o
  quando query/path/explain non bastano.
- Dopo aver modificato il codice, esegui `graphify update .` per tenere il grafo
  aggiornato (solo AST, nessun costo API).
- La skill è in `.claude/skills/graphify/SKILL.md`, trigger `/graphify`.

Se il comando `graphify` non è disponibile (container nuovo), installalo con
`python3 -m pip install --user graphifyy` — l'hook `SessionStart` in
`.claude/settings.json` prova a farlo automaticamente.
