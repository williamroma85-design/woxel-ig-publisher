# Graph Report - woxel-ig-publisher  (2026-08-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 39 nodes · 65 edges · 8 communities (5 shown, 3 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cd04d285`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- refresh_token.py
- main
- woxel_daily_publish.py
- upload_image_any
- publish_post
- graphify-guard.sh
- graphify-session-start.sh
- get_github_creds

## God Nodes (most connected - your core abstractions)
1. `upload_image_any()` - 11 edges
2. `log()` - 7 edges
3. `main()` - 6 edges
4. `publish_post()` - 6 edges
5. `main()` - 5 edges
6. `get_ig_user_id()` - 5 edges
7. `multipart_upload()` - 5 edges
8. `ensure_github_repo()` - 4 edges
9. `gh_api()` - 4 edges
10. `upload_image_github()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `upload_image_any()` --indirect_call--> `_upload_0x0()`  [INFERRED]
  woxel_daily_publish.py → woxel_daily_publish.py  _Bridges community 2 → community 3_
- `get_ig_user_id()` --calls--> `log()`  [EXTRACTED]
  woxel_daily_publish.py → woxel_daily_publish.py  _Bridges community 1 → community 3_
- `main()` --calls--> `publish_post()`  [EXTRACTED]
  woxel_daily_publish.py → woxel_daily_publish.py  _Bridges community 1 → community 4_
- `publish_post()` --calls--> `log()`  [EXTRACTED]
  woxel_daily_publish.py → woxel_daily_publish.py  _Bridges community 3 → community 4_
- `upload_image_any()` --calls--> `get_github_creds()`  [EXTRACTED]
  woxel_daily_publish.py → woxel_daily_publish.py  _Bridges community 3 → community 7_

## Import Cycles
- None detected.

## Communities (8 total, 3 thin omitted)

### Community 0 - "refresh_token.py"
Cohesion: 0.39
Nodes (7): encrypt_for_github(), gh_request(), log(), main(), Chiama Meta /refresh_access_token e ritorna (nuovo_token, expires_in_seconds)., Cripta il segreto con la public key del repo (libsodium sealed box)., refresh_meta_token()

### Community 1 - "main"
Cohesion: 0.29
Nodes (7): get_ig_user_id(), get_token(), http_get(), main(), Resolve IG user ID from token., Data odierna in Europe/Rome — il runner GitHub Actions è in UTC., today_in_rome()

### Community 2 - "woxel_daily_publish.py"
Cohesion: 0.53
Nodes (5): multipart_upload(), Send a multipart/form-data POST. Returns raw response bytes., _upload_0x0(), _upload_catbox(), _upload_tmpfiles()

### Community 3 - "upload_image_any"
Cohesion: 0.60
Nodes (6): ensure_github_repo(), gh_api(), log(), Host preferito: GitHub raw (compatibile con Meta). Fallback:…, upload_image_any(), upload_image_github()

### Community 4 - "publish_post"
Cohesion: 0.50
Nodes (4): convert_png_to_jpeg(), http_post(), publish_post(), Converte PNG in JPEG (richiesto da IG Content Publishing). Ritorna path JPEG…

## Knowledge Gaps
- **3 isolated node(s):** `graphify-guard.sh script`, `PATH`, `graphify-session-start.sh script`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `upload_image_any()` connect `upload_image_any` to `woxel_daily_publish.py`, `publish_post`, `get_github_creds`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `get_ig_user_id()` connect `main` to `woxel_daily_publish.py`, `upload_image_any`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `upload_image_any()` (e.g. with `_upload_0x0()` and `_upload_tmpfiles()`) actually correct?**
  _`upload_image_any()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify-guard.sh script`, `PATH`, `graphify-session-start.sh script` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._