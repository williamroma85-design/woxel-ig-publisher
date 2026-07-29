#!/usr/bin/env python3
"""
Lint the copy fields (`h`, `s`, `caption`) of editorial_plan_data.json against the
Woxel voice and typography rules.

Usage:
    python3 lint_copy.py                          # default plan file
    python3 lint_copy.py path/to/plan.json --json

Stdlib only. Exit code 1 if anything is flagged.
"""

import argparse
import json
import os
import re
import sys

DEFAULT_PLAN = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..',
    'editorial_plan_data.json',
)

MAX_HEADLINE_LINES = 3
MAX_HEADLINE_CHARS = 18
MAX_SUBHEAD_CHARS = 150
MAX_HASHTAGS = 12
MIN_HASHTAGS = 8

# Accented capitals typed as apostrophes — visible typographic errors at 1080px.
FAKE_ACCENT = re.compile(r"\b([A-ZÀ-Ü]+)['’](?=[\s.\n]|$)")
BANNED = ('rivoluzionar', 'game changer', 'incredibil', 'pazzesc')


def lint_post(post):
    issues = []
    headline = post.get('h', '')
    subhead = post.get('s', '')
    caption = post.get('caption', '')

    lines = headline.split('\n')
    if len(lines) > MAX_HEADLINE_LINES:
        issues.append(f"headline su {len(lines)} righe (max {MAX_HEADLINE_LINES})")
    for line in lines:
        if len(line) > MAX_HEADLINE_CHARS:
            issues.append(f"riga headline di {len(line)} char: “{line}”")
    if headline and not headline.rstrip().endswith('.'):
        issues.append("headline senza punto finale")
    if headline != headline.upper():
        issues.append("headline non in maiuscolo")
    for match in FAKE_ACCENT.finditer(headline):
        issues.append(f"accento reso con apostrofo: “{match.group(0)}” → usa À/È/Ù")

    if len(subhead) > MAX_SUBHEAD_CHARS:
        issues.append(f"subhead di {len(subhead)} char (max {MAX_SUBHEAD_CHARS})")
    if '?' in subhead:
        issues.append("punto interrogativo nel subhead — l'aggancio lo fa la headline")
    if '!' in subhead or '!' in headline:
        issues.append("punto esclamativo — fuori tono di voce")

    if caption:
        if 'Link in bio' not in caption:
            issues.append("caption senza CTA “Link in bio”")
        tags = re.findall(r'#\w+', caption)
        if not (MIN_HASHTAGS <= len(tags) <= MAX_HASHTAGS):
            issues.append(f"{len(tags)} hashtag (attesi {MIN_HASHTAGS}–{MAX_HASHTAGS})")
    for word in BANNED:
        if word in (headline + subhead + caption).lower():
            issues.append(f"parola fuori tono: “{word}”")

    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', nargs='?', default=os.path.normpath(DEFAULT_PLAN))
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    with open(args.plan, encoding='utf-8') as f:
        plan = json.load(f)

    results, alternation = [], []
    for week in plan.get('weeks', []):
        for post in week.get('posts', []):
            results.append({'post': post.get('n'), 'issues': lint_post(post)})
            alternation.append((post.get('n'), post.get('b')))

    # Two consecutive posts on the same background flatten the grid.
    for (prev_name, prev_bg), (name, bg) in zip(alternation, alternation[1:]):
        if prev_bg and prev_bg == bg:
            for r in results:
                if r['post'] == name:
                    r['issues'].append(f"stesso sfondo di {prev_name} — l'alternanza si rompe")

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        flagged = 0
        for r in results:
            if r['issues']:
                flagged += 1
                print(r['post'])
                for issue in r['issues']:
                    print(f"   {issue}")
        print(f"\n{len(results)} post · {flagged} da sistemare")

    return 1 if any(r['issues'] for r in results) else 0


if __name__ == '__main__':
    sys.exit(main())
