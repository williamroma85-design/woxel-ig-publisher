#!/usr/bin/env python3
"""
Refresh Meta long-lived Instagram Business token via /refresh_access_token,
then write the new token back into the GitHub repository secret WOXEL_META_TOKEN.

Designed to run weekly via .github/workflows/refresh-token.yml.

Required env vars:
  WOXEL_META_TOKEN  — current long-lived token (will be replaced)
  GH_PAT            — classic PAT with `repo` scope (can update repo secrets)
  GITHUB_REPOSITORY — owner/repo (auto-set by Actions)
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from base64 import b64encode

REFRESH_URL = 'https://graph.instagram.com/refresh_access_token'
SECRET_NAME = 'WOXEL_META_TOKEN'


def log(msg):
    print(msg, flush=True)


def refresh_meta_token(token):
    """Chiama Meta /refresh_access_token e ritorna (nuovo_token, expires_in_seconds)."""
    qs = urllib.parse.urlencode({
        'grant_type': 'ig_refresh_token',
        'access_token': token,
    })
    url = f'{REFRESH_URL}?{qs}'
    req = urllib.request.Request(url, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        raise RuntimeError(f"Refresh fallito: HTTP {e.code} {body}")
    new_token = data.get('access_token')
    expires_in = int(data.get('expires_in') or 0)
    if not new_token:
        raise RuntimeError(f"Risposta Meta senza access_token: {data}")
    return new_token, expires_in


def gh_request(method, path, gh_token, body=None):
    url = f'https://api.github.com{path}'
    headers = {
        'Authorization': f'token {gh_token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'WoxelTokenRefresher/1.0',
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            txt = r.read().decode('utf-8', errors='replace')
            return r.status, (json.loads(txt) if txt else {})
    except urllib.error.HTTPError as e:
        txt = e.read().decode('utf-8', errors='replace')
        try:
            return e.code, json.loads(txt)
        except Exception:
            return e.code, {'_raw': txt}


def encrypt_for_github(public_key_b64, secret_value):
    """Cripta il segreto con la public key del repo (libsodium sealed box)."""
    from nacl import encoding, public  # type: ignore
    pk = public.PublicKey(public_key_b64.encode('utf-8'), encoding.Base64Encoder())
    sealed_box = public.SealedBox(pk)
    encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
    return b64encode(encrypted).decode('utf-8')


def main():
    meta_token = os.environ.get('WOXEL_META_TOKEN', '').strip()
    gh_pat     = os.environ.get('GH_PAT', '').strip()
    repo       = os.environ.get('GITHUB_REPOSITORY', '').strip()

    if not meta_token:
        log("ERRORE: secret WOXEL_META_TOKEN mancante.")
        sys.exit(1)
    if not gh_pat:
        log("ERRORE: secret GH_PAT mancante (serve scope `repo` per aggiornare i secret).")
        sys.exit(1)
    if not repo or '/' not in repo:
        log(f"ERRORE: GITHUB_REPOSITORY non valido: '{repo}'")
        sys.exit(1)

    log(f"Repo target: {repo}")
    log("→ Chiamo /refresh_access_token su graph.instagram.com …")
    new_token, expires_in = refresh_meta_token(meta_token)
    days = expires_in // 86400
    log(f"  Nuovo token ottenuto (lunghezza={len(new_token)}). Scade tra {days} giorni "
        f"(~{expires_in} secondi).")

    if new_token == meta_token:
        log("  Nota: il nuovo token coincide col precedente (Meta a volte non lo ruota se troppo recente). "
            "Aggiorno comunque il secret per sicurezza.")

    log(f"→ Recupero public key del repo per criptare il secret …")
    code, key_data = gh_request('GET', f'/repos/{repo}/actions/secrets/public-key', gh_pat)
    if code != 200:
        log(f"ERRORE recupero public key: HTTP {code} {key_data}")
        sys.exit(1)
    key_id = key_data['key_id']
    public_key_b64 = key_data['key']

    log(f"→ Cripto e aggiorno il secret '{SECRET_NAME}' …")
    encrypted = encrypt_for_github(public_key_b64, new_token)
    code, resp = gh_request('PUT', f'/repos/{repo}/actions/secrets/{SECRET_NAME}', gh_pat, {
        'encrypted_value': encrypted,
        'key_id': key_id,
    })
    if code not in (201, 204):
        log(f"ERRORE update secret: HTTP {code} {resp}")
        sys.exit(1)

    log(f"  ✅ Secret '{SECRET_NAME}' aggiornato. HTTP {code}.")
    log(f"=== Token rinnovato. Prossima scadenza tra ~{days} giorni. ===")


if __name__ == '__main__':
    main()
