"""把幾張候選拼成一張總覽：python3 art/v5/sheet.py <輸出.jpg> <raw 檔名（不含副檔名）>…（兩欄，每張 900 寬）"""
import sys, os
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); out, names = sys.argv[1], sys.argv[2:]
W = 900; ims = [(n, Image.open(os.path.join(H, 'raw', n + '.png')).convert('RGB')) for n in names]
th = [(n, i.resize((W, int(i.height * W / i.width)))) for n, i in ims]; h = max(t.height for _, t in th)
S = Image.new('RGB', (2 * W, ((len(th) + 1) // 2) * h)); d = ImageDraw.Draw(S)
for k, (n, t) in enumerate(th):
    S.paste(t, ((k % 2) * W, (k // 2) * h)); d.rectangle(((k % 2) * W, (k // 2) * h, (k % 2) * W + 9 * len(n) + 8, (k // 2) * h + 16), fill='black'); d.text(((k % 2) * W + 4, (k // 2) * h + 2), n, fill='yellow')
S.save(os.path.join(H, out), quality=86)
