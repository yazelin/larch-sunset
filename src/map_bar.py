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
               say('吧檯上留著一只碟形杯。杯底剩下薄薄一層，金黃沉在底下，粉紅浮在上面。\n杯子旁邊壓著一張摺好的便條。', speaker='player'),
               say('牆上的掛鐘停在兩點十七分。三年前，她就是抬頭看了這座鐘，說我是她今天最後一個客人。\n不知道是誰把它停在那裡的。', speaker='player'),
               card('card_anya_note'),
               say('水槽裡有一小撮灰。灰底下壓著半張沒燒完的紙，是她的字。\n風味筆記。燒掉的那一半捲成黑邊，剩下的字斷在三個地方。\n我認得這三個空格。那是她給我的第一杯酒。', speaker='player'),
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
                   '『香：＿＿＿＿糖漿，兩匙。他說剛好。』',
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
                   say('甜白酒為底，番紅花糖漿兩匙，粉紅胡椒磨在杯口。〈破曉〉。', speaker='player')
               ])
           ]),

        # 2. 吧檯角落的黃銅調酒匙視覺道具（尚未取得時顯現於吧檯面上，拿到後立即消失）
        ev('prop_spoon_visual', 0, 8, name='黃銅調酒匙視覺',
           free={'url': art['prop-spoon-tall'], 'x': 10.85, 'y': 4.35, 'w': 0.35, 'h': 2.7},
           conditions=[cond('spoon_taken', False)]),

        # 黃銅調酒匙調查行動點（位於吧檯外側 x=11, y=6）
        ev('spoon', *PT['interact_spoon'], name='黃銅調酒匙', trigger='action',
           actions=[
               branch([cond('spoon_taken', True)],
                      [say('杯架角落已經空了，黃銅調酒匙已收入隨身背包中。', speaker='player')],
                      [
                          say('杯架角落靜靜躺著這把常用的黃銅調酒匙。螺紋細密精緻，柄端被反覆握持得溫潤光滑。\n她總是用這把匙輕巧地貼著杯壁旋轉，讓酒液如晚霞般層層舒展。', speaker='player'),
                          item('spoon', '黃銅調酒匙'),
                          sound('item'),
                          setv('spoon_taken', True),
                          setv('phase', 'storage'),
                          balloon('heart', target='player'),
                          say('調酒匙末端微扁而質地堅硬。有了它，就能去左上角香料儲藏間撬開木榫暗格，取得第一步所需的【番紅花糖漿】了！', speaker='player'),
                          jump('card_mem2_enter'),
                      ])
           ]),

        # 3. 通往香料儲藏間（左上拱門通道）
        ev('door_storage', *PT['door_storage'], name='通往香料儲藏間', trigger='touch',
           actions=[
               sound('door'),
               jump('m-storage', arrive={'x': 8, 'y': 9, 'direction': 'up'}),
           ]),

        # 4. 通往臥室梳妝台（右上拱門通道）
        ev('door_bedroom', *PT['door_bedroom'], name='通往臥室梳妝台', trigger='touch',
           actions=[
               sound('door'),
               jump('m-bedroom', arrive={'x': 8, 'y': 9, 'direction': 'up'}),
           ]),

        # 5. 調酒工作台（材料齊全後啟動調酒儀式，位於吧檯內側 x=9, y=3）
        ev('shaker', *PT['interact_shaker'], name='調酒工作台', trigger='action',
           conditions=[cond('box_unlocked', True), cond('cocktail_mixed', False)],
           actions=[
               say('所有被她刻意藏匿的材料，終於在深夜的吧檯前聚齊：\n一瓶金黃濃稠的【番紅花糖漿】、一柄質地堅硬的【黃銅調酒匙】、一罐散發觸電般麻刺感的【粉紅胡椒研磨罐】……以及那張揭示了殘酷真相的病歷單。', speaker='player'),
               # 調酒步驟一：底色注入
               choice_action(
                   '【調酒儀式 · 第一步：基底注入】在高腳杯底應該先注入哪種材料？',
                   [
                       ('【緩緩注入深金黃色的「番紅花糖漿」】', [
                           sound('heal'),
                           flash('#ffb347', strength=0.6, duration=450),
                           say('厚重濃稠的金黃糖漿順著杯壁緩緩流淌入高腳杯底。宛如初升朝陽的第一抹熔金，溫潤甘甜的草本清香瞬間充盈了空氣。', speaker='player'),
                       ]),
                       ('【直接倒滿烈酒】', [
                           sound('guard'),
                           say('「不行，沒有厚重的金黃糖漿沉底，晚霞的漸層就無法成型。」沈淮穩住心神，重新倒入番紅花糖漿。', speaker='player'),
                           sound('heal'),
                           flash('#ffb347', strength=0.6, duration=450),
                       ]),
                   ],
                   speaker='player',
               ),
               wait(300),
               # 調酒步驟二：調酒匙旋轉
               choice_action(
                   '【調酒儀式 · 第二步：旋轉融合】手握黃銅調酒匙，該以何種手法調和？',
                   [
                       ('【貼緊杯壁，以優雅而穩定的節奏勻速旋轉】', [
                           sound('slash'),
                           say('手握調酒匙貼緊杯壁，以安雅平日最熟悉的手勢勻速旋轉。金黃的酒液如旋渦般融為一體，純淨透亮，折射出璀璨溫暖的琥珀光芒。', speaker='player'),
                       ]),
                       ('【用力上下抽動調酒匙】', [
                           sound('guard'),
                           say('「太過粗暴會破壞酒體的清澈度。」沈淮放輕力道，改以手腕帶動調酒匙，在杯中旋出一道優美的金黃漩渦。', speaker='player'),
                           sound('slash'),
                       ]),
                   ],
                   speaker='player',
               ),
               wait(300),
               # 調酒步驟三：研磨粉紅胡椒
               choice_action(
                   '【調酒儀式 · 第三步：舌尖最後的刺痛】最後的點睛之筆是……？',
                   [
                       ('【輕輕轉動研磨罐，撒上細碎嫣紅的「粉紅胡椒」】', [
                           flash('#ff69b4', strength=0.8, duration=500),
                           sound('burst'),
                           say('轉動研磨罐，細碎微紅的胡椒顆粒如落櫻般散落在金黃酒面上。油脂在燈下悄然暈染，一股極具誘惑又帶有刺痛微辣的奇妙辛香撲鼻而來！金黃與粉紅交織融合，宛如深秋黃昏最後的落日晚霞。', speaker='player'),
                       ]),
                   ],
                   speaker='player',
               ),
               sound('door'),
               say('機關「喀噠」一聲沉悶作響，杯架下方的暗格悄然滑出，裡面躺著一封完整的白色遺書。', speaker='player'),
               setv('cocktail_mixed', True),
               setv('phase', 'confession'),
               jump('card_confession'),
           ]),

        # 安雅的靈魂虛影（調完酒後現身於吧檯外側高腳椅前 x=7, y=6）
        npc('anya_ghost', 7, 6, walker(art['walk-anya-spirit']), direction='up',
            conditions=[cond('cocktail_mixed', True)]),

    ]

    # 物件圖層事件（自動從 layout 放置於地圖外圍 hold_cells）
    events += layout.events(D, urls)

    guidance = [
        {'text': '看看吧檯上的空杯和便條', 'eventId': 'note', 'conditions': [cond('note_read', False)]},
        {'text': '拿取旁邊吧檯角落的黃銅調酒匙', 'eventId': 'spoon', 'conditions': [cond('spoon_taken', False)]},
        {'text': '帶著黃銅調酒匙前往左上香料儲藏間撬開暗格', 'eventId': 'door_storage', 'conditions': [cond('storage_pried', False)]},
        {'text': '帶著心型鑰匙前往右上臥室梳妝台（密碼 0217）', 'eventId': 'door_bedroom', 'conditions': [cond('box_unlocked', False)]},
        {'text': '在吧檯依序調製『晚霞』（番紅花→黃銅匙→研磨粉）', 'eventId': 'shaker', 'conditions': [cond('cocktail_mixed', False)]},
        {'text': '做出終局抉擇', 'eventId': 'shaker', 'conditions': []},
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
