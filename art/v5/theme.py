# -*- coding: utf-8 -*-
"""片尾主題曲〈晚霞〉（人聲，gemini-web）。歌詞在 canon/歌詞.md。
  python3 art/v5/theme.py [候選數]   → art/v5/music_raw/theme_<n>.mp3；選定後 python3 art/v5/theme.py pick <n> → assets/bgm/theme.mp3（-14 LUFS）"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import music_lib as M
H = os.path.dirname(os.path.abspath(__file__)); M.RAW = os.path.join(H, 'music_raw')
lyr = open(os.path.join(H, '../../canon/歌詞.md'), encoding='utf-8').read().split('## ', 1)[1]
TAG = {'主歌一': 'Verse 1', '副歌一': 'Chorus 1', '主歌三': 'Verse 2', '副歌二': 'Chorus 2', '尾': 'Outro, almost spoken'}
lyr = '\n'.join(('[' + TAG[l[3:].strip()] + ']') if l.startswith('## ') else l for l in ('## ' + lyr).splitlines() if l.strip())
P = ('A tender Mandarin pop ballad from Taiwan, sung by a gentle, slightly husky male voice in his thirties, intimate and close like he is talking to someone who is gone. '
     'Felt piano and solo cello lead, soft string quartet joins in the chorus, light brushed drums only in the second chorus, 66 BPM, warm, bittersweet, ends quietly on piano alone. '
     'Clear Taiwanese Mandarin pronunciation, sing every section once, exactly as written and in this order (Verse 1, Chorus 1, Verse 2, Chorus 2, Outro), no repeats, no added words; keep the intro short so the whole lyric fits:\n' + lyr)
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'pick':
        src = os.path.join(M.RAW, f'theme_{sys.argv[2]}.mp3'); out = os.path.join(H, '../../assets/bgm/theme.mp3')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-b:a', '192k', out], check=True); print(out)
    else:
        bk = M.bashrc_key()
        for i in range(1, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 3):
            n = f'theme_{i}'; M.PROMPT[n] = P; M.VOCALS[n] = 'vocals'
            if not os.path.exists(os.path.join(M.RAW, n + '.mp3')): M.gen(n, bk, tries=8)
