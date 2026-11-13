# -*- coding: utf-8 -*-
"""片尾主題曲〈Saffron in My Glass〉（英文人聲，gemini-web）。歌詞在 canon/歌詞-英文.md。
  python3 art/v5/theme.py [候選數]   → art/v5/music_raw/theme_<n>.mp3；選定後 python3 art/v5/theme.py pick <n> → assets/bgm/theme.mp3（-14 LUFS）"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import music_lib as M
H = os.path.dirname(os.path.abspath(__file__)); M.RAW = os.path.join(H, 'music_raw')
# gemini-web「創作音樂」會照主題自己寫詞，指定歌詞不會照唱（2026-11-13 試四首都另編一套）。所以只給故事內容，產完用 listen_song_en.py 聽寫，逐句對劇本。
# 曲風照作者 2026-11-13 給的舊版同名曲（女聲、鋼琴、電吉他、鼓、貝斯，約兩分半）。提示只寫要有的內容。
P = ('A bittersweet English pop ballad titled "Saffron in My Glass", sung by a warm, clear female voice. Soft piano opens, clean electric guitar and bass join, gentle drums from the first chorus, about 76 BPM, fades out quietly. '
     'The song tells this story, in simple words: a tiny bar with seven stools on a rainy alley. The woman behind the counter was slowly losing her sense of taste, so with every drink she asked him "is it sweet?" and he tasted it for her. '
     'She wrote everything in a little notebook in her own hand. She is gone now after a long illness. He opens her notebook and builds her cocktail, the Sunset, layer by layer: hibiscus red at the bottom, saffron gold in the middle, pink on top. '
     'It stings his tongue for a moment, and then it is sweet. He answers her: "it is still sweet". She used to tell him "remember to eat", so he eats, keeps the bar open, and at dusk he goes up to the roof to look at the evening sky. '
     'Tender, grateful, he keeps living. The chorus contains the line "there is saffron in my glass".')
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'pick':
        src = os.path.join(M.RAW, f'theme_{sys.argv[2]}.mp3'); out = os.path.join(H, '../../assets/bgm/theme.mp3')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-b:a', '192k', out], check=True); print(out)
    else:
        bk = M.bashrc_key()
        for i in range(1, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 3):
            n = f'theme_{i}'; M.PROMPT[n] = P; M.VOCALS[n] = 'vocals'
            if not os.path.exists(os.path.join(M.RAW, n + '.mp3')): M.gen(n, bk, tries=8)
