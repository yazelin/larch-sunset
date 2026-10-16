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

        # 1. 便條紙與空高腳杯（在吧檯桌面上 x=8, y=6）
        ev('note', *PT['interact_note'], name='便條紙與空高腳杯', trigger='action',
           conditions=[cond('note_read', False)],
           actions=[
               say('吧檯頂上的黃銅吊燈泛著暖黃微光，橡木桌面上映著一圈朦朧的寂靜。\n空氣裡沒有了往常那股清甜的柑橘與微苦草本香氣——那是安雅平時站在這裡時，身上總會帶著的溫度。', speaker='player'),
               say('一只空的高腳杯底座下，壓著一張折得工整的淡黃色便條。\n便條紙右下角赫然簽著初遇的時間標記：【02:17】。\n沈淮抬頭看了一眼吧檯上方牆上的古董掛鐘——秒針早停了，指針同樣永遠定格在——【深夜 02:17】。\n那是三年前安雅第一次推開這扇大門的時刻。', speaker='player'),
               card('card_anya_note'),
               say('翻開便條背面，底下還夾著半張未完成的【風味筆記】。\n字跡斑駁，留著三個關鍵的空白——她是在考我，看我是否真的還記得那晚初遇的所有細節。', speaker='player'),
               # 第一道回憶：基酒底色
               choice_action(
                   '【風味回憶之一：杯底的基調】\n相遇那夜下著暴雨，她全身濕透走進酒吧。沈淮為她調出的第一抹溫暖，基酒的底色與甘甜是……？',
                   [
                       ('【貴腐晚收甜白酒】（熔金般的暖黃、濃郁蜂蜜與草本甘甜）', [
                           sound('heal'),
                           say('「沒錯……金黃得像日出，甜中帶著草本微苦回甘。那是我們約定好要一同調出的顏色。」', speaker='player'),
                       ]),
                       ('【黑麥威士忌】（泥煤煙燻與刺鼻辛辣）', [
                           sound('guard'),
                           say('「不……安雅怕苦，也受不了刺鼻的泥煤煙燻。初遇像破曉，絕不是這般漆黑沈重。」', speaker='player'),
                       ]),
                       ('【高純度伏特加】（冰冷刺骨，透明無味）', [
                           sound('guard'),
                           say('「不對……伏特加太冰冷了。那晚的吧檯，流淌的是融化寒意的溫甜。」', speaker='player'),
                       ]),
                   ],
                   speaker='player',
               ),
               # 第二道回憶：中段香氣
               choice_action(
                   '【風味回憶之二：溫潤的草本香】\n為了讓金黃酒液散發出如晚霞般的獨特光暈與草本回甘，安雅曾偷偷藏匿了什麼珍貴原料？',
                   [
                       ('【封存於香料儲藏間的「番紅花糖漿」】', [
                           sound('holy'),
                           say('「是番紅花！那種沉穩的草本清香……對了，她把那一瓶純手工慢熬的糖漿，藏進了儲藏間百葉窗下的暗格裡！」', speaker='player'),
                       ]),
                       ('【普通白砂糖水】（平淡無奇的甜膩）', [
                           sound('guard'),
                           say('「不對，那種香氣絕非普通糖水。那是她細細焙乾、浸泡了一整個月的特殊草本……」', speaker='player'),
                       ]),
                       ('【乾燥薄荷碎葉】（清涼嗆鼻）', [
                           sound('guard'),
                           say('「薄荷會破壞溫暖的層次。安雅曾笑著拍開我的手：『沈淮，要用溫潤如金的香料才行。』」', speaker='player'),
                       ]),
                   ],
                   speaker='player',
               ),
               # 第三道回憶：舌尖刺痛
               choice_action(
                   '【風味回憶之三：舌尖最後的刺痛】\n而在吞嚥的剎那，在喉頭留下如觸電般酥麻、微辣且難以忘懷的刺激……那是？',
                   [
                       ('【粉紅胡椒（如觸電般麻刺的微辣果香）】', [
                           sound('burst'),
                           flash('#ff69b4', strength=0.6),
                           say('「沒錯……粉紅胡椒！咬碎時喉嚨會泛起觸電般的酥麻感，像她第一次牽我手時的心跳……那罐胡椒鎖在她臥室的木盒裡！」', speaker='player'),
                       ]),
                       ('【紅辣椒粉（灼燒喉嚨的痛感）】', [
                           sound('guard'),
                           say('「絕不是辣椒的灼傷。她說過那是『像觸電般的酥麻』……」', speaker='player'),
                       ]),
                       ('【檸檬皮苦素（純粹酸澀）】', [
                           sound('guard'),
                           say('「酸澀只會讓人皺眉，留不下那種心顫的刺痛感……」', speaker='player'),
                       ]),
                   ],
                   speaker='player',
               ),
               sound('confirm'),
               flash('#ffd700', strength=0.7),
               balloon('idea', target='player'),
               say('「我想起來了……所有的配方都在我的腦海裡重現了！\n這把常用的【黃銅調酒匙】就放在旁邊的吧檯角落，先拿上它，等等撬開暗格和調酒都必須用到它！」', speaker='player'),
               setv('flavor_deduced', True),
               setv('note_read', True),
               setv('phase', 'spoon'),
           ],
           pages=[
               page('note_read_page', [cond('note_read', True)], [
                   say('便條紙背面已經被推理完整：『甜白酒為底、番紅花提香、粉紅胡椒收尾……這就是我們的初遇之味。』', speaker='player')
               ])
           ]),

        # 2. 吧檯角落的黃銅調酒匙視覺道具（尚未取得時顯現於吧檯面上，拿到後立即消失）
        ev('prop_spoon_visual', 0, 8, name='黃銅調酒匙視覺',
           free={'url': art['prop-spoon'], 'x': 11.2, 'y': 3.3, 'w': 0.35, 'h': 0.35},
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
        {'text': '閱讀吧檯上的便條紙與空高腳杯（初遇時間 02:17）', 'eventId': 'note', 'conditions': [cond('note_read', False)]},
        {'text': '拿取旁邊吧檯角落的黃銅調酒匙', 'eventId': 'spoon', 'conditions': [cond('spoon_taken', False)]},
        {'text': '帶著黃銅調酒匙前往左上香料儲藏間撬開暗格', 'eventId': 'door_storage', 'conditions': [cond('storage_pried', False)]},
        {'text': '帶著心型鑰匙前往右上臥室梳妝台（密碼 0217）', 'eventId': 'door_bedroom', 'conditions': [cond('box_unlocked', False)]},
        {'text': '在吧檯依序調製『晚霞』（番紅花→黃銅匙→研磨粉）', 'eventId': 'shaker', 'conditions': [cond('cocktail_mixed', False)]},
        {'text': '做出終局抉擇', 'eventId': 'shaker', 'conditions': []},
    ]

    # 現在的吧檯比回憶裡暗一些（回憶篇是全亮的暖燈，兩邊要看得出差別）
    env = {
        'weather': 'clear',
        'intensity': 0,
        'darkness': 0.25,
        'shake': 0,
        'lights': [
            {'id': 'bar-light', 'x': 9, 'y': 3, 'radius': 5, 'color': '#ffb347', 'flicker': True},
            {'id': 'lounge-light', 'x': 10, 'y': 7, 'radius': 6, 'color': '#ffa726', 'flicker': False},
            {'id': 'door-left', 'x': 3, 'y': 1, 'radius': 3, 'color': '#ffd180', 'flicker': False},
            {'id': 'door-right', 'x': 17, 'y': 1, 'radius': 3, 'color': '#ffd180', 'flicker': False},
        ]
    }

    m = map_dict('深夜吧檯', W, H, ground_url, layout.walls(D), events, guidance, env)
    return map_node(MAP_ID, '深夜吧檯', m, bgm=art.get('bgm-bar', ''))
