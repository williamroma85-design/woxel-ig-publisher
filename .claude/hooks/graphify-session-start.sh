#!/usr/bin/env bash
# SessionStart hook: prepara graphify nei container effimeri (Claude Code on the web).
# - installa graphifyy se manca (disattivabile con GRAPHIFY_AUTO_INSTALL=0)
# - stampa un riepilogo del grafo esistente come contesto iniziale
set -u

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
export PATH="$HOME/.local/bin:$PATH"

if ! command -v graphify >/dev/null 2>&1 && [ "${GRAPHIFY_AUTO_INSTALL:-1}" = "1" ]; then
  timeout 300 python3 -m pip install --user --quiet --disable-pip-version-check graphifyy >/dev/null 2>&1 || true
fi

GRAPH="$PROJECT_DIR/graphify-out/graph.json"
if [ -f "$GRAPH" ]; then
  echo "graphify: knowledge graph disponibile in graphify-out/."
  echo "Usa 'graphify query \"<domanda>\"', 'graphify explain \"<nodo>\"', 'graphify path \"<A>\" \"<B>\"'"
  echo "prima di grep/read a tappeto. Dopo modifiche al codice: 'graphify update .'"
  if command -v graphify >/dev/null 2>&1; then
    timeout 60 graphify god-nodes --top 8 2>/dev/null || true
  fi
else
  echo "graphify: nessun grafo in graphify-out/. Costruiscilo con 'graphify .' per avere contesto persistente."
fi
exit 0
