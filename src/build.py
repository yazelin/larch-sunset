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
