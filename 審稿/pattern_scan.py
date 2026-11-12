#!/usr/bin/env python3
"""全劇句型掃描：閘門逐卡比，看不到跨卡重複，這支量整部的機械感。用法：python3 審稿/pattern_scan.py [劇本路徑]"""
import re, sys, collections, pathlib
p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'canon/劇本.md')
t = p.read_text()
cards = [(m.group(1), m.group(2)) for m in re.finditer(r'^## (\S+?)（.*?\n(.*?)(?=^## |\Z)', t, re.S | re.M)]
rows = [(k, l) for k, b in cards for l in b.splitlines() if '：' in l and not l.startswith('〔')]
nar = [l[3:] for _, l in rows if l.startswith('旁白：')]
dia = [l.split('：', 1)[1] for _, l in rows if not l.startswith('旁白：')]
first = [next((l[3:] for l in b.splitlines() if l.startswith('旁白：')), '') for _, b in cards]
head = collections.Counter(re.split('[，。]', f)[0][:6] for f in first if f)
chars = sum(len(l.split('：', 1)[1]) for _, l in rows)
print(f'卡 {len(cards)}　行 {len(rows)}（旁白 {len(nar)}、對白與心聲 {len(dia)}）　約 {(chars * .055 + len(rows) * 2) / 60:.1f} 分鐘')
print(f'卡首句以「時間，地點，」起頭：{sum(bool(re.match(r"(第.年|頭七|最後幾個月|幾個禮拜後|又一個|午後|安雅走後|春末|暴雨夜)[^，]*，[^，]*，", f)) for f in first)} 張')
print('卡首句前六字重複：' + '、'.join(f'{k}×{v}' for k, v in head.most_common() if v > 1))
print(f'旁白「把」字句 {sum("把" in l for l in nar)}／{len(nar)}　以他或她起頭 {sum(l[0] in "他她" for l in nar)}／{len(nar)}')
run = best = 0
for _, l in rows:
    run = run + 1 if l.startswith('旁白：') else 0; best = max(best, run)
print(f'旁白最長連續 {best} 句')
print('指揮位置的梗（左手邊、右手邊、右邊、左邊）：', len(re.findall(r'[左右]手?邊', '\n'.join(dia))))
print('對白句尾語助詞：' + '、'.join(f'{c}×{sum(bool(re.search(c + "[。？！]?$", l)) for l in dia)}' for c in '喔啦啊耶欸'))
for k in ('房東', '鑰匙', '兩口', '搬去哪', '住哪', '阿姨問', '妳媽'):
    print(f'「{k}」出現在：' + '、'.join(f'{c}×{b.count(k)}' for c, b in cards if k in b))
