"""香料儲藏間地圖（m-storage）：精緻日系厚塗手繪動漫風格，純分層遮擋與無雜訊沉浸介面。
依據原作原畫完整還原：
北牆百葉窗夕陽光斑、木製天平工作台＋暗格、兩側高聳香料藥草架、中央古石磚地面與地毯。
"""
import os, pathlib
from mapkit import *
import layout

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = layout.load('storage')
MAP_ID = D['map']['id']
W, H = D['map']['w'], D['map']['h']
PT = {k: tuple(v) for k, v in D['points'].items()}


def build_storage(art):
    real = not os.environ.get('BLOCKS') and (ROOT / 'assets/maps/storage_ground.webp').exists() and \
        all((ROOT / f"assets/objects/storage/{o['name']}.webp").exists() for o in layout.objects(D))
    kind = 'objects' if real else 'blocks'
    ground_url = f'/files/assets/maps/storage_{"ground" if real else "blocks"}.webp'
    urls = {o['name']: f"/files/assets/{kind}/storage/{o['name']}.webp" for o in layout.objects(D)}

    events = [
        # 主角 沈淮入場點（從南門進入 x=8, y=9）
        ev('hero', *PT['hero_start'], actor='player', direction='up', sprite=walker(art['walk-shen']), actorId='shen'),

        # 工作台抽屜（北側 x=8, y=4）：靠後巷那面牆返潮，抽屜咬死；要用黃銅匙照她教過的角度撬 → 回憶三
        ev('window_grate', *PT['window_grate'], name='工作台的抽屜', trigger='action',
           actions=[
               branch([cond('storage_pried', True)],
                      [say('抽屜已經空了。', speaker='player')],
                      [branch([cond('spoon_taken', True)],
                              [
                                  say('儲藏間靠後巷那面牆一直在返潮，空氣裡是八角、風乾橙皮和迷迭香的味道。\n窗縫透進一點路燈。', speaker='player'),
                                  say('糖漿平常放的那一格是空的。\n工作台的抽屜咬死了。她說過，這個抽屜有一個角度，只有她開得了。', speaker='player'),
                                  choice_action(
                                      '匙要插進哪裡？',
                                      [
                                          ('右邊滑軌的縫', [
                                              sound('slash'),
                                              say('匙的扁柄滑進右邊的縫，抵住了卡榫。', speaker='player'),
                                          ]),
                                          ('正中間的把手下面', [
                                              sound('hit'),
                                              say('正中間是一整塊實木，紋絲不動。我把匙移到右邊滑軌的縫。', speaker='player'),
                                              sound('slash'),
                                          ]),
                                      ],
                                      speaker='player',
                                  ),
                                  choice_action(
                                      '怎麼用力？',
                                      [
                                          ('手腕放輕，貼著慢慢轉', [
                                              sound('hit'),
                                              flash('#ffd700', strength=0.4),
                                              say('「不要用力。」跟她教我轉匙的時候一樣。\n卡榫鬆了一格，抽屜彈出半寸。', speaker='player'),
                                          ]),
                                          ('整個人壓下去', [
                                              sound('guard'),
                                              say('匙發出一聲細響。我收了力，手腕放輕，貼著慢慢轉。', speaker='player'),
                                              sound('hit'),
                                              flash('#ffd700', strength=0.4),
                                          ]),
                                      ],
                                      speaker='player',
                                  ),
                                  sound('door'),
                                  say('抽屜裡墊著一塊舊毛巾。毛巾上放著一小瓶番紅花糖漿，是她熬的最後一瓶。', speaker='player'),
                                  item('saffron', '番紅花糖漿'),
                                  sound('item'),
                                  wait(300),
                                  say('糖漿旁邊是一條細鍊子，掛著一把心型的小鑰匙。\n她總是貼身戴著，洗澡也不拿下來。那天早上，她的脖子上是空的。', speaker='player'),
                                  item('key', '心型吊墜鑰匙'),
                                  sound('item'),
                                  setv('storage_pried', True),
                                  setv('phase', 'bedroom'),
                                  jump('card_mem3_enter'),
                              ],
                              [
                                  say('工作台的抽屜咬死了，徒手拉不開。要有一樣扁而硬的東西。', speaker='player'),
                                  balloon('sweat', target='player'),
                              ])
                      ])
           ]),

        ev('look_numbers', 3, 5, name='牆上的字', trigger='action', marker={'label': '牆上的字', 'kind': 'talk'},
           actions=[say('架子旁的牆上，用鉛筆寫滿了進貨的數字。番紅花那一欄，最後幾個月都是同一個數字。\n她一直在熬糖漿。我以為是生意好。', speaker='player')]),

        # 返回吧檯的大門（南側雙開木門）
        ev('door_bar', *PT['door_bar'], name='返回吧檯', trigger='touch',
           actions=[
               sound('door'),
               jump('m-bar', arrive={'x': 3, 'y': 2, 'direction': 'down'}),
           ]),
    ]

    events += layout.events(D, urls)

    guidance = [
        {'text': '工作台的抽屜', 'eventId': 'window_grate', 'conditions': [cond('storage_pried', False)]},
        {'text': '回吧檯', 'eventId': 'door_bar', 'conditions': [cond('storage_pried', True)]},
    ]

    # 頭七的現在：冷藍、窗縫透進路燈
    env = {
        'weather': 'clear', 'intensity': 0, 'darkness': 0.5, 'shake': 0,
        'lights': [
            {'id': 'street-crack', 'x': 8, 'y': 3, 'radius': 4, 'color': '#7d95c4', 'flicker': False},
            {'id': 'door-glow', 'x': 8, 'y': 10, 'radius': 2.5, 'color': '#6f86b8', 'flicker': False},
        ],
        'ambience': {'tint': '#3c5c9c', 'tintStrength': 0.38, 'vignette': 0.4, 'particles': 'motes', 'density': 0.1},
    }

    m = map_dict('香料儲藏間', W, H, ground_url, layout.walls(D), events, guidance, env)
    return map_node(MAP_ID, '香料儲藏間', m, bgm=art.get('bgm-bar', ''))
