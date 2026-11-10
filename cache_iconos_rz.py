import json, urllib.request, urllib.error, re, time, random, unicodedata
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
BASE = Path(__file__).resolve().parent
CACHE = BASE/"data"/"cache_iconos_rz.jsonl"
CACHE.parent.mkdir(exist_ok=True)
def fetch(url):
    for attempt in range(3):
        try:
            req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"})
            with urllib.request.urlopen(req,timeout=30) as r:
                return r.status, r.read().decode("utf-8","replace")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception as e:
            if attempt==2: return 0, ""
            time.sleep(0.5*(attempt+1))
def parse(html, fifa_id):
    m=re.search(r"<h1[^>]*>([^<]+?)\s+(\d+)\s+OVR\s+in\s+FIFA Mobile 18</h1>", html)
    name=""; ovr=None
    if m:
        name=m.group(1).strip(); ovr=int(m.group(2))
    bg=(re.search(r"backgrounds_18/backgrounds_([A-Za-z0-9_]+)\.png", html) or [None,""])[1]
    bgwc=(re.search(r"backgrounds_18(?:wc)?/backgrounds_([A-Za-z0-9_]+)\.png", html) or [None,""])[1]
    bg2=(re.search(r"backgrounds_18/backgrounds_WC_ICON_([EM])\.png", html) or [None,""])[1]
    if not bg: bg=bg2 or ""
    cw=(re.search(r"clubLogos_18/(\d+)\.png", html) or [None,None])[1]
    mclub=re.search(r'clubLogos_18/(\d+)\.png', html)
    club=int(mclub.group(1)) if mclub else None
    mshot=re.search(r"players_(\d+)/p([^\"']+)\.png", html)
    # imagen de jugador: puede ser players_18/p5419_IC1.png o players_18wc/p570.png
    pl=re.search(r"(players_18(?:wc)?/p[^\"']+\.png)", html)
    plpic=pl.group(1) if pl else None
    picovr=re.search(r"players_18/(p\w+\.png)", html)
    pos=(re.search(r'class="position[^"]*"[^>]*>([^<]+)</div>', html) or [None,""])[1]
    short=(re.search(r'class="name[^"]*"[^>]*>([^<]+)</div>', html) or [None,""])[1]
    title=(re.search(r"<title>([^|<]+)", html) or [None,""])[1]
    mname=re.search(r"<meta name=\"og:title\" content=\"([^|<]+)\"", html)
    ogtitle=mname.group(1).strip() if mname else None
    maction=re.search(r"players_18/(p[\w\.]+\.png)", html)
    action_shot=maction.group(1) if maction else None
    variant=None
    if action_shot:
        m2=re.search(r"_([A-Za-z_]+)\.png$", action_shot)
        if m2: variant=m2.group(1)
    return {
        "fifa_id":fifa_id, "ok": bool(m), "name":name, "ovr":ovr,
        "background_code":bg, "club_id":club, "position_mobile":pos.strip(), "short_name":short.strip(),
        "title":title, "og_title":ogtitle, "action_shot":action_shot, "action_variant":variant, "player_image_url":plpic,
    }
def main():
    rows=json.loads((BASE/"iconos_list.json").read_text(encoding="utf-8"))
    cache={}
    if CACHE.exists():
        for line in open(CACHE,encoding="utf-8",errors="replace"):
            try: o=json.loads(line); cache[o["fifa_id"]]=o
            except: pass
    todo=[r["fifa_id"] for r in rows if r["fifa_id"] not in cache]
    print("todo", len(todo))
    if not todo: return
    with open(CACHE,"a",encoding="utf-8") as fh:
        def one(fid):
            status,html=fetch(f"https://renderz.app/18/player/{fid}")
            res=parse(html,fid)
            res["status"]=status
            return res
        with ThreadPoolExecutor(max_workers=8) as ex:
            futs={ex.submit(one,fid):fid for fid in todo}
            for fut in as_completed(futs):
                res=fut.result()
                cache[res["fifa_id"]]=res
                fh.write(json.dumps(res,ensure_ascii=False)+"\n"); fh.flush()
                print(res["fifa_id"], res.get("ovr"), res.get("position_mobile"), res.get("background_code"), res.get("club_id"), flush=True)
    print("cache ok", len(cache))
if __name__=="__main__":
    main()
