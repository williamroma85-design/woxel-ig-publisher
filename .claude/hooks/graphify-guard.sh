#!/usr/bin/env bash
# PreToolUse guard per graphify.
# Se graphify non e' installato (o il grafo non esiste) esce in silenzio:
# un hook non deve mai rompere una sessione.
set -u

MODE="${1:-search}"

find_graphify() {
  if command -v graphify >/dev/null 2>&1; then command -v graphify; return 0; fi
  for c in "$HOME/.local/bin/graphify" "/usr/local/bin/graphify"; do
    [ -x "$c" ] && { echo "$c"; return 0; }
  done
  return 1
}

GRAPHIFY_BIN="$(find_graphify)" || exit 0
[ -f "${CLAUDE_PROJECT_DIR:-$PWD}/graphify-out/graph.json" ] || exit 0

exec "$GRAPHIFY_BIN" hook-guard "$MODE"
