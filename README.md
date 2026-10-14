# 《晚霞是舌尖最後的刺痛》Larch RPG 版

> 「如果你還記得我們初遇的滋味，就替我把它完成吧。」

患有無法逆轉味覺中樞神經病變的調酒師安雅，歷時三年研發出外觀宛如晚霞般美麗、實為神經止痛毒劑的調酒配方。沈淮在深夜的吧檯醒來，循著安雅留下的便條與暗格機關，探索深夜吧檯、香料儲藏間與臥室梳妝台，解開初遇滋味與終點真相的 RPG 互動視覺小說。

---

## 遊戲架構

- **平台**：[Larch Story Studio](https://larch.ink)
- **RPG 系統**：`larch-rpg-system` 地圖行走、探索檢驗、道具系統與多房間切換
- **地圖**：
  1. `m-bar` 深夜吧檯（調酒工作台、調酒匙、便條紙、安雅靈魂虛影）
  2. `m-storage` 香料儲藏間（百葉窗暗格、番紅花糖漿、心型吊墜鑰匙）
  3. `m-bedroom` 臥室梳妝台（心型藤蔓雕花木盒、粉紅胡椒研磨罐、病歷單真相）
- **結局分支**：
  - **結局 A（真結局）**：共赴的辣度（端起酒杯，一口飲盡，在夕陽與痛覺中陪伴她）
  - **結局 B（壞結局）**：冷卻的餘溫（遵從遺願倒進水槽，餘生再嚐不出任何溫度）

---

## 開發與建置

```bash
# 組出專案 JSON
python3 src/build.py

# 推送到 Larch 平台
python3 src/push.py "更新說明"

# 本機即時預覽
python3 ~/larch-preview/serve.py dist/project.json
```

---

## 授權與社群

- 程式碼：MIT © 林亞澤
- [GitHub @yazelin](https://github.com/yazelin) · [Facebook](https://facebook.com/yazelin) · [Buy Me a Coffee](https://buymeacoffee.com/yazelin)
