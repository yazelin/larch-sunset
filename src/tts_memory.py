"""全劇配音：台詞在 memory.L，聲線跟 tts11.py 一樣。已存在的檔跳過（重跑只補缺的）。
這部的「調」全部唸 tiáo（調酒、調一杯、調到…），送出前一律換成同音的「條」；橋接服務的替身表只涵蓋「調酒」「調出來」。
FORCE=1：全部重產（作者 2026-10-17：Larch 能帶情緒了，全部重生），連橋接服務的快取一起繞過（要等 larch-tts-bridge PR #8 部署）。
"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
import memory, tts11

FORCE = bool(os.environ.get('FORCE'))
lines = memory.voice_lines()


def one(item):
    fn, text, voice, emo = item
    if not FORCE and os.path.exists(os.path.join(tts11.OUT_DIR, fn)):
        return
    for k in range(3):   # 橋接服務忙或 Larch 429 時會逾時，重試就好
        try:
            return tts11.gen_tts(text.replace('調', '條'), voice, emo, fn, force=FORCE)
        except Exception as e:  # noqa: BLE001
            print('retry', fn, k + 1, repr(e)[:80], flush=True)
    print('FAIL', fn, flush=True)


# 3 線並行：橋接服務的 LARCH_LANES=3，Larch 帳號會因為並行太高被凍結，不要調高（記憶：reference_larch_account_frozen_ai_abuse）
with ThreadPoolExecutor(3) as ex:
    list(ex.map(one, lines))
print('done', len(lines))
