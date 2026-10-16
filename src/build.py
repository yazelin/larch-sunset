"""組出 dist/project.json：骨架＋RPG地圖＋劇情卡＋配音演出。"""
import json, pathlib, shutil
import cards, variables, art, mapkit
import map_bar, map_storage, map_bedroom, memory

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT_ID = 'project-8cb1ab7e-891c-46b4-bd38-df29060e5717'


def load_skeleton():
    return json.loads((ROOT / 'skeleton/project.json').read_text(encoding='utf-8'))


def rpg_database(a):
    def actor(id, name, walk, portrait, role='party'):
        return {
            'id': id,
            'name': name,
            'title': '',
            'profile': '',
            'role': role,
            'walk': mapkit.walker(a[walk]),
            'portrait': a[portrait],
            'join': 'stay' if id == 'shen' else 'later',
            'kit': 'none',
            'rig': '',
            'joinVariable': ''
        }
    return {
        'version': 1,
        'heroId': 'shen',
        'leadSwitch': False,
        'actors': [
            actor('shen', '沈淮', 'walk-shen', 'p-shen'),
            actor('anya', '安雅', 'walk-anya', 'p-anya'),
            actor('anya-spirit', '安雅（靈魂）', 'walk-anya-spirit', 'p-anya-spirit')
        ]
    }


def build():
    p = load_skeleton()
    board = p['boards'][0]
    board['nodes'], board['edges'] = [], []
    p['nodes'], p['edges'] = board['nodes'], board['edges']
    p['variables'] = variables.project_variables()

    a = art.paths()
    v = art.VOICES

    # RPG 系統插件設定
    p['settings'].setdefault('plugins', {})
    p['settings']['plugins']['larch-rpg-system'] = {
        'enabled': True,
        'settings': {
            'database': json.dumps(rpg_database(a), ensure_ascii=False)
        }
    }

    # 封面與 CG 收藏庫
    p['settings']['titleCoverImage'] = a['cover']
    p['settings']['projectThumbnail'] = a['cover']
    p['settings'].setdefault('titleScreen', {})['bgm'] = a['bgm-bar']
    p['settings']['cgGallerySource'] = 'picked'
    p['settings']['cgGalleryItems'] = [
        {'url': a['cover'], 'title': '晚霞是舌尖最後的刺痛'},
        {'url': a['cg-mem1'], 'title': '暴雨的夜'},
        {'url': a['cg-mem2'], 'title': '黃銅匙'},
        {'url': a['cg-mem3'], 'title': '想看晚霞'},
        {'url': a['cg-cocktail'], 'title': '初遇與終點的晚霞'},
        {'url': a['cg-ending-burn'], 'title': '共赴晚霞'},
        {'url': a['cg-ending-cold'], 'title': '冷卻的餘溫'},
        {'url': a['bg-bar'], 'title': '深夜吧檯'},
        {'url': a['bg-storage'], 'title': '香料儲藏間'},
        {'url': a['bg-bedroom'], 'title': '臥室梳妝台'}
    ]

    # UI 主題風格搭配：暗夜暖橙酒吧風
    p['settings']['menuUi'] = {
        'preset': 'night',
        'accent': '#ff7b39',
        'title': '晚霞是舌尖最後的刺痛',
        'eyebrow': '調酒師的記憶收納',
        'buttons': ['bag', 'save', 'load', 'title']
    }
    p['settings']['battleUi'] = {
        'preset': 'night',
        'panel': '#1e1b18',
        'accent': '#ff7b39'
    }

    N = board['nodes'].append
    L = lambda x, y: cards.link(board, x, y)

    # 2. 地圖卡：深夜吧檯、香料儲藏間、臥室梳妝台
    N(map_bar.build_bar(a))
    N(map_storage.build_storage(a))
    N(map_bedroom.build_bedroom(a))


    # 3. 劇情卡片（供地圖事件直接演出或跳轉）
    # (b) 臥室回憶與真相卡
    N(cards.dialogue('card_bedroom_memory', '安雅的回憶',
                     '『沈淮，粉紅胡椒不是辣椒，但咬碎的時候，喉嚨會有一種像觸電一樣的麻辣感……就像我第一次牽你手時一樣。』',
                     bg='', speaker='安雅（回憶）',
                     voiceUrl=v['anya-memory'],
                     actors=[cards.actor('安雅（回憶）', a['p-anya'], 'right')]))

    shock_text = "病歷單上赫然印著：【味覺中樞全面壞死】……\n\n「味覺中樞壞死？！這是什麼意思？！她……早就嚐不出味道了？！」\n材料都齊全了，我必須立刻回到吧檯。"
    N(cards.dialogue('card_bedroom_shock', '病歷單的真相',
                     shock_text,
                     bg='', speaker='沈淮',
                     actors=[cards.actor('沈淮', a['p-shen'], 'left')]))

    # (c) 調酒完成：安雅遺書獨白卡
    confession_text = "『當你調出這杯酒時，我已經先喝下它了。\n我的世界早就失去所有味道，痛卻一天比一天清楚。我研發了三年，把神經止痛毒劑做成這杯酒……它很美，金黃像日出，粉紅像晚霞。\n沈淮，這是我為自己選的終點。\n你調出來的這一杯，不要嚐它，替我倒掉。』"
    N(cards.dialogue('card_confession', '安雅的遺書獨白',
                     confession_text,
                     bg=a['cg-cocktail'], speaker='安雅（獨白）',
                     voiceUrl=v['anya-confession'], bgm=a['bgm-confession'],
                     actors=[cards.actor('安雅（獨白）', a['p-anya-spirit'], 'right')]))

    # (d) 終局抉擇卡
    choice_texts = [
        '【共赴的辣度】端起酒杯，一口飲盡',
        '【冷卻的餘溫】遵從遺願，倒進水槽'
    ]
    N(cards.choice('card_choice', '節點 5：終局抉擇', '你要如何抉擇？', choice_texts, speaker='沈淮', bg=a['cg-cocktail']))
    # 序幕、便條與回憶穿插在解謎中（design/重寫.md）
    memory.build(board, a)
    L('card_confession', 'card_choice')
    cards.choice_link(board, 'card_choice', 'ending_burn_1', 0)
    cards.choice_link(board, 'card_choice', 'ending_cold_1', 1)

    # (e) 結局 A（共赴晚霞）
    N(cards.dialogue('ending_burn_1', '共赴的辣度',
                     '我沒有聽妳的話。\n\n我端起酒杯，一口飲盡。',
                     bg=a['cg-cocktail'], speaker='沈淮',
                     voiceUrl=v['shen-burn-1'],
                     actors=[cards.actor('沈淮', a['p-shen'], 'left')]))

    N(cards.dialogue('ending_burn_2', '心跳的刺痛',
                     '入口先是番紅花的溫潤金黃，隨即，粉紅胡椒那股狂暴的辛辣在咽喉裡燃燒撕裂。\n胸口像被火灼燒，但那股微辣的刺痛感……確實是心跳的感覺。\n\n朦朧的淚光中，吧檯對面彷彿映出了她初遇時溫柔的微笑……',
                     bg=a['cg-cocktail'], speaker='沈淮',
                     voiceUrl=v['shen-burn-2'],
                     actors=[cards.actor('沈淮', a['p-shen'], 'left')]))

    # 結局 A 終局：完全由精美專屬 CG 替代，移除任何「結局 A」等文字標記
    N(cards.dialogue('ending_burn_3', '共赴晚霞',
                     '眼前的光線逐漸暈散成一片金黃與淡粉。\n安雅……這一次，妳不必一個人走。',
                     bg=a['cg-ending-burn'], speaker='沈淮',
                     voiceUrl=v['shen-burn-3'],
                     actors=[]))

    L('ending_burn_1', 'ending_burn_2')
    L('ending_burn_2', 'ending_burn_3')

    # (f) 結局 B（冷卻的餘溫）
    N(cards.dialogue('ending_cold_1', '冷卻的餘溫',
                     '手在發抖，但我還是把杯子翻轉，倒進了水槽。\n\n金黃的液體被流水沖淡，淡粉色的胡椒碎粒在不鏽鋼表面旋轉著消逝。空氣裡那股短暫的辣香，轉瞬間被冰冷的水氣沖刷得一乾二淨。',
                     bg=a['bg-bar'], speaker='沈淮',
                     voiceUrl=v['shen-cold-1'],
                     actors=[cards.actor('沈淮', a['p-shen'], 'left')]))

    # 結局 B 終局：完全由精美專屬 CG 替代，移除任何「結局 B」等文字標記
    N(cards.dialogue('ending_cold_2', '冷卻的餘溫',
                     '屋子裡重新歸於死寂。\n我遵從了妳最後的願望活了下來，但從此以後，我的舌尖與心臟……再也嚐不出任何溫度。',
                     bg=a['cg-ending-cold'], speaker='沈淮',
                     voiceUrl=v['shen-cold-2'],
                     actors=[]))

    L('ending_cold_1', 'ending_cold_2')


    (ROOT / 'dist').mkdir(exist_ok=True)
    out_file = ROOT / 'dist/project.json'
    out_file.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding='utf-8')

    # 同步 assets 目錄至 dist/assets 供本機 serve.py /files/assets/... 直供
    dst = ROOT / 'dist/assets'
    shutil.rmtree(dst, ignore_errors=True)
    if (ROOT / 'assets').exists():
        shutil.copytree(ROOT / 'assets', dst)

    nodes_count = len(board['nodes'])
    edges_count = len(board['edges'])
    print(f'Build finished! Output: {out_file} ({nodes_count} nodes, {edges_count} edges)')
    return p


if __name__ == '__main__':
    build()
