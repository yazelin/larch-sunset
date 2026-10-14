"""吧檯空間地圖（m-bar）：起點、調酒台、連接儲藏間與臥室。"""
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
        # 主角 沈淮
        ev('hero', 7, 6, actor='player', direction='up', sprite=walker(art['walk-shen']), actorId='shen'),

        # 1. 便條紙與空高腳杯
        ev('note', 7, 4, name='便條紙', trigger='action',
           conditions=[cond('note_read', False)],
           marker={'label': '便條紙', 'kind': 'quest'},
           actions=[
               card('card_bar_start'),
               card('card_anya_note'),
               setv('note_read', True),
               setv('phase', 'spoon'),
               balloon('idea', target='player'),
           ]),

        # 2. 吧檯角落的調酒匙
        ev('spoon', 12, 4, name='黃銅調酒匙', trigger='action',
           conditions=[cond('spoon_taken', False)],
           marker={'label': '黃銅調酒匙', 'kind': 'quest'},
           actions=[
               say('在吧檯角落的杯架旁，靜靜放著一把常用的黃銅調酒匙。匙柄帶有精細的螺紋，質地堅硬，平時她總是用這把匙輕巧地攪拌酒液。', speaker='沈淮'),
               item('spoon', '黃銅調酒匙'),
               sound('item'),
               setv('spoon_taken', True),
               setv('phase', 'storage'),
               balloon('heart', target='player'),
               say('有了這把調酒匙，或許能撬開儲藏間卡死的百葉窗暗格。', speaker='沈淮'),
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

        # 5. 調酒台（搜齊材料後可調酒）
        ev('shaker', 8, 4, name='調酒台', trigger='action',
           conditions=[cond('box_unlocked', True), cond('cocktail_mixed', False)],
           marker={'label': '調製『晚霞』', 'kind': 'quest'},
           actions=[
               say('材料已經齊全了：黃銅調酒匙、番紅花糖漿、粉紅胡椒研磨罐……還有這只高腳杯。', speaker='沈淮'),
               flash('#ffb347', strength=0.6, duration=400),
               sound('heal'),
               say('【注入番紅花糖漿】濃稠燦爛的金黃色液體注入杯底，宛如地平線初升的朝陽，散發溫潤甘甜的草本清香。', speaker='沈淮'),
               wait(400),
               sound('slash'),
               say('【黃銅匙攪拌】拿起黃銅調酒匙貼著杯壁輕輕攪拌——金黃色液體旋轉著融為一體，純淨透亮，折射出璀璨的琥珀光澤。', speaker='沈淮'),
               wait(400),
               flash('#ff69b4', strength=0.7, duration=500),
               sound('burst'),
               say('【研磨粉紅胡椒】旋轉研磨罐，磨入細碎顆粒，表面浮起一層曖昧的淡粉色油脂與碎粒。金黃與粉紅交織，如落日晚霞。', speaker='沈淮'),
               sound('door'),
               say('杯架下方的機關「喀噠」一聲下沉，吧檯暗格彈開，裡面是一封完整的遺書。', speaker='沈淮'),
               setv('cocktail_mixed', True),
               setv('phase', 'confession'),
               jump('card_confession'),
           ]),

        # 安雅的靈魂虛影（調完酒後現身於吧檯對面）
        npc('anya_ghost', 8, 3, walker(art['walk-anya-spirit']), direction='down',
            conditions=[cond('cocktail_mixed', True)]),
    ]

    guidance = [
        {'text': '閱讀吧檯上的便條紙', 'eventId': 'note', 'conditions': [cond('note_read', False)]},
        {'text': '拿取吧檯角落的調酒匙', 'eventId': 'spoon', 'conditions': [cond('spoon_taken', False)]},
        {'text': '前往香料儲藏間調查', 'eventId': 'door_storage', 'conditions': [cond('storage_pried', False)]},
        {'text': '前往臥室梳妝台開鎖', 'eventId': 'door_bedroom', 'conditions': [cond('box_unlocked', False)]},
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
            {'id': 'bar-light', 'x': 7.5, 'y': 3.5, 'radius': 4.5, 'color': '#ffb347', 'flicker': True},
            {'id': 'shelf-light', 'x': 11.5, 'y': 2, 'radius': 3.5, 'color': '#ffa07a', 'flicker': False},
            {'id': 'door-light', 'x': 2, 'y': 8, 'radius': 2.5, 'color': '#ffd180', 'flicker': False},
        ],
        'ambience': {
            'particles': 'embers',
            'density': 0.4,
            'rays': 0.5,
            'vignette': 0.35,
            'tint': '#ff7733',
            'tintStrength': 0.15
        }
    }

    m = map_dict('深夜吧檯', W, H, art['bg-bar'], walls(), events, guidance, env)
    return map_node(MAP_ID, '深夜吧檯', m, bgm=art.get('bgm-bar', ''))
