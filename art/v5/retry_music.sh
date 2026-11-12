#!/bin/bash
# Gemini 音樂額度用完時：每 30 分鐘試一次，〈頭七〉與主題曲都有了就結束（最多試 10 次）
cd ~/larch-sunset
for i in $(seq 10); do
  [ -f assets/bgm/seventh.mp3 ] || python3 art/v5/bgm.py seventh >> art/v5/bgm2.log 2>&1
  ls art/v5/music_raw/theme_[0-9].mp3 >/dev/null 2>&1 || python3 art/v5/theme.py 2 >> art/v5/theme.log 2>&1
  [ -f assets/bgm/seventh.mp3 ] && ls art/v5/music_raw/theme_[0-9].mp3 >/dev/null 2>&1 && { echo "都有了（第 $i 次）"; exit 0; }
  sleep 1800
done
echo "試了 10 次還沒齊"; ls assets/bgm art/v5/music_raw
