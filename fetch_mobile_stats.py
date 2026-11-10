#!/usr/bin/env python3
"""
Fetch REAL FIFA Mobile 18 engine stats for every card in the three databases
from RenderZ's __data.json endpoints:
    https://renderz.app/18/player/{id}/__data.json  -> {"type":"redirect","location":"/18/player/<id>-<slug>"}
    https://renderz.app/{location}/__data.json      -> {"type":"data","nodes":[...]}

Output: data/cache_mobile_stats.jsonl  (one line per fifa_id, resumable)
Fields: fifa_id, status, slug, card_name, first_name, last_name, rating, position,
        foot, weak_foot_rating, skill_boost_code, avg1..avg6, stats{24 keys}, total_stats,
        boosted_stats
"""
import json, sys, time, urllib.request, urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = Path(__file__).resolve().parent
CACHE = BASE / "data" / "cache_mobile_stats.jsonl"

def collect_ids():
    ids = set()
    # base CSV (all OK cards)
    with open(BASE / "fifa_mobile_18_base.csv", encoding="utf-8") as fh:
        header = fh.readline()
        delim = ";" if header.count(";") > header.count(",") else ","
        for line in fh:
            try:
                fid = int(line.split(delim, 1)[0])
                ids.add(fid)
            except Exception:
                pass
    # eventos fetch cache (all 6,571 captured cards)
    ev = BASE / "data" / "cache_eventos.jsonl"
    if ev.exists():
        for line in open(ev, encoding="utf-8", errors="replace"):
            try:
                o = json.loads(line)
                ids.add(int(o["fifa_id"]))
            except Exception:
                pass
    # iconos list (69)
    ic = BASE / "iconos_list.json"
    if ic.exists():
        for r in json.loads(ic.read_text(encoding="utf-8")):
            ids.add(int(r["fifa_id"]))
    return sorted(ids)

def get_json(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    try:
        body = urllib.request.urlopen(req, timeout=timeout).read()
        return json.loads(body)
    except urllib.error.HTTPError as e:
        return {"type": "http_error", "code": e.code}
    except Exception:
        return {"type": "net_error"}

def resolve_player(payload):
    nodes = payload.get("nodes", [])
    for node in nodes:
        if isinstance(node, dict) and node.get("type") == "data" and isinstance(node.get("data"), list):
            if node["data"] and isinstance(node["data"][0], dict) and "player" in node["data"][0]:
                return node["data"]
    # fallback: any data node with player
    for node in nodes:
        if isinstance(node, dict) and node.get("type") == "data" and isinstance(node.get("data"), list):
            for entry in node["data"]:
                if isinstance(entry, dict) and "player" in entry:
                    return node["data"]
    return None

sys.path.insert(0, str(BASE))
from devalue import unflatten

def extract(fid, node_data):
    obj = unflatten(node_data)
    p = obj.get("player") if isinstance(obj, dict) else None
    if not isinstance(p, dict):
        return None
    s = p.get("stats", {})
    avg = p.get("avgStats", {})
    return {
        "fifa_id": fid,
        "slug": (p.get("images", {}).get("playerCardImage") or "").rsplit("/", 1)[-1],
        "card_name": p.get("cardName"),
        "first_name": p.get("firstName"),
        "last_name": p.get("lastName"),
        "common_name": p.get("commonName"),
        "rating": p.get("rating"),
        "position": p.get("position"),
        "foot": p.get("foot"),
        "weak_foot_rating": p.get("weakFootRating"),
        "source": p.get("source"),
        "height": p.get("height"),
        "weight": p.get("weight"),
        "club_name": p.get("clubName"),
        "nation_name": p.get("nationName"),
        "skill_boost_code": p.get("skillBoost"),
        "avg1": avg.get("avg1"), "avg2": avg.get("avg2"), "avg3": avg.get("avg3"),
        "avg4": avg.get("avg4"), "avg5": avg.get("avg5"), "avg6": avg.get("avg6"),
        "stats": dict(s),
        "total_stats": p.get("totalStats"),
        "boosted_stats": p.get("boostedStats", {}),
        "status": "ok",
    }

def fetch_one(fid):
    j0 = get_json(f"https://renderz.app/18/player/{fid}/__data.json")
    if j0.get("type") == "redirect":
        loc = j0["location"]
        j1 = get_json("https://renderz.app" + loc + "/__data.json")
    elif j0.get("type") == "data":
        j1 = j0
    else:
        return {"fifa_id": fid, "status": f"error_{j0.get('type')}"}

    if j1.get("type") != "data":
        return {"fifa_id": fid, "status": f"error_{j1.get('type')}"}
    node_data = resolve_player(j1)
    if node_data is None:
        return {"fifa_id": fid, "status": "error_no_player"}
    rec = extract(fid, node_data)
    return rec if rec else {"fifa_id": fid, "status": "error_extract"}

def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    ids = collect_ids()
    if limit:
        ids = ids[:limit]
    done = {}
    if CACHE.exists():
        for line in open(CACHE, encoding="utf-8", errors="replace"):
            try:
                o = json.loads(line)
                done[int(o["fifa_id"])] = True
            except Exception:
                pass
    todo = [i for i in ids if i not in done]
    print(f"total ids {len(ids)} | already cached {len(done)} | todo {len(todo)}", flush=True)
    if not todo:
        print("nothing to do")
        return
    CACHE.parent.mkdir(exist_ok=True)
    ok = err = 0
    with open(CACHE, "a", encoding="utf-8") as fh:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(fetch_one, fid): fid for fid in todo}
            for n, fut in enumerate(as_completed(futs), 1):
                rec = fut.result()
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
                if rec["status"] == "ok":
                    ok += 1
                else:
                    err += 1
                if n % 200 == 0 or n == len(todo):
                    print(f"  mobile stats {n}/{len(todo)} ok={ok} err={err}", flush=True)
    print(f"DONE ok={ok} err={err} cache={CACHE}")

if __name__ == "__main__":
    main()
