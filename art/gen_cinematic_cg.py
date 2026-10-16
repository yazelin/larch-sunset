"""全劇 CG 電影感重繪（design/重寫.md「CG」一節，2026-10-17）。
每張都帶在場角色的定錨；杯型全劇統一碟形香檳杯（coupe）；先產〈共赴晚霞〉當風格樣張給作者定調。
用法：python3 art/gen_cinematic_cg.py cg_ending_burn [次數]  → art/raw/cine/<名>_<n>.png
"""
import sys, pathlib, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import codex11

R = pathlib.Path(__file__).resolve().parent.parent
ANYA, SHEN, SPIRIT, BAR = (R / f'assets/art/{n}.webp' for n in ('p_anya', 'p_shen', 'p_anya_spirit', 'bg_bar_full'))

STYLE = ('Cinematic anime feature-film still, painterly, high-end Japanese animated film lighting, restrained and literary. '
         'Anamorphic lens feel, shallow depth of field, soft bokeh, subtle film grain. Only motivated light sources. '
         'Low saturation overall with one accent colour. Asymmetric composition with negative space; foreground objects partly frame the shot. '
         'Melancholic, tender, tragic. Faces must match the reference images exactly; hands with five fingers. '
         'Any cocktail glass is a COUPE (wide shallow champagne coupe on a thin stem), never a martini glass or wine glass. '
         'No text, no letters, no logos, no watermark. 16:9.')
WHO = {
    'anya': 'ANYA: young woman, dark brown hair in a loose low bun with soft side strands, gentle brown eyes, dusty-pink apron over a cream cable-knit sweater',
    'shen': 'SHEN: young man, short tousled dark brown hair, brown eyes',
    'spirit': 'ANYA as a spirit: the same woman, same apron and sweater, semi-transparent, softly glowing, edges dissolving into light',
    'bar': 'the bar interior: wooden counter with brass rail, amber bottle shelves, big window, brass pendant lamps',
}

# 每張：在場（定錨）、畫面。背後的理由與美感寫在 design/重寫.md 的 CG 表
CG = {
    'cg_ending_burn': (['shen', 'spirit', 'bar'],
        'Deep night after closing; the room is cold blue from the street light through the window. Low side angle along the counter. '
        'SHEN in his bartender uniform (white shirt, black waistcoat, black tie) sits on a bar stool on the customer side, slumped forward, '
        'cheek resting on his folded arms on the counter, eyes half closed, a faint peaceful smile, one tear. Near his hand, in sharp focus, '
        'an empty coupe glass with a thin residue of deep gold at the bottom and rose pink on top. Behind the counter, at her usual place, '
        'stands ANYA as a spirit, leaning toward him across the counter, one hand reaching to touch his hair, crying and smiling at once. '
        'Warm gold and soft pink light spreads from her and swallows the cold blue of the room, like a sunset filling the bar; dust motes glow gold. '
        'An out-of-focus wall clock above shows 2:17. SHEN lower left foreground, ANYA\'s light upper right, the glass at the centre.'),
    'cg_ending_cold': (['shen', 'bar'],
        'The coldest image of the story. Night, the bar in cold blue. Seen from behind the counter: SHEN in his bartender uniform stands with his back half to us at the steel bar sink, '
        'holding an upturned coupe glass under the running tap; golden liquid thins in the water and a few pink peppercorn flecks swirl toward the drain, '
        'the only warm colour in the frame. Behind the counter, her place is empty: an apron hangs on a hook. Wide shot, lots of empty dark space.'),
    'cg_cocktail': ([],
        'Still life. On the dark wooden counter of an empty bar at night, one coupe glass in sharp focus: deep gold settled at the bottom, rose pink floating on top, '
        'tiny pink peppercorn flecks on the surface, like the sun sinking under a sunset. It is the only warm light in a cold blue room. '
        'Behind it, out of focus, the empty place behind the counter where a bartender would stand, a brass bar spoon resting there. Low angle, close.'),
    'cg_mem1_towel': (['anya', 'shen', 'bar'],
        'Three years ago, a stormy night, almost closing. Warm amber pendant light inside, cold blue rain streaking the dark window. '
        'SHEN is a customer, NOT a bartender: soaked plain white shirt with open collar (no waistcoat, no tie), wet hair, sitting on a bar stool. '
        'ANYA leans across the counter and dries his hair with a white towel; her hand has stopped beside his ear; their faces are close, eyes meeting, silence. '
        'A coupe glass of pale gold with pink peppercorns on the rim stands between them. Close two-shot, foreground counter edge out of focus.'),
    'cg_mem2_teach': (['anya', 'shen', 'bar'],
        'Late summer, early evening before opening: the only true daylight of the story, a low orange sunset beam through the big window. '
        'Close-up on hands: behind the counter SHEN, in a casual white shirt with rolled sleeves (no waistcoat, no tie), holds a long thin brass bar spoon in a tall clear mixing glass; '
        'ANYA stands right behind him, her right hand wrapped over the back of his right hand on the spoon. Clear golden liquid spins in a smooth spiral. '
        'Their faces at the edge of the frame, turned toward each other, inches apart.'),
    'cg_mem3_shoulder': (['anya', 'shen', 'bar'],
        'Same counter, same lamp as the first meeting, but darker: after closing in the third year. One warm pendant lamp, deep blue night outside. '
        'ANYA sits on a bar stool beside SHEN (bartender uniform) on the customer side, her head on his shoulder, eyes closed, a bittersweet smile. '
        'SHEN looks down at her. On the counter a coupe glass and a small bottle of saffron syrup. Quiet, tender, a little sad.'),
    'cg_mem3b_glasses': (['anya', 'bar'],
        'Before dawn. Wide shot from the far end of the dark bar. ANYA, small in the frame, sits alone at the counter wearing a man\'s oversized white shirt (no apron), '
        'her hair down. A long row of coupe glasses lines the whole counter, each one with just one sip missing, gold and pink. '
        'A single warm lamp above her; the window behind is pale cold blue. Beautiful at first glance, unbearable once understood.'),
    'cg_mem4_rooftop': (['anya', 'shen'],
        'The only outdoor scene and the only real sunset of the story: a city rooftop in autumn, the whole sky burning from gold to pink to violet. '
        'Backlit, near-silhouette: ANYA (cream sweater, no apron) leans against SHEN (casual clothes), slow dancing in the wind; '
        'a coupe glass glowing in the backlight rests on the railing beside them. Wide, lots of sky, her hair blown by the wind.'),
}


def one(name, n):
    who, scene = CG[name]
    refs = [{'anya': ANYA, 'shen': SHEN, 'spirit': SPIRIT, 'bar': BAR}[w] for w in who]
    cast = ' '.join(f'Reference {i + 1} is {WHO[w]}.' for i, w in enumerate(who))
    prompt = f'{STYLE} {cast} Scene: {scene}'
    return codex11.gen(prompt, str(R / f'art/raw/cine/{name}_{n}.png'), refs=[str(r) for r in refs], size='1536x1024')


if __name__ == '__main__':
    name, k = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1
    with cf.ThreadPoolExecutor(k) as ex:
        for f in ex.map(lambda n: one(name, n), range(1, k + 1)):
            print(f)
