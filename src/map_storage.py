"""香料儲藏間地圖（m-storage）：調查百葉窗暗格，取得番紅花糖漿與心型鑰匙。"""
from mapkit import *

W, H = 12, 9
MAP_ID = 'm-storage'


def walls():
    w = set()
    for x in range(W):
        for y in range(H):
            # 外牆邊界（留出底部門口）
            if y == 0 or x == 0 or x == W - 1:
                w.add((x, y))
            if y == H - 1 and x != 6:
                w.add((x, y))
            # 兩側香料層架
            if (1 <= x <= 2 or 9 <= x <= 10) and 2 <= y <= 4:
                w.add((x, y))
            # 窗台兩側
            if y == 1 and x in (4, 7):
                w.add((x, y))
    return w


def build_storage(art):
    events = [
        # 主角 沈淮入場點
        ev('hero', 6, 7, actor='player', direction='up', sprite=walker(art['walk-shen']), actorId='shen'),

        # 窗台暗格（百葉窗）
        ev('window_grate', 6, 1, name='百葉窗暗格', trigger='action',
           marker={'label': '百葉窗暗格', 'kind': 'quest'},
           actions=[
               branch([cond('storage_pried', True)],
                      [say('暗格已經被撬開了，裡面的番紅花糖漿與心型鑰匙已被取出。', speaker='沈淮')],
                      [branch([cond('spoon_taken', True)],
                              [
                                  say('我將黃銅調酒匙插進木窗縫隙稍稍使力——『喀噠！』卡榫應聲彈開，窗台下的暗格滑出！', speaker='沈淮'),
                                  sound('hit'),
                                  flash('#ffd700', strength=0.6, duration=350),
                                  say('裡面放著一瓶深金黃色的【番紅花糖漿】。', speaker='沈淮'),
                                  item('saffron', '番紅花糖漿'),
                                  sound('item'),
                                  wait(300),
                                  say('等等……糖漿後方還躺著一串金屬鑰匙！這串【心型吊墜鑰匙】……安雅平時總戴在胸口，從不離身。它一定能打開她鎖在臥室裡的東西。', speaker='沈淮'),
                                  item('key', '心型吊墜鑰匙'),
                                  sound('item'),
                                  balloon('idea', target='player'),
                                  setv('storage_pried', True),
                                  setv('phase', 'bedroom'),
                              ],
                              [
                                  say('鐵木卡榫咬得太死，徒手完全拉不開。必須找到細長又堅硬的金屬工具才能撬開。', speaker='沈淮'),
                                  balloon('sweat', target='player'),
                              ])
                      ])
           ]),

        # 返回吧檯的大門
        ev('door_bar', 6, 8, name='返回吧檯', trigger='touch',
           marker={'label': '返回吧檯', 'kind': 'exit'},
           actions=[
               sound('door'),
               jump('m-bar', arrive={'x': 2, 'y': 8, 'direction': 'right'}),
           ]),
    ]

    guidance = [
        {'text': '使用調酒匙撬開百葉窗暗格', 'eventId': 'window_grate', 'conditions': [cond('storage_pried', False)]},
        {'text': '帶著心型鑰匙返回吧檯', 'eventId': 'door_bar', 'conditions': []},
    ]

    env = {
        'weather': 'clear',
        'intensity': 0,
        'darkness': 0.45,
        'shake': 0,
        'fog': {'density': 0.2, 'color': '#edd8b0'},
        'lights': [
            {'id': 'window-sun', 'x': 6, 'y': 1, 'radius': 5, 'color': '#ffb347', 'flicker': False},
            {'id': 'door-glow', 'x': 6, 'y': 7.5, 'radius': 2.5, 'color': '#ffa07a', 'flicker': false if 'false' in globals() else False},
        ],
        'ambience': {
            'particles': 'motes',
            'density': 0.5,
            'rays': 0.7,
            'vignette': 0.35,
            'tint': '#e6a860',
            'tintStrength': 0.2
        }
    }

    m = map_dict('香料儲藏間', W, H, art['bg-storage'], walls(), events, guidance, env)
    return map_node(MAP_ID, '香料儲藏間', m, bgm=art.get('bgm-bar', ''))
