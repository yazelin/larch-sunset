"""回憶篇三張 CG(design/回憶篇.md)。定錨:安雅立繪、沈淮立繪、吧檯背景。產出在 art/raw/mem/,選定後裁 16:9 轉 webp 進 assets/art/。"""
import sys, pathlib, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import codex11

R = pathlib.Path(__file__).resolve().parent.parent
A, S, BAR = R / 'assets/art/p_anya.webp', R / 'assets/art/p_shen.webp', R / 'assets/art/bg_bar_full.webp'
STYLE = ('Soft anime illustration, painterly cel shading, warm amber bar lighting, same art style as the reference images. '
         'Reference 1 is ANYA: young woman, dark brown hair in a loose low bun with soft side strands, gentle brown eyes. '
         'Reference 2 is SHEN: young man, short tousled dark brown hair, white shirt, black waistcoat, black tie, bartender. '
         'Reference 3 is the bar interior (wooden counter, amber-lit bottle shelves, big window). '
         'Keep both faces exactly like the references. No text, no letters, no signs, no clock. Cinematic 16:9 composition, '
         'characters fill the frame. Exactly one ANYA and one SHEN, two hands each.')
CG = {
    'cg_mem1_rain': 'Rainy night, almost closing time. ANYA sits on a bar stool at the counter, completely soaked by the storm: wet hair with droplets, '
                    'a dry white towel draped over her shoulders, wearing a damp cream cable-knit sweater (NO apron). She holds a coupe glass with both hands; '
                    'the cocktail is golden with tiny pink peppercorn flecks floating on top. She has just taken a sip and is laughing, eyes slightly teary from the spice. '
                    'SHEN stands behind the counter facing her, smiling softly. Rain streaks on the dark window behind, warm lamps inside.',
    'cg_mem2_spoon': 'Early evening before opening, orange sunset light pouring through the big window. Behind the counter, ANYA wears her dusty-pink apron over the cream sweater '
                     'and holds a long brass bar spoon in a mixing glass; SHEN stands just behind her right shoulder and gently places his hand over hers on the spoon, guiding it. '
                     'A smooth golden swirl spins inside the glass. Both are blushing; ANYA looks down at their hands, SHEN looks at her. Close, intimate framing on hands and faces.',
    'cg_mem2_spoon_v2': 'Close two-shot behind the counter at early evening, orange sunset light from the big window. ANYA wears her dusty-pink apron over the cream sweater '
                        'and holds a long thin brass bar spoon in her RIGHT hand; SHEN stands right behind her and his RIGHT hand is wrapped over the back of her right hand, '
                        'so both hands hold the same spoon together. Her LEFT hand steadies a tall clear mixing glass with NO ice; inside, clear golden liquid spins in a smooth spiral. '
                        'Both are blushing; ANYA looks down at their joined hands, SHEN looks at her. The joined hands on the spoon are the focus of the picture.',
    'cg_mem3_shoulder': 'Late night after closing, the bar is empty and dim, one warm pendant lamp, deep blue night outside the window. ANYA (dusty-pink apron over cream sweater) '
                        'sits on a bar stool beside SHEN in front of the counter, resting her head on his shoulder, eyes half closed with a faint bittersweet smile. '
                        'SHEN looks down at her tenderly. A half-finished golden cocktail and a small bottle of syrup sit on the counter in front of them. Quiet, tender, a little sad.',
}

def one(k):
    return codex11.gen(STYLE + ' Scene: ' + CG[k], str(R / f'art/raw/mem/{k}.png'), refs=[str(A), str(S), str(BAR)], size='1536x1024')

if __name__ == '__main__':
    keys = sys.argv[1:] or list(CG)
    with cf.ThreadPoolExecutor(3) as ex:
        for k, f in zip(keys, ex.map(one, keys)): print(k, f)
