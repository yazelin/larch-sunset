"""深夜吧檯地圖（m-bar）：精緻日系厚塗手繪動漫風格，純分層遮擋與無雜訊沉浸介面。
依據原作「THE AMBER GROTTO」原畫完整還原：
弧形實木吧檯＋高腳椅＋左側翻板通道、大琥珀酒櫃、右側皮革沙發卡座雅座區、中央深紅金邊地毯。
"""
import os, pathlib
from mapkit import *
import layout

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = layout.load('bar')
MAP_ID = D['map']['id']
W, H = D['map']['w'], D['map']['h']
PT = {k: tuple(v) for k, v in D['points'].items()}


def build_bar(art):
    real = not os.environ.get('BLOCKS') and (ROOT / 'assets/maps/bar_ground.webp').exists() and \
        all((ROOT / f"assets/objects/bar/{o['name']}.webp").exists() for o in layout.objects(D))
    kind = 'objects' if real else 'blocks'
    ground_url = f'/files/assets/maps/bar_{"ground" if real else "blocks"}.webp'
    urls = {o['name']: f"/files/assets/{kind}/bar/{o['name']}.webp" for o in layout.objects(D)}

    events = [
        # 主角 沈淮（開場立於中央天鵝絨紅毯 x=12, y=7）
        ev('hero', *PT['hero_start'], actor='player', direction='up', sprite=walker(art['walk-shen']), actorId='shen'),

        # 1. 空杯與便條（吧檯桌面 x=8, y=6）→ 燒到一半的風味筆記三題 → 回憶一
        ev('note', *PT['interact_note'], name='空杯與便條', trigger='action',
           conditions=[cond('note_read', False)],
           actions=[
               say('吧檯的燈我沒開。窗外的路燈照進來，冷冷的，落在她的位置上。\n空氣裡沒有柑橘，也沒有草本。她站在這裡的時候，身上總是那個味道。', speaker='player'),
               say('吧檯上留著一只碟形杯。杯底乾成一圈金黃，上緣黏著幾粒粉紅胡椒。\n杯子旁邊壓著一張摺好的便條。', speaker='player'),
               say('牆上的掛鐘停在兩點十七分。三年前，她就是抬頭看了這座鐘，說我是她今天最後一個客人。', speaker='player'),
               card('card_anya_note'),
               say('水槽裡有一小撮灰。灰底下壓著半張沒燒完的紙，是她的字。\n風味筆記。燒掉的那一半捲成黑邊，剩下的字斷在三個地方。\n我認得這三種材料。那是她給我的第一杯酒。', speaker='player'),
               # 第一格：底
               choice_action(
                   '『底：＿＿＿＿。要甜，不要苦。他怕苦。』',
                   [
                       ('貴腐甜白酒', [
                           sound('heal'),
                           say('貴腐甜白酒。那一晚她從酒櫃最上層拿下來，瓶身還沾著灰。', speaker='player'),
                       ]),
                       ('黑麥威士忌', [
                           sound('guard'),
                           say('她怕苦，我也怕苦。那一杯裡沒有一點煙燻。', speaker='player'),
                       ]),
                       ('伏特加', [
                           sound('guard'),
                           say('伏特加太冷了。那一晚我渾身濕透，她給我的是暖的。', speaker='player'),
                       ]),
                   ],
                   speaker='player',
               ),
               # 第二格：香
               choice_action(
                   '『香：＿＿＿＿糖漿。〈破曉〉是一小匙，這一杯要兩匙。』',
                   [
                       ('番紅花', [
                           sound('holy'),
                           say('番紅花。她自己熬的，一次只熬一小瓶，平常收在儲藏間。', speaker='player'),
                       ]),
                       ('白砂糖', [
                           sound('guard'),
                           say('白糖水調不出那種顏色。那一杯是金的。', speaker='player'),
                       ]),
                       ('薄荷', [
                           sound('guard'),
                           say('我第一次伸手拿薄荷的時候，她笑著拍開我的手：「要溫的，沈淮。」', speaker='player'),
                       ]),
                   ],
                   speaker='player',
               ),
               # 第三格：收尾
               choice_action(
                   '『收尾：＿＿＿＿，磨在杯口。像天快亮。』',
                   [
                       ('粉紅胡椒', [
                           sound('burst'),
                           flash('#ff69b4', strength=0.5),
                           say('粉紅胡椒。咬碎的時候，舌尖會麻一下。', speaker='player'),
                       ]),
                       ('紅辣椒粉', [
                           sound('guard'),
                           say('辣椒會燒。那一杯不會燒，只是麻了一下。', speaker='player'),
                       ]),
                       ('檸檬皮', [
                           sound('guard'),
                           say('檸檬太酸了。那一杯是甜的，最後才麻一下。', speaker='player'),
                       ]),
                   ],
                   speaker='player',
               ),
               say('〈破曉〉。那是她給那杯酒取的名字。\n紙的最上面燒掉了，只剩一個字的下半截。我看了很久，認不出來。', speaker='player'),
               setv('flavor_deduced', True),
               setv('note_read', True),
               setv('phase', 'spoon'),
               jump('card_mem1_enter'),
           ],
           pages=[
               page('note_read_page', [cond('note_read', True)], [
                   say('甜白酒為底，番紅花糖漿，粉紅胡椒磨在杯口。〈破曉〉。可是這一張寫的是兩匙。', speaker='player')
               ])
           ]),

        # 2. 吧檯角落的黃銅調酒匙視覺道具（尚未取得時顯現於吧檯面上，拿到後立即消失）
        ev('prop_spoon_visual', 0, 8, name='黃銅調酒匙視覺',
           free={'url': art['prop-spoon-tall'], 'x': 10.85, 'y': 4.35, 'w': 0.35, 'h': 2.7},
           conditions=[cond('spoon_taken', False)]),

        # 黃銅調酒匙（吧檯外側 x=11, y=6）：她唯一沒藏的東西 → 回憶二
        ev('spoon', *PT['interact_spoon'], name='黃銅調酒匙', trigger='action',
           actions=[
               branch([cond('spoon_taken', True)],
                      [say('匙在我口袋裡。', speaker='player')],
                      [
                          say('吧檯角落，黃銅匙洗得很乾淨，放在她平常放的位置。\n她把東西都收走了，只留下這一把。', speaker='player'),
                          item('spoon', '黃銅調酒匙'),
                          sound('item'),
                          setv('spoon_taken', True),
                          setv('phase', 'storage'),
                          jump('card_mem2_enter'),
                      ])
           ]),

        # 3. 通往香料儲藏間（左上）
        ev('door_storage', *PT['door_storage'], name='通往香料儲藏間', trigger='touch',
           actions=[
               sound('door'),
               jump('m-storage', arrive={'x': 8, 'y': 9, 'direction': 'up'}),
           ]),

        # 4. 上樓的樓梯（右上，通往兩人的臥室）
        ev('door_bedroom', *PT['door_bedroom'], name='上樓', trigger='touch',
           actions=[
               sound('door'),
               jump('m-bedroom', arrive={'x': 8, 'y': 9, 'direction': 'up'}),
           ]),

        # 5. 她的工作位（吧檯內側 x=9, y=3）：調〈晚霞〉→ 杯墊下的遺言
        ev('shaker', *PT['interact_shaker'], name='她的位置', trigger='action',
           conditions=[cond('phase', 'mix'), cond('cocktail_mixed', False)],
           actions=[
               say('我走進吧檯，站到她的位置。\n三年來，我第一次站在這裡，她不在旁邊。', speaker='player'),
               choice_action(
                   '先放什麼？',
                   [
                       ('甜白酒，再兩匙番紅花糖漿', [
                           sound('heal'),
                           flash('#ffb347', strength=0.4, duration=450),
                           say('甜白酒倒進碟形杯，糖漿順著杯壁滑下去，沉在底下。', speaker='player'),
                       ]),
                       ('先磨胡椒', [
                           sound('guard'),
                           say('她說過，胡椒最後才放。我先倒了甜白酒和糖漿。', speaker='player'),
                           flash('#ffb347', strength=0.4, duration=450),
                       ]),
                   ],
                   speaker='player',
               ),
               wait(300),
               choice_action(
                   '匙怎麼轉？',
                   [
                       ('貼著杯壁，慢慢轉，不要用力', [
                           sound('slash'),
                           say('貼著杯壁，慢慢轉。我好像又感覺到她的手覆在我手上。\n金黃在杯裡旋開，沒有混。', speaker='player'),
                       ]),
                       ('用力攪勻', [
                           sound('guard'),
                           say('「不要用力。」她的聲音好像就在耳邊。我放輕手，貼著杯壁慢慢轉。', speaker='player'),
                           sound('slash'),
                       ]),
                   ],
                   speaker='player',
               ),
               wait(300),
               choice_action(
                   '最後是那罐胡椒。',
                   [
                       ('磨在杯口', [
                           flash('#ff69b4', strength=0.6, duration=500),
                           sound('burst'),
                           say('我轉了三下研磨罐。粉紅的碎粒落在金黃上，慢慢浮起來。\n金黃沉在底下，粉紅浮在上面。跟她留下的那只空杯，是同一個顏色。', speaker='player'),
                       ]),
                   ],
                   speaker='player',
               ),
               say('我照她的習慣，把杯子放上她出杯用的那塊杯墊。\n杯墊底下露出一角紙。', speaker='player'),
               setv('cocktail_mixed', True),
               setv('phase', 'confession'),
               jump('card_confession'),
           ]),

        # 頭七店裡她的東西：可選看，不擋主線（design/重寫.md 第二輪）
        ev('look_apron', 12, 3, name='她的圍裙', trigger='action', marker={'label': '她的圍裙', 'kind': 'talk'},
           actions=[say('掛鉤上是她的圍裙。口袋裡有一支沒蓋好的筆，和一張寫了一半的進貨單。\n她的字總是往右上斜，像在趕時間。我把筆蓋蓋上。', speaker='player')]),
        ev('look_labels', 8, 3, name='酒櫃的標籤', trigger='action', marker={'label': '酒櫃的標籤', 'kind': 'talk'},
           actions=[say('酒櫃上每一瓶都貼著她手寫的標籤。「甜白酒，貴腐，別給客人倒太滿。」\n最上層那瓶寫著：「沈淮的，不准賣。」我不知道她什麼時候貼的。', speaker='player')]),
        ev('look_mug', 13, 6, name='她的馬克杯', trigger='action', marker={'label': '她的馬克杯', 'kind': 'talk'},
           actions=[say('吧檯尾巴擺著她的馬克杯，杯緣有一圈淡淡的口紅印。\n她調一整晚的酒，自己只喝白開水，說舌頭要留給客人。我拿起來，裡面的水早就乾了。', speaker='player')]),

        # 頭七的她：調完酒後出現在吧檯後她的位置（10,3）
        npc('anya_ghost', 10, 3, walker(art['walk-anya-spirit']), direction='down',
            conditions=[cond('cocktail_mixed', True)]),

    ]

    # 物件圖層事件（自動從 layout 放置於地圖外圍 hold_cells）
    events += layout.events(D, urls)

    guidance = [
        {'text': '看看吧檯上的空杯和便條', 'eventId': 'note', 'conditions': [cond('note_read', False)]},
        {'text': '吧檯角落的黃銅匙', 'eventId': 'spoon', 'conditions': [cond('spoon_taken', False)]},
        {'text': '去儲藏間找她熬的番紅花糖漿', 'eventId': 'door_storage', 'conditions': [cond('phase', 'storage')]},
        {'text': '上樓，回我們的房間', 'eventId': 'door_bedroom', 'conditions': [cond('phase', 'bedroom')]},
        {'text': '站到她的位置', 'eventId': 'shaker', 'conditions': [cond('phase', 'mix')]},
    ]

    # 頭七的現在：冷藍主光（窗外路燈），只留吧檯上那只空杯一點暖光；回憶是暖金，兩邊一眼看得出（design/重寫.md 光的顏色）
    env = {
        'weather': 'clear',
        'intensity': 0,
        'darkness': 0.55,
        'shake': 0,
        'lights': [
            {'id': 'window-street', 'x': 15, 'y': 5, 'radius': 9, 'color': '#6f8fc9', 'flicker': False},
            {'id': 'bar-cold', 'x': 9, 'y': 4, 'radius': 6, 'color': '#5d78b0', 'flicker': False},
            {'id': 'glass-warm', 'x': 8, 'y': 5, 'radius': 1.6, 'color': '#ffb35c', 'flicker': True},
            {'id': 'door-left', 'x': 3, 'y': 1, 'radius': 2.5, 'color': '#7d95c4', 'flicker': False},
            {'id': 'door-right', 'x': 17, 'y': 1, 'radius': 2.5, 'color': '#7d95c4', 'flicker': False},
        ],
        # 引擎的 ambience.tint 會替整張圖蒙一層色（rpg-engine 內建範例的雪地就這樣用）
        'ambience': {'tint': '#3c5c9c', 'tintStrength': 0.38, 'vignette': 0.4, 'particles': 'motes', 'density': 0.12},
    }

    m = map_dict('頭七的吧檯', W, H, ground_url, layout.walls(D), events, guidance, env)
    return map_node(MAP_ID, '頭七的吧檯', m, bgm=art.get('bgm-bar', ''))
