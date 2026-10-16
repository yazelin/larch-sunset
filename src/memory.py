"""劇本台詞（design/重寫.md，2026-10-17 定稿）：序幕、便條，與穿插在解謎中的回憶。
找到一樣東西就回到一段過去：答完風味筆記→回憶一、拿匙→回憶二、儲藏間→回憶三。
回憶都用現在的吧檯分層圖，靠燈光、時間、人物位置區分；配音檔名＝台詞 id。
現在（頭七）用沈淮第一人稱，回憶用第三人稱。
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
    # 序幕：開頭獨白＋頭七回店
    'prologue': [
        (SHEN, '都說味道是最後才會忘記的東西。比臉晚，比聲音晚。', 'p_shen_open1', 'calm'),
        (SHEN, '很多年以後，一杯酒送到嘴邊，人就回到了那一晚。', 'p_shen_open2', 'calm'),
        (SHEN, '安雅走後第七天，我才知道，最先被帶走的，就是味道。', 'p_shen_open3', 'sad'),
        ('', '頭七。人家說，這一晚她會回家。', None, ''),
        ('', '店門口的燈箱已經七天沒亮了。我推開門，門上的鈴響了一聲，跟三年前一模一樣。', None, ''),
    ],
    # 空杯旁的便條：只交代店與生活，不提酒
    'card_anya_note': [
        (ANYA, '沈淮：店交給你了。冰箱裡有我包好的餃子，記得吃飯。', 'n_anya_1', 'calm'),
        (ANYA, '酒櫃第二層那瓶甜白酒快沒了，下次叫貨多叫一箱。', 'n_anya_2', 'calm'),
        (ANYA, '不要每天都等到兩點十七分才關門。', 'n_anya_3', 'sad'),
        ('', '她寫便條，從來不署名。', None, ''),
    ],
    # 答完風味筆記，進回憶一
    'card_mem1_enter': [
        ('', '窗外開始下雨了。', None, ''),
        (SHEN, '三年前的那個晚上，也在下雨。', 'mem_shen_enter', 'sad'),
    ],
    # 回憶一：他淋濕進門，她是調酒師（設定 A，作者 2026-10-16 拍板）
    'card_mem1_intro': [
        ('', '三年前。雨下得很大，打烊前最後一刻，門上的鈴響了。', None, ''),
        (SHEN, '還有營業嗎？', 'a_mem1_shen_open', 'calm'),
        (ANYA, '還有一杯的時間。', 'a_mem1_anya_open', 'calm'),
        ('', '她從吧檯後面遞出一條毛巾，笑了笑。', None, ''),
        (ANYA, '先擦乾，再點酒。', 'a_mem1_anya_towel', 'happy'),
    ],
    'card_mem1_seat': [
        ('', '他坐上高腳椅，拿毛巾胡亂擦著頭髮。她撐著吧檯看他。', None, ''),
        (ANYA, '你是來躲雨，還是來喝酒的？', 'a_mem1_anya_why', 'happy'),
    ],
    'card_mem1_rain': [(ANYA, '那雨停之前，你都是我的客人。', 'a_mem1_anya_guest', 'happy')],
    'card_mem1_both': [
        (ANYA, '貪心。', 'a_mem1_anya_greedy', 'happy'),
        ('', '她轉身去拿杯子。', None, ''),
    ],
    'card_mem1_order': [(ANYA, '想喝什麼？', 'a_mem1_anya_order', 'calm')],
    'card_mem1_bitter': [
        ('', '她拿酒瓶的手停了一下，抬頭看他。', None, ''),
        (ANYA, '……你也怕苦？', 'a_mem1_anya_bitter', 'calm'),
    ],
    'card_mem1_strong': [(ANYA, '淋成這樣還喝烈的？看你也不像會喝苦的人。今晚聽我的。', 'a_mem1_anya_strong', 'happy')],
    'card_mem1_mix': [
        (ANYA, '那我調一杯我自己最喜歡的。還沒給別人喝過。', 'a_mem1_anya_fav', 'happy'),
        ('', '金黃的甜白酒，一小匙番紅花糖漿，最後她在杯口磨了幾粒粉紅胡椒，把杯子推到他面前。', None, ''),
        (ANYA, '最黑的時候，喝一杯天亮。', 'a_mem1_anya_dark', 'calm'),
    ],
    'card_mem1_stare': [(ANYA, '看我做什麼？喝酒。', 'a_mem1_anya_stare', 'happy')],
    'card_mem1_taste': [
        ('', '他咬到胡椒，舌尖麻了一下，愣住了。她撐著吧檯看他，等他開口。', None, ''),
        (SHEN, '好辣……可是好甜。', 'a_mem1_shen_spicy', 'surprised'),
        (ANYA, '像不像天快亮的時候？', 'a_mem1_anya_dawn', 'happy'),
        (SHEN, '像。', 'a_mem1_shen_like', 'calm'),
        ('', '她笑了。那是她那一晚第一次真的笑。', None, ''),
        (ANYA, '那就叫它〈破曉〉。', 'a_mem1_anya_name', 'happy'),
        ('', '她這才發現他髮尾的水還在往吧檯上滴。她拿過毛巾，探身越過吧檯，替他把頭髮擦乾。', None, ''),
        ('', '她的手停在他耳邊，過了很久才拿開。', None, ''),
        ('', '她抬頭看牆上的掛鐘。', None, ''),
        (ANYA, '兩點十七分。你是我今天最後一個客人。', 'a_mem1_anya_last', 'calm'),
        (SHEN, '那我明天早一點來。', 'a_mem1_shen_tomorrow', 'calm'),
        (ANYA, '……兩點十七分。我會記得。', 'a_mem1_anya_remember', 'happy'),
    ],
    'card_mem1_leave': [
        (ANYA, '喂。', 'a_mem1_anya_hey', 'calm'),
        ('', '她追到門口，把一把傘塞進他手裡。指尖碰到的時候，她沒有馬上縮回去。', None, ''),
        (ANYA, '明天要還。', 'a_mem1_anya_return', 'happy'),
    ],
    'card_mem1_cg': [('', '那天晚上的雨，一直下到天亮。', None, '')],
    # 回憶二：她教他用黃銅匙
    'card_mem2_enter': [
        ('', '匙柄被她握得發亮。', None, ''),
    ],
    'card_mem3_enter': [
        ('', '糖漿的瓶口還黏著一圈乾掉的金黃。', None, ''),
    ],
    'card_mem2_intro': [
        ('', '幾個月後。開店前的傍晚，夕陽從大窗照進來。', None, ''),
        (ANYA, '沈淮，過來。今天教你調酒。', 'a_mem2_anya_teach', 'happy'),
        (ANYA, '吧檯角落那把匙，幫我拿過來。', 'a_mem2_anya_spoon', 'calm'),
    ],
    'card_mem2_spoon': [
        (ANYA, '貼著杯壁，慢慢轉。不要用力。', 'a_mem2_anya_how', 'calm'),
        (SHEN, '這樣？', 'a_mem2_shen_like', 'calm'),
        ('', '杯裡的顏色一下子全攪混了。', None, ''),
    ],
    'card_mem2_again': [
        ('', '他又轉了一次。顏色還是攪成一團。', None, ''),
        (ANYA, '你不行啦。手給我。', 'a_mem2_anya_hand', 'happy'),
    ],
    'card_mem2_hands': [
        ('', '她站到他身後，手覆上他的手。匙沿著杯壁轉了一圈，金黃在杯裡慢慢旋開，沒有混。', None, ''),
        (ANYA, '感覺到了嗎？', 'a_mem2_anya_feel', 'calm'),
        (SHEN, '……感覺到了。', 'a_mem2_shen_feel', 'calm'),
        ('', '匙停了。她的手沒有放開。', None, ''),
        (ANYA, '你的手好冰。', 'a_mem2_anya_cold', 'calm'),
        (SHEN, '是妳的手太燙。', 'a_mem2_shen_hot', 'calm'),
        ('', '誰都沒有先退開。', None, ''),
    ],
    'card_mem2_grip': [('', '他翻過手，把她的手握進掌心。', None, '')],
    'card_mem2_turn': [('', '他轉過身。她就在他面前，近到看得見她的睫毛在抖。', None, '')],
    'card_mem2_mine': [
        (ANYA, '……這把匙是我的。只借你。', 'a_mem2_anya_mine', 'calm'),
        ('', '她說完，才慢慢把手抽回去。', None, ''),
    ],
    'card_mem2_cg': [('', '那把匙，她一直放在自己的位置上。', None, '')],
    # 回憶三：甜嗎
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
        (ANYA, '如果有一天，我嚐不出你調的酒了呢？', 'a_mem3_anya_ifone', 'sad'),
        (SHEN, '那我就調到妳嚐得出來為止。', 'a_mem3_shen_until', 'calm'),
        ('', '她把臉埋進他的肩膀，很久沒有抬起來。', None, ''),
    ],
    'card_mem3_cg': [('', '那是她第一次說想看晚霞。', None, '')],
}


def voice_lines():
    """給配音腳本：[(檔名, 文字, 聲線, 情緒)]"""
    return [(f'{vid}.mp3', tx, VOICE[sp][0], emo or VOICE[sp][1]) for ls in L.values() for sp, tx, vid, emo in ls if vid]


def _card(cid, title, art, bg='', **kw):
    lines = [(sp, tx, f'/files/assets/voice/{vid}.mp3' if vid else None) for sp, tx, vid, _ in L[cid]]
    actors = [cards.actor(n, art['p-anya'] if n == ANYA else art['p-shen'], 'right' if n == ANYA else 'left')
              for n in (SHEN, ANYA) if any(sp == n for sp, *_ in L[cid])] if not bg else []
    return cards.dialogue(cid, title, lines, bg=bg, actors=actors, **kw)


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

    # 序幕與便條
    N(_card('prologue', '序幕：頭七', art, bg=art['bg-bar'], start=True, bgm=art.get('bgm-bar')))
    N(_card('card_anya_note', '安雅的便條', art))
    # 每段回憶的入口（地圖事件 jump 過來）
    N(_card('card_mem1_enter', '回憶：兩點十七分', art))
    N(_card('card_mem2_enter', '回憶：黃銅匙', art))
    N(_card('card_mem3_enter', '回憶：甜嗎', art))

    # ── 回憶一〈02:17，暴雨〉：他淋濕進門（9,9）；她在吧檯後（10,3）；高腳椅（9,6）；門口（9,10） ──
    guest = lambda x, y, d: ev('hero', x, y, actor='player', direction=d, sprite=walker(art['walk-shen-casual']), actorId='shen')
    m1 = [
        guest(9, 9, 'up'),
        ev('mem1-intro', 1, 11, trigger='auto', once=True, actions=[card('card_mem1_intro'), setv('mem1', 'seat')]),
        npc('mem1-anya', 10, 3, anya, direction='down', name='安雅', marker={'label': '安雅', 'kind': 'talk'},
            actions=[say('她用下巴指了指吧檯前的高腳椅。', speaker='player')]),
        ev('mem1-seat', 9, 6, name='吧檯前的高腳椅', marker={'label': '坐下', 'kind': 'quest'}, conditions=[cond('mem1', 'seat')],
           actions=[
               # 第一個動作不能是選擇題：按互動鍵的那一下會直接選到選擇題的第一個選項
               card('card_mem1_seat'),
               choice_action('回答她：躲雨，還是喝酒？', [
                   ('「躲雨。」', [card('card_mem1_rain')]),
                   ('「都有。」', [card('card_mem1_both')]),
               ], speaker='player'),
               card('card_mem1_order'),
               choice_action('點什麼？', [
                   ('「不要太苦就好。」', [card('card_mem1_bitter')]),
                   ('「來杯最烈的。」', [card('card_mem1_strong')]),
               ], speaker='player'),
               card('card_mem1_mix'),
               choice_action('杯子推到你面前。', [
                   ('喝一口', []),
                   ('先看著她', [card('card_mem1_stare')]),
               ], speaker='player'),
               card('card_mem1_taste'), setv('mem1', 'leave'),
           ]),
        ev('mem1-door', 9, 10, name='門口', marker={'label': '雨小了，該走了', 'kind': 'quest'}, conditions=[cond('mem1', 'leave')],
           actions=[card('card_mem1_leave'), setv('mem1', 'done'), jump('card_mem1_cg')]),
    ]
    g1 = [
        {'text': '坐到吧檯前的高腳椅', 'eventId': 'mem1-seat', 'conditions': [cond('mem1', 'seat')]},
        {'text': '雨小了，往門口走', 'eventId': 'mem1-door', 'conditions': [cond('mem1', 'leave')]},
    ]
    N(_map('m-mem-1', '回憶：暴雨的夜', art, m1, g1,
           _env(0, [('m1-bar', 9, 3, 6, '#ffc46b', False), ('m1-lounge', 10, 7, 7, '#ffb04d', False), ('m1-door', 9, 9, 3, '#ffd18a', False)])))
    N(_card('card_mem1_cg', '回憶：初遇', art, bg=art['cg-mem1']))

    # ── 回憶二〈黃銅匙〉：她在吧檯後（10,3）教他；匙在吧檯前角落（11,6） ──
    m2 = [
        guest(9, 7, 'up'),   # 還在學，穿便服；第三年才換上調酒師的衣服
        ev('mem2-intro', 1, 11, trigger='auto', once=True, actions=[card('card_mem2_intro'), setv('mem2', 'spoon')]),
        # 吧檯角落的匙：跟現在的吧檯同一張道具圖、同一個位置，拿起來就消失
        ev('mem2-spoon-visual', 0, 8, name='黃銅調酒匙視覺', free={'url': art['prop-spoon-tall'], 'x': 10.85, 'y': 4.35, 'w': 0.35, 'h': 2.7},
           conditions=[cond('mem2', 'spoon')]),
        ev('mem2-spoon', 11, 6, name='黃銅調酒匙', marker={'label': '黃銅匙', 'kind': 'quest'}, conditions=[cond('mem2', 'spoon')],
           actions=[say('吧檯角落的黃銅調酒匙，柄被她握得發亮。', speaker='player'), item('spoon_old', '黃銅調酒匙'), setv('mem2', 'teach')]),
        npc('mem2-anya', 10, 3, anya, direction='down', name='安雅', marker={'label': '安雅', 'kind': 'talk'},
            actions=[branch([cond('mem2', 'teach')],
                            [remove('spoon_old', '黃銅調酒匙'), card('card_mem2_spoon'),
                             choice_action('又混了。', [
                                 ('「妳教我。」', []),
                                 ('再試一次', [card('card_mem2_again')]),
                             ], speaker='player'),
                             card('card_mem2_hands'),
                             choice_action('她的手還覆在你手上。', [
                                 ('握緊她的手', [card('card_mem2_grip')]),
                                 ('轉過身', [card('card_mem2_turn')]),
                             ], speaker='player'),
                             card('card_mem2_mine'), setv('mem2', 'done'), jump('card_mem2_cg')],
                            [say('她在等那把匙。吧檯角落。', speaker='player')])]),
    ]
    g2 = [
        {'text': '拿吧檯角落的黃銅匙', 'eventId': 'mem2-spoon', 'conditions': [cond('mem2', 'spoon')]},
        {'text': '繞進吧檯，把匙交給她', 'eventId': 'mem2-anya', 'conditions': [cond('mem2', 'teach')]},
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
               choice_action('回答她甜不甜。', [('「剛好。」', []), ('「有點太甜。」', [])], speaker='player'),
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


    # 地圖上演出的對話卡（card(...) 叫的）也要是專案裡的卡
    have = {n['id'] for n in board['nodes']}
    for cid in L:
        if cid not in have:
            N(_card(cid, cid.replace('card_', ''), art))

    # 回憶結束回到原本那張地圖（主角回到該地圖的起點，變數與背包都還在）
    link('prologue', 'm-bar')
    link('card_mem1_enter', 'm-mem-1')
    link('card_mem1_cg', 'm-bar')
    link('card_mem2_enter', 'm-mem-2')
    link('card_mem2_cg', 'm-bar')
    link('card_mem3_enter', 'm-mem-3')
    link('card_mem3_cg', 'm-storage')
