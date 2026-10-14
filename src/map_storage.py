"""香料儲藏間地圖（m-storage）：純分層層架遮擋、調查百葉窗暗格，取得番紅花糖漿與心型鑰匙。"""
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

        # ── 純分層遮擋物：左側香料層架與右側置物架 ──
        ev('obj_shelf_left', 0, 1, name='左側香料層架遮擋',
           free={'url': art['obj-storage-left'], 'x': 0.0, 'y': 1.5, 'w': 3.0, 'h': 5.0}),
        ev('obj_shelf_right', 11, 1, name='右側金屬置物架遮擋',
           free={'url': art['obj-storage-right'], 'x': 9.0, 'y': 1.5, 'w': 3.0, 'h': 5.0}),

        # 窗台暗格（百葉窗）
        ev('window_grate', 6, 1, name='百葉窗暗格', trigger='action',
           marker={'label': '百葉窗暗格', 'kind': 'quest'},
           actions=[
               branch([cond('storage_pried', True)],
                      [say('百葉窗下的暗格已被撬開，裡面原本隱藏的番紅花糖漿與心型鑰匙已被取出。', speaker='沈淮')],
                      [branch([cond('spoon_taken', True)],
                              [
                                  say('儲藏間陰涼而乾燥，空氣中混合著陳年八角、風乾橙皮與迷迭香的微苦草本香氣。\n夕陽的餘光透過百葉窗的細縫斜斜割進來，在浮塵中照亮了縫隙深處那抹深邃的琥珀金光。', speaker='沈淮'),
                                  say('我取出那柄黃銅調酒匙，將扁平堅韌的柄端插進百葉窗的木榫縫隙中，沉下身子稍稍發力——', speaker='沈淮'),
                                  sound('hit'),
                                  flash('#ffd700', strength=0.6, duration=350),
                                  say('『喀噠！』\n伴隨著一聲清脆的木榫彈響，窗台下方的隱藏暗格平滑地彈了出來！', speaker='沈淮'),
                                  say('暗格天鵝絨襯墊中央，端端正正擺著一瓶封存完好的【番紅花糖漿】。那濃郁純淨的金黃色澤，宛如凝固的黎明。', speaker='沈淮'),
                                  item('saffron', '番紅花糖漿'),
                                  sound('item'),
                                  wait(300),
                                  say('等等……糖漿後方還躺著一串金屬鑰匙！\n那是一串雕刻著纖細藤蔓的【心型吊墜鑰匙】……安雅平時總戴在胸口，貼著肌膚，從不離身。', speaker='沈淮'),
                                  say('握在手心裡，冰冷的金屬彷彿還帶著某種令人心悸的餘溫。這把鑰匙，一定能打開她在臥室裡鎖著的所有秘密。', speaker='沈淮'),
                                  item('key', '心型吊墜鑰匙'),
                                  sound('item'),
                                  balloon('idea', target='player'),
                                  setv('storage_pried', True),
                                  setv('phase', 'bedroom'),
                              ],
                              [
                                  say('窗台木榫咬合得死緊，徒手根本扒不開。必須找到細長而質地堅硬的金屬工具才能撬開這處暗格。', speaker='沈淮'),
                                  balloon('sweat', target='player'),
                              ])
                      ])
           ]),

        # 拾取後的番紅花糖漿與鑰匙視覺道具（在暗格彈開後展示）
        ev('prop_saffron_item', 0, 2, name='番紅花糖漿道具',
           free={'url': art['prop-saffron'], 'x': 5.5, 'y': 1.1, 'w': 0.9, 'h': 0.9},
           conditions=[cond('storage_pried', True)]),

        # 返回吧檯的大門
        ev('door_bar', 6, 8, name='返回吧檯', trigger='touch',
           marker={'label': '返回吧檯', 'kind': 'exit'},
           actions=[
               sound('door'),
               jump('m-bar', arrive={'x': 2, 'y': 8, 'direction': 'right'}),
           ]),
    ]

    guidance = [
        {'text': '使用黃銅調酒匙撬開百葉窗暗格', 'eventId': 'window_grate', 'conditions': [cond('storage_pried', False)]},
        {'text': '帶著心型鑰匙返回吧檯前往臥室', 'eventId': 'door_bar', 'conditions': []},
    ]

    env = {
        'weather': 'clear',
        'intensity': 0,
        'darkness': 0.45,
        'shake': 0,
        'fog': {'density': 0.2, 'color': '#edd8b0'},
        'lights': [
            {'id': 'window-sun', 'x': 6, 'y': 1, 'radius': 5, 'color': '#ffb347', 'flicker': False},
            {'id': 'door-glow', 'x': 6, 'y': 7.5, 'radius': 2.5, 'color': '#ffa07a', 'flicker': False},
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
