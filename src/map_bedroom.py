"""臥室梳妝台地圖（m-bedroom）：使用心型鑰匙打開木盒，發現粉紅胡椒與病歷單真相。"""
from mapkit import *

W, H = 12, 9
MAP_ID = 'm-bedroom'


def walls():
    w = set()
    for x in range(W):
        for y in range(H):
            # 外牆邊界（留出底部門口）
            if y == 0 or x == 0 or x == W - 1:
                w.add((x, y))
            if y == H - 1 and x != 3:
                w.add((x, y))
            # 左側雙人床
            if 1 <= x <= 3 and 2 <= y <= 5:
                w.add((x, y))
            # 右側梳妝台與大衣櫃
            if 8 <= x <= 10 and 1 <= y <= 2:
                w.add((x, y))
    return w


def build_bedroom(art):
    events = [
        # 主角 沈淮入場點
        ev('hero', 3, 7, actor='player', direction='up', sprite=walker(art['walk-shen']), actorId='shen'),

        # 梳妝台雕花木盒
        ev('vanity_box', 8, 2, name='雕花木盒', trigger='action',
           marker={'label': '雕花木盒', 'kind': 'quest'},
           actions=[
               branch([cond('box_unlocked', True)],
                      [say('木盒已經打開了，病歷單的碎頁已被握在手中，空氣裡殘留著淡淡的粉紅胡椒香氣。', speaker='沈淮')],
                      [branch([cond('storage_pried', True)],
                              [
                                  say('心型鑰匙插入鎖孔，順時針輕轉——「喀啦」，鎖扣彈開！', speaker='沈淮'),
                                  sound('door'),
                                  flash('#ffb6c1', strength=0.6, duration=350),
                                  say('裡面放著一罐【粉紅胡椒研磨罐】，以及幾張染血的病歷單碎頁。', speaker='沈淮'),
                                  item('pepper', '粉紅胡椒研磨罐'),
                                  sound('item'),
                                  # 播放回憶卡（安雅配音）與真相卡（沈淮震驚配音）
                                  card('card_bedroom_memory'),
                                  card('card_bedroom_shock'),
                                  setv('box_unlocked', True),
                                  setv('truth_known', True),
                                  setv('phase', 'mix'),
                                  balloon('exclamation', target='player'),
                              ],
                              [
                                  say('木盒上的小銅鎖雕刻著心型藤蔓，鎖孔極其纖巧。強行撬開只會損壞盒子，需要對應的心型小鑰匙。', speaker='沈淮'),
                                  balloon('sweat', target='player'),
                              ])
                      ])
           ]),

        # 返回吧檯的大門
        ev('door_bar', 3, 8, name='返回吧檯', trigger='touch',
           marker={'label': '返回吧檯', 'kind': 'exit'},
           actions=[
               sound('door'),
               jump('m-bar', arrive={'x': 13, 'y': 8, 'direction': 'left'}),
           ]),
    ]

    guidance = [
        {'text': '使用心型鑰匙打開木盒', 'eventId': 'vanity_box', 'conditions': [cond('box_unlocked', False)]},
        {'text': '帶著粉紅胡椒返回吧檯調酒', 'eventId': 'door_bar', 'conditions': []},
    ]

    env = {
        'weather': 'clear',
        'intensity': 0,
        'darkness': 0.4,
        'shake': 0,
        'fog': {'density': 0.15, 'color': '#fcd5ce'},
        'lights': [
            {'id': 'vanity-light', 'x': 8.5, 'y': 2.5, 'radius': 4.5, 'color': '#ffccd5', 'flicker': True},
            {'id': 'bed-lamp', 'x': 2, 'y': 2, 'radius': 3.5, 'color': '#ffe5d9', 'flicker': False},
        ],
        'ambience': {
            'particles': 'petals',
            'density': 0.4,
            'rays': 0.4,
            'vignette': 0.4,
            'tint': '#e8a598',
            'tintStrength': 0.15
        }
    }

    m = map_dict('臥室梳妝台', W, H, art['bg-bedroom'], walls(), events, guidance, env)
    return map_node(MAP_ID, '臥室梳妝台', m, bgm=art.get('bgm-bar', ''))
