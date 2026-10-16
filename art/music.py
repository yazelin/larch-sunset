# -*- coding: utf-8 -*-
"""《晚霞》配樂：走 .11 的 gemini-web /api/music（作者 2026-10-17 指定；腳本沿用《十一分鐘》art/music.py），產完切 60 秒循環、量響度（沿用 larch-taoyuan/bgm.py 的 find_start／make／seam_score）。
服務偶爾逾時，重試就好（記憶：音樂會撞 548 秒逾時，跟 worker 無關）。這台連 ddns 會被擋，走內網 IP、不驗憑證。
  python3 art/music.py gen [名字…]   → art/music_raw/<名字>.mp3
  python3 art/music.py loop [名字…]  → assets/bgm/<名字>.mp3（60 秒循環、-16 LUFS）"""
import base64, importlib.util, json, os, ssl, subprocess, sys, threading, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.dirname(H)
RAW, OUT = os.path.join(H, 'music_raw'), os.path.join(G, 'assets/bgm')
URL = 'https://192.168.11.11/gemini-web/api/music'
CTX = ssl._create_unverified_context()
TRACKS = {
    # design/重寫.md「BGM」：器樂、不要人聲、可循環；悲傷到讓人也想喝下晚霞（作者 2026-10-17）
    'theme': 'Melancholic jazz ballad for an empty late-night cocktail bar seven days after a funeral, solo felt piano, a lonely cello answering, '
             'rain on the window, a simple tender four-note love motif, heartbreaking and beautiful, 62 BPM, minor key, instrumental, no vocals, loopable',
    'storm': 'Warm intimate jazz piano trio on a stormy night in a small cocktail bar near closing time, soft upright bass, brushed snare, heavy rain outside, '
             'a first meeting, shy romantic tension under the surface, the same four-note love motif hidden in the melody, 70 BPM, instrumental, no vocals, loopable',
    'spoon': 'Tender romantic piano and strings at golden-hour sunset in an empty bar before opening, warm cello melody, gentle nylon guitar, '
             'falling in love, with a faint bittersweet shadow, 76 BPM, instrumental, no vocals, loopable',
    'almost': 'Fragile solo piano before dawn, very slow, a quiet sustained cello drone, a clock ticking softly, a woman alone hiding a secret from the man she loves, '
              'loving and devastating, 56 BPM, minor, instrumental, no vocals, loopable',
    'rooftop': 'Cinematic romantic waltz on a windy city rooftop at sunset, sweeping strings, solo violin and piano, a slow dance with the person you love, '
               'secretly the last time, aching and gorgeous, 3/4 time, 84 BPM, instrumental, no vocals, loopable',
    'letter': 'Heartbreaking solo piano with a soft string quartet for reading a farewell letter, very sparse, long silences between notes, quiet rain, '
              'grief and tenderness, the four-note love motif played once very slowly, 52 BPM, minor, instrumental, no vocals, loopable',
    'together': 'The full version of a melancholic love theme, rising slowly from solo piano into lush strings and a warm wordless pad, '
                'two lovers reunited in light, tragic and transcendent, like a sunset swallowing the night, 60 BPM, instrumental, no vocals, loopable',
    'cold': 'Cold lonely ambient piano in an empty bar at 2 a.m. years later, distant city hum, a music-box version of the four-note love motif slowly fading, '
            'numb and hollow, 58 BPM, instrumental, no vocals, loopable',
}


def key():
    for line in open(os.path.expanduser('~/.bashrc'), encoding='utf-8'):
        if line.startswith('export GEMINI_IMAGE_KEY='): return line.split('=', 1)[1].strip().strip('"')
    raise RuntimeError('找不到 GEMINI_IMAGE_KEY')


def one(name, k, tries=4):
    os.makedirs(RAW, exist_ok=True)
    for n in range(tries):
        req = urllib.request.Request(URL, method='POST', data=json.dumps({'prompt': TRACKS[name], 'timeout': 720}).encode(),
                                     headers={'Content-Type': 'application/json', 'x-goog-api-key': k})
        try: d = json.load(urllib.request.urlopen(req, timeout=900, context=CTX))
        except Exception as e: print(f'{name} 第{n + 1}次 例外 {e!r}', flush=True); continue
        if d.get('success'):
            p = os.path.join(RAW, f'{name}.mp3'); open(p, 'wb').write(base64.b64decode(d['audio']))
            print(f"{name} 好了 worker={d.get('worker_id')} {d.get('elapsed_seconds', 0):.0f} 秒", flush=True); return
        print(f"{name} 第{n + 1}次 失敗 {d.get('message') or d.get('error')}", flush=True)
    print(f'{name} 四次都失敗', flush=True)


def loop(name):
    spec = importlib.util.spec_from_file_location('tybgm', os.path.expanduser('~/larch-taoyuan/bgm.py'))
    B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)   # 只借函式，不跑它的 main（它的路徑是桃園的）
    src = os.path.join(RAW, f'{name}.mp3'); os.makedirs(OUT, exist_ok=True); out = os.path.join(OUT, f'{name}.mp3')
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    B.LEN = min(60, int(dur) - 4)
    base, best = B.find_start(src), None
    for off in [0, .5, -.5, 1, -1, 1.5, -1.5, 2, -2]:
        s = max(0.0, base + off); B.make(src, s, out); z, d = B.seam_score(out)
        if best is None or abs(z) < abs(best[0]): best = (z, s, d)
        if abs(z) < 3: break
    z, s, d = best; B.make(src, s, out)
    print(f'{name} 原曲 {dur:.0f} 秒 → 循環 {d:.1f} 秒，從 {s:.0f} 秒起，接縫 z={z:+.1f}', flush=True)


if __name__ == '__main__':
    cmd, names = sys.argv[1], sys.argv[2:] or list(TRACKS)
    if cmd == 'gen':
        k = key(); ts = [threading.Thread(target=one, args=(n, k)) for n in names]
        for t in ts: t.start()
        for t in ts: t.join()
    else:
        for n in names: loop(n)
