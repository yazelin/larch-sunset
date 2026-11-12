# -*- coding: utf-8 -*-
"""《晚霞》第五版分鏡 CG。每個鏡頭：在場（角色鍵，帶定錨）、場景（帶空景定錨）、要不要帶兩杯酒的道具定錨、畫面。
  python3 art/v5/shots.py list                 列出鏡頭與參考
  python3 art/v5/shots.py gen <鏡頭|all> [張數]   → art/v5/raw/<鏡頭>_<n>.png（走共用排隊）
  python3 art/v5/shots.py install <鏡頭>_<n> …    選定 → assets/art/cg/<鏡頭>.webp（長邊 1600）
在場的每個角色都要有定錨（art/v5/ref/）；沒有人的鏡頭在場寫 []。"""
import os, subprocess, sys, re
H = os.path.dirname(os.path.abspath(__file__))
STYLE = ('Cinematic still from a hand-drawn animated feature film, painterly anime style, restrained and literary. '
         'Anamorphic lens feel, shallow depth of field, soft bokeh, subtle film grain. Only motivated light sources. '
         'Low saturation overall with one accent colour. Asymmetric composition with negative space; a foreground object partly frames the shot. '
         'Characters are Taiwanese adults with natural proportions. Each character\'s FACE and HAIR must match their reference image exactly; '
         'take CLOTHES from the text below, not from the reference. Hands have five fingers and really hold what they hold. '
         'Any cocktail is served in a tall slim champagne FLUTE on a thin stem, never a coupe, martini or wine glass. '
         'No text, no letters, no captions, no logos, no watermark. 16:9.')
FACE = {'anya': 'ANYA: woman around thirty, dark brown hair in a loose low bun with soft strands around her face, gentle brown eyes',
        'shen': 'SHEN: man around thirty, short tousled dark brown hair, brown eyes, lean',
        'azhong': 'AH-ZHONG: stocky man in his mid fifties, short grey crew cut, tanned, stubble, faded navy short-sleeved work shirt',
        'xiaokui': 'XIAO-KUI: petite woman in her mid twenties, chin-length light-brown bob with wispy bangs, mustard-yellow knit cardigan over a white blouse',
        'mother': "ANYA'S MOTHER: slim woman of about sixty, short permed black hair greying at the temples, dusty-blue floral blouse under a beige cardigan"}
WEAR = {'anya': 'dusty-pink bib apron over a cream cable-knit sweater, sleeves pushed up',
        'anya_summer': 'dusty-pink bib apron over a cream short-sleeved linen blouse',
        'anya_home': 'at home, no apron: a loose cream T-shirt and soft trousers, hair in a messy bun',
        'anya_off': 'day off, no apron: a light cream cardigan over a dusty-pink long dress',
        'anya_clinic': 'no apron: a cream blouse and a light beige jacket, a shoulder bag',
        'anya_ill': 'no apron; visibly thinner and paler, hair tied loosely low, a thick cream cardigan over a dusty-pink top',
        'shen_office': 'office worker: white dress shirt, dark narrow tie, dark suit trousers; no waistcoat',
        'shen_shirt': 'white shirt with open collar, sleeves rolled to the elbow, dark trousers; no tie, no waistcoat',
        'shen_apron': 'white shirt with open collar and rolled sleeves under a charcoal-grey bib apron; no tie, no waistcoat',
        'shen_jacket': 'dark casual jacket over a white shirt; no tie, no waistcoat',
        'shen_home': 'at home: a plain grey T-shirt and loose trousers',
        'shen_black': 'black shirt and black trousers, tired eyes',
        'shen_seventh': 'white shirt with open collar, sleeves rolled unevenly, dark trousers, no apron, no tie, no waistcoat; exhausted, faint stubble, shadows under his eyes'}
SET = {'bar': 'the bar from the reference image (tiny narrow neighbourhood bar: straight dark-wood counter, seven round leather stools, amber back-bar shelves, three brass pendant lamps, glass-paned door and alley window at one end, staircase doorway at the other)',
       'bar_night': 'the same bar at deep night, closed, as in the reference image: back-bar lights off, only ONE pendant lamp lit over the counter, the rest in cold blue street light, rain on the window',
       'room': 'the upstairs bedroom from the reference image (double bed with wooden headboard, bedside table with lamp, wardrobe, window with thin curtains, door to the stair landing)',
       'kitchen': 'the upstairs kitchen and dining corner from the reference image (old white fridge, small counter with stove, small square dining table)',
       'roof': 'the rooftop from the reference image (waist-high concrete parapet, steel water tower, potted plants, stairwell door) under a real sunset sky, red near the horizon, gold above, pink clouds',
       'front': 'the bar entrance seen from the alley as in the reference image (wooden door with glass pane, window, blank lightbox, wet asphalt, street lamp)'}
DRINK = {'dawn': 'The cocktail is the LEFT glass of the drinks reference: a slim flute, deep ruby-red syrup in the bottom third, pale gold sparkling wine above, a little crushed pink peppercorn on one side of the rim.',
         'sunset': 'The cocktail is the MIDDLE glass of the drinks reference: a slim flute with three layers, deep ruby red at the bottom, saffron gold in the middle, pale rose-pink sparkling on top, a little crushed pink peppercorn on one side of the rim.',
         'spoon': 'The bar spoon is the long thin GOLD Japanese bar spoon with a twisted stem from the drinks reference.'}
WARM = 'Warm amber and gold light, a memory of good days.'
COLD = 'Cold blue room, one pool of warm lamp light; the seventh night after her death; still and hollow.'
# 鏡頭：(在場 [角色鍵], 場景鍵或 None, [道具鍵], 畫面)
S = {
 'open_busy': (['anya_summer', 'shen_apron', 'azhong', 'xiaokui'], 'bar', [], 'A summer Friday night, the bar full and loud: all seven stools taken (other regulars are soft-focus backs and shoulders). Behind the narrow counter ANYA and SHEN work squeezed side by side: she is mid-laugh, nudging him with her elbow, a bottle in her right hand; he carries a few empty glasses. AH-ZHONG sits on the stool nearest the door with a beer bottle and an empty glass; XIAO-KUI sits mid-counter photographing her drink with her smartphone: she holds the phone upright between herself and the glass, the lit SCREEN faces her (and us, we see the drink shown on the screen), and the BACK of the phone with its camera lenses points away from her toward the glass. ' + WARM),
 'open_laugh': (['anya_summer', 'shen_apron', 'azhong', 'xiaokui'], 'bar', ['dawn'], 'Behind the counter ANYA, laughing, slides a flute along the counter top toward SHEN, who stands next to her behind the counter wiping his hands, his hand stopping beside the stem. Across the counter XIAO-KUI and AH-ZHONG watch them, grinning. The pendant lamps light all four faces. Medium shot from the customer side.  SPATIAL RULE: ANYA stands on the floor BEHIND the counter (the bartender side). The solid counter is between her and the customer side; her body is visible only from the waist up, rising above the counter top, and her hips and legs are completely hidden behind the counter front. No part of her body passes through or sinks into the counter top; she may rest her forearms or elbows ON the counter top. ' + WARM),
 'return_closed': (['shen_seventh'], 'bar_night', [], 'SHEN stands alone on the customer side of the counter under the single lit lamp, his palm resting on a plain white unsealed envelope with the outline of a key inside. All seven stools are empty. Wide shot, he is small in the frame. ' + COLD),
 'return_water': (['shen_seventh'], 'bar_night', [], 'SHEN sits on a stool at the counter under the single lamp, one hand around half a glass of plain water, a closed palm-sized notebook lying by his other hand. The six other stools are empty in blue light. Rain on the window. Medium side shot. ' + COLD),
 'rain_towel': (['anya', 'shen_office'], 'bar', [], 'A stormy spring night, almost closing time. SHEN, a first-time customer soaked by the rain, sits on a stool, shirt wet, collar open; his wet dark tie lies coiled on the counter. ANYA, standing behind the counter, leans forward over it from the waist and reaches across to dry the ends of his hair with a white towel; his own hand has stopped half raised near his forehead; their faces are close. He has not ordered yet: there is NO cocktail, flute or drink on the counter, only his tie. Heavy rain lit cold blue behind the glass door.  SPATIAL RULE: ANYA stands on the floor BEHIND the counter (the bartender side). The solid counter is between her and the customer side; her body is visible only from the waist up, rising above the counter top, and her hips and legs are completely hidden behind the counter front. No part of her body passes through or sinks into the counter top; she may rest her forearms or elbows ON the counter top. ' + WARM),
 'rain_dawn': (['anya', 'shen_office'], 'bar', ['dawn', 'spoon'], 'Close on the counter. ANYA slowly pours pale sparkling wine down the back of the gold bar spoon into the flute, which already holds ruby syrup at the bottom; the pale gold layer is forming on top. SHEN (damp hair, collar open, no tie) sits opposite with both hands on the counter edge, watching the glass. Bubbles catch the lamp light. ' + WARM),
 'rain_umbrella': (['anya', 'shen_office'], 'bar', [], 'Just inside the glass-paned door of the bar. ANYA presses a folded dark umbrella into the hand of SHEN (collar open, no tie); their fingertips touch on the handle and they look at each other. Warm light from the bar on them; through the glass, rain in cold blue street light. Two-shot from the waist up.'),
 'weeks_regular': (['anya', 'shen_office', 'azhong'], 'bar', [], 'A late spring night. SHEN sits at the counter in front of ANYA, loosening his tie with one hand. AH-ZHONG sits on the stool by the door holding a beer bottle, grinning sideways at him. Behind the counter ANYA looks down as she pours a glass of water, hiding a small smile. ' + WARM),
 'weeks_water': (['anya', 'shen_office'], 'bar', [], 'After closing in early summer: the back-bar shelf lights are off, the pendant lamps still on. ANYA and SHEN (no tie, collar open) sit side by side on two stools on the customer side, knees touching; her foot rests on the rung of his stool. Two glasses of plain water on the counter in the lamp light. Quiet, close. ' + WARM),
 'clinic_day': (['anya_clinic', 'mother'], None, [], 'A hospital consultation room on a July afternoon. Daylight through window blinds falls in stripes. ANYA sits in front of the desk, calm, both hands in her lap; her MOTHER sits beside her, leaning forward with her knees pressed together. A doctor in a white coat, seen from behind and out of focus, points at a monitor whose screen is a blur. Cool neutral colours; the only warmth is the light on ANYA\'s hands.'),
 'lesson_hands': (['anya_summer', 'shen_shirt', 'xiaokui'], 'bar', ['dawn', 'spoon'], 'A Saturday afternoon before opening, daylight from the alley window. Behind the counter SHEN and ANYA stand side by side facing the counter. SHEN holds a green sparkling-wine bottle in his RIGHT hand, gripping it around the middle of the bottle body, tilted with its open neck pointing DOWN toward the flute, and a thin stream of wine runs from the bottle mouth onto the bowl of the gold bar spoon, which he holds in his LEFT hand just above the liquid inside the flute. ANYA stands close at his right side: her right hand rests on top of his right hand on the bottle, guiding the tilt, and her left hand lightly holds his left wrist. Exactly four hands in total, each with five fingers, each clearly attached to its owner; the bottle is held in the air above the counter, not lying on it. In the flute the pale gold layer is settling over the ruby bottom. XIAO-KUI sits opposite with her chin on her hand, amused. The window light falls on the three pairs of hands.'),
 'confess_words': (['anya_summer', 'shen_shirt'], 'bar', [], 'After closing, only two pendant lamps on. SHEN stands at the sink behind the counter holding a half-dried glass with the cloth stuffed inside it, flustered, ears red, mid-sentence. ANYA stands beside him, also behind the counter, bent forward with laughter with one elbow on the counter top, the back of her other hand against her mouth.  SPATIAL RULE: ANYA stands on the floor BEHIND the counter (the bartender side). The solid counter is between her and the customer side; her body is visible only from the waist up, rising above the counter top, and her hips and legs are completely hidden behind the counter front. No part of her body passes through or sinks into the counter top; she may rest her forearms or elbows ON the counter top. ' + WARM),
 'confess_kiss': (['anya_summer', 'shen_shirt'], 'bar', [], 'After closing, beside the counter. ANYA rises on tiptoe and kisses SHEN; the fingers of one of her hands are laced through his, his other hand rests on the side of her waist. Both in profile, lit by one warm pendant lamp; the door is shut, deep blue night beyond the glass. Tender, quiet.'),
 'together_hands': (['anya', 'shen_shirt', 'azhong', 'xiaokui'], 'bar', [], 'An autumn weekend night, the bar full. Camera behind the counter at waist height: in the foreground, below the counter top and hidden from the customers, ANYA\'s hand and SHEN\'s hand are clasped. They stand shoulder to shoulder, glancing sideways at each other, trying not to smile. Beyond the counter, out of focus, XIAO-KUI leans forward grinning and AH-ZHONG raises his beer bottle. ' + WARM),
 'quit_proposal': (['anya', 'shen_shirt'], 'bar', [], 'After closing in spring, one pendant lamp. SHEN leans back against the sink holding a glass cloth, serious, looking at her. ANYA stands at the glass rack with a glass in one hand, her other hand stopped in mid-air, not looking at him. The lamp lights the rim of her glass. Space between them; the warmth has gone tense.'),
 'quit_door': (['anya', 'shen_shirt'], 'bar', [], 'The same night. SHEN stands on the customer side near the door, half turned to leave, jaw tight, one shirt cuff buttoned and the other hanging loose. ANYA stands behind the counter at the glass rack holding a glass, eyes down. The whole counter lies between them under one lamp. Wide shot, long shadows.'),
 'quit_apron': (['anya', 'shen_shirt'], 'bar', [], 'The next afternoon before opening, soft window light. SHEN stands at the sink with his sleeves rolled, washing glasses. ANYA stands just behind him holding out a charcoal-grey apron, about to drop it over his shoulder, a small apologetic smile. A paper bag and two open boxes of pan-fried dumplings steam on the counter beside them.'),
 'home_fridge': (['anya_home', 'shen_home'], 'kitchen', [], 'Late morning. SHEN stands at the open refrigerator holding a carton of eggs with nowhere to put it: the shelves are crowded with opened liquor bottles. ANYA ducks under his arm and reaches in to pull two bottles out, laughing. White fridge light on their hands, daylight on the kitchen counter. Playful, domestic.'),
 'home_mother': (['anya_home', 'shen_shirt', 'mother'], 'kitchen', [], 'A summer evening at the small dining table under the pendant lamp. MOTHER and ANYA sit facing each other; ANYA has just lifted her eyes to give her mother a quick warning look. SHEN stands at the side of the table dividing a steamed fish into their bowls with chopsticks. Three dishes, a soup, three rice bowls. The window is turning dark blue.'),
 'dusk_recipe': (['anya_summer', 'shen_apron'], 'bar', ['sunset', 'spoon'], 'After closing in late summer. Behind the counter ANYA steadies the gold bar spoon and floats pale rose sparkling wine onto the gold layer in the flute: three layers, ruby, gold, pink. SHEN stands beside her holding a steel jigger, watching closely. An opened bottle of golden dessert wine stands by. ' + WARM),
 'dusk_midnight': (['anya_summer', 'shen_apron'], 'bar', ['sunset'], 'Two in the morning, back-bar dark, one warm pendant lamp. ANYA sits beside SHEN on the customer side, her forehead resting on his shoulder, a pen still in her hand over a small open notebook. Two three-layer flutes and two covered paper bowls of wonton soup stand on the counter. Tired, happy.'),
 'almost_return': (['anya', 'shen_jacket'], 'bar', [], 'After closing in autumn. SHEN stands on the customer side in his jacket, one hand pressed on the counter beside a small hospital appointment slip (blank, no readable text), looking at her. ANYA stands at the sink, a glass of water in her right hand, her left hand stopped half raised toward her ear. The lamp lights the slip of paper between them.'),
 'almost_answer': (['anya', 'shen_jacket'], 'bar', [], 'The same night. Over SHEN\'s shoulder (he is in his jacket, seen from behind, slightly out of focus) we see ANYA across the counter, facing him with a steady, reassuring small smile, her hand around a glass of water. The appointment slip lies on the counter between them. The lamp lights her face; street light from the door rims his shoulder.'),
 'roof_dawn': (['anya_off', 'shen_shirt'], 'roof', ['dawn', 'spoon'], 'A day-off evening in autumn. By the inner side of the parapet SHEN layers a drink on a small folding table, pouring along the gold bar spoon; ANYA leans against him and steadies the flute with her fingers. The low western sun lights their hands and the ruby bottom of the glass. Wind in her hair.'),
 'roof_dance': (['anya_off', 'shen_shirt'], 'roof', ['dawn'], 'ANYA rests her cheek on SHEN\'s chest; he holds one of her hands and wraps his other arm around her back; they sway on the spot with no music. The sky turns from gold to pink; a half-finished flute stands on the ledge inside the parapet; wind lifts the hem of his shirt. Wide shot, most of the frame is sky.'),
 'winter_tell': (['anya_ill', 'shen_home'], 'room', [], 'A winter night, only the bedside lamp on. ANYA sits on the edge of the bed; SHEN stands in front of her; both of them still have a hand on the same glass of water between them. The lamp lights her knees and his hands; cold white light from the stair landing shows through the open door. He has just heard something he cannot take in.'),
 'winter_door': (['anya_ill', 'shen_home'], 'room', [], 'The same night. SHEN stands in the bedroom doorway with his back to her, one hand on the door handle. ANYA sits on the edge of the bed, head down, both hands gripping a corner of the blanket. The bedside lamp lights her hands; white landing light falls on his back through the door.'),
 'winter_finger': (['anya_ill', 'shen_home'], 'room', [], 'Dawn. SHEN sits on the edge of the bed with his head lowered, eyes red. ANYA leans against his shoulder; her little finger is hooked around his little finger on his knee. On the bedside table a full glass of water and a weekly pill organizer side by side. Grey-white light through the thin curtains; the bedside lamp is still on.'),
 'last_regulars': (['anya_ill', 'shen_apron', 'azhong', 'xiaokui'], 'bar', [], 'Early evening, opening time in her last months. ANYA sits on a stool on the CUSTOMER side of the counter, smiling; SHEN stands beside her. Behind the counter XIAO-KUI dries glasses at the sink; AH-ZHONG bends to set down a crate of beer. Pendant lamps on, dusk light through the door. Ordinary, warm, a little fragile.'),
 'last_taste': (['anya_ill', 'shen_apron', 'xiaokui'], 'bar', [], 'After closing, back-bar dark. ANYA and SHEN sit side by side on the customer side; she rests her face on his shoulder. XIAO-KUI reaches in to take away an empty glass. The lamp lights their hands, a glass of water and a mixing glass with a straw.'),
 'farewell_room': (['anya_ill', 'shen_shirt'], 'room', [], 'An ordinary afternoon, the window open, soft daylight, curtains moving. ANYA sits propped against the headboard and holds SHEN\'s hand; he sits on the edge of the bed. A freshly washed white shirt lies folded by her pillow; half a glass of water on the bedside table. Both in profile; she is smiling a little.'),
 'farewell_mother': (['mother', 'shen_black'], None, [], 'A plain office room in a funeral home, flat white daylight from a window. ANYA\'S MOTHER sits at a table squaring a small stack of documents; SHEN sits beside her with both hands pressing a folder on his lap, head lowered. A glass of water stands near her hand. Papers show no readable text. Muted greys.'),
 'farewell_bed': (['shen_seventh'], 'room', [], 'The seventh night. The room is lit by a pale ceiling light. SHEN sits on the door side of the bed only, his palm pressed flat on the empty half of the bed. A closed takeaway meal box sits on the bedside table. The stair landing light is on beyond the door. The room is tidy and emptied.'),
 'notebook_open': (['shen_seventh'], 'bar_night', [], 'SHEN stands behind the counter under the single lamp, his left hand holding open a palm-sized notebook, his right hand at the edge of the page. The handwriting is too small to read. Beyond the counter the seven empty stools stand in cold blue. There is NO cocktail, flute or wine glass anywhere on the counter: no drink has been made yet. ' + COLD),
 'notebook_august': (['shen_seventh'], 'bar_night', ['spoon'], 'Close. SHEN bends over the small notebook, a fingertip resting on one handwritten line (unreadable). The lamp lights the page. Behind him, in the dark back-bar, the gold bar spoon hangs from a hook. There is NO cocktail, flute or wine glass anywhere on the counter: no drink has been made yet. ' + COLD),
 'flash_syrup': (['anya_summer', 'shen_apron'], 'bar', [], 'A memory seen from over ANYA\'s shoulder (her shoulder, bun and one hand on a glass of water are the out-of-focus foreground). Across the counter SHEN sits holding a small tasting glass, wincing at how sweet it is, half laughing. A small cup stands by the sink. After closing, warm gold lamp light.'),
 'notebook_autumn': (['shen_seventh'], 'bar_night', [], 'SHEN sits behind the counter, his left hand flat on the notebook page (an ordinary hand: one thumb and four fingers, five digits in total), his right hand gripping the cloth of his trousers at the knee. Tears run down his face; he looks down at the page. The stool opposite him is empty in cold blue. There is NO cocktail, flute or wine glass anywhere on the counter: no drink has been made yet. ' + COLD),
 'flash_roof': (['anya_off', 'shen_shirt'], 'roof', ['dawn', 'spoon'], 'A memory from ANYA\'s side: she sits by the parapet in the near foreground, in profile, looking up at him. SHEN stands pouring along the gold bar spoon into a flute, concentrating; the western sun warms his face and the wind lifts the hem of his shirt.'),
 'notebook_last': (['shen_seventh'], 'bar_night', [], 'High angle, close on the counter. The notebook lies open at its last page: three hand-coloured bands, red, gold and pink, with crossed-out scribbles beside them (unreadable). SHEN\'s hand rests beside the page; to the right lies the unsealed white envelope. Only his hand and forearm are in frame. There is NO cocktail, flute or wine glass anywhere on the counter: no drink has been made yet. ' + COLD),
 'door_closed': (['shen_seventh', 'mother'], 'bar_night', [], 'Inside the bar at the glass-paned door. SHEN stands with his right hand flat against the wooden part of the door, head lowered. Through the glass, ANYA\'S MOTHER stands outside in the alley holding a bag with a food container, street light on her shoulder, looking at the door. Inside, only the one lamp. There is NO cocktail, flute or wine glass anywhere on the counter: no drink has been made yet. ' + COLD),
 'door_meal': (['mother'], 'front', [], 'From the alley at night. ANYA\'S MOTHER stands at the bar door seen from behind in three-quarter view, facing the door, her face turned away from us and worried, not smiling, one hand still on the door frame; a bag with a covered bowl sits on the ground by her feet. Behind the glass, the dim silhouette of a man with his head down. The street lamp shines white on the lid of the bowl. She is not knocking.'),
 'sunset_layers': (['shen_seventh'], 'bar_night', ['sunset', 'spoon'], 'SHEN stands behind the counter under the single lamp, the gold bar spoon in his left hand, pouring pale rose sparkling wine along its back with his right: three layers, ruby, gold, pink, glow in the flute. A covered bowl of food and the open notebook lie at his elbow. ' + COLD),
 'sunset_gold': (['shen_seventh'], 'bar_night', ['sunset'], 'SHEN holds the flute: the pink layer is gone and half of the gold; ruby remains at the bottom. His other hand has stopped beside the unopened bowl. The envelope lies further along the counter in blue window light. He stares at the glass, tasting nothing. ' + COLD),
 'sunset_meal': (['shen_seventh'], 'bar_night', [], 'SHEN sits behind the counter eating rice with a braised egg from the opened bowl with a spoon, a phone held to his ear, tear tracks on his face. Beside the open notebook stands the flute, now completely EMPTY and drained, only a faint red trace at the very bottom, no liquid in it. The seven stools opposite are still empty, but the lamp light feels warmer.'),
 'evening_bar': (['shen_apron', 'azhong', 'xiaokui'], 'bar', ['sunset', 'spoon'], 'A few weeks later, early evening, the bar open again: the lightbox outside the door is lit, all three pendant lamps on. SHEN stands behind the counter layering a drink along the gold bar spoon. AH-ZHONG sits on his old stool by the door with a bottled beer; XIAO-KUI holds up her phone to photograph a three-layer flute. ' + WARM),
 'evening_roof': (['shen_shirt'], 'roof', [], 'Another evening before opening. SHEN stands alone by the parapet, one hand on the wall, both sleeves rolled neatly to the same height, looking west. Sunset light on the side of his face; warm light spills from the stairwell door behind him. Wide shot, a lot of sky.'),
}

# 不在劇本裡的圖：封面
EXTRA = {
 'cover': (['anya', 'shen_apron'], 'bar', ['sunset'], 'Key art for the film. Early evening just before opening: low sunset light pours through the glass door and the alley window and lays red, gold and pink bands across the room. In the RIGHT foreground on the dark-wood counter, in sharp focus, stands one flute with the three-layer cocktail, glowing like a small sunset. Behind the counter in the centre of the frame, slightly out of focus, ANYA laughs with her head tilted toward SHEN, who stands beside her drying a glass and smiling down at her. The LEFT third of the frame is calm and dark (plain wall and the shadowed near end of the counter), with nothing important in it, for a title.'),
}
S.update(EXTRA)


def refs(k):
    cast, st, props, _ = S[k]
    names = [c.split('_')[0] for c in cast]
    r = [(n, f'ref/{n}.webp') for n in names] + ([(st, f'ref/{st}.webp')] if st else []) + ([('drinks', 'ref/drinks.webp')] if props else [])
    miss = [p for _, p in r if not os.path.exists(os.path.join(H, p))]
    assert not miss, f'{k} 缺定錨：{miss}'
    return r


def prompt(k):
    cast, st, props, text = S[k]
    r = refs(k)
    who = [f"{FACE[c.split('_')[0]]}" + (f"; wearing: {WEAR[c]}" if c in WEAR else '') for c in cast]
    order = '; '.join(f'image {i + 1} = {n.upper()}' for i, (n, _) in enumerate(r))
    return '\n\n'.join(x for x in [STYLE, f'Reference images in order: {order}.', 'CHARACTERS IN FRAME (nobody else has a visible face):\n- ' + '\n- '.join(who) if who else 'No people.',
                                   f'PLACE: {SET[st]}.' if st else '', ' '.join(DRINK[p] for p in props), 'SHOT: ' + text] if x)


def check():
    sys.path.insert(0, os.path.join(H, '../../src')); import script
    want = set(script.SHOTS.values())
    have = set(S) - set(EXTRA)
    assert want == have, f'劇本有、分鏡沒有：{want - have}；分鏡有、劇本沒有：{have - want}'
    for k, (cast, st, props, text) in S.items():
        refs(k)
        for name in ('ANYA\'S MOTHER', 'MOTHER', 'AH-ZHONG', 'XIAO-KUI', 'SHEN', 'ANYA'):
            key = {'ANYA\'S MOTHER': 'mother', 'MOTHER': 'mother', 'AH-ZHONG': 'azhong', 'XIAO-KUI': 'xiaokui', 'SHEN': 'shen', 'ANYA': 'anya'}[name]
            body = text.replace("ANYA'S MOTHER", 'MOTHER') if name == 'ANYA' else text
            assert not re.search(rf'\b{re.escape(name)}\b', body) or key in [c.split('_')[0] for c in cast], f'{k}：畫面寫到 {name}，在場沒列'


if __name__ == '__main__':
    cmd = sys.argv[1]; check()
    if cmd == 'list':
        for k in S: print(k, [n for n, _ in refs(k)])
    elif cmd == 'prompt':
        print(prompt(sys.argv[2]))
    elif cmd == 'gen':
        ks = list(S) if sys.argv[2] == 'all' else sys.argv[2].split(','); n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        os.makedirs(os.path.join(H, 'raw'), exist_ok=True); procs = []
        for k in ks:
            pf = os.path.join(H, 'prompts', f'shot_{k}.txt'); open(pf, 'w').write(prompt(k))
            have = len([f for f in os.listdir(os.path.join(H, 'raw')) if re.fullmatch(rf'{k}_\d+\.png(\.lock)?', f)])
            for i in range(have + 1, have + n + 1):
                procs.append(subprocess.Popen([sys.executable, 'gen.py', f'raw/{k}_{i}.png', pf, *[p for _, p in refs(k)]], cwd=H))
        bad = [p.args[2] for p in procs if p.wait()]
        print('送出', len(procs), '失敗', bad)
    elif cmd == 'install':
        from PIL import Image
        out = os.path.join(H, '../../assets/art/cg'); os.makedirs(out, exist_ok=True)
        for pick in sys.argv[2:]:
            k = pick.rsplit('_', 1)[0]; assert k in S, pick
            im = Image.open(os.path.join(H, 'raw', pick + '.png')).convert('RGB'); im.thumbnail((1600, 1600))
            im.save(os.path.join(out, k + '.webp'), quality=86); print('installed', k, im.size)
