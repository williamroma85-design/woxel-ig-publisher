#!/usr/bin/env python3
"""
Woxel Daily Instagram Publisher v2 — GitHub Actions edition
Uses Instagram Business Login API (graph.instagram.com) + image host fallback chain
(GitHub raw → catbox → 0x0 → tmpfiles).
Reads the editorial plan, finds today's post, and publishes it.
Runs automatically Mon / Tue / Thu / Fri at 09:00 Europe/Rome via GitHub Actions.
"""

import json, os, sys, time, tempfile, urllib.request, urllib.parse, urllib.error, uuid
from datetime import date

# ── Config ────────────────────────────────────────────────────────────────────
IG_API       = 'https://graph.instagram.com/v21.0'
CATBOX_URL   = 'https://catbox.moe/user/api.php'
ZEROX0_URL   = 'https://0x0.st'
TMPFILES_URL = 'https://tmpfiles.org/api/v1/upload'

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
GITHUB_API   = 'https://api.github.com'
GITHUB_REPO  = os.environ.get('WOXEL_CDN_REPO', 'woxel-ig-assets')
PLAN_FILE    = os.path.join(SCRIPT_DIR, 'editorial_plan_data.json')
POSTS_DIR    = os.path.join(SCRIPT_DIR, 'new_posts')
LOG_FILE     = os.path.join(SCRIPT_DIR, 'woxel_publish_log.txt')

def log(msg):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except Exception:
        pass

def get_token():
    tok = os.environ.get('WOXEL_META_TOKEN', '').strip()
    if not tok:
        raise RuntimeError(
            "WOXEL_META_TOKEN non trovato nell'ambiente. "
            "Imposta il secret nel repo: Settings → Secrets and variables → Actions → New repository secret."
        )
    return tok

def http_post(url, params, timeout=60):
    data = urllib.parse.urlencode(params).encode()
    req  = urllib.request.Request(url, data=data, method='POST')
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def http_get(url, timeout=30):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read())

def multipart_upload(url, fields, file_field, filename, file_bytes, content_type='application/octet-stream', timeout=30):
    """Send a multipart/form-data POST. Returns raw response bytes."""
    boundary = f'----WoxelBoundary{uuid.uuid4().hex}'
    body = b''
    for name, value in fields.items():
        body += f'--{boundary}\r\n'.encode()
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        body += f'{value}\r\n'.encode()
    body += f'--{boundary}\r\n'.encode()
    body += f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'.encode()
    body += f'Content-Type: {content_type}\r\n\r\n'.encode()
    body += file_bytes + b'\r\n'
    body += f'--{boundary}--\r\n'.encode()

    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    req.add_header('Content-Length', str(len(body)))
    req.add_header('User-Agent', 'WoxelPublisher/2.0')
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def get_github_creds():
    """PAT per il repo CDN (woxel-ig-assets). Letta dal secret GH_PAT."""
    tok = os.environ.get('GH_PAT', '').strip()
    if not tok:
        return None
    return tok

def gh_api(method, path, gh_token, body=None, timeout=30):
    url = f'{GITHUB_API}{path}'
    data = None
    headers = {
        'Authorization': f'token {gh_token}',
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'WoxelPublisher/2.0',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    if body is not None:
        data = json.dumps(body).encode()
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            txt = r.read().decode('utf-8', errors='replace')
            return r.status, (json.loads(txt) if txt else {})
    except urllib.error.HTTPError as e:
        txt = e.read().decode('utf-8', errors='replace')
        try:
            return e.code, json.loads(txt)
        except Exception:
            return e.code, {'_raw': txt}

def ensure_github_repo(gh_user, gh_token):
    code, data = gh_api('GET', f'/repos/{gh_user}/{GITHUB_REPO}', gh_token)
    if code == 200:
        default_branch = data.get('default_branch', 'main')
        for wait in (0, 2, 4, 6):
            if wait:
                time.sleep(wait)
            c, d = gh_api('GET', f'/repos/{gh_user}/{GITHUB_REPO}/git/refs/heads/{default_branch}', gh_token)
            if c == 200:
                return
        raise RuntimeError(f"Repo esiste ma ref {default_branch} non trovato dopo retry.")
    if code == 404:
        log(f"    Repo {gh_user}/{GITHUB_REPO} non esiste. Creo ora …")
        code2, data2 = gh_api('POST', '/user/repos', gh_token, {
            'name': GITHUB_REPO,
            'description': 'Woxel IG Publisher image hosting (auto-managed)',
            'private': False,
            'auto_init': True,
        })
        if code2 not in (200, 201):
            raise RuntimeError(f"Creazione repo fallita: HTTP {code2} {data2}")
        default_branch = data2.get('default_branch', 'main')
        log(f"    Repo creato: https://github.com/{gh_user}/{GITHUB_REPO} (branch: {default_branch})")
        for wait in (2, 3, 5, 8, 13):
            time.sleep(wait)
            c, d = gh_api('GET', f'/repos/{gh_user}/{GITHUB_REPO}/git/refs/heads/{default_branch}', gh_token)
            if c == 200:
                log(f"    Branch {default_branch} pronto.")
                return
            log(f"    Branch non ancora pronto (HTTP {c}), riprovo …")
        raise RuntimeError(f"Branch {default_branch} non disponibile dopo creazione repo.")
    raise RuntimeError(f"Check repo fallito: HTTP {code} {data}")

def upload_image_github(image_path, gh_user, gh_token):
    import base64
    with open(image_path, 'rb') as f:
        content_b64 = base64.b64encode(f.read()).decode()
    base = os.path.basename(image_path)
    filename = f"{int(time.time())}_{uuid.uuid4().hex[:8]}_{base}"
    path = f'/repos/{gh_user}/{GITHUB_REPO}/contents/{filename}'
    last_err = None
    for attempt, wait in enumerate([0, 2, 4, 8], start=1):
        if wait:
            time.sleep(wait)
        code, data = gh_api('PUT', path, gh_token, {
            'message': f'Upload {filename}',
            'content': content_b64,
        })
        if code in (200, 201):
            url = data.get('content', {}).get('download_url')
            if not url:
                raise RuntimeError(f"Upload GitHub: download_url assente: {data}")
            return url
        last_err = (code, data)
        log(f"    GitHub PUT tentativo {attempt} HTTP {code}: {data.get('message', data)}")
        if code not in (404, 422, 409):
            break
    raise RuntimeError(f"Upload GitHub fallito dopo retry: HTTP {last_err[0]} {last_err[1]}")

def convert_png_to_jpeg(png_path):
    """Converte PNG in JPEG (richiesto da IG Content Publishing). Ritorna path JPEG temporaneo.
    Usa Pillow (cross-platform, installato via requirements.txt nel workflow)."""
    tmp_jpg = os.path.join(tempfile.gettempdir(), f"woxel_{uuid.uuid4().hex}.jpg")
    try:
        from PIL import Image  # type: ignore
        im = Image.open(png_path).convert('RGB')
        im.save(tmp_jpg, 'JPEG', quality=90)
        return tmp_jpg
    except Exception as e:
        raise RuntimeError(f"Conversione PNG→JPEG fallita: {e}. "
                           "Verifica che Pillow sia installato (pip install Pillow).")

def _upload_0x0(img_bytes, filename, content_type):
    raw = multipart_upload(
        ZEROX0_URL,
        fields={'expires': '24'},
        file_field='file',
        filename=filename,
        file_bytes=img_bytes,
        content_type=content_type,
    )
    url = raw.decode('utf-8', errors='replace').strip()
    if not url.startswith('http'):
        raise RuntimeError(f"0x0.st unexpected response: {url[:300] or '(empty)'}")
    return url

def _upload_catbox(img_bytes, filename, content_type):
    raw = multipart_upload(
        CATBOX_URL,
        fields={'reqtype': 'fileupload'},
        file_field='fileToUpload',
        filename=filename,
        file_bytes=img_bytes,
        content_type=content_type,
    )
    url = raw.decode('utf-8', errors='replace').strip()
    if not url.startswith('http'):
        raise RuntimeError(f"Catbox unexpected response: {url[:300] or '(empty)'}")
    return url

def _upload_tmpfiles(img_bytes, filename, content_type):
    raw = multipart_upload(
        TMPFILES_URL,
        fields={},
        file_field='file',
        filename=filename,
        file_bytes=img_bytes,
        content_type=content_type,
    )
    txt = raw.decode('utf-8', errors='replace').strip()
    try:
        data = json.loads(txt)
    except Exception:
        raise RuntimeError(f"tmpfiles unexpected response: {txt[:300] or '(empty)'}")
    url = data.get('data', {}).get('url', '')
    if '/tmpfiles.org/' in url and '/dl/' not in url:
        url = url.replace('tmpfiles.org/', 'tmpfiles.org/dl/', 1)
    if not url.startswith('http'):
        raise RuntimeError(f"tmpfiles parsed url invalid: {data}")
    return url

def upload_image_any(image_path):
    """Host preferito: GitHub raw (compatibile con Meta). Fallback: catbox/0x0/tmpfiles."""
    gh_token = get_github_creds()
    if gh_token:
        try:
            code, data = gh_api('GET', '/user', gh_token)
            if code != 200:
                raise RuntimeError(f"/user HTTP {code}: {data}")
            gh_user = data.get('login')
            if not gh_user:
                raise RuntimeError(f"/user senza campo login: {data}")
            log(f"    Upload via GitHub raw (user={gh_user}, repo={GITHUB_REPO}) …")
            ensure_github_repo(gh_user, gh_token)
            url = upload_image_github(image_path, gh_user, gh_token)
            log(f"    OK GitHub → {url}")
            return url
        except Exception as e:
            log(f"    GitHub KO: {e} — provo fallback")
    else:
        log(f"    Secret GH_PAT non configurato — salto GitHub, uso fallback hosting.")

    with open(image_path, 'rb') as f:
        img_bytes = f.read()
    filename = os.path.basename(image_path)
    ext = os.path.splitext(filename)[1].lower()
    content_type = 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'
    last_err = None
    for attempt in range(1, 4):
        try:
            log(f"    Tentativo {attempt}/3 upload via catbox.moe …")
            url = _upload_catbox(img_bytes, filename, content_type)
            log(f"    OK catbox.moe → {url}")
            return url
        except Exception as e:
            log(f"    catbox.moe tentativo {attempt} KO: {e}")
            last_err = e
            if attempt < 3:
                time.sleep(2 * attempt)
    for name, fn in (('0x0.st', _upload_0x0), ('tmpfiles.org', _upload_tmpfiles)):
        try:
            log(f"    Tentativo upload via {name} …")
            url = fn(img_bytes, filename, content_type)
            log(f"    OK {name} → {url}")
            return url
        except Exception as e:
            log(f"    {name} KO: {e}")
            last_err = e
    raise RuntimeError(f"Tutti gli host immagine hanno fallito. Ultimo errore: {last_err}")

def get_ig_user_id(token):
    """Resolve IG user ID from token."""
    url = f'{IG_API}/me?fields=user_id,username&access_token={urllib.parse.quote(token)}'
    res = http_get(url)
    uid = res.get('user_id') or res.get('id')
    uname = res.get('username', '?')
    log(f"  Token valido. Account IG: @{uname} (id={uid})")
    return uid

def publish_post(post, token, ig_user_id):
    slug     = post['n']
    caption  = post['caption']
    img_path = os.path.join(POSTS_DIR, f'{slug}.png')

    if not os.path.exists(img_path):
        log(f"  ERROR: immagine non trovata in {img_path}")
        return False

    log(f"  Conversione PNG→JPEG (richiesta da IG Content Publishing) …")
    try:
        jpg_path = convert_png_to_jpeg(img_path)
        log(f"    JPEG temporaneo: {jpg_path} ({os.path.getsize(jpg_path)} bytes)")
    except Exception as e:
        log(f"  ERROR conversione: {e}")
        return False

    log(f"  Upload immagine {slug}.jpg …")
    try:
        cdn_url = upload_image_any(jpg_path)
    except Exception as e:
        log(f"  ERROR upload: {e}")
        return False
    finally:
        try:
            os.remove(jpg_path)
        except Exception:
            pass
    log(f"  CDN URL: {cdn_url}")

    log("  Creazione container IG …")
    res = http_post(f'{IG_API}/{ig_user_id}/media', {
        'image_url':   cdn_url,
        'caption':     caption,
        'access_token': token,
    })
    container_id = res.get('id')
    if not container_id:
        log(f"  ERROR creazione container: {res}")
        return False
    log(f"  Container ID: {container_id}")

    time.sleep(3)

    log("  Pubblicazione su Instagram …")
    res = http_post(f'{IG_API}/{ig_user_id}/media_publish', {
        'creation_id':  container_id,
        'access_token': token,
    })
    media_id = res.get('id')
    if not media_id:
        log(f"  ERROR pubblicazione: {res}")
        return False
    log(f"  ✅ Pubblicato! Media ID: {media_id}")
    return media_id

def today_in_rome():
    """Data odierna in Europe/Rome — il runner GitHub Actions è in UTC."""
    try:
        from zoneinfo import ZoneInfo
        from datetime import datetime
        return datetime.now(ZoneInfo('Europe/Rome')).date().isoformat()
    except Exception:
        return date.today().isoformat()

def main():
    today = today_in_rome()
    log(f"=== Woxel Daily Publisher v2 — {today} ===")

    token = get_token()

    try:
        ig_user_id = get_ig_user_id(token)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        log(f"  ERROR token/identità: HTTP {e.code} {body}")
        sys.exit(1)
    except Exception as e:
        log(f"  ERROR rete su /me: {e}")
        sys.exit(1)

    with open(PLAN_FILE) as f:
        plan = json.load(f)

    target_slug = sys.argv[1] if len(sys.argv) > 1 else None

    today_posts = []
    skipped_unapproved = []
    for week in plan['weeks']:
        for post in week['posts']:
            if post.get('stato') == 'published':
                continue
            if target_slug:
                if post['n'] == target_slug:
                    today_posts.append(post)
            else:
                if post['date'] == today:
                    if post.get('approved', True):
                        today_posts.append(post)
                    else:
                        skipped_unapproved.append(post)

    if not today_posts:
        if target_slug:
            log(f"Post '{target_slug}' non trovato nel piano (o già pubblicato).")
        elif skipped_unapproved:
            log(f"Tutti i post di {today} in attesa di approvazione — nessuna pubblicazione.")
        else:
            log(f"Nessun post schedulato per {today}. Fine.")
        return

    if target_slug:
        log(f"Modo mirato: pubblico '{target_slug}'")
    else:
        log(f"Trovati {len(today_posts)} post approvati per oggi.")
    any_failure = False
    for post in today_posts:
        log(f"Pubblicazione: {post['n']}")
        try:
            media_id = publish_post(post, token, ig_user_id)
            if media_id:
                post['stato']        = 'published'
                post['published_at'] = time.strftime('%Y-%m-%dT%H:%M:%S')
                post['media_id']     = media_id
            else:
                any_failure = True
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            log(f"  ERROR HTTP {e.code}: {body}")
            any_failure = True
        except Exception as e:
            log(f"  ERROR: {type(e).__name__}: {e}")
            any_failure = True

    with open(PLAN_FILE, 'w') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    log("=== Fine ===\n")
    if any_failure:
        sys.exit(2)

if __name__ == '__main__':
    main()
