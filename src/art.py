"""美術資源與網址定義：真 RPG 45度俯視地圖與切圖物件。"""

ART = {
    # 45 度高角度俯視純地面底圖
    'ground-bar': '/files/assets/maps/bar_ground.webp',
    'ground-storage': '/files/assets/maps/storage_ground.webp',
    'ground-bedroom': '/files/assets/maps/bedroom_ground.webp',

    # 對話卡背景相容別名
    'bg-bar': '/files/assets/maps/bar_ground.webp',
    'bg-storage': '/files/assets/maps/storage_ground.webp',
    'bg-bedroom': '/files/assets/maps/bedroom_ground.webp',

    # 45 度獨立切圖物件（透明去背 PNG / WEBP）
    'obj-bar-counter': '/files/assets/objects/obj_bar_counter.webp',
    'obj-wood-box': '/files/assets/objects/obj_wood_box.webp',

    # 45 度實體道具
    'prop-spoon': '/files/assets/props/prop_spoon.webp',
    # 匙下方補透明到 y+h-1=6.05（圖的長寬比要跟 w:h 一樣，改 h 要重產圖），排序在吧檯（圖框下緣第 6 列）之後畫，才不會被吧檯蓋住
    'prop-spoon-tall': '/files/assets/props/prop_spoon_tall.webp',
    'prop-saffron': '/files/assets/props/prop_saffron.webp',
    'prop-key': '/files/assets/props/prop_key.webp',
    'prop-pepper': '/files/assets/props/prop_pepper.webp',

    # 原作 CG 與封面（故事劇情卡使用，全部一律為 webp 格式）
    'cover': '/files/assets/art/cover.webp',
    # 配樂：gemini-web 重配、切 58.5 秒循環（art/music.py，作者 2026-10-17）
    'bgm-bar': '/files/assets/bgm/theme.mp3',
    'bgm-storm': '/files/assets/bgm/storm.mp3',
    'bgm-spoon': '/files/assets/bgm/spoon.mp3',
    'bgm-almost': '/files/assets/bgm/almost.mp3',
    'bgm-rooftop': '/files/assets/bgm/rooftop.mp3',
    'bgm-confession': '/files/assets/bgm/letter.mp3',
    'bgm-together': '/files/assets/bgm/together.mp3',
    'bgm-cold': '/files/assets/bgm/cold.mp3',
    'bg-black': '/files/assets/art/bg_black.webp',   # 進回憶的過場：全黑，不讓前一張地圖透出來
    'cg-cocktail': '/files/assets/art/cg_cocktail.webp',
    'cg-ending-burn': '/files/assets/art/cg_ending_burn.webp',
    'cg-ending-cold': '/files/assets/art/cg_ending_cold.webp',
    # 回憶篇（design/回憶篇.md）
    'cg-mem1': '/files/assets/art/cg_mem1_towel.webp',
    'cg-mem2': '/files/assets/art/cg_mem2_teach.webp',
    'cg-mem3': '/files/assets/art/cg_mem3_shoulder.webp',
    'cg-mem3b': '/files/assets/art/cg_mem3b_glasses.webp',
    'cg-mem4': '/files/assets/art/cg_mem4_rooftop.webp',

    # 角色行走圖 (Walker Sprites, 3x4, 48x64)
    'walk-shen': '/files/assets/art/walk/walk-shen.webp',
    'walk-anya': '/files/assets/art/walk/walk-anya.webp',
    # 回憶一、二：還不是調酒師的沈淮（便服）
    'walk-shen-casual': '/files/assets/art/walk/walk-shen-casual.webp',
    'walk-anya-spirit': '/files/assets/art/walk/walk-anya-spirit.webp',

    # 角色立繪 (Portraits)
    'p-shen': '/files/assets/art/p_shen.webp',
    'p-anya': '/files/assets/art/p_anya.webp',
    'p-anya-spirit': '/files/assets/art/p_anya_spirit.webp',

    # 配樂 (BGM)
}

VOICES = {
    'shen-start': '/files/assets/voice/shen_start.mp3',
    'anya-note': '/files/assets/voice/anya_note.mp3',
    'anya-memory': '/files/assets/voice/anya_memory.mp3',
    'anya-confession': '/files/assets/voice/anya_confession.mp3',
    'shen-burn-1': '/files/assets/voice/shen_burn_1.mp3',
    'shen-burn-2': '/files/assets/voice/shen_burn_2.mp3',
    'shen-burn-3': '/files/assets/voice/shen_burn_3.mp3',
    'shen-cold-1': '/files/assets/voice/shen_cold_1.mp3',
    'shen-cold-2': '/files/assets/voice/shen_cold_2.mp3',
}


def paths():
    return dict(ART)
