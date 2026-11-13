"""從 canon/劇本.md 讀台詞。每個 `## 代號（時空）` 是一張卡；`〔圖：名字〕（構圖說明）` 從下一句起換這張 CG；其餘每行「講者：台詞」。
講者後面的括號：（心）是心聲、（念）是筆記本上她寫的字。"""
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
SRC = R / 'canon/劇本.md'
HEAD = re.compile(r'^## (\w+)(?:（(.*)）)?')
LINE = re.compile(r'^([^：\s#>〔-][^：]{0,12})：(.+)$')
SHOT = re.compile(r'^〔圖：(\w+)〕(?:（(.*)）)?$')


def parse(text=None):
    """回傳 L {卡: [(講者, 標記, 台詞)]}、WHEN {卡: 時空}、SHOTS {(卡, 第幾句): 圖名}、DESC {圖名: 構圖說明}。"""
    text = text if text is not None else SRC.read_text(encoding='utf-8')
    L, WHEN, SHOTS, DESC, cur = {}, {}, {}, {}, None
    for raw in text.splitlines():
        s = raw.strip()
        h = HEAD.match(s)
        if h:
            cur = h.group(1); L[cur] = []; WHEN[cur] = h.group(2) or ''; continue
        if cur is None or not s:
            continue
        g = SHOT.match(s)
        if g:
            SHOTS[(cur, len(L[cur]))] = g.group(1); DESC[g.group(1)] = g.group(2) or ''; continue
        m = LINE.match(s)
        if not m:
            continue
        who = re.match(r'^(.+?)（(.+)）$', m.group(1))
        name, tag = (who.group(1), who.group(2)) if who else (m.group(1), '')
        L[cur].append((name, tag, m.group(2).strip()))
    return L, WHEN, SHOTS, DESC


L, WHEN, SHOTS, DESC = parse()
ORDER = [k for k in L if L[k]]

if __name__ == '__main__':
    t, w, sh, d = parse('## a（春天，店裡）\n〔圖：a_1〕（她笑）\n安雅（心）：好。\n〔圖：a_2〕\n旁白：燈。\n## credits\n〔片尾字卷〕\n')
    assert t == {'a': [('安雅', '心', '好。'), ('旁白', '', '燈。')], 'credits': []} and w['a'] == '春天，店裡', (t, w)
    assert sh == {('a', 0): 'a_1', ('a', 1): 'a_2'} and d == {'a_1': '她笑', 'a_2': ''}, (sh, d)
    n = sum(len(v) for v in L.values())
    print(len(ORDER), '張卡', n, '句', len(SHOTS), '個換圖點', sorted({x[0] + (f'（{x[1]}）' if x[1] else '') for v in L.values() for x in v}))
    print('卡片開頭沒標圖、沿用上一張的：', [k for k in ORDER if (k, 0) not in SHOTS])
    print('ok')
