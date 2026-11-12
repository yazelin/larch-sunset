# 晚霞

Larch 視覺小說。巷子裡一間只有七張高腳椅的小酒吧，調酒師安雅和加班到深夜的沈淮，從一個暴雨夜的第一杯〈破曉〉開始，鬥嘴、吵架、一起把店撐起來，過了三年。她走後的第七天，他回到店裡，翻開她從不讓人看的小筆記本。

**2026-11 起是重製版**：單線、純劇情卡、一個結局、全程自動播放、不配音（設計 `design/重製.md`）。舊版《晚霞是舌尖最後的刺痛》（RPG 地圖、兩個結局）的劇本與程式留在 git 歷史；`src/build_v2_maps.py`、`src/push_v2.py`、`src/map_*.py`、`src/memory.py`、`art/` 底下第五版以前的腳本是舊版的，重製版的建置不再使用。

- 公開站：`docs/index.html`（兩杯酒的做法、她的病、結局為什麼改寫、參考資料）

## 資料夾

| 路徑 | 內容 |
|---|---|
| `canon/劇本.md` | 劇本。每個 `## 代號（時空）` 是一張卡，`〔圖：名字〕` 從下一句起換那張 CG |
| `canon/歌詞.md` | 片尾主題曲〈晚霞〉歌詞 |
| `design/` | 重製設計與代決紀錄（`重製.md`）、調酒與病理考據（`研究-調酒.md`、`研究-病理.md`）、角色卡 |
| `審稿/` | 寫稿準則（`準則.md`）、逐卡閘門（`runner.py`）、整部通讀（`whole_read.py`）、全劇句型掃描（`pattern_scan.py`） |
| `src/` | `script.py` 讀劇本、`build.py` 組成 `dist/project.json`、`push.py` 推上 Larch、`credits.txt` 片尾名單、`plugin/` 片尾字卷插件 |
| `art/v5/` | 第五版素材產線：`ref/` 定錨（角色、空景、兩杯酒）、`shots.py` 分鏡與產圖、`bgm.py` 配樂、`theme.py` 主題曲 |
| `assets/` | 正式素材：`art/cg/` 鏡頭圖、`bgm/` 配樂與主題曲 |
| `tests/` | `play_auto.mjs` 免點試玩 |

## 指令

    python3 審稿/runner.py next canon/劇本.md      # 各卡審稿狀態與下一步
    python3 審稿/runner.py gate canon/劇本.md <卡>  # 改過的卡跟上一版比（讀稿人找問題、評審兩兩比較）
    python3 審稿/whole_read.py                     # 幾位讀稿人各讀一遍全劇，只找跨卡的問題
    python3 審稿/pattern_scan.py                   # 全劇句型統計（重複開頭、旁白句型、重複交代）
    python3 art/v5/shots.py list                   # 鏡頭與各自帶的定錨
    python3 art/v5/shots.py gen <鏡頭|all> [張數]   # 產候選圖到 art/v5/raw/（走全機共用的產圖排隊）
    python3 art/v5/shots.py install <鏡頭>_<n>      # 選定 → assets/art/cg/<鏡頭>.webp
    python3 art/v5/bgm.py [名字…]                  # 配樂（gemini-web，代聽驗收）
    python3 art/v5/theme.py 3                      # 主題曲候選
    python3 src/build.py                           # 產出 dist/project.json
    SPEED=16 node tests/play_auto.mjs              # 只按「開始遊戲」，要自己播到片尾再回標題
    python3 src/push.py "這次改了什麼"              # 推上 Larch（素材走 jsDelivr 孤兒 tag，要先 commit 並 git push）

`tests/` 需要本機預覽器 `~/larch-preview` 與 Playwright。產圖與配樂要連自架服務，金鑰從環境變數與本機設定檔讀，不放進 repo。

## 分工

劇本方向與角色由作者決定。文字由 AI 依作者的方向撰寫，並用審稿閘門與整部通讀把關；美術、配樂與主題曲由 AI 生成；程式由 AI 製作。這一版沒有配音。

## 授權

程式碼以 MIT 授權（`LICENSE`）。故事文字、美術、音樂與公開站內容以 CC BY-NC 4.0 授權（`LICENSE-CONTENT.md`）。

[GitHub @yazelin](https://github.com/yazelin) · [Facebook](https://facebook.com/yazelin) · [Buy Me a Coffee](https://buymeacoffee.com/yazelin)
