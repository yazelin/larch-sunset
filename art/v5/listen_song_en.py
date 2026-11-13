# -*- coding: utf-8 -*-
"""請 Gemini 聽寫一首歌，對照 canon/歌詞.md 人工比：python3 art/v5/listen_song.py music_raw/theme_1.mp3"""
import sys, base64, json, subprocess, tempfile, urllib.request, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import music_lib as M
tmp = tempfile.mktemp(suffix='.mp3'); subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', sys.argv[1], '-ac', '1', '-b:a', '64k', tmp], check=True)
b = base64.b64encode(open(tmp, 'rb').read()).decode(); os.remove(tmp)
ask = '這是一首英文歌。請逐句聽寫歌詞（英文原文，每句一行，每句前面標開始的秒數，聽不清楚的字用□），最後另起一行寫：歌手性別、樂器、整體情緒、咬字是否清楚、有沒有唱到一半中斷或結尾突然切掉。只輸出這些。'
body = {'contents': [{'parts': [{'text': ask}, {'inline_data': {'mime_type': 'audio/mp3', 'data': b}}]}], 'generationConfig': {'temperature': 0}}
for m in M.AUD_MODELS * 2:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'x-goog-api-key': M.audit_key()}), timeout=240))
        print(m); print(r['candidates'][0]['content']['parts'][0]['text']); break
    except Exception as e: print(m, repr(e)[:100])
