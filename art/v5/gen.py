# 呼叫自架的 codex-image 服務（環境變數 CODEX_IMAGE_BASE、CODEX_IMAGE_KEY）：python3 tools/gen.py <輸出.png> <提示詞檔> [參考圖...]
import sys, os, json, base64, urllib.request
out, pf, refs = sys.argv[1], sys.argv[2], sys.argv[3:]
# ponytail: 檔案鎖讓兩條隊伍不畫同一張；已存在或有人在畫就跳過。要重畫請先刪掉輸出檔與 .lock
if os.path.exists(out) or os.path.exists(out + ".lock"):
    print("skip", out); sys.exit(0)
open(out + ".lock", "w").close()
# 走全機共用的送圖排隊（~/.cache/cg_jobs：interval 秒一張、同時最多 max_inflight 張；跟其他作品的產線共用，照 buchan/cg_jobs.py 的 _queue）
import fcntl, time, uuid
Q = os.path.expanduser("~/.cache/cg_jobs"); os.makedirs(Q, exist_ok=True)
def _live():
    try: live = json.load(open(os.path.join(Q, "inflight.json")))
    except (OSError, ValueError): live = {}
    return {k: t for k, t in live.items() if os.path.exists(f"/proc/{k.split('-')[0]}") and time.time() - t < 1200}
def _rd(name, d):
    try: return float(open(os.path.join(Q, name)).read())
    except (OSError, ValueError): return d
tag = f"{os.getpid()}-{uuid.uuid4().hex}"
while True:
    with open(os.path.join(Q, "lock"), "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX); live = _live()
        if len(live) < _rd("max_inflight", 999):
            w = _rd("last", 0) + _rd("interval", 30) - time.time()
            if w > 0: time.sleep(w)
            open(os.path.join(Q, "last"), "w").write(str(time.time()))
            live[tag] = time.time(); json.dump(live, open(os.path.join(Q, "inflight.json"), "w")); break
    time.sleep(10)
def _done():
    with open(os.path.join(Q, "lock"), "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX); live = _live(); live.pop(tag, None); json.dump(live, open(os.path.join(Q, "inflight.json"), "w"))
body = {"prompt": open(pf, encoding="utf-8").read(), "size": os.environ.get("GEN_SIZE", "1536x1024")}   # 直式：GEN_SIZE=1024x1536
if refs: body["reference_images_base64"] = [base64.b64encode(open(r, "rb").read()).decode() for r in refs]
req = urllib.request.Request((os.environ.get("CODEX_IMAGE_BASE") or open(os.path.expanduser("~/.config/codex-image/base")).read().strip()).rstrip("/") + "/v1/images/generate",
    data=json.dumps(body).encode(), headers={"Content-Type": "application/json",
    "Authorization": "Bearer " + os.environ["CODEX_IMAGE_KEY"]})
try: r = json.load(urllib.request.urlopen(req, timeout=900))
finally: _done()
img = r["images"][0]
data = base64.b64decode(img["b64_json"]) if img.get("b64_json") else urllib.request.urlopen(img["url"]).read()
open(out, "wb").write(data); os.remove(out + ".lock"); print("ok", out, len(data))
