#!/bin/bash
# 定錨候選：每個兩張。角色帶安雅立繪當畫風參考；夜景酒吧等白天那張出來才能產（另跑）。
cd ~/larch-sunset/art/v5
A=../../assets/art/p_anya.webp
for n in 1 2; do
  for k in azhong xiaokui mother; do GEN_SIZE=1024x1536 python3 gen.py anchors/${k}_$n.png prompts/$k.txt $A & done
  for k in set_bar set_room set_roof set_front prop_drinks; do python3 gen.py anchors/${k}_$n.png prompts/$k.txt & done
done
wait; ls -la anchors
