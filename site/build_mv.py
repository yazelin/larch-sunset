# -*- coding: utf-8 -*-
"""產生 docs/theme.html（片尾主題曲 MV 頁：畫面跟著歌詞一鏡一鏡換，中英對照歌詞一次一句）、docs/img/mv/*.webp、docs/music/theme*.lrc。
python3 site/build_mv.py
做法照《餘燼》的 ~/larch-ember/site/build_mv.py：分鏡表在 site/mv_storyboard.json，start 對齊歌詞的第幾句（或秒數），
這支程式把它換成秒、檢查順序與音檔長度。歌詞與每句的秒數在 site/theme_lyrics.json。
頁面含結局畫面，開始畫面上有寫。embed=1 時不顯示返回連結，播完或按「繼續」送 {type:'larch:mv:done'} 給父層。"""
import difflib, json, os, re, subprocess
from PIL import Image

G = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))


def duration(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))


def resolve(key, sb, lines, dur):
    shots = []
    for s in sb['shots']:
        st = s['start']
        t0 = float(st['t']) if 't' in st else lines[st['line'] - 1]['t']
        shots.append(dict(t0=round(t0, 2), cg=s['cg'], move=s['move'], blank=bool(s.get('blank')), tone=s.get('tone', 'warm'), rain=bool(s.get('rain'))))
    for a, b in zip(shots, shots[1:]):
        assert b['t0'] > a['t0'], f'{key} 分鏡時間沒有往前：{a} {b}'
        a['t1'] = b['t0']
    shots[-1]['t1'] = round(dur, 2)
    assert shots[-1]['t0'] < dur, f'{key} 最後一鏡超過音檔長度'
    return shots


def export(cg):
    out = os.path.join(G, f'docs/img/mv/{cg}.webp')
    src = os.path.join(G, f'assets/art/cg/{cg}.webp')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if not os.path.exists(out) or os.path.getmtime(src) > os.path.getmtime(out):   # CG 重畫後要跟著換
        im = Image.open(src).convert('RGB')
        im.thumbnail((1600, 1600), Image.LANCZOS)
        im.save(out, quality=80, method=6)
    return out


def norm(w):
    return re.sub(r"[^a-z']", '', w.lower())


def word_times(lines, words):
    """把定稿英文歌詞的每個字對到 Whisper 逐字時間：對得上的字取它的開始秒數，對不上的在前後之間平均分；每句第一個字不早於那一句的開始。"""
    lyric = [(i, w) for i, x in enumerate(lines) for w in x['en'].split()]
    a, b = [norm(w) for _, w in lyric], [norm(w[0]) for w in words]
    t = [None] * len(lyric)
    for m in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(m.size): t[m.a + k] = words[m.b + k][1]
    out = [[] for _ in lines]
    for j, (i, w) in enumerate(lyric): out[i].append([w, t[j]])
    for i, ws in enumerate(out):
        end = lines[i + 1]['t'] - .4 if i + 1 < len(lines) else lines[i]['t'] + 6
        ws[0][1] = lines[i]['t']                                   # 句首一律照校正過的句子時間
        for k in range(1, len(ws)):
            if ws[k][1] is None or ws[k][1] <= ws[k - 1][1] or ws[k][1] > end:
                nxt = next((ws[q][1] for q in range(k + 1, len(ws)) if ws[q][1] is not None and ws[k - 1][1] < ws[q][1] <= end), None)
                gap = next((q - k + 1 for q in range(k + 1, len(ws)) if ws[q][1] == nxt), len(ws) - k + 1) if nxt else len(ws) - k + 1
                ws[k][1] = ws[k - 1][1] + ((nxt or end) - ws[k - 1][1]) / gap
        for w in ws: w[1] = round(w[1], 2)
    return out


def lrc(lines, field, by):
    def stamp(t): return f'[{int(t // 60):02d}:{t % 60:05.2f}]'
    return '[ti:晚霞 片尾主題曲]\n[by:' + by + ']\n\n' + '\n'.join(stamp(x['t']) + x[field] for x in lines) + '\n'


if __name__ == '__main__':
    LY = json.load(open(os.path.join(HERE, 'theme_lyrics.json'), encoding='utf-8'))
    SB = json.load(open(os.path.join(HERE, 'mv_storyboard.json'), encoding='utf-8'))['theme']
    lines = LY['lines']
    assert all(x['en'] and x['zh'] for x in lines), '歌詞有空的句子：' + str([i + 1 for i, x in enumerate(lines) if not (x['en'] and x['zh'])])
    assert all(b['t'] > a['t'] for a, b in zip(lines, lines[1:])), '歌詞時間沒有往前'
    dur = duration(os.path.join(G, 'assets/bgm/theme.mp3'))
    assert lines[-1]['t'] < dur
    shots = resolve('theme', SB, lines, dur)
    words = json.load(open(os.path.join(HERE, 'theme_words.json'), encoding='utf-8'))['words']
    env = json.load(open(os.path.join(HERE, 'theme_env.json'), encoding='utf-8'))
    wt = word_times(lines, words)
    SEC = ['verse', 'chorus', 'verse', 'chorus', 'verse', 'outro']   # 六段，每段四句
    out_lines = []
    for i, x in enumerate(lines):
        segs = x['zh'].split('　'); w = wt[i]
        z = [[('　' if j else '') + g, w[min(len(w) - 1, len(w) * j // len(segs))][1] + (.25 if j == 0 else 0)] for j, g in enumerate(segs)]
        out_lines.append(dict(t=x['t'], en=x['en'], zh=x['zh'], sec=SEC[i // 4], nth=i % 4, key=bool(x.get('key')), w=w, z=z))
    last_end = max(w[2] for w in words)
    for s in shots:
        export(s['cg']); s['img'] = f"img/mv/{s['cg']}.webp"
    data = {'theme': dict(title=SB['title'], dur=round(dur, 2), fade=round(last_end + 1.2, 2), hz=env['hz'], audio=LY['audio'], shots=shots, lines=out_lines, env=env['env'])}
    os.makedirs(os.path.join(G, 'docs/music'), exist_ok=True)
    open(os.path.join(G, 'docs/music/theme.lrc'), 'w', encoding='utf-8').write(lrc(lines, 'en', '英文歌詞照成品聽寫，時間由辨識對齊後校正'))
    open(os.path.join(G, 'docs/music/theme.zh.lrc'), 'w', encoding='utf-8').write(lrc(lines, 'zh', '中文歌詞版，歌裡沒有唱；時間同英文'))
    css = open(os.path.join(HERE, 'mv.css'), encoding='utf-8').read()
    js = open(os.path.join(HERE, 'mv.js'), encoding='utf-8').read()
    page = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="color-scheme" content="dark">
<title>晚霞 · 片尾主題曲</title>
<meta name="description" content="Larch 視覺小說《晚霞》的片尾主題曲 MV：畫面跟著歌走，中英對照歌詞。內含結局畫面。">
<meta name="theme-color" content="#120d16">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=LXGW+WenKai+TC:wght@400;700&family=Noto+Sans+TC:wght@500;700&family=Noto+Serif+TC:wght@500;700;900&display=swap">
<style>{css}</style>
</head>
<body>
<div class="film" aria-hidden="true"><i id="fA"></i><i id="fB"></i></div>
<div class="tone warm" aria-hidden="true"></div><div class="tone cold" aria-hidden="true"></div>
<div class="shade" aria-hidden="true"></div>
<div class="wash" aria-hidden="true"></div>
<div class="glow" aria-hidden="true"></div>
<canvas id="fx" aria-hidden="true"></canvas>
<div class="grain" id="grain" aria-hidden="true"></div>
<div class="intro" aria-hidden="true"><small>ENDING THEME</small><b>晚霞</b><i></i><span>片尾主題曲</span></div>
<div class="lyric" aria-live="off"><p id="lA"></p><p id="lB"></p></div>
<div class="bars" aria-hidden="true"></div>
<div class="prog" id="prog" aria-hidden="true"></div>
<div class="black" id="black" aria-hidden="true"></div>
<div class="endcard" aria-hidden="true"><b>記得吃飯。</b><i></i><span>晚霞</span></div>
<div class="start" id="start">
  <p class="k">片尾主題曲</p>
  <p class="t" id="stitle">晚霞</p>
  <button type="button" id="go" class="go" aria-label="播放"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg><span>播放</span></button>
  <p class="s" id="sub">內含結局畫面，建議玩過再看。</p>
</div>
<a class="back" href="./#ost">← 回公開站</a>
<button type="button" id="next" class="next" hidden>繼續</button>
<button type="button" id="again" class="again" hidden>再看一次</button>
<p class="sign" id="sign">晚霞 · 林亞澤</p>
<script>
const MV = {json.dumps(data, ensure_ascii=False)};
{js}
</script>
</body>
</html>
"""
    open(os.path.join(G, 'docs/theme.html'), 'w', encoding='utf-8').write(page)
    print('docs/theme.html', len(shots), '鏡', len(lines), '句', '長', round(dur, 1))
