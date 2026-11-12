# -*- coding: utf-8 -*-
"""《晚霞》第五版配樂：七首完整曲（gemini-web，約三分鐘），不切循環，頭尾淡入淡出；代聽驗收，有人聲就重產，最多三次。
  python3 art/v5/bgm.py [名字…]   → art/v5/music_raw/<名>.mp3 → -16 LUFS → assets/bgm/<名>.mp3
music_lib.py 是 ~/larch-ember/art/music.py 的複本（產生、代聽）。哪張卡用哪一首在 src/build.py 的 TRACK_BY_PREFIX。"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import music_lib as M
H = os.path.dirname(os.path.abspath(__file__))
M.RAW, M.OUT = os.path.join(H, 'music_raw'), os.path.join(H, '../../assets/bgm')
CORE = 'felt piano and solo cello as the two lead voices, soft string quartet behind, intimate chamber sound, close warm recording'
TAIL = 'instrumental only, no vocals, no singing, no choir, no humming, a complete piece of about three minutes with a gentle intro and a soft natural ending'
T = {   # 名字：(提示詞, 給代聽的場景)
 'main': (f'Main theme of a quiet love story set in a tiny neighbourhood bar, a simple four-note rising motif on felt piano answered by a solo cello, warm sunset colours, tender and bittersweet, hopeful at the end, 66 BPM, major key with a minor turn, {CORE}',
          '片頭與尾聲：巷子裡的小酒吧重新開門，溫暖、苦中帶甜、日子繼續過下去'),
 'dawn': (f'A rainy spring night, two strangers meeting across a bar counter, shy warmth, light rain-like piano arpeggios, a slow cello line that smiles, gentle upright bass, 72 BPM, starts hesitant and becomes warm, {CORE}',
          '第一年春天暴雨夜：上班族躲雨走進小酒吧，調酒師遞毛巾，兩人第一次見面，害羞而溫暖'),
 'days': (f'Everyday happiness of a couple running a small bar together, playful and light, pizzicato strings and a bouncy felt piano, soft brushed snare, a little jazz waltz feel, regulars teasing them, warm amber light, 104 BPM, major key, {CORE}',
          '兩個人一起顧店過日子：鬥嘴、熟客起鬨、教調酒、搬來同住，輕快、溫暖、有笑聲'),
 'alone': (f'Very sparse and restrained, single piano notes with long silences and one low sustained cello tone, a woman deciding alone to hide her illness, a closed door after an argument, quiet, cold daylight, 52 BPM, minor, {CORE}',
           '診間、兩人大吵後、差點被拆穿：她一個人扛著祕密，極簡、克制、安靜'),
 'sunset': (f'Rooftop at dusk, the only real sunset in the story, a slow waltz in 3/4 for two people swaying without music, wide open sky, cello melody soaring gently over rolling piano, golden and aching, 60 BPM, major key with longing, {CORE}',
            '第三年秋天頂樓看晚霞：兩人沒有音樂慢慢晃著跳舞，金色、遼闊、很美也很捨不得'),
 'winter': (f'The last winter months, ordinary evenings that are running out, slow tender piano chords like breathing, a fragile cello line, moments of small laughter inside sadness, 56 BPM, warm but fading, {CORE}',
            '最後幾個月：她病重仍坐在吧檯邊陪他開店，溫柔、平靜、時間快沒了'),
 'seventh': (f'The seventh night after her death, an empty bar lit by one lamp, rain on the window, cold and hollow, a few isolated felt piano notes over a faint low drone, cello only as distant long tones, numb grief, almost no melody, 48 BPM, minor, {CORE}',
             '頭七深夜：他一個人回到空店，只開一盞燈，冷、空、麻木的悲傷'),
}


def finish(name):
    src = os.path.join(M.RAW, f'{name}.mp3'); out = os.path.join(M.OUT, f'{name}.mp3')
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af',
                    f'loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:d=2,afade=t=out:st={dur - 5:.2f}:d=5', '-b:a', '160k', out], check=True)
    return dur


def main(names):
    bk, ak = M.bashrc_key(), M.audit_key()
    os.makedirs(M.OUT, exist_ok=True)
    for n in names:
        M.PROMPT[n] = f'{T[n][0]}, {TAIL}'
        for k in range(3):
            if not M.gen(n, bk):
                continue
            a = M.listen(os.path.join(M.RAW, f'{n}.mp3'), T[n][1], ak) or {}
            if a.get('has_vocals'):
                print(f'{n} 第{k + 1}次有人聲，重產', flush=True); continue
            d = finish(n)
            print(f"{n} 完成 {d:.0f} 秒 適配 {a.get('fits_scene')} {a.get('mood')} {a}", flush=True); break
        else:
            print(f'{n} 三次都沒過', flush=True)


if __name__ == '__main__':
    main(sys.argv[1:] or list(T))
