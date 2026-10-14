"""吧檯空間地圖（m-bar）：純分層遮擋、吧檯調酒台、連接儲藏間與臥室。"""
from mapkit import *

W, H = 16, 10
MAP_ID = 'm-bar'


def walls():
    w = set()
    for x in range(W):
        for y in range(H):
            # 外牆邊界（留出門口）
            if y == 0 or x == 0 or x == W - 1:
                w.add((x, y))
            if y == H - 1 and x not in (2, 13):
                w.add((x, y))
            # 吧檯桌面（y == 4, x: 2..13，但兩側留出走道）
            if y == 4 and 2 <= x <= 13:
                w.add((x, y))
            # 後方酒架展示櫃（y in 1..2, x in 3..12）
            if 1 <= y <= 2 and 3 <= x <= 12:
                w.add((x, y))
    return w


def build_bar(art):
    events = [
        # 主角 沈淮（調酒師，可在吧檯內外穿梭）
        ev('hero', 7, 6, actor='player', direction='up', sprite=walker(art['walk-shen']), actorId='shen'),

        # ── 純分層遮擋物：吧檯桌面（Y-sorting 自動實現人站在吧檯後方時下半身被遮擋）──
        ev('obj_counter', 0, 1, name='吧檯桌面遮擋',
           free={'url': art['obj-bar-counter'], 'x': 2.0, 'y': 3.3, 'w': 12.0, 'h': 2.0}),

        # 1. 便條紙與空高腳杯（在吧檯桌面上清晰可見）
        ev('note', 7, 4, name='便條紙與空高腳杯', trigger='action',
           conditions=[cond('note_read', False)],
           marker={'label': '便條紙與高腳杯', 'kind': 'quest'},
           actions=[
               say('午夜兩點十七分。吧檯頂上的黃銅吊燈泛著暖黃微光，橡木桌面上映著一圈朦朧的寂靜。\n空氣裡沒有了往常那股清甜的柑橘與微苦草本香氣——那是安雅平時站在這裡時，身上總會帶著的溫度。', speaker='player'),
               say('一只空的高腳杯倒扣在吧檯中央，底座壓著一張折得工整的淡黃色便條。字跡纖細、末筆微微下沉，那是她的字。', speaker='player'),
               card('card_anya_note'),
               setv('note_read', True),
               setv('phase', 'spoon'),
               balloon('idea', target='player'),
               say('『初遇的滋味……金黃的甜白酒、泛著淡粉色的微辣感。我得把那杯酒調出來。』', speaker='player'),
           ],
           pages=[
               page('note_read_page', [cond('note_read', True)], [
                   say('杯底留著安雅的便條紙：『如果你還記得我們初遇的滋味，就替我把它完成吧。』', speaker='player')
               ])
           ]),

        # 2. 吧檯角落的黃銅調酒匙（桌面上可見實物）
        ev('spoon', 12, 4, name='黃銅調酒匙', trigger='action',
           free={'url': art['prop-spoon'], 'x': 11.7, 'y': 3.6, 'w': 0.8, 'h': 0.8},
           conditions=[cond('spoon_taken', False)],
           marker={'label': '黃銅調酒匙', 'kind': 'quest'},
           actions=[
               say('杯架角落靜靜躺著這把常用的黃銅調酒匙。螺紋細密精緻，柄端被反覆握持得溫潤光滑。\n她總是用這把匙輕巧地貼著杯壁旋轉，讓酒液如晚霞般層層舒展。', speaker='player'),
               item('spoon', '黃銅調酒匙'),
               sound('item'),
               setv('spoon_taken', True),
               setv('phase', 'storage'),
               balloon('heart', target='player'),
               say('調酒匙末端微扁而堅硬。或許……可以用它撬開儲藏間那扇卡死多年的百葉窗木暗格。', speaker='player'),
           ],
           pages=[
               page('spoon_taken_page', [cond('spoon_taken', True)], [
                   say('杯架角落已經空了，黃銅調酒匙已收入隨身背包中。', speaker='player')
               ])
           ]),

        # 3. 儲藏間大門
        ev('door_storage', 2, 9, name='通往香料儲藏間', trigger='touch',
           marker={'label': '香料儲藏間', 'kind': 'exit'},
           actions=[
               sound('door'),
               jump('m-storage', arrive={'x': 6, 'y': 7, 'direction': 'up'}),
           ]),

        # 4. 臥室大門
        ev('door_bedroom', 13, 9, name='通往臥室梳妝台', trigger='touch',
           marker={'label': '臥室梳妝台', 'kind': 'exit'},
           actions=[
               sound('door'),
               jump('m-bedroom', arrive={'x': 3, 'y': 7, 'direction': 'up'}),
           ]),

        # 5. 調酒工作台（材料齊全後啟動調酒儀式）
        ev('shaker', 8, 4, name='調酒工作台', trigger='action',
           conditions=[cond('box_unlocked', True), cond('cocktail_mixed', False)],
           marker={'label': '調製『晚霞』', 'kind': 'quest'},
           actions=[
               say('所有被她刻意藏匿的材料，終於在深夜的吧檯前聚齊：\n一瓶金黃濃稠的【番紅花糖漿】、一柄質地堅硬的【黃銅調酒匙】、一罐散發觸電般麻刺感的【粉紅胡椒研磨罐】……以及那張揭示了殘酷真相的病歷單。', speaker='player'),
               flash('#ffb347', strength=0.6, duration=450),
               sound('heal'),
               say('【第一步：注入番紅花糖漿】\n深金黃色的厚重糖漿順著杯壁緩緩流淌入高腳杯底。宛如初升朝陽的第一抹熔金，溫潤甘甜的草本清香瞬間充盈了空氣。', speaker='player'),
               wait(450),
               sound('slash'),
               say('【第二步：黃銅匙勻速攪拌】\n手握調酒匙貼緊杯壁，以優雅而穩定的節奏旋轉。金黃的酒液如旋渦般融為一體，純淨透亮，折射出璀璨溫暖的琥珀光芒。', speaker='player'),
               wait(450),
               flash('#ff69b4', strength=0.75, duration=500),
               sound('burst'),
               say('【第三步：研磨粉紅胡椒】\n轉動研磨罐，細碎微紅的胡椒顆粒如落櫻般散落在金黃酒面上。油脂在燈下悄然暈染，一股極具誘惑又帶有刺痛微辣的奇妙辛香撲鼻而來！金黃與粉紅交織融合，宛如深秋黃昏最後的落日晚霞。', speaker='player'),
               sound('door'),
               say('機關「喀噠」一聲沉悶作響，杯架下方的暗格悄然滑出，裡面躺著一封完整的白色遺書。', speaker='player'),
               setv('cocktail_mixed', True),
               setv('phase', 'confession'),
               jump('card_confession'),
           ]),

        # 安雅的靈魂虛影（調完酒後現身於吧檯對面）
        npc('anya_ghost', 8, 3, walker(art['walk-anya-spirit']), direction='down',
            conditions=[cond('cocktail_mixed', True)]),
    ]

    guidance = [
        {'text': '閱讀吧檯上的便條紙與空高腳杯', 'eventId': 'note', 'conditions': [cond('note_read', False)]},
        {'text': '拿取吧檯角落的黃銅調酒匙', 'eventId': 'spoon', 'conditions': [cond('spoon_taken', False)]},
        {'text': '前往香料儲藏間調查百葉窗暗格', 'eventId': 'door_storage', 'conditions': [cond('storage_pried', False)]},
        {'text': '前往臥室梳妝台使用心型鑰匙開盒', 'eventId': 'door_bedroom', 'conditions': [cond('box_unlocked', False)]},
        {'text': '在吧檯調製『晚霞』', 'eventId': 'shaker', 'conditions': [cond('cocktail_mixed', False)]},
        {'text': '做出終局抉擇', 'eventId': 'shaker', 'conditions': []},
    ]

    env = {
        'weather': 'clear',
        'intensity': 0,
        'darkness': 0.35,
        'shake': 0,
        'fog': {'density': 0.15, 'color': '#ffa07a'},
        'lights': [
            {'id': 'bar-light', 'x': 7, 'y': 3, 'radius': 4.5, 'color': '#ffb347', 'flicker': True},
            {'id': 'shelf-light', 'x': 11, 'y': 2, 'radius': 3.5, 'color': '#ffa07a', 'flicker': False},
            {'id': 'door-light', 'x': 2, 'y': 8, 'radius': 2.5, 'color': '#ffd180', 'flicker': False},
        ],
        'ambience': {
            'particles': 'embers',
            'density': 0.45,
            'rays': 0.5,
            'vignette': 0.35,
            'tint': '#ff7733',
            'tintStrength': 0.15
        }
    }

    m = map_dict('深夜吧檯', W, H, art['bg-bar'], walls(), events, guidance, env)
    return map_node(MAP_ID, '深夜吧檯', m, bgm=art.get('bgm-bar', ''))
