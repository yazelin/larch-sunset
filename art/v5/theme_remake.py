# -*- coding: utf-8 -*-
"""主題曲重製：把作者給的原曲附給 gemini-web「創作音樂」，指定歌詞。python3 art/v5/theme_remake.py <原曲.mp3|-> <輸出編號>
原曲給 - 就不附檔，只把歌詞放在提示最前面。輸出 art/v5/music_raw/theme_<編號>.mp3，產完用 listen_song_en.py 聽寫比對。"""
import base64, json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import music_lib as M
H = os.path.dirname(os.path.abspath(__file__))
lyr = '[Verse 1]' + open(os.path.join(H, '../../canon/歌詞-英文.md'), encoding='utf-8').read().split('[Verse 1]', 1)[1].strip()
src, n = sys.argv[1], sys.argv[2]
style = 'English pop ballad, warm clear female lead vocal, piano, clean electric guitar, bass, gentle drums, bittersweet, about 76 BPM, fades out quietly at the end.'
if src == '-':
    body = {'prompt': f'Write a song with these exact lyrics. Do not write new lyrics; sing these words only, in this order.\n\nLyrics:\n{lyr}\n\nStyle: {style}'}
else:
    body = {'prompt': f'Remake the attached song. Keep its melody, female voice, tempo and arrangement, but replace the lyrics with exactly the following words, in this order, with no other words.\n\nLyrics:\n{lyr}\n\nStyle: {style}',
            'file': base64.b64encode(open(src, 'rb').read()).decode(), 'filename': 'original.mp3'}
body.update(timeout=720, vocals='vocals')
req = urllib.request.Request(M.URL, method='POST', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'x-goog-api-key': M.bashrc_key()})
d = json.load(urllib.request.urlopen(req, timeout=900, context=M.CTX))
if d.get('success'):
    out = os.path.join(H, 'music_raw', f'theme_{n}.mp3'); open(out, 'wb').write(base64.b64decode(d['audio'])); print('產好', out, d.get('worker_id'))
else:
    print('失敗', str(d.get('message') or d.get('error') or d)[:400])
