---
name: taste
description: Design taste for Woxel Instagram posts — the visual system, composition rules, and copy constraints behind the 1080×1080 carousel assets in new_posts/. Use when creating, reviewing, critiquing, or fixing a post image, when writing or editing the `h` / `s` / `caption` fields in editorial_plan_data.json, or when the user asks to improve the look, layout, typography, or design of Woxel posts.
---

# Woxel post taste

The Woxel feed is one thing: **flat two-colour typographic posters**. No photos, no
gradients, no drop shadows, no icons, no stock illustration. All the design work happens
in typography, spacing, and the alternation of two colours down the grid. Anything that
breaks that reads as a different brand.

Before touching a post, look at 2–3 existing assets in `new_posts/` with the Read tool.
Match what is there; do not reinvent it.

## The system (measured from shipped assets)

Canvas — 1080 × 1080, RGB, PNG.

Palette — exactly two colours, no third:

| Token | Hex | Role |
| --- | --- | --- |
| ink | `#0F1A2E` | deep navy |
| bone | `#F4F4F2` | warm off-white |

Every post is either ink-on-bone or bone-on-ink. In `editorial_plan_data.json` the pair
lives in `b` (background) and `f` (foreground). **The feed alternates**: the plan runs a
strict 50/50 split (10 dark, 10 light). When adding posts, keep the alternation — two
consecutive posts on the same background flatten the grid.

Type — one condensed grotesque for headlines (heavy weight, all caps, tight tracking),
one humanist sans for the subhead. Never mix in a third family, never use italic, never
use a serif.

Grid, in pixels:

- left margin `80`, right rule ends at `1000` (rule width `920`)
- headline block starts at `y = 110`
- headline: cap height ≈ `64`, line pitch ≈ `73`, max 3 lines
- hairline rule directly under the headline, 2px, full `80 → 1000`
- subhead: cap height ≈ `26`, line pitch ≈ `44`, starts ≈ `50` below the rule
- logotype: bottom-right, occupying roughly `x 940–1040`, `y 996–1040`

Subhead colour is the foreground at ~70% opacity against the background — a step down
from the headline, never the same weight.

## Composition rules

1. **Kill the dead half.** The single worst trait of the current assets is that all the
   ink sits in the top ~45% and the bottom ~500px is empty. A post is finished when the
   lower zone earns its space. Fix it with one of these, never with more type:
   - anchor the text block to the optical centre (leave roughly equal air above and
     below) and keep only the logotype in the footer, or
   - add one supporting element in the lower zone: an oversized post numeral, a second
     hairline, a full-bleed colour band, or a short CTA line at the baseline.
   Do not fill space by making the headline bigger than 3 lines' worth of content.
2. **One focal point.** The headline wins. If the subhead competes on size or weight,
   shrink the subhead.
3. **Margins are inviolable.** Nothing but the logotype crosses `x < 80`, `x > 1000`, or
   `y > 1000`. Instagram crops the grid preview to a centre square — keep the headline
   clear of the outer `~60px` on every side.
4. **Ragged right, never justified, never centred.** Left-aligned flush edge at `x = 80`
   for headline, rule, and subhead alike. The shared left edge is the whole layout.
5. **Break headline lines on meaning**, not on width. `IL DENTISTA / CHE RISPONDE /
   SEMPRE.` reads; `IL DENTISTA CHE / RISPONDE SEMPRE.` does not.
6. **Contrast stays above 12:1.** The two brand colours give ~14.9:1 — do not tint,
   fade, or overlay them to something weaker.

## Copy constraints (the `h`, `s`, `caption` fields)

- `h` — headline. All caps, 2–3 lines, ≤ 18 characters per line, **ends with a period**.
  The period is part of the brand voice: declarative, closed, no hype.
- Use real typographic characters. `PIÙ`, not `PIU'` or `PIU’`. Accented capitals exist;
  a straight or curly apostrophe standing in for an accent is a typographic error and it
  is visible at 1080px. Same for `È` (never `E'`).
- `s` — subhead. 1–3 lines, ≤ 150 characters, short declarative sentences separated by
  full stops. No question marks in the subhead; the headline does the hooking.
- `caption` — Italian, short lines, one idea per line, blank line between blocks, a
  `👉 Link in bio` CTA, then 8–12 hashtags on the last line. Emoji only in the CTA line.
- Voice: second person singular, present tense, concrete numbers over adjectives
  (`in 30 secondi`, `ROI in 30 giorni`), no exclamation marks, no "rivoluzionario",
  no "game changer".

## Reviewing a post

Run the auditor, then read the image and judge what the script cannot:

```bash
python3 .claude/skills/taste/scripts/audit_post.py new_posts/            # all posts
python3 .claude/skills/taste/scripts/audit_post.py new_posts/35-roi-30-giorni.png
python3 .claude/skills/taste/scripts/lint_copy.py                        # h / s / caption
```

`audit_post.py` needs Pillow (`pip install pillow`) and checks canvas size, palette
purity, safe margins, contrast, logotype placement, and the dead-space ratio.
`lint_copy.py` is stdlib-only and checks the plan's copy fields: headline length and
case, the closing period, fake accents (`PIU’` → `PIÙ`), subhead length, hashtag count,
the CTA, and the ink/bone alternation. Neither can judge line breaks, hierarchy, or
whether the writing is any good — do that by eye, with the image open, against the
rules above.

Report findings as concrete edits ("headline breaks after CHE — move RISPONDE up"), not
as adjectives ("feels unbalanced").

## When generating new post images

The renderer lives outside this repo — this repo only publishes the PNGs. If asked to
generate images here, first say so and confirm the approach, then match the measured
grid above exactly, and embed the real brand fonts rather than substituting DejaVu or
Liberation, which will silently change the look of the whole feed.

See `references/design-system.md` for the full token table, the per-post colour
alternation map, and worked before/after examples.
