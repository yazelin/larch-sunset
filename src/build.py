"""組出 dist/project.json：第五版（2026-11），單線、純劇情卡、一個結局（設計 design/重製.md）。
canon/劇本.md 的每個 `##` 是一張對話卡，照劇本順序串起來；〔圖〕標記的那一句換背景，不放立繪。全程自動播放、沒有選項、不配音。
python3 src/build.py
"""
import json, os, pathlib, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
import script, cards

R = ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT_ID = 'project-8cb1ab7e-891c-46b4-bd38-df29060e5717'
A = '/files/assets/'
TEXT_MS = 55
AUTO = {'enabled': True, 'mode': 'delay', 'delayMs': 2000}
HINT = ['這是一部從頭到尾會自己播放的小說，大約四十分鐘。', '戴上耳機，不用點滑鼠，看到最後。想快一點，點一下畫面。']
NAME = '晚霞'
DESCRIPTION = ('巷子裡一間只有七張高腳椅的小酒吧。調酒師安雅和加班到深夜的沈淮，從一個暴雨夜的第一杯〈破曉〉開始，'
               '鬥嘴、吵架、一起把店撐起來，過了三年。她走後的第七天，他回到店裡，翻開她從不讓人看的小筆記本。'
               '單線劇情、一個結局，全程自動播放。')
# 配樂：每張卡用哪一首（assets/bgm/<名>.mp3）。同一首連續的卡不重設，曲子不會從頭重播；'' 是安靜
TRACK_BY_PREFIX = [('open', 'days'), ('return', 'seventh'), ('rain', 'dawn'), ('weeks', 'dawn'), ('clinic', 'alone'), ('lesson', 'days'),
                   ('confess', 'dawn'), ('together', 'days'), ('quit_1', 'alone'), ('quit_2', 'alone'), ('quit_3', 'days'), ('home', 'days'),
                   ('dusk', 'days'), ('almost', 'alone'), ('roof', 'sunset'), ('winter_1', 'alone'), ('winter_2', 'alone'), ('winter_3', 'winter'),
                   ('last', 'winter'), ('farewell_1', 'winter'), ('farewell_2', ''), ('farewell_3', 'seventh'), ('notebook', 'seventh'),
                   ('flash_1', 'days'), ('flash_2', 'sunset'), ('door', 'seventh'), ('sunset_1', ''), ('sunset_2', ''), ('sunset_3', 'sunset'),
                   ('evening', 'main')]
SPEAKER = {'念': '{}的筆記', '心': '{}（心）'}
LINE_SFX = {('door_1', 0): '/sfx/knock.mp3'}   # 逐句音效（Larch 內建音效庫）：頭七那晚的敲門聲。內建庫只有短的雨聲、風聲，環境音交給配樂
# 換圖時機：劇本每張卡只標一張圖，畫的是那張卡最要緊的一刻。同一場戲接續的卡，前半沿用上一張圖，演到那一刻才換（值是那一句的開頭）
SHOT_AT = {'open_2': '旁白：她又碰了碰他的手肘', 'rain_2': '旁白：她先倒洛神花糖漿', 'rain_3': '旁白：她把傘塞進他手裡', 'confess_2': '旁白：他彎下身',
           'quit_2': '旁白：他把捲起的袖子拉下來', 'roof_2': '旁白：她把他的手按在自己腰上', 'winter_2': '沈淮：我現在坐不下去', 'sunset_3': '旁白：他把杯子放下，拉過飯碗'}
# 同一張卡裡再換一次圖（沿用別張已有的圖）
EXTRA_SHOTS = {('farewell_3', '旁白：後門關上'): 'front_night', ('evening_2', '旁白：他沿樓梯下樓'): 'evening_bar'}
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


def title_of(cid):
    return script.WHEN[cid].replace('，', '・')[:24] or cid


def story_card(cid, bg_carry, bgm=''):
    """一張劇本卡 → 一張對話卡；〔圖〕標記的那一句換背景。回傳 (卡, 這張卡結束時的背景)。"""
    lines, bgs, bg = [], [], bg_carry
    raw = [f'{n}（{g}）：{x}' if g else f'{n}：{x}' for n, g, x in script.L[cid]]
    at = {}
    for (c, i), sh in script.SHOTS.items():
        if c == cid:
            at[next(k for k, l in enumerate(raw) if l.startswith(SHOT_AT[cid])) if cid in SHOT_AT and i == 0 else i] = sh
    for (c, anchor), sh in EXTRA_SHOTS.items():
        if c == cid:
            at[next(k for k, l in enumerate(raw) if l.startswith(anchor))] = sh
    for i, (name, tag, text) in enumerate(script.L[cid]):
        url = shot_url(at.get(i, ''))
        if url:
            bg = url
        lines.append((SPEAKER[tag].format(name) if tag else name, text)); bgs.append(url)
    card = cards.dialogue(cid, title_of(cid), lines, bg=bgs[0] or bg_carry or '', bgm=bgm or None)
    for dst, b in zip(card['data']['dialogueLines'], bgs):
        if b:
            dst['background'] = b
    for (c, i), u in LINE_SFX.items():
        if c == cid:
            card['data']['dialogueLines'][i]['sfxUrl'] = u
    ops = [{'id': f'cgop-{cid}-{sh}', 'mode': 'unlock', 'url': shot_url(sh)} for (c, _), sh in script.SHOTS.items()
           if c == cid and sh in {k for k, _ in GALLERY} and shot_url(sh)]
    if ops:
        card['data']['cgOps'] = ops
    card['data'].update(stage={'actors': []}, characterLayers=[], autoAdvance=dict(AUTO))
    return card, bg


def credits_card(bg):
    content = (R / 'src/credits.txt').read_text(encoding='utf-8').strip()
    return {'id': 'credits', 'type': 'story', 'position': {'x': 0, 'y': 0}, 'data': {
        'type': 'plugin', 'title': '製作名單', 'text': '', 'voiceMode': 'off', 'stage': {'actors': []}, 'characterLayers': [], 'background': bg,
        'pluginId': 'credits-roll', 'pluginCardId': 'roll', 'pluginVersion': '1.0.0', 'pluginName': '片尾字卷', 'pluginCardName': '片尾字卷',
        'pluginIcon': 'scroll', 'pluginColor': '#8a6d2a', 'pluginPresentation': 'fullscreen', 'pluginFrame': {'showTitle': False, 'showButton': False},
        'pluginSkippable': True, 'pluginReadVars': [], 'pluginWriteVars': [], 'pluginAssets': [], 'platforms': ['web'],
        'pluginHtml': (R / 'src/plugin/credits_roll_card.html').read_text(encoding='utf-8'),
        'pluginValues': {'content': content, 'speed': 16, 'autoContinue': True, 'endHold': 8, 'continueLabel': '回到標題', 'bgColor': '#0b0a10',
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
    board.update(name='晚霞', thumbnail=cover, description='從第一年春天的暴雨夜，到她走後的第七天。')
    p['variables'] = []
    s = p['settings']
    s['plugins'] = {**{k: ({**v, 'enabled': False} if k in ('larch-inventory', 'larch-rpg-system') else v) for k, v in s.get('plugins', {}).items()}, 'credits-roll': {'enabled': True}}
    s.update(showRpgHud=False, textSpeed=TEXT_MS, stageFit='contain', titleCoverImage=cover, projectThumbnail=cover,
             cgGalleryEnabled=bool(GALLERY), cgGallerySource='picked',
             cgGalleryItems=[{'url': cover, 'title': NAME}] + [{'url': shot_url(k), 'title': t, 'locked': True} for k, t in GALLERY if shot_url(k)])
    p['projectThumbnail'] = cover
    s.setdefault('titleScreen', {})['bgm'] = music('main') or s.get('titleScreen', {}).get('bgm', '')
    ci = s.setdefault('customInterfaces', {})   # 作品專屬介面（ui/）：標題與對話框；線上要另外用 Larch 介面工具寫進去
    for k in ('title', 'dialogue'):
        ci[k] = {'html': (R / f'ui/{k}.html').read_text(encoding='utf-8'), 'enabled': True}
    N = board['nodes'].append
    hint = cards.dialogue('hint', '開始之前', [('旁白', t) for t in HINT], bg=cover)
    hint['data'].update(start=True, autoAdvance=dict(AUTO), stage={'actors': []}, characterLayers=[])
    N(hint)
    prev, ptrack, bg = 'hint', None, ''
    for cid in script.ORDER:
        t = track(cid)
        url = music(t) if t and t != ptrack else ''
        c, bg = story_card(cid, bg, bgm=url)
        if t == '' and ptrack:   # 安靜的卡：停掉上一首
            c['data'].update(bgm='', bgmVolume=0, bgmLoop=False)
        ptrack = t if (url or t == '') else ptrack
        N(c); cards.link(board, prev, cid); prev = cid
    N(credits_card(bg)); cards.link(board, prev, 'credits')
    (R / 'dist').mkdir(exist_ok=True)
    out = R / 'dist/project.json'
    out.write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding='utf-8')
    shutil.rmtree(R / 'dist/assets', ignore_errors=True)
    (R / 'dist/assets').mkdir()
    for sub in ('art/cg', 'bgm', 'sfx'):
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
