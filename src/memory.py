"""回憶篇（design/回憶篇.md，作者 2026-10-16 拍板）：遺言之後、終局抉擇之前，回到三年前跟還活著的安雅相處三段。
三段都用現在的吧檯分層圖，靠燈光、時間、人物位置區分；台詞全部在這一份，配音檔名＝台詞 id。
"""
import pathlib
from mapkit import *
import cards, layout

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = layout.load('bar')
W, H = D['map']['w'], D['map']['h']
ANYA, SHEN = '安雅', '沈淮'
VOICE = {ANYA: ('Chinese (Mandarin)_Soft_Girl', 'calm'), SHEN: ('Chinese (Mandarin)_Gentle_Youth', 'calm')}

# 台詞：卡片 id → [(講者, 文字, 配音 id 或 None, 情緒)]。講者空字串＝旁白，不配音
L = {
    'card_mem_enter': [
        ('', '杯子裡的金黃慢慢沉到底，粉紅的胡椒碎浮在上面。', None, ''),
        (SHEN, '三年前的那個晚上，也是兩點十七分。', 'mem_shen_enter', 'sad'),
        ('', '窗外響起了雨聲。', None, ''),
    ],
    'card_mem1_intro': [
        ('', '三年前。雨下得很大，打烊前最後一刻，門上的鈴響了。', None, ''),
        (ANYA, '還有營業嗎？', 'mem1_anya_open', 'calm'),
        (SHEN, '還有一杯的時間。', 'mem1_shen_open', 'calm'),
        ('', '她全身都濕透了，坐上吧檯前的高腳椅，髮梢還在滴水。', None, ''),
    ],
    'card_mem1_talk': [
        (ANYA, '謝謝。', 'mem1_anya_thanks', 'calm'),
        (ANYA, '我不喝苦的，煙燻味也不行。', 'mem1_anya_nobitter', 'calm'),
        (ANYA, '有沒有喝起來，像天快亮的東西？', 'mem1_anya_dawn', 'happy'),
        (SHEN, '坐一下，我調給妳。', 'mem1_shen_mix', 'calm'),
    ],
    'card_mem1_peat': [(ANYA, '這個聞起來像燒焦的木頭。', 'mem1_anya_peat', 'happy')],
    'card_mem1_bitters': [(ANYA, '苦的不要。', 'mem1_anya_bitters', 'calm')],
    'card_mem1_taste': [
        ('', '她雙手捧著杯子喝了一口，咬到胡椒，嗆了一下，然後笑出來。', None, ''),
        (ANYA, '好辣……可是好甜。', 'mem1_anya_spicy', 'happy'),
        (ANYA, '真的像天快亮了。', 'mem1_anya_likedawn', 'happy'),
        ('', '她抬頭看牆上的掛鐘。', None, ''),
        (ANYA, '兩點十七分。我會記得。', 'mem1_anya_remember', 'happy'),
    ],
    'card_mem1_cg': [('', '那天晚上的雨，一直下到天亮。', None, '')],
    'card_mem2_intro': [
        ('', '幾個月後。開店前的傍晚，夕陽從大窗照進來。', None, ''),
        (ANYA, '又混掉了。', 'mem2_anya_mixed', 'sad'),
        ('', '她站在吧檯後面，杯裡的顏色攪成一團。', None, ''),
    ],
    'card_mem2_spoon': [
        (SHEN, '用這個，貼著杯壁慢慢轉。', 'mem2_shen_spoon', 'calm'),
        (ANYA, '這樣？', 'mem2_anya_like', 'calm'),
    ],
    'card_mem2_pull': [
        (ANYA, '你說的我聽不懂，你來。', 'mem2_anya_youdo', 'happy'),
        ('', '她拉過他的手，放在自己的手上。', None, ''),
    ],
    'card_mem2_hands': [
        ('', '他的手覆在她手上，匙沿著杯壁轉了一圈。金黃在杯裡慢慢旋開，沒有混。', None, ''),
        (ANYA, '……手好燙。', 'mem2_anya_hot', 'happy'),
        (SHEN, '是妳的手太冰。', 'mem2_shen_cold', 'happy'),
        (ANYA, '這把匙借我。以後就是我的了。', 'mem2_anya_mine', 'happy'),
    ],
    'card_mem2_cg': [('', '那之後，那把匙一直放在她的位置上。', None, '')],
    'card_mem3_intro': [
        ('', '第三年。打烊後，店裡只剩他們兩個。', None, ''),
        (ANYA, '來，試試這杯。', 'mem3_anya_try', 'happy'),
    ],
    'card_mem3_ask': [(ANYA, '甜嗎？', 'mem3_anya_sweet', 'calm')],
    'card_mem3_sugar': [
        ('', '她沒有回答，又往杯裡加了兩匙糖漿，自己嚐了一口。', None, ''),
        (ANYA, '嗯，剛好。', 'mem3_anya_justright', 'calm'),
    ],
    'card_mem3_why': [
        (SHEN, '怎麼了？', 'mem3_shen_why', 'calm'),
        (ANYA, '沒事。', 'mem3_anya_nothing', 'calm'),
    ],
    'card_mem3_shoulder': [
        ('', '她繞出吧檯，在他旁邊的高腳椅坐下，頭靠上他的肩膀。', None, ''),
        (ANYA, '沈淮，我想看一次真正的晚霞。', 'mem3_anya_sunset', 'sad'),
        (SHEN, '明天傍晚就帶妳去。', 'mem3_shen_tomorrow', 'calm'),
        ('', '她笑了一下，沒有說好。', None, ''),
    ],
    'card_mem3_cg': [('', '那是她第一次說想看晚霞。', None, '')],
    'card_mem_return': [
        ('', '雨聲停了。燈暗下來，吧檯上只剩那一杯。', None, ''),
        (SHEN, '妳想看的晚霞，在這杯裡。', 'mem_shen_return', 'sad'),
    ],
}


def voice_lines():
    """給配音腳本：[(檔名, 文字, 聲線, 情緒)]"""
    return [(f'{vid}.mp3', tx, VOICE[sp][0], emo or VOICE[sp][1]) for ls in L.values() for sp, tx, vid, emo in ls if vid]


def _card(cid, title, art, bg=''):
    lines = [(sp, tx, f'/files/assets/voice/{vid}.mp3' if vid else None) for sp, tx, vid, _ in L[cid]]
    actors = [cards.actor(n, art['p-anya'] if n == ANYA else art['p-shen'], 'right' if n == ANYA else 'left')
              for n in (SHEN, ANYA) if any(sp == n for sp, *_ in L[cid])] if not bg else []
    return cards.dialogue(cid, title, lines, bg=bg, actors=actors)


def _env(darkness, lights):
    return {'weather': 'clear', 'intensity': 0, 'darkness': darkness, 'shake': 0,
            'lights': [dict(zip(('id', 'x', 'y', 'radius', 'color', 'flicker'), l)) for l in lights]}


def _map(mid, title, art, events, guidance, env):
    real = (ROOT / 'assets/maps/bar_ground.webp').exists()
    kind = 'objects' if real else 'blocks'
    urls = {o['name']: f"/files/assets/{kind}/bar/{o['name']}.webp" for o in layout.objects(D)}
    events = events + [dict(e, id=e['id'].replace('obj-m-bar', f'obj-{mid}')) for e in layout.events(D, urls)]
    m = map_dict(title, W, H, f'/files/assets/maps/bar_{"ground" if real else "blocks"}.webp', layout.walls(D), events, guidance, env)
    return map_node(mid, title, m, bgm=art.get('bgm-memory', art.get('bgm-bar', '')))


def build(board, art):
    N = board['nodes'].append
    link = lambda a, b: cards.link(board, a, b)
    shen = lambda x, y, d: ev('hero', x, y, actor='player', direction=d, sprite=walker(art['walk-shen']), actorId='shen')
    anya = walker(art['walk-anya'])

    # 進入回憶：遺言之後
    N(_card('card_mem_enter', '回憶：兩點十七分', art))

    # ── 回憶一〈02:17，暴雨〉：她坐在吧檯前（9,6），沈淮從前場開始 ──
    m1 = [
        shen(13, 7, 'left'),
        ev('mem1-intro', 1, 11, trigger='auto', once=True, actions=[card('card_mem1_intro'), setv('mem1', 'towel')]),
        ev('mem1-towel', 15, 7, name='沙發扶手上的乾毛巾', marker={'label': '乾毛巾', 'kind': 'quest'}, conditions=[cond('mem1', 'towel')],
           actions=[say('沙發扶手上掛著一條乾毛巾。', speaker='player'), item('towel', '乾毛巾'), setv('mem1', 'give')]),
        npc('mem1-anya', 9, 6, anya, direction='up', name='安雅', marker={'label': '安雅', 'kind': 'talk'},
            actions=[branch([cond('mem1', 'give')],
                            [remove('towel', '乾毛巾'), card('card_mem1_talk'), setv('mem1', 'mix')],
                            [say('她冷得一直發抖。先找點東西讓她擦乾。', speaker='player')])]),
        ev('mem1-mix', 9, 3, name='吧檯工作台', marker={'label': '替她調第一杯', 'kind': 'quest'}, conditions=[cond('mem1', 'mix')],
           actions=[
               # 第一個動作不能是選擇題：按互動鍵的那一下會直接選到第一個選項
               say('她說，要喝起來像天快亮的東西。他看著酒櫃想了一下。', speaker='player'),
               choice_action('基酒用什麼？', [
                   ('貴腐甜白酒', [say('金黃的甜白酒倒進杯底，像還沒亮透的天色。', speaker='player')]),
                   ('泥煤威士忌', [card('card_mem1_peat'), say('他把瓶子放回去，換了甜白酒。', speaker='player')]),
               ], speaker='player'),
               choice_action('再加一點什麼？', [
                   ('番紅花糖漿', [say('一小匙番紅花糖漿，杯裡的金黃亮了起來。', speaker='player')]),
                   ('苦精', [card('card_mem1_bitters'), say('他收起苦精，改拿番紅花糖漿。', speaker='player')]),
               ], speaker='player'),
               choice_action('最後收尾？', [
                   ('粉紅胡椒', [say('磨碎的粉紅胡椒落在酒面上。', speaker='player')]),
                   ('肉桂粉', [say('他聞了一下，把肉桂放回架上，拿起粉紅胡椒。', speaker='player')]),
               ], speaker='player'),
               card('card_mem1_taste'), setv('mem1', 'done'), jump('card_mem1_cg'),
           ]),
    ]
    g1 = [
        {'text': '拿沙發上的乾毛巾給她', 'eventId': 'mem1-towel', 'conditions': [cond('mem1', 'towel')]},
        {'text': '把毛巾交給安雅', 'eventId': 'mem1-anya', 'conditions': [cond('mem1', 'give')]},
        {'text': '從左邊翻板繞進吧檯，替她調第一杯', 'eventId': 'mem1-mix', 'conditions': [cond('mem1', 'mix')]},
    ]
    N(_map('m-mem-1', '回憶：暴雨的夜', art, m1, g1,
           _env(0, [('m1-bar', 9, 3, 6, '#ffc46b', False), ('m1-lounge', 10, 7, 7, '#ffb04d', False), ('m1-sofa', 15, 6, 4, '#ffd18a', False)])))
    N(_card('card_mem1_cg', '回憶：初遇', art, bg=art['cg-mem1']))

    # ── 回憶二〈黃銅匙〉：她在吧檯後（10,3），匙在吧檯前角落（11,6） ──
    m2 = [
        shen(9, 7, 'up'),
        ev('mem2-intro', 1, 11, trigger='auto', once=True, actions=[card('card_mem2_intro'), setv('mem2', 'spoon')]),
        ev('mem2-spoon', 11, 6, name='黃銅調酒匙', marker={'label': '黃銅匙', 'kind': 'quest'}, conditions=[cond('mem2', 'spoon')],
           actions=[say('吧檯角落的黃銅調酒匙，跟了他好幾年。', speaker='player'), item('spoon_old', '黃銅調酒匙'), setv('mem2', 'teach')]),
        npc('mem2-anya', 10, 3, anya, direction='down', name='安雅', marker={'label': '安雅', 'kind': 'talk'},
            actions=[branch([cond('mem2', 'teach')],
                            [remove('spoon_old', '黃銅調酒匙'), card('card_mem2_spoon'),
                             choice_action('怎麼教她？', [
                                 ('握住她的手示範', []),
                                 ('在旁邊說給她聽', [card('card_mem2_pull')]),
                             ], speaker='player'),
                             card('card_mem2_hands'), setv('mem2', 'done'), jump('card_mem2_cg')],
                            [say('她盯著攪混的杯子嘆氣。吧檯角落那把黃銅匙，或許幫得上忙。', speaker='player')])]),
    ]
    g2 = [
        {'text': '拿吧檯角落的黃銅匙', 'eventId': 'mem2-spoon', 'conditions': [cond('mem2', 'spoon')]},
        {'text': '繞進吧檯，教她用黃銅匙', 'eventId': 'mem2-anya', 'conditions': [cond('mem2', 'teach')]},
    ]
    N(_map('m-mem-2', '回憶：開店前的傍晚', art, m2, g2,
           _env(0, [('m2-sun', 14, 4, 8, '#ff8a3d', False), ('m2-bar', 9, 3, 5, '#ffb35c', False)])))
    N(_card('card_mem2_cg', '回憶：黃銅匙', art, bg=art['cg-mem2']))

    # ── 回憶三〈甜嗎〉：她在吧檯後（10,3），推過來的杯子在吧檯前（10,6） ──
    m3 = [
        shen(12, 7, 'up'),
        ev('mem3-intro', 1, 11, trigger='auto', once=True, actions=[card('card_mem3_intro'), setv('mem3', 'glass')]),
        npc('mem3-anya', 10, 3, anya, direction='down', name='安雅'),
        ev('mem3-glass', 10, 6, name='她推過來的那杯', marker={'label': '她推過來的那杯', 'kind': 'quest'}, conditions=[cond('mem3', 'glass')],
           actions=[
               card('card_mem3_ask'),
               choice_action('甜嗎？', [('「剛好。」', []), ('「有點太甜。」', [])], speaker='player'),
               card('card_mem3_sugar'),
               choice_action('她看起來有點不一樣。', [
                   ('問她怎麼了', [card('card_mem3_why')]),
                   ('什麼都不說', [say('他沒有問，只是看著她把杯子收回去。', speaker='player')]),
               ], speaker='player'),
               card('card_mem3_shoulder'), setv('mem3', 'done'), jump('card_mem3_cg'),
           ]),
    ]
    g3 = [{'text': '喝她推過來的那杯', 'eventId': 'mem3-glass', 'conditions': [cond('mem3', 'glass')]}]
    N(_map('m-mem-3', '回憶：打烊之後', art, m3, g3,
           _env(0.3, [('m3-lamp', 10, 4, 5, '#ffc078', False)])))
    N(_card('card_mem3_cg', '回憶：想看晚霞', art, bg=art['cg-mem3']))

    # 回到現實
    N(_card('card_mem_return', '回到現實', art, bg=art['cg-cocktail']))

    # 地圖上演出的對話卡（card(...) 叫的）也要是專案裡的卡
    have = {n['id'] for n in board['nodes']}
    for cid in L:
        if cid not in have:
            N(_card(cid, cid.replace('card_', ''), art))

    link('card_mem_enter', 'm-mem-1')
    link('card_mem1_cg', 'm-mem-2')
    link('card_mem2_cg', 'm-mem-3')
    link('card_mem3_cg', 'card_mem_return')
    return 'card_mem_enter', 'card_mem_return'
