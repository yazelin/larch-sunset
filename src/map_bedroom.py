"""臥室梳妝台地圖（m-bedroom）：純分層大床與梳妝台遮擋、使用心型鑰匙解鎖木盒與病歷真相。"""
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

        # ── 純分層遮擋物：左側大床與右側梳妝台 ──
        ev('obj_bed', 0, 1, name='臥室大床遮擋',
           free={'url': art['obj-bedroom-bed'], 'x': 0.0, 'y': 2.0, 'w': 4.0, 'h': 5.0}),
        ev('obj_vanity', 11, 1, name='梳妝台鏡台遮擋',
           free={'url': art['obj-bedroom-vanity'], 'x': 7.5, 'y': 1.5, 'w': 4.0, 'h': 4.0}),

        # 梳妝台雕花木盒
        ev('vanity_box', 8, 2, name='雕花木盒', trigger='action',
           marker={'label': '雕花木盒', 'kind': 'quest'},
           actions=[
               branch([cond('box_unlocked', True)],
                      [say('雕花木盒已經開啟，幾張泛黃染血的病歷單碎頁已被握在手心。空氣中依然殘留著那股微弱而刺痛的粉紅胡椒香氣。', speaker='沈淮')],
                      [branch([cond('storage_pried', True)],
                              [
                                  say('推開臥室的門，屋裡安靜得能聽見自己逐漸紊亂的心跳聲。\n梳妝台上散落著乾枯的花瓣，中央擺著那只刻滿心型藤蔓的小胡桃木盒。交往的這三年裡，她從不曾讓我碰它。', speaker='沈淮'),
                                  say('我將胸前那串心型鑰匙對準鎖孔輕輕旋入——順時針輕轉，簧片發出極微小而沉重的回響。', speaker='沈淮'),
                                  sound('door'),
                                  flash('#ffb6c1', strength=0.6, duration=350),
                                  say('「喀啦！」木盒彈開！\n裡面赫然放著一罐精巧的【粉紅胡椒研磨罐】，以及幾張折疊多次、染有暗紅斑漬的醫院病歷單碎頁。', speaker='沈淮'),
                                  item('pepper', '粉紅胡椒研磨罐'),
                                  sound('item'),
                                  # 播放回憶卡（安雅輕柔女孩語音）與真相卡（沈淮震驚語音）
                                  card('card_bedroom_memory'),
                                  card('card_bedroom_shock'),
                                  setv('box_unlocked', True),
                                  setv('truth_known', True),
                                  setv('phase', 'mix'),
                                  balloon('exclamation', target='player'),
                              ],
                              [
                                  say('木盒上的小銅鎖雕刻著心型藤蔓，鎖孔極其纖巧緊密。強行撬開只會損壞盒子，需要對應的那串心型小鑰匙。', speaker='沈淮'),
                                  balloon('sweat', target='player'),
                              ])
                      ])
           ]),

        # 解鎖後在梳妝台上顯現的粉紅胡椒研磨罐道具
        ev('prop_pepper_item', 0, 2, name='粉紅胡椒道具',
           free={'url': art['prop-pepper'], 'x': 8.5, 'y': 1.6, 'w': 0.8, 'h': 0.8},
           conditions=[cond('box_unlocked', True)]),

        # 返回吧檯的大門
        ev('door_bar', 3, 8, name='返回吧檯', trigger='touch',
           marker={'label': '返回吧檯', 'kind': 'exit'},
           actions=[
               sound('door'),
               jump('m-bar', arrive={'x': 13, 'y': 8, 'direction': 'left'}),
           ]),
    ]

    guidance = [
        {'text': '使用心型吊墜鑰匙打開梳妝台木盒', 'eventId': 'vanity_box', 'conditions': [cond('box_unlocked', False)]},
        {'text': '帶著粉紅胡椒與病歷單返回吧檯調酒', 'eventId': 'door_bar', 'conditions': []},
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
