import subprocess, pathlib, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent.parent
GEN = pathlib.Path.home() / '.claude/skills/codex-imagegen/codex-imagegen.sh'
CUTOUT = pathlib.Path.home() / 'cutout-skill/cutout.py'
RAW = ROOT / 'art/raw'
RAW.mkdir(parents=True, exist_ok=True)

PROPS = {
    'prop_spoon': "A single vintage brass bar spoon with a twisted spiral handle and a flat teardrop muddler tip, gleaming warm golden brass. Viewed from 45-degree top-down angle as an RPG game item. On a perfectly flat solid pure magenta #FF00FF background. No shadow, no ground, crisp clean edges. No text.",
    'prop_saffron': "A small ornate vintage apothecary glass bottle filled with radiant golden saffron syrup, cork stopper, golden amber glow. 45-degree top-down RPG game item. On a perfectly flat solid pure magenta #FF00FF background. No shadow, no ground, crisp clean edges. No text.",
    'prop_key': "An antique brass heart-pendant key with intricate vine filigree and a delicate heart-shaped bow. 45-degree top-down RPG game item. On a perfectly flat solid pure magenta #FF00FF background. No shadow, no ground, crisp clean edges. No text.",
    'prop_pepper': "A small vintage wooden and glass pink peppercorn spice grinder mill, showing rosy pink peppercorns inside. 45-degree top-down RPG game item. On a perfectly flat solid pure magenta #FF00FF background. No shadow, no ground, crisp clean edges. No text.",
}

def gen_one(k, prompt):
    raw_path = RAW / f'{k}_raw.png'
    out_path = RAW / f'{k}.png'
    if not raw_path.exists():
        print(f'Generating {k}...')
        cmd = ['bash', str(GEN), prompt, str(raw_path)]
        subprocess.run(cmd, check=True)
    if not out_path.exists():
        print(f'Keying out {k}...')
        cmd2 = ['python3', str(CUTOUT), 'key', str(raw_path), '-o', str(out_path)]
        subprocess.run(cmd2, check=True)
    return str(out_path)

def main():
    with cf.ThreadPoolExecutor(max_workers=3) as pool:
        futs = {pool.submit(gen_one, k, p): k for k, p in PROPS.items()}
        for fut in cf.as_completed(futs):
            k = futs[fut]
            try:
                res = fut.result()
                print(f'Finished {k}: {res}')
            except Exception as e:
                print(f'Error on {k}: {e}')

if __name__ == '__main__':
    main()
