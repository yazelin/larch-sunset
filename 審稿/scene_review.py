#!/usr/bin/env python3
"""讀稿人、提示詞、一幕幕讀稿（sweep）。從《續》的 xu/審稿/scene_review.py 移植（2026-10-23，作者同意）；日常用 runner.py 的 read／packet／gate／ship，不必直接叫這支。
  sweep <劇本.md> [場代號…]   每場讀稿人各找問題（含七項評分），另做設定查證；不給場代號就全部
  status <劇本.md>            每場審到第幾輪、審過後有沒有改
輸出存到 審稿/紀錄/。llmshare 只用 deepseek-v4.1-flash:1017（作者 2026-10-20）。"""
import os, subprocess, sys, pathlib, datetime, time, re, json, hashlib
ROOT = pathlib.Path(__file__).resolve().parent.parent          # ~/larch-sunset
OUT = pathlib.Path(__file__).resolve().parent / '紀錄'; OUT.mkdir(exist_ok=True)
RPM_FILE = pathlib.Path.home() / '.cache' / 'llmshare-rpm'      # 本機所有 llmshare 呼叫共用的請求時間戳（跟《續》同一個檔）
AVAIL = pathlib.Path.home() / '.cache' / 'sunset-review-readers.json'


def rpm_slot(limit=15):
    """llmshare 這把金鑰每分鐘只准 15 次（2026-10-22 量到）；本機所有呼叫加起來最近 60 秒滿 limit 次就等。"""
    import fcntl
    RPM_FILE.parent.mkdir(exist_ok=True)
    while True:
        with open(RPM_FILE, 'a+') as f:
            fcntl.flock(f, fcntl.LOCK_EX); f.seek(0); now = time.time()
            ts = [float(x) for x in f.read().split() if now - float(x) < 60]
            if len(ts) < limit:
                f.seek(0); f.truncate(); f.write(' '.join(map(str, ts + [now]))); return
            wait = 60.5 - (now - min(ts))
        time.sleep(wait)


def _bashrc(name):   # .bashrc 尾端的 export 對非互動腳本無效，直接讀檔
    for l in open(os.path.expanduser('~/.bashrc'), encoding='utf-8', errors='ignore'):
        if l.strip().startswith(('export ' + name + '=', name + '=')): return l.split('=', 1)[1].strip().strip('"').strip("'")
    return os.environ.get(name, '')


def ds(p):
    rpm_slot(); return subprocess.run(['llmshare', 'raw', 'deepseek-v4.1-flash:1017', p], capture_output=True, text=True, timeout=600).stdout.strip()
def gm(p):   # 作者自架 gemini-web（.11 瀏覽器驅動）；長回應可能截斷，所以不做查證
    import urllib.request
    q = urllib.request.Request('http://192.168.11.11:8070/api/chat', data=json.dumps({'prompt': p, 'timeout': 300}).encode(),
                               headers={'Content-Type': 'application/json', 'x-goog-api-key': _bashrc('GEMINI_IMAGE_KEY')})
    try: j = json.loads(urllib.request.urlopen(q, timeout=360).read().decode()); return (j.get('text') or j.get('response') or '').strip()
    except Exception: return ''
def ag(model):   # 本機 agy（Antigravity CLI）；plan 模式、在 /tmp 跑，不讀檔不改檔
    def f(p):
        try:
            r = subprocess.run(['agy', '-p', p + '\n只回答，不要讀檔或使用任何工具。', '--model', model, '--mode', 'plan'], capture_output=True, text=True, timeout=900, cwd='/tmp')
            return '' if 'AGY_ERROR' in r.stdout or 'quota' in r.stdout.lower()[:300] else r.stdout.strip()
        except Exception: return ''
    return f
def cx(p):
    r = subprocess.run(['codex', 'exec', '-m', os.environ.get('CODEX_MODEL', 'gpt-6.1-sol'), '--skip-git-repo-check', '-s', 'read-only', '-C', '/tmp', '-'], input=p, capture_output=True, text=True, timeout=900).stdout
    return r.split('tokens used', 1)[-1].split('\n', 1)[-1].strip() if 'tokens used' in r else r.strip()
_ds_lock = __import__('threading').Lock()
def qw(p):   # llmshare 上的 qwen3.5:397b；2026-10-29 argon 額度用完（七天）時補第三位讀稿人
    try: return subprocess.run(['llmshare', 'raw', 'qwen3.5:397b', p], capture_output=True, text=True, timeout=900, env={**os.environ, 'LLMSHARE_ALLOW_ANY': '1'}).stdout.strip()
    except Exception: return ''


def dsl(p):   # 同一時間只送一個、間隔 3 秒
    with _ds_lock: time.sleep(3); return ds(p)

# 讀稿人＝四個家族各一位（跟《續》同一組）。2026-10-23 移植時 agy 的 opus 與 argon 額度用完，所以 available() 會把它們拿掉；
# google 家族缺席時用作者自架的 gemini-web 補位（《續》因為長回應截斷不用它，這裡只在 argon 不在時才上場）。
# 要強制指定：環境變數 READERS=codex,deepseek,geminiweb
PREFERRED = {'opus': ag('claude-opus-5-5-high'), 'codex': cx, 'argon': ag('gemini-4-argon-high'), 'deepseek': dsl}
FALLBACK = {'google': ('geminiweb', gm)}
FAMILY = {'qwen': 'alibaba', 'claude': 'anthropic', 'opus': 'anthropic', 'codex': 'openai', 'argon': 'google', 'geminiweb': 'google', 'deepseek': 'deepseek'}
ALL = {**PREFERRED, 'geminiweb': gm, 'qwen': qw}


def available():
    """探一次各讀稿人（快取 30 分鐘），額度用完或沒回應的拿掉；google 家族全缺時補 gemini-web。"""
    if os.environ.get('READERS', 'deepseek,geminiweb,qwen'): return {k: ALL[k] for k in os.environ.get('READERS', 'deepseek,geminiweb,qwen').split(',') if k in ALL}
    cache = json.loads(AVAIL.read_text()) if AVAIL.exists() else {}
    if time.time() - cache.get('t', 0) > 1800:
        ok = {}
        for k, f in PREFERRED.items():
            try: ok[k] = bool(f('回一個字：好。').strip()) if k in ('opus', 'argon') else True   # codex、deepseek 失敗由 call() 重試，不先探
            except Exception: ok[k] = False
        cache = {'t': time.time(), 'ok': ok}; AVAIL.write_text(json.dumps(cache))
    r = {k: f for k, f in PREFERRED.items() if cache['ok'].get(k)}
    if not any(FAMILY[k] == 'google' for k in r): k, f = FALLBACK['google']; r[k] = f
    return r


READERS = available()

READ = """你是互動小說（視覺小說）的挑剔審稿人，用台灣讀者的耳朵一幕一幕讀，也要出聲念念看。下面是一場戲（第 N 行是這場內的行號）。
格式說明：「講者：台詞」；「安雅（心）」「沈淮（心）」是心聲；「旁白」只該寫畫面上看得到的事；〔圖〕是演出標記，後面括號是給畫圖的人的說明，不用挑。
這部作品：台灣一間兩個人顧的小酒吧。安雅是做了很多年的調酒師，溫暖、愛笑、在吧檯後面說了算、什麼都自己扛；她得的是唾液腺腺樣囊狀癌，沿神經復發，味覺一年比一年少，她選擇不治療、瞞著沈淮，每一聲「甜嗎」都是借他的舌頭。沈淮原本是加班到深夜的上班族，後來辭職站吧檯，話不多、會開玩笑、嘴笨。調性：成人、浪漫、克制。

一、找問題。類型只用這些：
真人不會這樣說（出聲念出來沒有人會這樣講）、念不出口的書面語、搭配不當、口氣不合角色或身分、角色走樣、單字連答、口頭禪重複、旁白替讀者下結論或解釋心情、含蓄到看不懂、對話接不上、金句腔、調酒寫得不像真的調酒師、病的描寫不真實（突然全好、把病寫成懲罰、瞞病瞞得太刻意、暗示到他應該聽得懂）、設定矛盾（只限這一場真的出現的設定）。
每個問題一行：「行號｜原句｜類型｜為什麼｜建議怎麼改（一句）」。最多 12 個，最嚴重的排前面；沒問題的句子不用提。

二、找好句。這一場最打動人的句子，最多三句，每句一行：「好句｜行號｜原句｜好在哪（一句）」。這一場一句都沒有，就只寫一行「好句｜無｜｜這一場沒有打動人的句子」。

三、真人的痕跡。看這一場的對白有沒有真人說話的痕跡（打斷、說一半、答非所問、重複、顧左右而言他）。只寫一行：「痕跡｜有或沒有｜一句說明」。這一場沒有對白就寫「痕跡｜不適用｜」。

不要客套，不要寫戲。
【這一幕的背景】{ctx}
【場景】
{body}"""

FACT = """你是設定查證員。下面是一場戲，以及這部作品的設定來源（可信的依據）與調酒、醫學研究整理。
把這場戲裡每一個有設定性的內容（人名、稱呼、時間、地點、物件與它的來由、調酒的材料與手法、病的表現、誰知道什麼）逐一分類：
符合設定｜與設定矛盾｜違反研究D節｜不確定。
（「違反研究D節」在這部作品指：調酒或醫學寫法跟研究整理相反。）
每個一行：「原句｜類別｜依據（引設定來源或研究的原句；沒有就寫「無依據」）｜風險（一句）」。
重要：你自己的記憶不可靠，沒有依據就一律標「不確定」。只列有設定性的內容，最多 15 個。
【設定來源】
{canon}
【研究整理】
{hist}
【這一幕的背景】{ctx}
【場景】
{body}"""

CANON_FIX = ""


def canon_text():
    return (ROOT / 'design/重製.md').read_text(encoding='utf-8') + '\n\n' + ((ROOT / 'design/角色.md').read_text(encoding='utf-8') if (ROOT / 'design/角色.md').exists() else '')


def research_d():   # 兩份研究的「判定」與「建議改法」段（全文太長）
    out = []
    for f in ('design/研究-調酒.md', 'design/研究-病理.md'):
        t = (ROOT / f).read_text(encoding='utf-8')
        out.append('\n'.join(sec for sec in re.split(r'\n(?=## )', t) if sec.startswith(('## 一', '## 三、建議', '## 五'))))
    return '\n\n'.join(out)[:12000]


STATE = pathlib.Path(__file__).resolve().parent / '狀態.json'
def _h(t): return hashlib.md5(t.encode()).hexdigest()[:8]
def _load(): return json.loads(STATE.read_text()) if STATE.exists() else {}
def mark(p, title, body):
    st = _load(); e = st.setdefault(p.name, {}).setdefault(title, {'輪': 0}); e.update(hash=_h(body), 時間=datetime.datetime.now().strftime('%m-%d %H:%M'), 輪=e['輪'] + 1); STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1))
def status(p):
    st = _load().get(p.name, {}); _, sc = scenes(p)
    for title, body in sc:
        e = st.get(title); tag = '從沒審過' if not e else ('已審（內容沒變）' if e['hash'] == _h(body) else '審過後改了，要複審')
        print(f"{tag:<14} 第{e['輪'] if e else 0}輪 {e['時間'] if e else '':<12} {title}")

def scenes(p): return scenes_text(p.read_text(encoding='utf-8'))
def scenes_text(text):
    """→ (檔頭背景, [(場代號, 帶行號的這一場)])。場代號＝ ## 後面括號前的代號（例如 m_letter）；修改紀錄不算一場。"""
    text = text.split('\n## 修改紀錄')[0]
    lines = text.splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith('## ')] + [len(lines)]
    ctx = '\n'.join(lines[:8])[:900]
    out = []
    for a, b in zip(idx, idx[1:]):
        code = lines[a][3:].strip().split('（')[0].strip()
        out.append((code, '\n'.join(f'{k+1}｜{t}' for k, t in enumerate(lines[a:b]) if t.strip())))
    return ctx, out

def call(f, prompt, tries=3):
    r = ''
    for k in range(tries):
        r = f(prompt)
        if r and 'rate' not in r.lower()[:200]: return r
        time.sleep(25)
    return r or '（沒有回應）'

def sweep(p, keys):
    from concurrent.futures import ThreadPoolExecutor
    ctx, sc = scenes(p); sc = [s for s in sc if not keys or s[0] in keys]
    canon, hist = canon_text(), research_d()
    stamp = datetime.datetime.now().strftime('%m%d_%H%M%S'); d = OUT / f'sweep_{p.stem}_{stamp}'; d.mkdir()
    def one(item):
        title, body = item; body = body[:14000]
        jobs = {**{f'讀_{w}': (f, READ.format(ctx=ctx, body=body)) for w, f in READERS.items()},
                '查證_deepseek': (dsl, FACT.format(canon=canon, hist=hist, ctx=ctx, body=body)), '查證_qwen': (qw, FACT.format(canon=canon, hist=hist, ctx=ctx, body=body))}
        with ThreadPoolExecutor(len(jobs)) as ex2: res = dict(zip(jobs, ex2.map(lambda fp: call(*fp), jobs.values())))
        out = f'# {title}\n\n' + ''.join(f'## {k}\n{v}\n\n' for k, v in res.items()) + f'## 原文\n{body}\n'
        (d / (re.sub(r'\W', '_', title)[:40] + '.md')).write_text(out); mark(p, title, body); return title
    with ThreadPoolExecutor(1) as ex:   # ponytail: 一次一場、場內並行；機器負載低再加
        for t in ex.map(one, sc): print('完成', t, flush=True)
    print('存到', d); return d

if __name__ == '__main__':
    mode, a = sys.argv[1], pathlib.Path(sys.argv[2])
    if mode == 'sweep': sweep(a, sys.argv[3:]); sys.exit()
    if mode == 'status': status(a); sys.exit()
