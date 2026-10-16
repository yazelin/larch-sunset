"""臥室梳妝台地圖（m-bedroom）：精緻日系厚塗手繪動漫風格，純分層遮擋與無雜訊沉浸介面。
依據原作原畫完整還原：
左側蕾絲窗簾窗台、古典雕花橢圓鏡梳妝台＋化妝凳＋心型木盒、右側溫馨碎花被褥床、雙門衣櫃與扶手椅。
"""
import os, pathlib
from mapkit import *
import layout

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = layout.load('bedroom')
MAP_ID = D['map']['id']
W, H = D['map']['w'], D['map']['h']
PT = {k: tuple(v) for k, v in D['points'].items()}


def build_bedroom(art):
    real = not os.environ.get('BLOCKS') and (ROOT / 'assets/maps/bedroom_ground.webp').exists() and \
        all((ROOT / f"assets/objects/bedroom/{o['name']}.webp").exists() for o in layout.objects(D))
    kind = 'objects' if real else 'blocks'
    ground_url = f'/files/assets/maps/bedroom_{"ground" if real else "blocks"}.webp'
    urls = {o['name']: f"/files/assets/{kind}/bedroom/{o['name']}.webp" for o in layout.objects(D)}

    events = [
        # 主角 沈淮入場點（從南門進入 x=8, y=9）
        ev('hero', *PT['hero_start'], actor='player', direction='up', sprite=walker(art['walk-shen']), actorId='shen'),

        # ── 梳妝台上擺放的精巧胡桃木雕花木盒（符合梳妝台比例）──
        ev('obj_box_prop', 0, 5, name='梳妝台木盒視覺',
           free={'url': art['obj-wood-box'], 'x': 4.1, 'y': 3.0, 'w': 0.45, 'h': 0.38}),

        # 梳妝台的木盒（x=4, y=4）：鑰匙＋她最後一晚重設的轉盤 → 病歷與有毒的胡椒 → 回憶四
        ev('vanity_box', *PT['vanity_box'], name='她的木盒', trigger='action',
           actions=[
               branch([cond('box_unlocked', True)],
                      [say('木盒開著。絨布上只剩病歷，研磨罐在我口袋裡。', speaker='player')],
                      [branch([cond('storage_pried', True)],
                              [
                                  say('臥室裡還是她的味道。\n梳妝台中間擺著那只刻滿藤蔓的胡桃木盒。三年來，她從不讓我碰它。', speaker='player'),
                                  say('心型鑰匙轉開了鎖，盒蓋卻還是打不開。鎖孔下面是一組四位數的轉盤。', speaker='player'),
                                  say('轉盤上纏著一張新的紙條，是她的字：\n『如果你已經往前走了，就不要打開它。』', speaker='player'),
                                  input_action(
                                      '四個數字。',
                                      variable='box_pass',
                                      answer='0217|217|02:17|2:17|02 17|2點17分|兩點十七分',
                                      placeholder='四位數',
                                      right=[
                                          sound('holy'),
                                          flash('#ffb6c1', strength=0.5, duration=500),
                                          say('0217。\n我沒有往前走。', speaker='player'),
                                          item('pepper', '粉紅胡椒研磨罐'),
                                          sound('item'),
                                          card('card_box_truth'),
                                          setv('box_unlocked', True),
                                          setv('truth_known', True),
                                          setv('phase', 'bed'),
                                          jump('card_mem4_enter'),
                                      ],
                                      wrong=[
                                          sound('guard'),
                                          say('轉盤沒有動。她會用的數字，只有一個。', speaker='player'),
                                      ],
                                  ),
                              ],
                              [
                                  say('木盒鎖著。鎖孔很小，是心型的。', speaker='player'),
                              ])
                      ])
           ]),

        # 她那一側的床（床尾 x=10, y=7）：她最後一句「睡吧」→ 回吧檯調酒
        ev('bed', 10, 7, name='她那一側的床', trigger='action', conditions=[cond('phase', 'bed')],
           actions=[card('card_bed'), setv('phase', 'mix')]),

        ev('look_cream', 6, 4, name='護手霜', trigger='action', marker={'label': '護手霜', 'kind': 'talk'},
           actions=[say('梳妝台上有一條護手霜，擠到只剩扁扁的一片。\n她每天開店前都要擦，說調酒的手不能乾。我替她買過一條新的，還沒拆。', speaker='player')]),

        # 返回吧檯的大門（南側雙開木門）
        ev('door_bar', *PT['door_bar'], name='返回吧檯', trigger='touch',
           actions=[
               sound('door'),
               jump('m-bar', arrive={'x': 17, 'y': 2, 'direction': 'down'}),
           ]),
    ]

    events += layout.events(D, urls)

    guidance = [
        {'text': '她的木盒', 'eventId': 'vanity_box', 'conditions': [cond('box_unlocked', False)]},
        {'text': '她那一側的床', 'eventId': 'bed', 'conditions': [cond('phase', 'bed')]},
        {'text': '下樓，回吧檯', 'eventId': 'door_bar', 'conditions': [cond('phase', 'mix')]},
    ]

    # 頭七的現在：冷藍，只留梳妝台一盞小燈
    env = {
        'weather': 'clear', 'intensity': 0, 'darkness': 0.5, 'shake': 0,
        'lights': [
            {'id': 'window-street', 'x': 2, 'y': 2, 'radius': 5, 'color': '#7d95c4', 'flicker': False},
            {'id': 'vanity-lamp', 'x': 4, 'y': 2, 'radius': 2, 'color': '#ffcf9e', 'flicker': True},
        ],
        'ambience': {'tint': '#3c5c9c', 'tintStrength': 0.38, 'vignette': 0.4, 'particles': 'motes', 'density': 0.1},
    }

    m = map_dict('我們的房間', W, H, ground_url, layout.walls(D), events, guidance, env)
    return map_node(MAP_ID, '我們的房間', m, bgm=art.get('bgm-bar', ''))
