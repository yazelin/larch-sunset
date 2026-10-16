# 《晚霞是舌尖最後的刺痛》Larch RPG 版

> 「最黑的時候，喝一杯天亮。」

安雅走後第七天，頭七的深夜，沈淮第一次回到兩人一起顧的那間酒吧。吧檯上留著一只空杯和一張只交代店務的便條。他照著燒到一半的配方一樣一樣找回材料，每找到一樣，就回到一段跟活著的她在一起的時候：暴雨夜的初遇、教他調酒的那把黃銅匙、她每一杯都問的「甜嗎」、頂樓唯一一次一起看的晚霞。最後他站到她的位置，調出她留給自己的那一杯〈晚霞〉。

設計文件：`design/重寫.md`（2026-10-17 定稿，含時間線、人物心境、CG 與配樂的理由）。

---

## 遊戲架構

- **平台**：[Larch Story Studio](https://larch.ink)，`larch-rpg-system` 地圖行走與事件。
- **頭七的現在**（冷藍色調，沈淮第一人稱）：
  1. `m-bar` 頭七的吧檯：空杯與便條、燒到一半的風味筆記、黃銅匙、她的工作位、她的圍裙／酒櫃標籤／馬克杯（可選看）
  2. `m-storage` 香料儲藏間：返潮咬死的抽屜（番紅花糖漿、心型鑰匙）、牆上的進貨數字（可選看）
  3. `m-bedroom` 我們的房間：木盒（病歷與有毒的粉紅胡椒）、她那一側的床、護手霜（可選看）
- **回憶**（暖金色調，第三人稱），穿插在解謎中：回憶一〈破曉〉、回憶二〈黃銅匙〉、回憶三〈甜嗎〉（含凌晨一整排杯子）、回憶四〈晚霞〉頂樓。
- **兩個結局**：〈共赴晚霞〉、〈冷卻的餘溫〉。介面不標「真結局」「好結局」。
- **素材**：8 張劇情 CG（`art/gen_cinematic_cg.py`，.11 codex-image）、8 首配樂（`art/music.py`，gemini-web，切 58.5 秒循環）、全劇配音（`src/tts_memory.py`，larch-tts-bridge；沈淮 Gentle_Youth、安雅 Soft_Girl）。台詞全在 `src/memory.py`。

---

## 開發與建置

```bash
python3 src/build.py                 # 組出 dist/project.json
python3 src/tts_memory.py            # 補缺的配音（FORCE=1 全部強制重配）
node tests/play_full.mjs             # 全劇自動試玩〈共赴晚霞〉；END=cold 走〈冷卻的餘溫〉
python3 ~/larch-preview/serve.py dist/project.json   # 本機預覽，畫面上可留回饋（dist/feedback/）
```

推上 Larch（只更新專案，不上架）：

1. 素材有改：commit、推 main、打新 tag，把 `src/push.py` 的 `CDN_TAG` 換成那個 tag 的 commit 編號（新 tag jsDelivr 要等刷新，commit 編號馬上能用）。
2. `DRY=1 python3 src/push.py x`：素材換成 jsDelivr 並逐一確認打得開，只產 `dist/project-larch.json`。
3. 最後一個改動之後重跑兩個結局的試玩，全過才推。
4. `python3 src/push.py "這次改了什麼"`：先存線上快照到 `snapshots/`，整包 PUT。推之前關掉 Larch 編輯器分頁。
5. 讀回核對卡片數，再用 `LIVE=<Larch 預覽網址> node tests/play_full.mjs` 在 Larch 本站跑兩個結局。

---

## 授權與社群

- 程式碼：MIT © 林亞澤
- [GitHub @yazelin](https://github.com/yazelin) · [Facebook](https://facebook.com/yazelin) · [Buy Me a Coffee](https://buymeacoffee.com/yazelin)
