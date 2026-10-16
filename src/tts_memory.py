"""回憶篇配音：台詞在 memory.L，聲線跟 tts11.py 一樣。已存在的檔跳過（重跑只補缺的）。"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import memory, tts11

for fn, text, voice, emo in memory.voice_lines():
    if os.path.exists(os.path.join(tts11.OUT_DIR, fn)):
        continue
    tts11.gen_tts(text, voice, emo, fn)
print('done', len(memory.voice_lines()))
