"""組出 dist/project.json：第五版（2026-11），單線、純劇情卡、一個結局（設計 design/重製.md）。
canon/劇本.md 的每個 `##` 是一張對話卡，照劇本順序串起來；〔圖〕標記的那一句換背景，不放立繪。沒有選項、不配音；玩家自己點著看（作者 11-12：不預設自動播放，要自動的人會自己按）。
python3 src/build.py
"""
import json, os, pathlib, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
import script, cards, labels

R = ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT_ID = 'project-8cb1ab7e-891c-46b4-bd38-df29060e5717'
A = '/files/assets/'
TEXT_MS = 55
NAME = '晚霞'
SITE = 'https://yazelin.github.io/larch-sunset/'   # 公開站：第二章全螢幕內嵌（作者 11-14：照《餘燼》）
DESCRIPTION = ('基隆慶安宮後面的巷子裡，有一間只有七張高腳椅的小酒吧，叫「回甘」。\n\n'
               '安雅走後的第七天，沈淮回到店裡，準備把鑰匙交出去。故事從這一晚往回講：三年前的暴雨夜，加班到深夜的他推門進來，'
               '喝到她調的第一杯〈破曉〉；後來兩個人一起顧店、吵架、和好，她生病，他陪到最後。頭七深夜，他翻開她從不讓人看的小筆記本。\n\n'
               '單線劇情、一個結局，沒有選項，不配音，全程約三十五分鐘。\n\n'
               '內容提醒：本作寫到癌症、親人過世，以及主角不想活下去的念頭（沒有任何方法的描寫），結局是他留下來好好吃飯。'
               '需要找人說話時，衛生福利部安心專線 1925 二十四小時有人接。\n\n'
               '飲酒過量，有害健康。酒後不開車，安全有保障。未滿十八歲請勿飲酒。\n\n'
               '文字、美術、配樂由 AI 依作者的方向與審稿製作。')
# 配樂：每張卡用哪一首（assets/bgm/<名>.mp3）。同一首連續的卡不重設，曲子不會從頭重播；'' 是安靜
TRACK_BY_PREFIX = [('open', 'days'), ('return', 'seventh'), ('rain', 'dawn'), ('weeks', 'dawn'), ('clinic', 'alone'), ('lesson', 'days'),
                   ('confess', 'dawn'), ('together', 'days'), ('quit_1', 'alone'), ('quit_2', 'alone'), ('quit_3', 'days'), ('home', 'days'),
                   ('dusk', 'days'), ('almost', 'alone'), ('roof', 'sunset'), ('winter_1', 'alone'), ('winter_2', 'alone'), ('winter_3', 'winter'),
                   ('last', 'winter'), ('farewell_1', 'winter'), ('farewell_gone', ''), ('farewell_2', ''), ('farewell_3', 'seventh'), ('notebook', 'seventh'),
                   ('flash_1', 'days'), ('flash_2', 'sunset'), ('door', 'seventh'), ('sunset_1', ''), ('sunset_2', ''), ('sunset_3', 'sunset'),
                   ('evening', 'main')]
SPEAKER = {'念': '{}的筆記', '心': '{}（心）'}
LINE_SFX = {('door_1', 0): '/sfx/knock.mp3'}   # 逐句音效（Larch 內建音效庫）：頭七那晚的敲門聲。內建庫只有短的雨聲、風聲，環境音交給配樂
# 換圖時機：劇本每張卡只標一張圖，畫的是那張卡最要緊的一刻。同一場戲接續的卡，前半沿用上一張圖，演到那一刻才換（值是那一句的開頭）
SHOT_AT = {}   # 第六版起改在劇本裡直接標：卡片開頭不標圖就沿用上一張，演到那一刻才寫〔圖：〕
EXTRA_SHOTS = {}
GALLERY = []   # (圖名, 標題)：CG 定稿後再填


def track(cid):
    return next((t for p, t in TRACK_BY_PREFIX if cid.startswith(p)), None)


FALLBACK = {'seventh': 'alone', 'theme': 'main'}   # 還沒產出來的曲子先用哪一首頂著（Gemini 音樂額度用完時）


def music(name):
    if name and not (R / f'assets/bgm/{name}.mp3').exists():
        name = FALLBACK.get(name)
    return A + f'bgm/{name}.mp3' if name and (R / f'assets/bgm/{name}.mp3').exists() else ''


def shot_url(shot):
    return A + f'art/cg/{shot}.webp' if (R / f'assets/art/cg/{shot}.webp').exists() else ''


def when(cid):
    """這張卡的時間標示：(模式, 主, 副)。頭七是「現在」；頭七第一次出現之後、尾聲之前的其他時間都是「回憶」。"""
    seg = script.WHEN[cid].split('，'); main, sub = seg[0], seg[1] if len(seg) > 1 else ''
    if main.startswith('頭七'):
        return '現在', '頭七', main[2:]
    order = script.ORDER; i = order.index(cid)
    seen_now = any(script.WHEN[c].startswith('頭七') for c in order[:i])
    later_now = any(script.WHEN[c].startswith('頭七') for c in order[i:])
    return ('回憶' if seen_now and later_now else ''), main, sub


def lab(shot, cid):
    """這張卡用的 CG 網址。時間標示不壓進圖裡，由常駐 UI（when_hud）照卡片代號顯示。"""
    return shot_url(shot) if shot else ''


def when_hud():
    """左上角的時間標示，以及回憶卡畫面外圍的暖白柔邊：Larch 常駐 UI（整個畫面、不攔點擊），換卡時照卡片代號換（規格見 larch_plugin_spec「遊戲常駐 UI」）。"""
    table = json.dumps({c: list(when(c)) for c in script.ORDER}, ensure_ascii=False)
    html = (R / 'src/plugin/when_hud.html').read_text(encoding='utf-8').replace('/*WHEN*/{}/*END*/', table)
    return {'enabled': True, 'playback': {'version': '1.0.0', 'permissions': ['player:ui'], 'defaults': {}, 'huds': [
        {'id': 'when', 'title': '時間標示', 'fullscreen': True,
         'interactive': False, 'readVariables': [], 'writeVariables': [], 'html': html}]}}


def title_of(cid):
    return script.WHEN[cid].replace('，', '・')[:24] or cid


def story_card(cid, carry, prev, bgm=''):
    """一張劇本卡 → 一張對話卡。carry 是上一張卡結束時的鏡頭名；prev 是上一張卡的代號。回傳 (卡, 這張卡結束時的鏡頭名)。
    時間換了（或進出回憶）時，第一句先出整頁字卡，第二句才出圖。"""
    raw = [f'{n}（{g}）：{x}' if g else f'{n}：{x}' for n, g, x in script.L[cid]]
    at = {}
    for (c, i), sh in script.SHOTS.items():
        if c == cid:
            at[next(k for k, l in enumerate(raw) if l.startswith(SHOT_AT[cid])) if cid in SHOT_AT and i == 0 else i] = sh
    for (c, anchor), sh in EXTRA_SHOTS.items():
        if c == cid:
            at[next(k for k, l in enumerate(raw) if l.startswith(anchor))] = sh
    w, pw = when(cid), when(prev) if prev else None
    new_time = pw is None or w[0] != pw[0] or (w[0] != '現在' and w[1] != pw[1])
    lines, bgs, shot = [], [], carry
    for i, (name, tag, text) in enumerate(script.L[cid]):
        url = ''
        if i in at and (R / f'assets/art/cg/{at[i]}.webp').exists():
            shot = at[i]; url = lab(shot, cid)
        lines.append((SPEAKER[tag].format(name) if tag else name, text)); bgs.append(url)
    if not bgs[0]:
        bgs[0] = lab(carry, cid)   # 沿用上一張卡的圖
    if new_time and len(bgs) > 1:
        first = bgs[0]; bgs[0] = A + labels.title(*w)
        if not bgs[1]:
            bgs[1] = first
    card = cards.dialogue(cid, title_of(cid), lines, bg=bgs[0] or '', bgm=bgm or None)
    for dst, b in zip(card['data']['dialogueLines'], bgs):
        if b:
            dst['background'] = b
    for (c, i), u in LINE_SFX.items():
        if c == cid:
            card['data']['dialogueLines'][i]['sfxUrl'] = u
    card['data'].update(stage={'actors': []}, characterLayers=[])
    return card, shot


def credits_card(bg):
    content = (R / 'src/credits.txt').read_text(encoding='utf-8').strip()
    return {'id': 'credits', 'type': 'story', 'position': {'x': 0, 'y': 0}, 'data': {
        'type': 'plugin', 'title': '製作名單', 'text': '', 'voiceMode': 'off', 'stage': {'actors': []}, 'characterLayers': [], 'background': bg,
        'pluginId': 'credits-roll', 'pluginCardId': 'roll', 'pluginVersion': '1.0.0', 'pluginName': '片尾字卷', 'pluginCardName': '片尾字卷',
        'pluginIcon': 'scroll', 'pluginColor': '#8a6d2a', 'pluginPresentation': 'fullscreen', 'pluginFrame': {'showTitle': False, 'showButton': False},
        'pluginSkippable': True, 'pluginReadVars': [], 'pluginWriteVars': [], 'pluginAssets': [], 'platforms': ['web'],
        'pluginHtml': (R / 'src/plugin/credits_roll_card.html').read_text(encoding='utf-8'),
        'pluginValues': {'content': content, 'speed': 16, 'autoContinue': True, 'endHold': 8, 'continueLabel': '看公開站', 'bgColor': '#0b0a10',
                         'bgOpacity': 0.8, 'textColor': '#f3ead8', 'accentColor': '#d9a441', 'font': 'serif'},
        **({'bgm': music('theme'), 'bgmVolume': 0.7, 'bgmLoop': False} if music('theme') else {})}}


def build():
    p = json.loads((R / 'skeleton/project.json').read_text(encoding='utf-8'))
    p = p.get('project', p)
    board = p['boards'][0]
    board['nodes'], board['edges'] = [], []
    p['nodes'], p['edges'] = board['nodes'], board['edges']
    p['name'], p['description'] = NAME, DESCRIPTION
    cover = A + 'art/cover.webp'
    board.update(name='晚霞', thumbnail=cover, description='從她走後的第七天，回到第一年春天的暴雨夜。')
    p['variables'] = []
    s = p['settings']
    s['plugins'] = {**{k: ({**v, 'enabled': False} if k in ('larch-inventory', 'larch-rpg-system') else v) for k, v in s.get('plugins', {}).items()}, 'credits-roll': {'enabled': True}, 'sunset-when': when_hud()}
    s.update(showRpgHud=False, textSpeed=TEXT_MS, stageFit='contain', titleCoverImage=cover, projectThumbnail=cover,
             cgGalleryEnabled=bool(GALLERY), cgGallerySource='picked',
             cgGalleryItems=[{'url': cover, 'title': NAME}] + [{'url': shot_url(k), 'title': t, 'locked': True} for k, t in GALLERY if shot_url(k)])
    p['projectThumbnail'] = cover
    s.setdefault('titleScreen', {})['bgm'] = music('main') or s.get('titleScreen', {}).get('bgm', '')
    ci = s.setdefault('customInterfaces', {})   # 作品專屬介面（ui/）：標題與對話框；線上要另外用 Larch 介面工具寫進去
    for k in ('title', 'dialogue'):
        ci[k] = {'html': (R / f'ui/{k}.html').read_text(encoding='utf-8'), 'enabled': True}
    N = board['nodes'].append
    shutil.rmtree(labels.OUT, ignore_errors=True)   # 時間標示圖每次重產
    prev, ptrack, bg = None, None, ''
    for cid in script.ORDER:
        t = track(cid)
        url = music(t) if t and t != ptrack else ''
        c, bg = story_card(cid, bg, prev, bgm=url)
        if t == '' and ptrack:   # 安靜的卡：停掉上一首
            c['data'].update(bgm='', bgmVolume=0, bgmLoop=False)
        ptrack = t if (url or t == '') else ptrack
        if prev is None:
            c['data']['start'] = True
        else:
            cards.link(board, prev, cid)
        N(c); prev = cid
    N(credits_card(shot_url(bg))); cards.link(board, prev, 'credits')
    # 第二章＝公開站：片尾字卷捲完跳過去，全螢幕嵌公開站（兩杯酒、她的病、結局為什麼改寫、原聲帶、參考資料），看完按「略過」回標題
    board['nodes'][-1]['data']['chapterEnd'] = True
    N({'id': 'to-site', 'type': 'story', 'position': {'x': 0, 'y': 0}, 'data': {
        'type': 'boardJump', 'title': '第二章・公開站', 'text': '', 'start': False, 'voiceMode': 'off', 'stage': {'actors': []},
        'jumpNodeId': 'site', 'jumpBoardId': 'board-site', 'characterLayers': []}})
    cards.link(board, 'credits', 'to-site')
    shell = ('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:#120d16}'
             f'iframe{{width:100%;height:100%;border:0;display:block}}</style><iframe src="{SITE}" allow="fullscreen; autoplay"></iframe>'
             "<script>parent.postMessage({type:'larch:ready'},'*');</script></html>")
    p['boards'].append({'id': 'board-site', 'kind': 'story', 'mode': 'story', 'name': '第二章・公開站', 'thumbnail': shot_url('evening_roof'),
                        'description': '公開站：兩杯酒怎麼調、她的病、結局為什麼改寫、原聲帶、參考資料', 'edges': [], 'nodes': [{
        'id': 'site', 'type': 'story', 'position': {'x': 100, 'y': 200}, 'data': {
            'type': 'miniGame', 'start': True, 'title': '第二章・公開站', 'text': '兩杯酒、她的病、結局為什麼改寫、原聲帶與參考資料。看完按「略過」回到標題。', 'voiceMode': 'off',
            'bgm': '', 'bgmVolume': 0, 'bgmLoop': False,
            'miniGameHtml': shell, 'miniGameNote': f'薄殼而已，內容在 {SITE}', 'miniGameReadVars': [], 'miniGameSkippable': True,
            'miniGameWriteVars': [], 'miniGamePresentation': 'fullscreen'}}]})
    (R / 'dist').mkdir(exist_ok=True)
    out = R / 'dist/project.json'
    out.write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding='utf-8')
    shutil.rmtree(R / 'dist/assets', ignore_errors=True)
    (R / 'dist/assets').mkdir()
    for sub in ('art/cg', 'art/lab', 'bgm', 'sfx'):
        if (R / 'assets' / sub).exists():
            shutil.copytree(R / 'assets' / sub, R / 'dist/assets' / sub)
    (R / 'dist/assets/art').mkdir(parents=True, exist_ok=True)
    shutil.copy(R / 'assets/art/cover.webp', R / 'dist/assets/art/cover.webp')
    ids = {n['id'] for n in board['nodes']}
    assert not [e for e in board['edges'] if e['source'] not in ids or e['target'] not in ids]
    missing = sorted({sh for sh in script.SHOTS.values() if not shot_url(sh)})
    print(f'Build finished! {out}（{len(board["nodes"])} 張卡、{len(board["edges"])} 條線；還沒有圖的鏡頭 {len(missing)} 個）')
    return p


if __name__ == '__main__':
    build()
