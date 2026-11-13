# -*- coding: utf-8 -*-
"""產生 docs/theme.html（片尾主題曲 MV 頁：畫面跟著歌詞一鏡一鏡換，中英對照歌詞一次一句）、docs/img/mv/*.webp、docs/music/theme*.lrc。
python3 site/build_mv.py
做法照《餘燼》的 ~/larch-ember/site/build_mv.py：分鏡表在 site/mv_storyboard.json，start 對齊歌詞的第幾句（或秒數），
這支程式把它換成秒、檢查順序與音檔長度。歌詞與每句的秒數在 site/theme_lyrics.json。
頁面含結局畫面，開始畫面上有寫。embed=1 時不顯示返回連結，播完或按「繼續」送 {type:'larch:mv:done'} 給父層。"""
import json, os, subprocess
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
        shots.append(dict(t0=round(t0, 2), cg=s['cg'], move=s['move'], blank=bool(s.get('blank'))))
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
    for s in shots:
        export(s['cg']); s['img'] = f"img/mv/{s['cg']}.webp"
    data = {'theme': dict(title=SB['title'], dur=round(dur, 2), audio=LY['audio'], shots=shots, lines=lines)}
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Noto+Sans+TC:wght@500;700&family=Noto+Serif+TC:wght@500;700&display=swap">
<style>{css}</style>
</head>
<body>
<div class="film" aria-hidden="true"><i id="fA"></i><i id="fB"></i></div>
<div class="shade" aria-hidden="true"></div>
<canvas id="fx" aria-hidden="true"></canvas>
<div class="lyric" aria-live="off"><p id="lA"></p><p id="lB"></p></div>
<div class="prog" id="prog" aria-hidden="true"></div>
<div class="black" id="black" aria-hidden="true"></div>
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
