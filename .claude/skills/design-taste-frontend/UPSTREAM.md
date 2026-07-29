# Provenance

- Source: https://github.com/Leonxlnx/taste-skill (MIT, © 2026 Leonxlnx)
- File installed: `skills/taste-skill/SKILL.md` → `SKILL.md` (unmodified)
- Upstream commit at install time: `e988add` (2026-07-23)
- Version: v2 (experimental). Upstream preserves the previous release as
  `taste-skill-v1` / install name `design-taste-frontend-v1`.

## Aggiornare

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

oppure, senza npx, ricopiando il file dall'upstream:

```bash
git clone --depth 1 https://github.com/Leonxlnx/taste-skill.git /tmp/taste-skill
cp /tmp/taste-skill/skills/taste-skill/SKILL.md .claude/skills/design-taste-frontend/SKILL.md
```

## Ambito

La skill copre **landing page, portfolio e redesign web**. Dichiara fuori scope
dashboard, tabelle dati e UI di prodotto multi-step, e non riguarda i post 1080×1080 di
Instagram: per quelli vale la skill `taste` in `.claude/skills/taste/`, che contiene il
sistema visivo Woxel misurato dagli asset reali.

Nel repo `woxel-ig-publisher` (publisher Python, nessun frontend) questa skill non si
attiverà da sola. È qui per i progetti web Woxel — sito, landing, pagine demo — quando
verranno lavorati da questa stessa sessione o copiando la cartella in `~/.claude/skills/`.

## Altre skill disponibili nello stesso repo upstream

`brandkit` (brand board e sistemi logo), `imagegen-frontend-web`, `imagegen-frontend-mobile`,
`redesign-skill`, `minimalist-skill`, `brutalist-skill`, `soft-skill`, `stitch-skill`,
`image-to-code-skill`, `output-skill`. Nessuna è installata: chiedi se ne serve una.
