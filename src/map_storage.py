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

        # 窗台暗格（北側天平工作台正下方 x=8, y=4）
        ev('window_grate', *PT['window_grate'], name='百葉窗工作台暗格', trigger='action',
           actions=[
               branch([cond('storage_pried', True)],
                      [say('百葉窗工作台下的暗格已被撬開，裡面原本隱藏的番紅花糖漿與心型鑰匙已被取出。', speaker='player')],
                      [branch([cond('spoon_taken', True)],
                              [
                                  say('儲藏間陰涼而乾燥，空氣中混合著陳年八角、風乾橙皮與迷迭香的微苦草本香氣。\n夕陽的餘光透過百葉窗的細縫斜斜割進來，在浮塵中照亮了天平工作台縫隙深處那抹深邃的琥珀金光。', speaker='player'),
                                  say('我取出那柄黃銅調酒匙。老工作台抽屜常年受潮，木榫緊緊咬死，必須像精密的調酒師一樣找到正確的著力點與角度。', speaker='player'),
                                  # 步驟一：尋找支點
                                  choice_action(
                                      '【木榫暗格撬動 · 著力支點】面對咬死的老胡桃木抽屜，調酒匙的扁平柄端應插向何處？',
                                      [
                                          ('【插進右側滑軌暗卡榫（傳來微弱金屬彈簧聲）】', [
                                              sound('slash'),
                                              say('調酒匙末端順利滑入右側縫隙，頂端準確抵住了卡榫簧片！', speaker='player'),
                                          ]),
                                          ('【直接插入正中央把手下方硬撬】', [
                                              sound('hit'),
                                              say('正中間是整塊厚實實心木，紋絲不動。沈淮改將匙端移向右側微有鬆動的滑軌縫隙。', speaker='player'),
                                              sound('slash'),
                                          ]),
                                      ],
                                      speaker='player',
                                  ),
                                  # 步驟二：力道與槓桿
                                  choice_action(
                                      '【木榫暗格撬動 · 槓桿角度】匙端已卡入卡榫，此時該如何施力？',
                                      [
                                          ('【手腕沉穩下壓，以 45 度角向上順時針輕挑】', [
                                              sound('hit'),
                                              flash('#ffd700', strength=0.5),
                                              say('「喀！」手腕巧勁一發，內部木卡齒鬆脫了一格，抽屜微微彈出半寸！', speaker='player'),
                                          ]),
                                          ('【用全身重量垂直向下硬壓】', [
                                              sound('guard'),
                                              say('調酒匙發出危險的金屬哀鳴！沈淮立刻收力，改以手腕巧勁順時針向上輕挑。', speaker='player'),
                                              sound('hit'),
                                              flash('#ffd700', strength=0.5),
                                          ]),
                                      ],
                                      speaker='player',
                                  ),
                                  # 步驟三：釋放彈舌
                                  choice_action(
                                      '【木榫暗格撬動 · 釋放底舌】抽屜露出了半寸縫隙，底層的黃銅鎖舌若隱若現！',
                                      [
                                          ('【以匙柄尖端精準下壓鎖舌彈片，順勢向外勾拉】', [
                                              sound('door'),
                                              flash('#ffd700', strength=0.7, duration=400),
                                              say('『喀噠！』伴隨著一聲清脆明快的木榫彈響，整層暗格平滑地彈了出來！', speaker='player'),
                                          ]),
                                      ],
                                      speaker='player',
                                  ),
                                  say('暗格天鵝絨襯墊中央，端端正正擺著一瓶封存完好的【番紅花糖漿】。那濃郁純淨的金黃色澤，宛如凝固的黎明。', speaker='player'),
                                  item('saffron', '番紅花糖漿'),
                                  sound('item'),
                                  wait(300),
                                  say('等等……糖漿後方還躺著一串金屬鑰匙！\n那是一串雕刻著纖細藤蔓的【心型吊墜鑰匙】……安雅平時總戴在胸口，貼著肌膚，從不離身。', speaker='player'),
                                  say('握在手心裡，冰冷的金屬彷彿還帶著某種令人心悸的餘溫。這把鑰匙，一定能打開她在臥室裡鎖著的所有秘密。', speaker='player'),
                                  item('key', '心型吊墜鑰匙'),
                                  sound('item'),
                                  balloon('idea', target='player'),
                                  setv('storage_pried', True),
                                  setv('phase', 'bedroom'),
                              ],
                              [
                                  say('工作台抽屜木榫咬合得死緊，徒手根本扒不開。必須找到細長而質地堅硬的金屬工具才能撬開這處暗格。', speaker='player'),
                                  balloon('sweat', target='player'),
                              ])
                      ])
           ]),



        # 返回吧檯的大門（南側雙開木門）
        ev('door_bar', *PT['door_bar'], name='返回吧檯', trigger='touch',
           actions=[
               sound('door'),
               jump('m-bar', arrive={'x': 3, 'y': 2, 'direction': 'down'}),
           ]),
    ]

    events += layout.events(D, urls)

    guidance = [
        {'text': '第一步：使用黃銅調酒匙撬開百葉窗暗格取得番紅花', 'eventId': 'window_grate', 'conditions': [cond('storage_pried', False)]},
        {'text': '帶著番紅花與心型鑰匙返回吧檯', 'eventId': 'door_bar', 'conditions': []},
    ]

    env = {
        'weather': 'clear',
        'intensity': 0,
        'darkness': 0,
        'shake': 0,
        'lights': [
            {'id': 'window-sun', 'x': 8, 'y': 3, 'radius': 5, 'color': '#ffb347', 'flicker': False},
            {'id': 'door-glow', 'x': 8, 'y': 10, 'radius': 3, 'color': '#ffa07a', 'flicker': False},
        ]
    }

    m = map_dict('香料儲藏間', W, H, ground_url, layout.walls(D), events, guidance, env)
    return map_node(MAP_ID, '香料儲藏間', m, bgm=art.get('bgm-bar', ''))
