"""畫面上的時間標示（作者 11-13：穿插回憶時，玩家要在畫面上看得出現在是什麼時候、是不是回憶）。
- label(圖, 模式, 主, 副)：在 CG 左上角壓一條標示，輸出到 assets/art/lab/。
- title(模式, 主, 副)：換時間時的整頁字卡。
模式：'回憶'（暖金）、'現在'（冷藍白）、''（不標模式）。同樣的輸入產出同樣的檔名，build 每次重產。"""
import hashlib, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = pathlib.Path(__file__).resolve().parent.parent
OUT = R / 'assets/art/lab'
TTC = '/usr/share/fonts/opentype/noto/NotoSerifCJK-{}.ttc'
INK = {'回憶': (241, 217, 166), '現在': (198, 214, 236), '': (244, 236, 220)}
BAR = [(179, 36, 63), (219, 165, 63), (234, 169, 182)]   # 由下往上：洛神紅、番紅花金、粉紅


def font(size, weight='Medium'):
    return ImageFont.truetype(TTC.format(weight), size, index=3)   # index 3 = TC


def _bar(d, x, y, w, h):
    seg = h / 3
    for i, c in enumerate(BAR):
        d.rectangle((x, y + h - (i + 1) * seg, x + w, y + h - i * seg), fill=c)


def _name(*parts):
    return hashlib.md5('|'.join(parts).encode()).hexdigest()[:10]


def label(src, mode, main, sub):
    """回傳 assets 底下的相對路徑（art/lab/…）。"""
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f'{pathlib.Path(src).stem}-{_name(mode, main, sub)}.webp'
    im = Image.open(src).convert('RGB'); W, H = im.size; s = W / 1600
    f_mode, f_main, f_sub = font(int(26 * s), 'SemiBold'), font(int(40 * s), 'SemiBold'), font(int(26 * s))
    d0 = ImageDraw.Draw(im)
    w_mode = d0.textlength(mode, font=f_mode) + 18 * s if mode else 0
    w_main, w_sub = d0.textlength(main, font=f_main), d0.textlength(sub, font=f_sub)
    pad, x0, y0 = 20 * s, 36 * s, 34 * s
    bw, bh = pad + 8 * s + 16 * s + w_mode + w_main + (22 * s + w_sub if sub else 0) + pad, 76 * s
    box = (int(x0), int(y0), int(x0 + bw), int(y0 + bh))
    blur = im.crop(box).filter(ImageFilter.GaussianBlur(10 * s)); im.paste(blur, box)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rounded_rectangle(box, radius=int(6 * s), fill=(14, 10, 20, 170))
    _bar(d, x0 + pad, y0 + 12 * s, 8 * s, bh - 24 * s)
    x = x0 + pad + 8 * s + 16 * s; ink = INK[mode]
    if mode:
        d.text((x, y0 + bh / 2), mode, font=f_mode, fill=ink + (255,), anchor='lm'); x += w_mode
    d.text((x, y0 + bh / 2), main, font=f_main, fill=(246, 239, 226, 255), anchor='lm'); x += w_main + 22 * s
    if sub:
        d.text((x, y0 + bh / 2), sub, font=f_sub, fill=(214, 204, 190, 255), anchor='lm')
    Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB').save(out, quality=86)
    return f'art/lab/{out.name}'


def title(mode, main, sub):
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f'title-{_name(mode, main, sub)}.webp'
    W, H = 1600, 900
    top, bot = ((38, 24, 20), (16, 10, 12)) if mode == '回憶' else ((16, 22, 38), (8, 9, 16)) if mode == '現在' else ((30, 20, 34), (12, 9, 16))
    im = Image.new('RGB', (W, H)); px = im.load()
    for y in range(H):
        t = y / (H - 1); c = tuple(round(a + (b - a) * t) for a, b in zip(top, bot))
        for x in range(W): px[x, y] = c
    d = ImageDraw.Draw(im); f_mode, f_main, f_sub = font(34, 'SemiBold'), font(96, 'SemiBold'), font(40)
    cx, cy = W // 2, H // 2 - 40
    w_main = d.textlength(main, font=f_main)
    _bar(d, cx - w_main / 2 - 44, cy - 60, 12, 120)
    if mode:
        d.text((cx, cy - 110), mode, font=f_mode, fill=INK[mode], anchor='mm')
    d.text((cx, cy), main, font=f_main, fill=(246, 239, 226), anchor='mm')
    if sub:
        d.text((cx, cy + 100), sub, font=f_sub, fill=(200, 190, 176), anchor='mm')
    im.save(out, quality=88)
    return f'art/lab/{out.name}'


if __name__ == '__main__':
    print(label(R / 'assets/art/cg/rain_towel.webp', '回憶', '第一年春天', '暴雨夜'), title('回憶', '第一年春天', '暴雨夜'), title('現在', '頭七', '深夜'))
