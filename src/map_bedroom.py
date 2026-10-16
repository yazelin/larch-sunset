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

        # 梳妝台調查行動點（位於梳妝凳前 x=4, y=4）
        ev('vanity_box', *PT['vanity_box'], name='雕花木盒', trigger='action',
           actions=[
               branch([cond('box_unlocked', True)],
                      [say('雕花木盒已經開啟，幾張泛黃染血的病歷單碎頁已被握在手心。空氣中依然殘留著那股微弱而刺痛的粉紅胡椒香氣。', speaker='player')],
                      [branch([cond('storage_pried', True)],
                              [
                                  say('推開臥室的門，屋裡安靜得能聽見自己逐漸紊亂的心跳聲。\n梳妝台上散落著乾枯的花瓣，中央擺著那只刻滿心型藤蔓的小胡桃木盒。交往的這三年裡，她從不曾讓我碰它。', speaker='player'),
                                  say('我將胸前那串心型鑰匙插進鎖孔旋轉……『喀啦』一聲，主鎖芯轉動了，但盒蓋內部卻傳來齒輪咬合的阻力！', speaker='player'),
                                  sound('door'),
                                  say('鎖孔下方竟緩緩滑出了一組四位數的黃銅轉盤密碼鎖！\n轉盤上方刻著安雅親手刻下的纖細小字：\n『我們相遇與停止的時刻……如果遺忘了，就永遠別打開它。』', speaker='player'),
                                  input_action(
                                      '請輸入四位數密碼（提示：便條紙抬頭與吧檯掛鐘上永遠定格的初遇時刻 02:17）：',
                                      variable='box_pass',
                                      answer='0217|217|02:17|2:17|02 17|2點17分|兩點十七分',
                                      placeholder='請輸入 4 位數密碼（例如 0217）',
                                      right=[
                                          sound('holy'),
                                          flash('#ffb6c1', strength=0.8, duration=500),
                                          balloon('heart', target='player'),
                                          say('「0217……深夜兩點十七分。那是便條紙上的時間，也是吧檯牆上時鐘永遠停下的時刻。」\n齒輪轉盤完美對齊，只聽「喀噠」一聲清響，盒蓋終於緩緩彈開！', speaker='player'),
                                          say('木盒內整齊墊著暗紅天鵝絨，中央靜靜放著一罐【粉紅胡椒研磨罐】……\n以及壓在底層、幾張染有暗紅斑漬的醫院病歷單。', speaker='player'),
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
                                      wrong=[
                                          sound('guard'),
                                          balloon('sweat', target='player'),
                                          say('密碼轉盤卡住了，數字不對。\n「初遇與停止的時刻……是便條紙抬頭與吧檯掛鐘停在的 02:17 嗎？」沈淮自言自語著，決定再試一次。', speaker='player'),
                                      ],
                                  ),
                              ],
                              [
                                  say('木盒上的小銅鎖雕刻著心型藤蔓，鎖孔極其纖巧緊密。強行撬開只會損壞盒子，需要對應的那串心型小鑰匙。', speaker='player'),
                                  balloon('sweat', target='player'),
                              ])
                      ])
           ]),



        # 返回吧檯的大門（南側雙開木門）
        ev('door_bar', *PT['door_bar'], name='返回吧檯', trigger='touch',
           actions=[
               sound('door'),
               jump('m-bar', arrive={'x': 17, 'y': 2, 'direction': 'down'}),
           ]),
    ]

    events += layout.events(D, urls)

    guidance = [
        {'text': '使用心型鑰匙與便條紙密碼 0217 打開雕花木盒', 'eventId': 'vanity_box', 'conditions': [cond('box_unlocked', False)]},
        {'text': '帶著粉紅胡椒返回吧檯調製晚霞', 'eventId': 'door_bar', 'conditions': []},
    ]

    env = {
        'weather': 'clear',
        'intensity': 0,
        'darkness': 0,
        'shake': 0,
        'lights': [
            {'id': 'sunset-window', 'x': 2, 'y': 2, 'radius': 5, 'color': '#ffccd5', 'flicker': False},
            {'id': 'vanity-lamp', 'x': 4, 'y': 2, 'radius': 3, 'color': '#ffe5d9', 'flicker': True},
        ]
    }

    m = map_dict('臥室梳妝台', W, H, ground_url, layout.walls(D), events, guidance, env)
    return map_node(MAP_ID, '臥室梳妝台', m, bgm=art.get('bgm-bar', ''))
