"""推到 Larch：快照 → 驗證 → 整包 PUT（包在 {"project": …}）→ 讀回比對。

    python3 src/push.py "這次改了什麼"
"""
import json, os, sys, time, pathlib, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(__file__))
import build

ROOT = build.ROOT
KEY = open(os.path.expanduser(os.environ.get('LARCH_KEY_FILE', '~/.config/larch/key'))).read().strip()
BASE = f'https://larch.ink/api/agent/projects/{build.PROJECT_ID}'


def req(method, path='', body=None, etag=None, tries=5):
    h = {'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'}
    if etag:
        h['If-Match'] = etag
    last = None
    for t in range(tries):
        try:
            r = urllib.request.Request(
                BASE + path,
                method=method,
                headers=h,
                data=json.dumps(body).encode() if body is not None else None
            )
            with urllib.request.urlopen(r, timeout=120) as resp:
                return resp.headers.get('ETag'), json.loads(resp.read() or b'{}')
        except urllib.error.HTTPError as e:
            last = f'{e.code} {e.read()[:300]}'
            if e.code != 429 and e.code < 500:
                raise SystemExit(f'{method} {path} → {last}')
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = repr(e)
        print(f'{method} {path} 失敗（{last}），{5 * (t + 1)} 秒後重試', flush=True)
        time.sleep(5 * (t + 1))
    raise SystemExit(f'{method} {path} 重試 {tries} 次仍失敗：{last}')


def merge_settings(online, built):
    m = json.loads(json.dumps(online or {}))
    plugins = m.setdefault('plugins', {})
    rpg = plugins.setdefault('larch-rpg-system', {'enabled': True, 'settings': {}})
    rpg['enabled'] = True
    rpg.setdefault('settings', {})['database'] = built['settings']['plugins']['larch-rpg-system']['settings']['database']
    for k in ('titleCoverImage', 'projectThumbnail', 'cgGallerySource', 'cgGalleryItems'):
        if k in built.get('settings', {}):
            m[k] = built['settings'][k]
    if (built.get('settings', {}).get('titleScreen') or {}).get('bgm'):
        m.setdefault('titleScreen', {})['bgm'] = built['settings']['titleScreen']['bgm']
    return m


def main(summary='升級 RPG 地圖系統與互動探索'):
    etag, cur = req('GET')
    online = cur.get('project', cur)
    snap = ROOT / 'snapshots' / time.strftime('%Y%m%d-%H%M%S.json')
    snap.parent.mkdir(exist_ok=True)
    snap.write_text(json.dumps(cur, ensure_ascii=False, indent=2), encoding='utf-8')
    print('已存線上快照：', snap)

    built = build.build()
    built['settings'] = merge_settings(online.get('settings'), built)

    body = {'project': built, 'summary': summary}
    new_etag, res = req('PUT', '', body, etag=etag)
    print(f'成功推送到 Larch！新 ETag: {new_etag}')
    return res


if __name__ == '__main__':
    msg = sys.argv[1] if len(sys.argv) > 1 else '升級 RPG 地圖系統與互動探索'
    main(msg)
