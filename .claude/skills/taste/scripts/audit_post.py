#!/usr/bin/env python3
"""
Audit Woxel Instagram post images against the brand design system.

Usage:
    python3 audit_post.py new_posts/                 # every PNG in the folder
    python3 audit_post.py new_posts/35-roi-30-giorni.png
    python3 audit_post.py new_posts/ --json

Checks what can be measured: canvas size, palette purity, safe margins, contrast,
logotype placement, vertical balance. Line breaks, hierarchy and copy quality still
need a human (or a Read of the image).

Requires Pillow:  pip install pillow
Exit code 1 if any post has an ERROR-level finding.
"""

import argparse
import json
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow non installato. Esegui: pip install pillow")

# ── Design tokens ─────────────────────────────────────────────────────────────
CANVAS = (1080, 1080)
INK = (0x0F, 0x1A, 0x2E)
BONE = (0xF4, 0xF4, 0xF2)
PALETTE = {'ink': INK, 'bone': BONE}

MARGIN_LEFT = 80
MARGIN_RIGHT = 1000        # right edge of the hairline rule
CONTENT_TOP = 110
LOGO_ZONE = (900, 960, 1080, 1080)   # x0, y0, x1, y1 — logotype may live here
MIN_CONTRAST = 12.0
MAX_DEAD_GAP = 300         # px of empty canvas between content and logotype
INK_THRESHOLD = 30         # per-channel delta that counts as "ink"
SAMPLE = 2                 # pixel sampling step


def relative_luminance(rgb):
    def channel(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def nearest_token(rgb, tolerance=12):
    for name, ref in PALETTE.items():
        if all(abs(rgb[i] - ref[i]) <= tolerance for i in range(3)):
            return name
    return None


def distance_to_brand_ramp(rgb):
    """
    Distance from the ink↔bone line in RGB space. Antialiasing and the 70%-opacity
    subhead both land on this ramp, so only colours far from it are real palette
    breaks.
    """
    ax, ay, az = INK
    dx, dy, dz = (BONE[i] - INK[i] for i in range(3))
    denom = dx * dx + dy * dy + dz * dz
    t = ((rgb[0] - ax) * dx + (rgb[1] - ay) * dy + (rgb[2] - az) * dz) / denom
    t = max(0.0, min(1.0, t))
    near = (ax + t * dx, ay + t * dy, az + t * dz)
    return sum((rgb[i] - near[i]) ** 2 for i in range(3)) ** 0.5


def is_ink(px, bg):
    return max(abs(px[i] - bg[i]) for i in range(3)) > INK_THRESHOLD


def in_logo_zone(x, y):
    x0, y0, x1, y1 = LOGO_ZONE
    return x0 <= x <= x1 and y0 <= y <= y1


def row_segments(rows, min_height=3):
    """Contiguous runs of rows that contain ink."""
    segments, start = [], None
    for y, count in enumerate(rows):
        if count and start is None:
            start = y
        elif not count and start is not None:
            if y - start >= min_height:
                segments.append((start, y - 1))
            start = None
    if start is not None:
        segments.append((start, len(rows) - 1))
    return segments


def audit(path):
    findings = []
    err = lambda m: findings.append(('ERROR', m))
    warn = lambda m: findings.append(('WARN', m))

    image = Image.open(path).convert('RGB')
    width, height = image.size
    px = image.load()

    if (width, height) != CANVAS:
        err(f"canvas {width}×{height}, atteso {CANVAS[0]}×{CANVAS[1]}")
        return {'file': path, 'findings': findings, 'metrics': {}}

    corners = [px[4, 4], px[width - 5, 4], px[4, height - 5]]
    bg = max(set(corners), key=corners.count)
    bg_token = nearest_token(bg)
    if bg_token is None:
        err(f"sfondo {'#%02X%02X%02X' % bg} fuori palette (ink #0F1A2E / bone #F4F4F2)")

    # Ink profiles.
    rows, cols = [0] * height, [0] * width
    fg_samples = {}
    for y in range(height):
        for x in range(0, width, SAMPLE):
            if is_ink(px[x, y], bg):
                rows[y] += 1
                cols[x] += 1
                if not in_logo_zone(x, y):
                    fg_samples[px[x, y]] = fg_samples.get(px[x, y], 0) + 1

    if not fg_samples:
        err("nessun contenuto rilevato sul canvas")
        return {'file': path, 'findings': findings, 'metrics': {}}

    fg = max(fg_samples, key=fg_samples.get)
    ratio = contrast_ratio(fg, bg)
    if ratio < MIN_CONTRAST:
        err(f"contrasto {ratio:.1f}:1 sotto il minimo {MIN_CONTRAST}:1")

    # Third colour: ignore antialiasing by only counting well-populated samples.
    total = sum(fg_samples.values())
    off_palette = {
        c: n for c, n in fg_samples.items()
        if n > total * 0.02 and distance_to_brand_ramp(c) > 24
    }
    if off_palette:
        worst = max(off_palette, key=off_palette.get)
        warn(f"colore fuori palette rilevato ({'#%02X%02X%02X' % worst}) — il sistema ne ammette due")

    # Margins (logotype excluded — it intentionally sits in the bleed).
    content_cols = [
        x for x in range(0, width, SAMPLE)
        if cols[x] and any(
            is_ink(px[x, y], bg) and not in_logo_zone(x, y)
            for y in range(0, height, SAMPLE)
        )
    ]
    left = min(content_cols) if content_cols else None
    right = max(content_cols) if content_cols else None
    if left is not None and left < MARGIN_LEFT - SAMPLE:
        err(f"contenuto a x={left}, oltre il margine sinistro di {MARGIN_LEFT}px")
    if right is not None and right > MARGIN_RIGHT + SAMPLE:
        warn(f"contenuto fino a x={right}, oltre il bordo della riga a {MARGIN_RIGHT}px")

    segments = row_segments(rows)
    content_segments = [s for s in segments if s[0] < LOGO_ZONE[1]]
    logo_segments = [s for s in segments if s[0] >= LOGO_ZONE[1]]

    if not logo_segments:
        err("logotipo assente nella fascia in basso a destra")
    if content_segments:
        top = content_segments[0][0]
        if abs(top - CONTENT_TOP) > 24:
            warn(f"il blocco testo parte a y={top}, la griglia lo vuole a y={CONTENT_TOP}")

        content_bottom = content_segments[-1][1]
        logo_top = logo_segments[0][0] if logo_segments else height
        dead_gap = logo_top - content_bottom
        if dead_gap > MAX_DEAD_GAP:
            warn(
                f"{dead_gap}px di canvas vuoto tra testo e logo "
                f"({dead_gap / height:.0%} dell'altezza) — la metà bassa non lavora"
            )
    else:
        content_bottom, dead_gap = None, None

    metrics = {
        'background': '#%02X%02X%02X' % bg,
        'background_token': bg_token,
        'foreground': '#%02X%02X%02X' % fg,
        'contrast': round(ratio, 1),
        'content_top': content_segments[0][0] if content_segments else None,
        'content_bottom': content_bottom,
        'dead_gap': dead_gap,
        'left_edge': left,
        'right_edge': right,
        'text_blocks': len(content_segments),
    }
    return {'file': path, 'findings': findings, 'metrics': metrics}


def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files.extend(
                os.path.join(p, f) for f in sorted(os.listdir(p))
                if f.lower().endswith('.png')
            )
        else:
            files.append(p)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+', help='PNG files or folders')
    parser.add_argument('--json', action='store_true', help='machine-readable output')
    args = parser.parse_args()

    results = [audit(f) for f in collect(args.paths)]

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            name = os.path.basename(r['file'])
            m = r['metrics']
            head = f"{name}"
            if m:
                head += (
                    f"  [{m['background_token'] or '?'} bg · contrasto {m['contrast']}:1"
                    f" · vuoto {m['dead_gap']}px]" if m.get('dead_gap') is not None
                    else f"  [{m['background_token'] or '?'} bg · contrasto {m['contrast']}:1]"
                )
            print(head)
            if not r['findings']:
                print("   ok")
            for level, msg in r['findings']:
                print(f"   {level}: {msg}")

        errors = sum(1 for r in results for lvl, _ in r['findings'] if lvl == 'ERROR')
        warns = sum(1 for r in results for lvl, _ in r['findings'] if lvl == 'WARN')
        print(f"\n{len(results)} post · {errors} error · {warns} warn")

    return 1 if any(lvl == 'ERROR' for r in results for lvl, _ in r['findings']) else 0


if __name__ == '__main__':
    sys.exit(main())
