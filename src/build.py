"""組出 dist/project.json：骨架＋RPG地圖＋劇情卡＋配音演出。"""
import json, pathlib, shutil
import cards, variables, art, mapkit
import map_bar, map_storage, map_bedroom, memory

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT_ID = 'project-8cb1ab7e-891c-46b4-bd38-df29060e5717'


def load_skeleton():
    return json.loads((ROOT / 'skeleton/project.json').read_text(encoding='utf-8'))


def rpg_database(a):
    def actor(id, name, walk, portrait, role='party'):
        return {
            'id': id,
            'name': name,
            'title': '',
            'profile': '',
            'role': role,
            'walk': mapkit.walker(a[walk]),
            'portrait': a[portrait],
            'join': 'stay' if id == 'shen' else 'later',
            'kit': 'none',
            'rig': '',
            'joinVariable': ''
        }
    return {
        'version': 1,
        'heroId': 'shen',
        'leadSwitch': False,
        'actors': [
            actor('shen', '沈淮', 'walk-shen', 'p-shen'),
            actor('anya', '安雅', 'walk-anya', 'p-anya'),
            actor('anya-spirit', '安雅（靈魂）', 'walk-anya-spirit', 'p-anya-spirit')
        ]
    }


def build():
    p = load_skeleton()
    p['boards'][0]['description'] = '頭七的吧檯、香料儲藏間、我們的房間，四段穿插的回憶，兩個結局。'   # 市集的章節說明從這裡抄（2026-10-18）
    # 角色資料照 design/重寫.md 定稿（2026-10-17 作者要修：舊背景寫「研發三年毒劑」、聲線誤設成沈淮的、立繪在 R2）
    anya = p['characters'][0]
    anya.update({
        'role': '女主角，調酒師，酒吧的主人',
        'backstory': '三年前的暴雨夜，替淋濕的沈淮調了一杯〈破曉〉。四個月後確診味覺中樞進行性壞死，沒有告訴任何人，開始教他調酒。'
                     '想為兩人調一杯〈晚霞〉，還沒調成，舌頭先不行了。',
        'secrets': '確診後瞞了沈淮快三年；說是偏頭痛的藥，其實是神經止痛藥。',
        'personality': '溫暖、愛笑、在吧檯後面說了算，會主動伸手，什麼都自己扛。',
        'speakingStyle': '短句，笑著管人；說到自己的事就停住，改問「甜嗎？」。',
        'voiceName': 'Chinese (Mandarin)_Soft_Girl',
        'portraitUrl': '/files/assets/art/p_anya.webp',
        'expressions': [
            {'id': 'expression-6ea37c5d-3e7d-4999-b045-d34380b7d823', 'kind': 'expression', 'name': '微笑', 'emotion': 'smile', 'imageUrl': '/files/assets/art/p_anya.webp'},
            {'id': 'expression-56bd4e18-9e8d-4e0d-83fd-909c4388ffbc', 'kind': 'expression', 'name': '頭七', 'emotion': 'spirit', 'imageUrl': '/files/assets/art/p_anya_spirit.webp'},
        ],
    })
    if not any(c.get('name') == '沈淮' for c in p['characters']):
        p['characters'].append({
            'id': 'character-3f6c2a9e-8b41-4d27-9c5e-1a7d4b2e6f80', 'name': '沈淮', 'slug': '沈淮',
            'role': '男主角，安雅教出來的調酒師',
            'backstory': '三年前淋著暴雨走進她的酒吧，之後每天坐到兩點十七分才走。她教他調酒，第二年起兩人一起顧店。',
            'secrets': '', 'personality': '安靜、怕苦，話不多，記得她說過的每一句。',
            'speakingStyle': '低聲、慢，第一人稱回想時很克制。',
            'voiceName': 'Chinese (Mandarin)_Gentle_Youth', 'voiceProvider': 'minimax',
            'portraitUrl': '/files/assets/art/p_shen.webp', 'expressions': [],
        })
    board = p['boards'][0]
    board['nodes'], board['edges'] = [], []
    p['nodes'], p['edges'] = board['nodes'], board['edges']
    p['variables'] = variables.project_variables()

    a = art.paths()
    v = art.VOICES

    # RPG 系統插件設定
    p['settings'].setdefault('plugins', {})
    p['settings']['plugins']['larch-rpg-system'] = {
        'enabled': True,
        'settings': {
            'database': json.dumps(rpg_database(a), ensure_ascii=False)
        }
    }

    # 封面與 CG 收藏庫
    p['settings']['titleCoverImage'] = a['cover']
    p['settings']['projectThumbnail'] = a['cover']
    p['settings'].setdefault('titleScreen', {})['bgm'] = a['bgm-bar']
    p['settings']['cgGallerySource'] = 'picked'
    p['settings']['cgGalleryItems'] = [
        {'url': a['cover'], 'title': '晚霞是舌尖最後的刺痛'},
        {'url': a['cg-mem1'], 'title': '破曉'},
        {'url': a['cg-mem2'], 'title': '只借你'},
        {'url': a['cg-mem3'], 'title': '甜嗎'},
        {'url': a['cg-mem3b'], 'title': '還差一點'},
        {'url': a['cg-mem4'], 'title': '有風就好'},
        {'url': a['cg-cocktail'], 'title': '晚霞'},
        {'url': a['cg-ending-burn'], 'title': '共赴晚霞'},
        {'url': a['cg-ending-cold'], 'title': '冷卻的餘溫'},
        {'url': a['bg-bar'], 'title': '頭七的吧檯'},
        {'url': a['bg-storage'], 'title': '香料儲藏間'},
        {'url': a['bg-bedroom'], 'title': '我們的房間'}
    ]

    # UI 主題風格搭配：暗夜暖橙酒吧風
    p['settings']['menuUi'] = {
        'preset': 'night',
        'accent': '#ff7b39',
        'title': '晚霞是舌尖最後的刺痛',
        'eyebrow': '調酒師的記憶收納',
        'buttons': ['bag', 'save', 'load', 'title']
    }
    p['settings']['battleUi'] = {
        'preset': 'night',
        'panel': '#1e1b18',
        'accent': '#ff7b39'
    }

    N = board['nodes'].append
    L = lambda x, y: cards.link(board, x, y)

    # 2. 地圖卡：深夜吧檯、香料儲藏間、臥室梳妝台
    N(map_bar.build_bar(a))
    N(map_storage.build_storage(a))
    N(map_bedroom.build_bedroom(a))


    # 3. 劇情卡片：序幕、便條、回憶、病歷、遺言、抉擇與兩個結局都在 memory.py（design/重寫.md）
    memory.build(board, a)
    # 兩個結局的最後一張停在畫面上，不要自己跳走（2026-10-19 作者在《雨幕》提醒的「無下一張時停留在此卡片」）
    ends = [n for n in board['nodes'] if n['id'] in ('ending_burn_4', 'ending_cold_3')]
    assert len(ends) == 2, [n['id'] for n in ends]
    for n in ends:
        n['data']['stayOnCard'] = True
    print('地圖內心話轉成配音卡：', memory.voice_map_lines(board))


    (ROOT / 'dist').mkdir(exist_ok=True)
    out_file = ROOT / 'dist/project.json'
    out_file.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding='utf-8')

    # 同步 assets 目錄至 dist/assets 供本機 serve.py /files/assets/... 直供
    dst = ROOT / 'dist/assets'
    shutil.rmtree(dst, ignore_errors=True)
    if (ROOT / 'assets').exists():
        shutil.copytree(ROOT / 'assets', dst)

    nodes_count = len(board['nodes'])
    edges_count = len(board['edges'])
    print(f'Build finished! Output: {out_file} ({nodes_count} nodes, {edges_count} edges)')
    return p


if __name__ == '__main__':
    build()
