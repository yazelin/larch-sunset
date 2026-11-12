#!/usr/bin/env python3
"""整部通讀：閘門逐卡比，看不到跨卡的事。把全劇一次給幾位讀稿人，只問跨卡問題；兩位以上提到同一句的列為要改。
  python3 審稿/whole_read.py [canon/劇本.md]   → 審稿/紀錄/whole_<時間>.md
讀稿人：deepseek（讀兩次）、codex、gemini-web；環境變數 WHOLE=deepseek,codex 可指定。"""
import sys, re, os, pathlib, datetime
from concurrent.futures import ThreadPoolExecutor
D = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(D))
import scene_review as sr
ASK = """你是視覺小說的總編，下面是整部劇本（每個「## 代號（時空）」是一張依序播放的卡；〔圖〕那行是給畫圖的人看的，不用挑）。
逐卡的用詞問題已經有人審過，你只找「要讀過前後才看得出來」的問題，類型只用這些：
時間對不上（年份、季節、幾點、過了多久）、誰知道什麼對不上（某人說出此時還不該知道的事，或忘了已經知道的事）、物件對不上（位置、數量、來由、前面沒有後面突然出現）、
回提找不到出處（後面引用的話或事，前面沒有或說法不同）、同一件事重複交代、稱呼不一致、角色前後像兩個人、因果斷掉（上一張卡的結果沒有接到下一張）、
祕密提早說破（安雅嚐不到味道這件事，在 notebook 卡之前任何人包括心聲都不該說破）、節奏（連續幾張卡沒有事情發生，或重場太快帶過）。
每個問題一行：「卡代號｜原句（照抄，可以只抄前半句）｜類型｜為什麼（要指出另一張卡的哪一句跟它衝突）｜建議怎麼改（一句）」。
最多 20 個，最嚴重的排前面；沒把握的不要寫；逐卡的用詞、語氣問題不要寫。最後一行寫「整體｜」加一句話：全劇讀完最大的一個問題。
【劇本】
"""
ASK_AI = """你是台灣的資深編劇，下面是一部視覺小說的整部劇本（每個「## 代號（時空）」是一張卡；〔圖〕那行不用挑）。
作者覺得台詞還有「AI 味」。你只找聽起來像 AI 寫的台詞與旁白，類型只用這些：
太工整（句子完整得像書面、對仗、排比、一句話把理由講完）、功能性台詞（這句話只為了讓觀眾知道某件事，真人不會講）、
每句都在推進（沒有廢話、岔題、接話尾，像在交接資訊）、金句或格言腔、情緒轉得沒有原因（上一句還在氣，下一句就好了，中間沒有讓人信的理由）、
同一個梗或句型反覆（下命令再回嘴、指位置、打分數之類用太多次）、旁白像舞台指示（一連串「他把什麼放到哪裡」）、不像這個人會說的話。
每個問題一行：「卡代號｜原句（照抄）｜類型｜為什麼｜改成什麼（直接寫出新句子，要像台灣人平常講話）」。
最多 25 個，最嚴重的排前面；沒把握的不要寫。最後一行寫「整體｜」加一句話：全劇最有 AI 味的是哪一點。
【劇本】
"""
def main(path):
    global ASK
    if os.environ.get('MODE') == 'ai': ASK = ASK_AI
    body = pathlib.Path(path).read_text()
    R = {'deepseek': sr.ds, 'deepseek2': sr.ds, 'codex': sr.cx, 'geminiweb': sr.gm}
    who = (os.environ.get('WHOLE') or 'deepseek,deepseek2,codex,geminiweb').split(',')
    with ThreadPoolExecutor(len(who)) as ex: outs = dict(zip(who, ex.map(lambda k: sr.call(R[k], ASK + body), who)))
    rows = []
    for w, t in outs.items():
        for l in t.splitlines():
            f = [x.strip() for x in l.strip().lstrip('-*0123456789. ').split('｜')]
            if len(f) >= 5 and re.match(r'^[a-z]+_?\d*', f[0]): rows.append((w, *f[:5]))
    norm = lambda s: re.sub(r'\W', '', s.split('：', 1)[-1])[:8]
    groups = {}
    for r in rows: groups.setdefault((r[1].split('／')[0].strip(), norm(r[2])), []).append(r)
    L = [f'# 整部通讀（{datetime.datetime.now():%m-%d %H:%M}，讀稿人 {"、".join(who)}）', '', '## 兩位以上提到（要改）']
    multi = [g for g in groups.values() if len({r[0].rstrip('2') for r in g}) > 1 or len({r[0] for r in g}) > 1]
    L += [f"- {g[0][1]}｜{g[0][2]}｜{g[0][3]}｜{g[0][4]}｜{g[0][5]}（{'、'.join(r[0] for r in g)}）" for g in multi] or ['（沒有）']
    L += ['', '## 只有一位提到（自己判斷）'] + [f"- {r[1]}｜{r[2]}｜{r[3]}｜{r[4]}｜{r[5]}（{r[0]}）" for g in groups.values() if g not in multi for r in g]
    L += ['', '## 整體'] + [f'- {w}：' + next((l.split('｜', 1)[1] for l in t.splitlines() if l.strip().startswith('整體｜')), '（沒寫）') for w, t in outs.items()]
    L += ['', '## 原始回覆'] + [f'### {w}\n{t}\n' for w, t in outs.items()]
    out = sr.OUT / f'whole_{datetime.datetime.now():%m%d_%H%M%S}.md'; out.write_text('\n'.join(L) + '\n')
    print('\n'.join(L[:L.index('## 原始回覆')])); print('存到', out)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else D.parent / 'canon/劇本.md')
