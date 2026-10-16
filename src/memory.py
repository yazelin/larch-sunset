"""劇本台詞（design/重寫.md，2026-10-17 定稿）：序幕、便條，與穿插在解謎中的回憶。
找到一樣東西就回到一段過去：答完風味筆記→回憶一、拿匙→回憶二、儲藏間→回憶三。
回憶都用現在的吧檯分層圖，靠燈光、時間、人物位置區分；配音檔名＝台詞 id。
現在（頭七）用沈淮第一人稱，回憶用第三人稱。
"""
import pathlib
from mapkit import *
import cards, layout

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = layout.load('bar')
W, H = D['map']['w'], D['map']['h']
ANYA, SHEN = '安雅', '沈淮'
VOICE = {ANYA: ('Chinese (Mandarin)_Soft_Girl', 'calm'), SHEN: ('Chinese (Mandarin)_Gentle_Youth', 'calm')}

# 台詞：卡片 id → [(講者, 文字, 配音 id 或 None, 情緒)]。講者空字串＝旁白，不配音
L = {
    # 序幕：開頭獨白＋頭七回店
    'prologue': [
        (SHEN, '都說味道是最後才會忘記的東西。比臉晚，比聲音晚。', 'p_shen_open1', 'calm'),
        (SHEN, '很多年以後，一杯酒送到嘴邊，人就回到了那一晚。', 'p_shen_open2', 'calm'),
        (SHEN, '她的頭七這一晚，我才知道，最先被帶走的，就是味道。', 'p_shen_open3', 'sad'),
        ('', '頭七。人家說，這一晚她會回家。', None, ''),
        ('', '店門口的燈箱，從她走後就沒再亮過。我推開門，門上的鈴響了一聲，跟三年前一模一樣。', None, ''),
    ],
    # 空杯旁的便條：只交代店與生活，不提酒
    'card_anya_note': [
        (ANYA, '沈淮：店交給你了。冰箱裡有我包好的餃子，記得吃飯。', 'n_anya_1', 'calm'),
        (ANYA, '後門記得上鎖。', 'n_anya_2', 'calm'),
        (ANYA, '不要每天都等到兩點十七分才關門。', 'n_anya_3', 'sad'),
        ('', '她寫便條，從來不署名。', None, ''),
    ],
    # 答完風味筆記，進回憶一
    'card_mem1_enter': [
        ('', '窗外開始下雨了。', None, ''),
        (SHEN, '三年前的那個晚上，也在下雨。', 'mem_shen_enter', 'sad'),
    ],
    # 回憶一：他淋濕進門，她是調酒師（設定 A，作者 2026-10-16 拍板）
    'card_mem1_intro': [
        ('', '三年前。雨下得很大，打烊前最後一刻，門上的鈴響了。', None, ''),
        (SHEN, '還有營業嗎？', 'a_mem1_shen_open', 'calm'),
        (ANYA, '還有一杯的時間。', 'a_mem1_anya_open', 'calm'),
        ('', '她從吧檯後面遞出一條毛巾，笑了笑。', None, ''),
        (ANYA, '先擦乾，再點酒。', 'a_mem1_anya_towel', 'happy'),
    ],
    'card_mem1_seat': [
        ('', '他坐上高腳椅，拿毛巾胡亂擦著頭髮。她撐著吧檯看他。', None, ''),
        (ANYA, '你是來躲雨，還是來喝酒的？', 'a_mem1_anya_why', 'happy'),
    ],
    'card_mem1_rain': [(ANYA, '那雨停之前，你都是我的客人。', 'a_mem1_anya_guest', 'happy')],
    'card_mem1_both': [
        (ANYA, '貪心。', 'a_mem1_anya_greedy', 'happy'),
        ('', '她轉身去拿杯子。', None, ''),
    ],
    'card_mem1_order': [(ANYA, '想喝什麼？', 'a_mem1_anya_order', 'calm')],
    'card_mem1_bitter': [
        ('', '她拿酒瓶的手停了一下，抬頭看他。', None, ''),
        (ANYA, '……你也怕苦？', 'a_mem1_anya_bitter', 'calm'),
    ],
    'card_mem1_strong': [(ANYA, '淋成這樣還喝烈的？看你也不像會喝苦的人。今晚聽我的。', 'a_mem1_anya_strong', 'happy')],
    'card_mem1_mix': [
        (ANYA, '那我調一杯我自己最喜歡的。還沒給別人喝過。', 'a_mem1_anya_fav', 'happy'),
        ('', '金黃的甜白酒，一小匙番紅花糖漿，最後她在杯口磨了幾粒粉紅胡椒，把杯子推到他面前。', None, ''),
        (ANYA, '最黑的時候，喝一杯天亮。', 'a_mem1_anya_dark', 'calm'),
    ],
    'card_mem1_stare': [(ANYA, '看我做什麼？喝酒。', 'a_mem1_anya_stare', 'happy')],
    'card_mem1_taste': [
        ('', '他咬到胡椒，舌尖麻了一下，愣住了。她撐著吧檯看他，等他開口。', None, ''),
        ('', '她也低頭抿了一口。甜味和胡椒的麻，在舌尖上慢慢分開。', None, ''),
        (SHEN, '好辣……可是好甜。', 'a_mem1_shen_spicy', 'surprised'),
        (ANYA, '像不像天快亮的時候？', 'a_mem1_anya_dawn', 'happy'),
        (SHEN, '像。', 'a_mem1_shen_like', 'calm'),
        ('', '她笑了。那是她那一晚第一次真的笑。', None, ''),
        (ANYA, '那就叫它〈破曉〉。', 'a_mem1_anya_name', 'happy'),
        ('', '她這才發現他髮尾的水還在往吧檯上滴。她拿過毛巾，探身越過吧檯，替他把頭髮擦乾。', None, ''),
        ('', '她的手停在他耳邊，過了很久才拿開。', None, ''),
        ('', '她抬頭看牆上的掛鐘。', None, ''),
        (ANYA, '兩點十七分。你是我今天最後一個客人。', 'a_mem1_anya_last', 'calm'),
        (SHEN, '那我明天早一點來。', 'a_mem1_shen_tomorrow', 'calm'),
        (ANYA, '……兩點十七分。我會記得。', 'a_mem1_anya_remember', 'happy'),
    ],
    'card_mem1_leave': [
        (ANYA, '喂。', 'a_mem1_anya_hey', 'calm'),
        ('', '她追到門口，把一把傘塞進他手裡。指尖碰到的時候，她沒有馬上縮回去。', None, ''),
        (ANYA, '明天要還。', 'a_mem1_anya_return', 'happy'),
    ],
    'card_mem1_cg': [('', '那天晚上的雨，一直下到天亮。', None, '')],
    # 回憶二：她教他用黃銅匙
    'card_mem2_enter': [
        (SHEN, '只借你。', 'mem2_shen_enter', 'sad'),
        ('', '那年夏天的尾巴。', None, ''),
    ],
    'card_mem3_enter': [
        ('', '瓶口還黏著一圈乾掉的金黃。她熬糖漿的時候，整間店都是這個味道。', None, ''),
        (SHEN, '第三年，她開始每一杯都問我甜不甜。', 'mem3_shen_enter', 'sad'),
    ],
    'card_mem2_intro': [
        ('', '開店前的午後，陽光斜斜照進大窗。他已經連著來了四個多月，每天都坐到兩點十七分，等她抬頭看鐘，才走。', None, ''),
        ('', '吧檯上放著一小瓶藥。她看了他一眼，把藥收進圍裙口袋。', None, ''),
        (ANYA, '偏頭痛。老毛病了。', 'a_mem2_anya_migraine', 'calm'),
        (ANYA, '沈淮，過來。今天教你調酒。', 'a_mem2_anya_teach', 'happy'),
        (ANYA, '吧檯角落那把匙，幫我拿過來。', 'a_mem2_anya_spoon', 'calm'),
    ],
    'card_mem2_spoon': [
        (ANYA, '貼著杯壁，慢慢轉。不要用力。', 'a_mem2_anya_how', 'calm'),
        (SHEN, '這樣？', 'a_mem2_shen_like', 'calm'),
        ('', '杯裡的顏色一下子全攪混了。', None, ''),
    ],
    'card_mem2_again': [
        ('', '他又轉了一次。顏色還是攪成一團。', None, ''),
        (ANYA, '你不行啦。手給我。', 'a_mem2_anya_hand', 'happy'),
    ],
    'card_mem2_hands': [
        ('', '她站到他身後，手覆上他的手。匙沿著杯壁轉了一圈，金黃在杯裡慢慢旋開，沒有混。', None, ''),
        (ANYA, '感覺到了嗎？', 'a_mem2_anya_feel', 'calm'),
        (SHEN, '……感覺到了。', 'a_mem2_shen_feel', 'calm'),
        (ANYA, '以後我調不動了，你要替我調。', 'a_mem2_anya_future', 'calm'),
        (SHEN, '那妳要一直站在旁邊盯著。', 'a_mem2_shen_watch', 'happy'),
        (ANYA, '……好。', 'a_mem2_anya_ok', 'sad'),
        ('', '匙停了。她的手沒有放開。', None, ''),
        (ANYA, '你的手好冰。', 'a_mem2_anya_cold', 'calm'),
        (SHEN, '是妳的手太燙。', 'a_mem2_shen_hot', 'calm'),
        ('', '誰都沒有先退開。', None, ''),
    ],
    'card_mem2_grip': [('', '他翻過手，把她的手握進掌心。', None, '')],
    'card_mem2_turn': [('', '他轉過身。她就在他面前，近到看得見她的睫毛在抖。', None, '')],
    'card_mem2_mine': [
        (ANYA, '……這把匙是我的。只借你。', 'a_mem2_anya_mine', 'calm'),
        ('', '他低下頭。她沒有躲。', None, ''),
        ('', '陽光落在吧檯上，杯子裡的金黃還在慢慢地轉。那是他們第一次接吻。', None, ''),
        ('', '很久以後，她才把手抽回去。', None, ''),
    ],
    'card_mem2_cg': [('', '那把匙，她一直放在自己的位置上。', None, '')],
    'card_mem1_back': [(SHEN, '窗外的雨還在下。吧檯前，只剩我一個人。', 'back1_shen', 'sad')],
    'card_mem2_back': [(SHEN, '匙在我手裡。她的手不在了。', 'back2_shen', 'sad')],
    'card_mem3_back': [(SHEN, '我還蹲在儲藏間的抽屜前，手裡是她熬的最後一瓶糖漿。', 'back3_shen', 'sad')],
    # 回憶三：甜嗎
    'card_mem3_intro': [
        ('', '第三年。他已經能自己站吧檯了。', None, ''),
        ('', '打烊後，兩個人換了位置：他坐到客人那一側，她回到吧檯後面，照例調一杯給他試。', None, ''),
        (ANYA, '來，試試這杯。', 'mem3_anya_try', 'happy'),
    ],
    'card_mem3_ask': [
        ('', '她把酒含在舌尖，停了一會，像在等味道回來。然後往杯裡加了兩匙糖漿。', None, ''),
        (ANYA, '照我記得的，應該剛好。', 'mem3_anya_justright', 'calm'),
        ('', '她把杯子推到他面前。', None, ''),
        (ANYA, '甜嗎？', 'mem3_anya_sweet', 'calm'),
    ],
    'card_mem3_ok': [('', '她鬆了一口氣似的笑了。', None, '')],
    'card_mem3_toosweet': [
        ('', '她愣了一拍。', None, ''),
        (ANYA, '……那你調的時候，少兩匙。', 'mem3_anya_less', 'calm'),
    ],
    'card_mem3_why': [
        (SHEN, '怎麼了？', 'mem3_shen_why', 'calm'),
        (ANYA, '沒事。偏頭痛。', 'mem3_anya_nothing', 'calm'),
    ],
    'card_mem3_shoulder': [
        ('', '她繞出吧檯，在他旁邊的高腳椅坐下，頭靠上他的肩膀。', None, ''),
        (ANYA, '沈淮，我想跟你一起看一次晚霞。', 'mem3_anya_sunset', 'sad'),
        (SHEN, '明天傍晚就帶妳去。', 'mem3_shen_tomorrow', 'calm'),
        (ANYA, '如果有一天，我嚐不出你調的酒了呢？', 'a_mem3_anya_ifone', 'sad'),
        (SHEN, '那我就調到妳嚐得出來為止。', 'a_mem3_shen_until', 'calm'),
        ('', '她把臉埋進他的肩膀，很久沒有抬起來。', None, ''),
    ],
    'card_mem3_cg': [('', '那是她第一次說，想跟他一起看晚霞。', None, '')],
    'card_mem3_night': [
        ('', '那天夜裡，他醒過來。床的另一邊是空的，還留著她的體溫。', None, ''),
        ('', '他下樓。店裡只開了一盞燈。', None, ''),
        ('', '她穿著他的襯衫，一個人坐在吧檯前。面前排著一整排碟形杯，每一杯都只少了一口。', None, ''),
        (SHEN, '安雅？', 'mem3_shen_night', 'surprised'),
        (ANYA, '在研發新酒。還差一點。', 'mem3_anya_almost', 'calm'),
        ('', '她把那瓶番紅花糖漿推到一邊，站起來，牽起他的手。', None, ''),
        (ANYA, '回去睡。明天還要開店。', 'mem3_anya_sleep', 'calm'),
        ('', '上樓的時候，她的手很冰。他以為是夜裡冷。', None, ''),
    ],
    # ---- 臥室：木盒、病歷、胡椒上的字條 ----
    'card_box_truth': [
        ('', '盒子裡墊著暗紅色的絨布。上面是一疊病歷，摺痕被摺開又摺回很多次。', None, ''),
        ('', '「味覺中樞進行性壞死。伴隨神經痛，將逐年加重。目前無治療方式，以止痛為主。」', None, ''),
        ('', '確診日期，是三年前的七月。', None, ''),
        (SHEN, '七月……', 'b_shen_july', 'sad'),
        (SHEN, '那年夏天的尾巴，她開始教我調酒。', 'b_shen_teach', 'sad'),
        ('', '病歷底下夾著一張處方箋，開的是神經止痛藥。藥名旁邊，她用鉛筆寫了三個字：偏頭痛。', None, ''),
        ('', '絨布中間放著一只粉紅胡椒研磨罐。是初遇那晚，她磨在我杯口的那一只。', None, ''),
        ('', '研磨罐上纏著一張字條。', None, ''),
        (ANYA, '這罐有毒。我用的就是它。不要碰。', 'b_anya_poison', 'sad'),
        (SHEN, '……原來不是心臟。', 'b_shen_heart', 'sad'),
        ('', '我把研磨罐握在手裡，握了很久。然後放進了口袋。', None, ''),
    ],
    'card_mem4_enter': [
        (SHEN, '三年裡，我只帶她看過一次晚霞。', 'mem4_shen_enter', 'sad'),
    ],
    # ---- 回憶四〈晚霞〉：頂樓（卡片＋CG 演出） ----
    'card_mem4_1': [
        ('', '第三年的秋天。一個公休日的傍晚，他終於帶她上了頂樓。', None, ''),
        ('', '風很大。整片天從金黃燒成粉紅，再一點一點暗下去。', None, ''),
        (ANYA, '晚霞我自己看過很多次。', 'mem4_anya_seen', 'calm'),
        (ANYA, '跟你一起看，才是這種顏色。', 'mem4_anya_color', 'happy'),
        ('', '他從保溫瓶裡倒出一杯〈破曉〉。是照著她教的，一個步驟都沒有少。', None, ''),
        (SHEN, '甜嗎？', 'mem4_shen_sweet', 'calm'),
        ('', '她喝了一口，看著天，很久才開口。', None, ''),
        (ANYA, '好甜。', 'mem4_anya_sweet', 'happy'),
        ('', '她把杯子捧在手心裡，靠上他的肩膀。', None, ''),
        (ANYA, '你調的，都好甜。', 'mem4_anya_yours', 'happy'),
    ],
    'card_mem4_2': [
        ('', '天暗下來以後，她把杯子擱在欄杆上，牽起他的手。', None, ''),
        (ANYA, '陪我跳一支。', 'mem4_anya_dance', 'happy'),
        (SHEN, '沒有音樂。', 'mem4_shen_nomusic', 'calm'),
        (ANYA, '有風就好。', 'mem4_anya_wind', 'calm'),
        ('', '他們在風裡慢慢地晃。她把臉貼在他胸口，聽了很久他的心跳。', None, ''),
        (ANYA, '沈淮，以後你要常常來看晚霞。', 'mem4_anya_often', 'sad'),
        (SHEN, '我們一起。', 'mem4_shen_together', 'calm'),
        ('', '她沒有回答。', None, ''),
    ],
    'card_mem4_return': [
        (SHEN, '她說好甜。', 'mem4_shen_ret1', 'sad'),
        (SHEN, '那時候，她已經什麼都嚐不出來了。', 'mem4_shen_ret2', 'sad'),
    ],
    # 她那一側的床
    'card_bed': [
        ('', '床的另一邊，枕套上還留著幾根她的頭髮。', None, ''),
        ('', '那天夜裡我醒過一次。她剛從樓下上來，身上很冰，躺回我身邊。', None, ''),
        ('', '我問她去了哪裡。', None, ''),
        (ANYA, '睡吧。', 'bed_anya_sleep', 'calm'),
        (SHEN, '那是她跟我說的最後一句話。', 'bed_shen_last', 'sad'),
        ('', '天亮的時候，她已經冷了。', None, ''),
        (SHEN, '她那天晚上，是在樓下喝了它。', 'bed_shen_downstairs', 'sad'),
    ],
    # ---- 杯墊下的遺言 ----
    'card_confession': [
        (ANYA, '沈淮：我就知道你會找到這裡。所以我賭你，最後一次會聽我的。', 'c_anya_1', 'sad'),
        (ANYA, '我瞞了你快三年。那年七月，我就知道自己會嚐不到味道。我本來想叫你不要再來了，可是你每天都坐到兩點十七分才走。', 'c_anya_2', 'sad'),
        (ANYA, '偏頭痛是假的。研發新酒是真的。', 'c_anya_3', 'sad'),
        (ANYA, '這杯叫〈晚霞〉，我本來是要調給你的。初遇是快要破曉，我想再給我們一個傍晚。', 'c_anya_4', 'sad'),
        (ANYA, '可是我調了快三年，還差一點，舌頭就先不行了。痛也一天比一天清楚。', 'c_anya_5', 'sad'),
        (ANYA, '所以最後，我把它留給了自己。毒在胡椒裡，我喝的就是這一杯。喝的時候，我嚐不出它對不對。', 'c_anya_6', 'sad'),
        (ANYA, '不要嚐它，替我倒掉。', 'c_anya_7', 'sad'),
        (ANYA, '店交給你了。好好吃飯。', 'c_anya_8', 'sad'),
    ],
    'card_spirit': [
        ('', '我抬起頭。', None, ''),
        ('', '吧檯後面，她平常站的位置，有一個很淡很淡的影子。她穿著那件圍裙，看著我手裡的杯子，輕輕搖頭。', None, ''),
        ('', '我端起杯子，繞出吧檯，坐到三年前那張高腳椅上。', None, ''),
        (SHEN, '妳到最後，都不知道這一杯對不對。', 'sp_shen_know', 'sad'),
    ],
    # ---- 結局〈共赴晚霞〉 ----
    'ending_burn_1': [
        (SHEN, '對不起。這一次，我不聽妳的。', 'eb_shen_sorry', 'sad'),
        ('', '金黃沉在底下，粉紅浮在上面。我一口喝完。', None, ''),
    ],
    'ending_burn_2': [
        ('', '先是甜白酒。然後是番紅花，溫的，像那天晚上她遞過來的毛巾。', None, ''),
        ('', '最後是胡椒。舌尖麻了一下，刺痛慢慢散開。', None, ''),
        ('', '毒是安靜的。胸口一點一點變輕，像要睡著了。', None, ''),
        (SHEN, '……甜的。', 'eb_shen_sweet', 'sad'),
        (SHEN, '是那天晚上的味道。', 'eb_shen_night', 'sad'),
    ],
    'ending_burn_3': [
        ('', '吧檯後面的影子抬起頭。她在哭，也在笑。', None, ''),
        (ANYA, '……傻瓜。', 'eb_anya_fool', 'sad'),
        (SHEN, '妳做到了。〈晚霞〉調對了。', 'eb_shen_done', 'calm'),
        ('', '我抬頭看那座停在兩點十七分的鐘。', None, ''),
        (SHEN, '……兩點十七分。我會記得。', 'eb_shen_remember', 'calm'),
        ('', '冷藍的店裡，光一點一點暈開，染成金黃和淡粉。', None, ''),
        (SHEN, '安雅……這一次，妳不必一個人走。', 'eb_shen_alone', 'calm'),
    ],
    'ending_burn_4': [
        (SHEN, '最先被帶走的，是味道。', 'eb_shen_close1', 'calm'),
        (SHEN, '最後留下來的，也是。', 'eb_shen_close2', 'calm'),
    ],
    # ---- 結局〈冷卻的餘溫〉 ----
    'ending_cold_1': [
        ('', '我的手在抖。', None, ''),
        ('', '我走回吧檯，把杯子翻過來。金黃被水沖淡，粉紅的胡椒碎在不鏽鋼上轉了幾圈，流進排水孔。', None, ''),
        ('', '吧檯後面的影子鬆了一口氣似的笑了。然後就不見了。', None, ''),
    ],
    'ending_cold_2': [
        ('', '我把研磨罐放回木盒，鎖上。', None, ''),
        ('', '店照常開。客人說，我調的〈破曉〉跟她調的一模一樣。', None, ''),
        ('', '我喝不出來。', None, ''),
        (SHEN, '醫生說，我的舌頭沒有問題。', 'ec_shen_doctor', 'calm'),
        (SHEN, '是她走的時候，把所有的味道都帶走了。', 'ec_shen_taken', 'sad'),
    ],
    'ending_cold_3': [
        ('', '每天晚上兩點十七分，我調一杯沒有毒的〈晚霞〉，放在她的位置上。', None, ''),
        (SHEN, '甜嗎？', 'ec_shen_sweet', 'sad'),
        ('', '沒有人回答。', None, ''),
        (SHEN, '最先被帶走的，是味道。我留下來，替她記得。', 'ec_shen_close', 'calm'),
    ],
}


# 地圖上沈淮的第一人稱內心話（地圖對話框掛不了音檔）：建置時轉成一句一張的對話卡，地圖改播卡片（作者 2026-10-17：要配）
MAP_LINES = {}


def _map_voice_id(text):
    import hashlib
    return 'mv_' + hashlib.md5(text.encode()).hexdigest()[:8]


def voice_map_lines(board):
    """把地圖事件裡含「我」的旁白換成帶配音的卡片；回傳新增的卡片數。"""
    import json as _j
    have = {n['id'] for n in board['nodes']}
    added = []

    def walk(o):
        # 地圖資料有的層是 JSON 字串（pluginValues），解開走完再包回去
        if isinstance(o, str) and o[:1] in '{[':
            try:
                d = _j.loads(o)
            except ValueError:
                return o
            return _j.dumps(walk(d), ensure_ascii=False)
        if isinstance(o, dict):
            if o.get('kind') == 'dialogue' and not o.get('cardId') and '我' in (o.get('text') or ''):
                t = o['text']; vid = _map_voice_id(t)
                MAP_LINES['card_' + vid] = [(SHEN, t, vid, 'sad')]
                if 'card_' + vid not in have:
                    have.add('card_' + vid); added.append(cards.dialogue('card_' + vid, '沈淮', [(SHEN, t, f'/files/assets/voice/{vid}.mp3')]))
                # text 要留空字串：引擎讀地圖時每個動作都會去處理 text，欄位不在整張地圖就讀不了（2026-10-17 推上 Larch 才發現）
                o['text'] = ''
                o.pop('speaker', None)
                o['cardId'] = 'card_' + vid
            for k in list(o): o[k] = walk(o[k])
        elif isinstance(o, list):
            for i in range(len(o)): o[i] = walk(o[i])
        return o
    for n in board['nodes']:
        if n['id'].startswith('m-'):
            walk(n['data'])
    board['nodes'].extend(added)
    return len(added)


def voice_lines():
    """給配音腳本：[(檔名, 文字, 聲線, 情緒)]"""
    return [(f'{vid}.mp3', tx, VOICE[sp][0], emo or VOICE[sp][1]) for ls in list(L.values()) + list(MAP_LINES.values()) for sp, tx, vid, emo in ls if vid]


def _card(cid, title, art, bg='', **kw):
    lines = [(sp, tx, f'/files/assets/voice/{vid}.mp3' if vid else None) for sp, tx, vid, _ in L[cid]]
    actors = [cards.actor(n, art['p-anya'] if n == ANYA else art['p-shen'], 'right' if n == ANYA else 'left')
              for n in (SHEN, ANYA) if any(sp == n for sp, *_ in L[cid])] if not bg else []
    return cards.dialogue(cid, title, lines, bg=bg, actors=actors, **kw)


def _env(darkness, lights):
    return {'weather': 'clear', 'intensity': 0, 'darkness': darkness, 'shake': 0,
            'lights': [dict(zip(('id', 'x', 'y', 'radius', 'color', 'flicker'), l)) for l in lights]}


def _map(mid, title, art, events, guidance, env, bgm='bgm-spoon'):
    real = (ROOT / 'assets/maps/bar_ground.webp').exists()
    kind = 'objects' if real else 'blocks'
    urls = {o['name']: f"/files/assets/{kind}/bar/{o['name']}.webp" for o in layout.objects(D)}
    events = events + [dict(e, id=e['id'].replace('obj-m-bar', f'obj-{mid}')) for e in layout.events(D, urls)]
    m = map_dict(title, W, H, f'/files/assets/maps/bar_{"ground" if real else "blocks"}.webp', layout.walls(D), events, guidance, env)
    return map_node(mid, title, m, bgm=art.get(bgm, ''))


def build(board, art):
    N = board['nodes'].append
    link = lambda a, b: cards.link(board, a, b)
    shen = lambda x, y, d: ev('hero', x, y, actor='player', direction=d, sprite=walker(art['walk-shen']), actorId='shen')
    anya = walker(art['walk-anya'])

    # 序幕與便條
    N(_card('prologue', '序幕：頭七', art, bg=art['bg-bar'], start=True, bgm=art.get('bgm-bar')))
    N(_card('card_anya_note', '安雅的便條', art))
    # 每段回憶的入口（地圖事件 jump 過來）
    N(_card('card_mem1_enter', '回憶：兩點十七分', art, bg=art['bg-black'], bgm=art['bgm-storm']))
    N(_card('card_mem2_enter', '回憶：黃銅匙', art, bg=art['bg-black']))
    N(_card('card_mem3_enter', '回憶：甜嗎', art, bg=art['bg-black']))

    # ── 回憶一〈02:17，暴雨〉：他淋濕進門（9,9）；她在吧檯後（10,3）；高腳椅（9,6）；門口（9,10） ──
    guest = lambda x, y, d: ev('hero', x, y, actor='player', direction=d, sprite=walker(art['walk-shen-casual']), actorId='shen')
    m1 = [
        guest(9, 9, 'up'),
        ev('mem1-intro', 1, 11, trigger='auto', once=True, actions=[card('card_mem1_intro'), setv('mem1', 'seat')]),
        npc('mem1-anya', 10, 3, anya, direction='down', name='安雅', marker={'label': '安雅', 'kind': 'talk'},
            actions=[say('她用下巴指了指吧檯前的高腳椅。', speaker='player')]),
        ev('mem1-seat', 9, 6, name='吧檯前的高腳椅', marker={'label': '坐下', 'kind': 'quest'}, conditions=[cond('mem1', 'seat')],
           actions=[
               # 第一個動作不能是選擇題：按互動鍵的那一下會直接選到選擇題的第一個選項
               card('card_mem1_seat'),
               choice_action('回答她：躲雨，還是喝酒？', [
                   ('「躲雨。」', [card('card_mem1_rain')]),
                   ('「都有。」', [card('card_mem1_both')]),
               ], speaker='player'),
               card('card_mem1_order'),
               choice_action('點什麼？', [
                   ('「不要太苦就好。」', [card('card_mem1_bitter')]),
                   ('「來杯最烈的。」', [card('card_mem1_strong')]),
               ], speaker='player'),
               card('card_mem1_mix'),
               choice_action('杯子推到你面前。', [
                   ('喝一口', []),
                   ('先看著她', [card('card_mem1_stare')]),
               ], speaker='player'),
               card('card_mem1_taste'), setv('mem1', 'leave'),
           ]),
        ev('mem1-door', 9, 10, name='門口', marker={'label': '雨小了，該走了', 'kind': 'quest'}, conditions=[cond('mem1', 'leave')],
           actions=[card('card_mem1_leave'), setv('mem1', 'done'), jump('card_mem1_cg')]),
    ]
    g1 = [
        {'text': '坐到吧檯前的高腳椅', 'eventId': 'mem1-seat', 'conditions': [cond('mem1', 'seat')]},
        {'text': '雨小了，往門口走', 'eventId': 'mem1-door', 'conditions': [cond('mem1', 'leave')]},
    ]
    N(_map('m-mem-1', '回憶：暴雨的夜', art, m1, g1,
           _env(0, [('m1-bar', 9, 3, 6, '#ffc46b', False), ('m1-lounge', 10, 7, 7, '#ffb04d', False), ('m1-door', 9, 9, 3, '#ffd18a', False)]), bgm='bgm-storm'))
    N(_card('card_mem1_cg', '回憶：初遇', art, bg=art['cg-mem1']))

    # ── 回憶二〈黃銅匙〉：她在吧檯後（10,3）教他；匙在吧檯前角落（11,6） ──
    m2 = [
        guest(9, 7, 'up'),   # 還在學，穿便服；第三年才換上調酒師的衣服
        ev('mem2-intro', 1, 11, trigger='auto', once=True, actions=[card('card_mem2_intro'), setv('mem2', 'spoon')]),
        # 吧檯角落的匙：跟現在的吧檯同一張道具圖、同一個位置，拿起來就消失
        ev('mem2-spoon-visual', 0, 8, name='黃銅調酒匙視覺', free={'url': art['prop-spoon-tall'], 'x': 10.85, 'y': 4.35, 'w': 0.35, 'h': 2.7},
           conditions=[cond('mem2', 'spoon')]),
        ev('mem2-spoon', 11, 6, name='黃銅調酒匙', marker={'label': '黃銅匙', 'kind': 'quest'}, conditions=[cond('mem2', 'spoon')],
           actions=[say('吧檯角落的黃銅調酒匙，柄被她握得發亮。', speaker='player'), item('spoon_old', '黃銅調酒匙'), setv('mem2', 'teach')]),
        npc('mem2-anya', 10, 3, anya, direction='down', name='安雅', marker={'label': '安雅', 'kind': 'talk'},
            actions=[branch([cond('mem2', 'teach')],
                            [remove('spoon_old', '黃銅調酒匙'), card('card_mem2_spoon'),
                             choice_action('又混了。', [
                                 ('「妳教我。」', []),
                                 ('再試一次', [card('card_mem2_again')]),
                             ], speaker='player'),
                             card('card_mem2_hands'),
                             choice_action('她的手還覆在你手上。', [
                                 ('握緊她的手', [card('card_mem2_grip')]),
                                 ('轉過身', [card('card_mem2_turn')]),
                             ], speaker='player'),
                             card('card_mem2_mine'), setv('mem2', 'done'), jump('card_mem2_cg')],
                            [say('她在等那把匙。吧檯角落。', speaker='player')])]),
    ]
    g2 = [
        {'text': '拿吧檯角落的黃銅匙', 'eventId': 'mem2-spoon', 'conditions': [cond('mem2', 'spoon')]},
        {'text': '繞進吧檯，把匙交給她', 'eventId': 'mem2-anya', 'conditions': [cond('mem2', 'teach')]},
    ]
    N(_map('m-mem-2', '回憶：開店前的午後', art, m2, g2,
           _env(0, [('m2-sun', 14, 4, 8, '#ff8a3d', False), ('m2-bar', 9, 3, 5, '#ffb35c', False)])))
    N(_card('card_mem2_cg', '回憶：黃銅匙', art, bg=art['cg-mem2']))

    # ── 回憶三〈甜嗎〉：她在吧檯後（10,3），推過來的杯子在吧檯前（10,6） ──
    m3 = [
        shen(12, 7, 'up'),
        ev('mem3-intro', 1, 11, trigger='auto', once=True, actions=[card('card_mem3_intro'), setv('mem3', 'glass')]),
        npc('mem3-anya', 10, 3, anya, direction='down', name='安雅'),
        ev('mem3-glass', 10, 6, name='她推過來的那杯', marker={'label': '她推過來的那杯', 'kind': 'quest'}, conditions=[cond('mem3', 'glass')],
           actions=[
               card('card_mem3_ask'),
               choice_action('回答她甜不甜。', [('「剛好。」', [card('card_mem3_ok')]), ('「有點太甜。」', [card('card_mem3_toosweet')])], speaker='player'),
               choice_action('她看起來有點不一樣。', [
                   ('問她怎麼了', [card('card_mem3_why')]),
                   ('什麼都不說', [say('他沒有問，只是看著她把杯子收回去。', speaker='player')]),
               ], speaker='player'),
               card('card_mem3_shoulder'), setv('mem3', 'done'), jump('card_mem3_cg'),
           ]),
    ]
    g3 = [{'text': '喝她推過來的那杯', 'eventId': 'mem3-glass', 'conditions': [cond('mem3', 'glass')]}]
    N(_map('m-mem-3', '回憶：打烊之後', art, m3, g3,
           _env(0.3, [('m3-lamp', 10, 4, 5, '#ffc078', False)])))
    N(_card('card_mem3_cg', '回憶：想看晚霞', art, bg=art['cg-mem3']))


    # 回憶三夜裡、臥室真相、回憶四、遺言、抉擇、結局
    cg = lambda k, alt: art.get(k) or art[alt]
    for k in ('card_mem1_back', 'card_mem2_back', 'card_mem3_back'):
        N(_card(k, '回到現在', art, bg=art['bg-black'], bgm=art['bgm-bar']))
    N(_card('card_mem3_night', '回憶：還差一點', art, bg=cg('cg-mem3b', 'cg-mem3'), bgm=art['bgm-almost']))
    N(_card('card_box_truth', '木盒', art, bgm=art['bgm-almost']))
    N(_card('card_mem4_enter', '回憶：晚霞', art, bg=art['bg-black']))
    N(_card('card_mem4_1', '回憶：頂樓', art, bg=cg('cg-mem4', 'cg-mem3'), bgm=art['bgm-rooftop']))
    N(_card('card_mem4_2', '回憶：有風就好', art, bg=cg('cg-mem4', 'cg-mem3')))
    N(_card('card_mem4_return', '回到現在', art, bg=art['bg-bedroom'], bgm=art['bgm-bar']))
    N(_card('card_bed', '她那一側的床', art))
    N(_card('card_confession', '杯墊下的信', art, bg=art['cg-cocktail'], bgm=art.get('bgm-confession')))
    N(_card('card_spirit', '頭七', art, bg=art['cg-cocktail']))
    N(cards.choice('card_choice', '抉擇', '她拜託我倒掉。', ['替她嚐', '照她說的倒掉'], speaker=SHEN, bg=art['cg-cocktail']))
    N(_card('ending_burn_1', '共赴晚霞', art, bg=art['cg-cocktail'], bgm=art['bgm-together']))
    N(_card('ending_burn_2', '共赴晚霞', art, bg=art['cg-cocktail']))
    N(_card('ending_burn_3', '共赴晚霞', art, bg=art['cg-ending-burn']))
    N(_card('ending_burn_4', '共赴晚霞', art, bg=art['cg-ending-burn']))
    N(_card('ending_cold_1', '冷卻的餘溫', art, bg=art['bg-bar'], bgm=art['bgm-cold']))
    N(_card('ending_cold_2', '冷卻的餘溫', art, bg=art['cg-ending-cold']))
    N(_card('ending_cold_3', '冷卻的餘溫', art, bg=art['cg-ending-cold']))

    # 地圖上演出的對話卡（card(...) 叫的）也要是專案裡的卡
    have = {n['id'] for n in board['nodes']}
    for cid in L:
        if cid not in have:
            N(_card(cid, cid.replace('card_', ''), art))

    # 回憶結束回到原本那張地圖（主角回到該地圖的起點，變數與背包都還在）
    link('prologue', 'm-bar')
    link('card_mem1_enter', 'm-mem-1')
    link('card_mem1_cg', 'card_mem1_back')
    link('card_mem1_back', 'm-bar')
    link('card_mem2_enter', 'm-mem-2')
    link('card_mem2_cg', 'card_mem2_back')
    link('card_mem2_back', 'm-bar')
    link('card_mem3_enter', 'm-mem-3')
    link('card_mem3_cg', 'card_mem3_night')
    link('card_mem3_night', 'card_mem3_back')
    link('card_mem3_back', 'm-storage')
    link('card_mem4_enter', 'card_mem4_1')
    link('card_mem4_1', 'card_mem4_2')
    link('card_mem4_2', 'card_mem4_return')
    link('card_mem4_return', 'm-bedroom')
    link('card_confession', 'card_spirit')
    link('card_spirit', 'card_choice')
    cards.choice_link(board, 'card_choice', 'ending_burn_1', 0)
    cards.choice_link(board, 'card_choice', 'ending_cold_1', 1)
    for a_, b_ in [('ending_burn_1', 'ending_burn_2'), ('ending_burn_2', 'ending_burn_3'), ('ending_burn_3', 'ending_burn_4'),
                   ('ending_cold_1', 'ending_cold_2'), ('ending_cold_2', 'ending_cold_3')]:
        link(a_, b_)
