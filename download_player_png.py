#!/usr/bin/env python3
"""
Descarga SOLO el PNG del jugador de su carta base de RenderZ (no la carta completa, no fondo, no club).

URL CDN: https://cdn-p2.frzdb.net/fifamobile/images/players_18/{filename}?v=848rffjv3we
  filename en la ficha base: p20801_AS.png (Ronaldo), p158023_AS.png (Messi), p235329.png (Gibbons 42),
  p212218_AS2.png (Laporte), etc. Se extrae exacto de https://renderz.app/18/player/{fifa_id}

Modos:
  --exact (defecto): 1) GET renderz.app/18/player/{id} -> extrae players_18/xxx.png
                      2) GET CDN xxx.png -> guarda en players_png/{rarity}/xxx.png
                      Es fiel a la carta base. 2 peticiones por jugador.
  --fast: adivina CDN con cadena _AS -> _AS2 -> "" (sin sufijo) -> _AS3...
          1 peticion si acierta a la primera (OVR>=80 suele ser _AS, <80 suele ser sin sufijo).
          Puede diferir en pose para casos raros como _AS2.

Salida:
  players_png/
    Bronze Rare/  (BR0)  p235329.png ...
    Silver Rare/  (SR1)
    Gold Rare/    (GR2)
    Epic Rare/    (ER3)
    Master Rare/  (MR4)
  players_png_manifest.csv  (fifa_id, name, ovr, position, rarity, filename, cdn_url, renderz_url, size_bytes, status)
  players_png_manifest.json
  data/cache_png_downloads.jsonl (reanudable, append-only)

Uso:
  python download_player_png.py --test
  python download_player_png.py --limit 100
  python download_player_png.py --workers 12
  python download_player_png.py --fast --limit 100
  python download_player_png.py --only-ids 20801,158023
  python download_player_png.py --export-only
"""
from __future__ import annotations
import argparse, csv, json, re, random, time, unicodedata
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.error

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
PNG_DIR = BASE_DIR / "players_png"
PNG_DIR.mkdir(exist_ok=True)
CACHE = DATA_DIR / "cache_png_downloads.jsonl"
MANIFEST_CSV = BASE_DIR / "players_png_manifest.csv"
MANIFEST_JSON = BASE_DIR / "players_png_manifest.json"
DB_CSV = BASE_DIR / "fifa_mobile_18_base.csv"
DB_JSON = BASE_DIR / "fifa_mobile_18_base.json"

CDN_TEMPLATE = "https://cdn-p2.frzdb.net/fifamobile/images/players_18/{filename}?v=848rffjv3we"
RENDERZ_TEMPLATE = "https://renderz.app/18/player/{fifa_id}"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
]

_SPECIAL={"Ł":"L","ł":"l","Ø":"O","ø":"o","ß":"ss","Æ":"AE","æ":"ae","Œ":"OE","œ":"oe","Ð":"D","ð":"d","Þ":"Th","þ":"th","Đ":"D","đ":"d"}
def sanitize(s):
    if s is None: return ""
    s=str(s)
    for k,v in _SPECIAL.items(): s=s.replace(k,v)
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r"[^A-Za-z0-9 .'\-]", " ", s)
    return re.sub(r"\s+"," ",s).strip()

def fetch_bytes(url, timeout=25):
    """Devuelve (status, bytes). 404 no es excepcion."""
    last=None
    for attempt in range(3):
        try:
            req=urllib.request.Request(url, headers={"User-Agent": random.choice(USER_AGENTS)})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            body=b""
            try: body=e.read()
            except: pass
            return e.code, body
        except Exception as e:
            last=e
            time.sleep(0.5*(attempt+1)+random.random()*0.5)
    raise RuntimeError(str(last))

def fetch_text(url, timeout=25):
    status, body = fetch_bytes(url, timeout)
    try:
        return status, body.decode("utf-8", errors="replace")
    except:
        return status, ""

def log(m): print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

def load_db():
    # Preferir JSON (tipos correctos + original)
    if DB_JSON.exists():
        d=json.load(open(DB_JSON, encoding="utf-8"))
        return d["players"]
    sample=DB_CSV.read_text(encoding="utf-8", errors="replace")[:2000]
    delim=";" if sample.count(";")>sample.count(",") else ","
    rows=list(csv.DictReader(open(DB_CSV, encoding="utf-8"), delimiter=delim))
    # normalizar claves a las del JSON
    out=[]
    for r in rows:
        out.append({
            "fifa_id": int(r["fifa_id"]),
            "short_name": r.get("short_name"), "full_name": r.get("full_name"),
            "position_mobile": r.get("position_mobile"), "ovr_mobile": int(r["ovr_mobile"]) if str(r.get("ovr_mobile","")).isdigit() else None,
            "rarity": r.get("rarity"), "background_code": r.get("background_code"),
        })
    return out

def load_cache():
    cache={}
    if CACHE.exists():
        for line in CACHE.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip(): continue
            try:
                o=json.loads(line); cache[int(o["fifa_id"])]=o
            except: pass
    return cache

def download_one_exact(player):
    fifa_id=player["fifa_id"]
    renderz_url=RENDERZ_TEMPLATE.format(fifa_id=fifa_id)
    rarity=player.get("rarity") or "SinRareza"
    rarity_dir = rarity.replace(" ", "_")
    dest_dir = PNG_DIR / rarity_dir
    dest_dir.mkdir(parents=True, exist_ok=True)
    try:
        status, html = fetch_text(renderz_url)
        if status==404:
            return {"fifa_id":fifa_id,"status":"not_found_renderz","renderz_url":renderz_url}
        if status!=200:
            return {"fifa_id":fifa_id,"status":"http_error_renderz","http_status":status,"renderz_url":renderz_url}
        m=re.search(r"players_18/([^\"']+\.png)", html)
        if not m:
            return {"fifa_id":fifa_id,"status":"parse_error_no_png","renderz_url":renderz_url}
        filename=m.group(1)
        # Fallback: si el filename de la pagina da 404 en CDN (casos p*_X.png o p*.png sin AS),
        # probar variantes _AS, _AS2, sin sufijo, _AS3...
        candidates=[filename, f"p{fifa_id}.png", f"p{fifa_id}_AS.png", f"p{fifa_id}_AS2.png", f"p{fifa_id}_AS3.png"]
        # deduplicar manteniendo orden
        seen=set(); uniq=[]
        for c in candidates:
            if c not in seen: seen.add(c); uniq.append(c)
        last_status=None
        for cand in uniq:
            cdn_url=CDN_TEMPLATE.format(filename=cand)
            dest=dest_dir/cand
            if dest.exists() and dest.stat().st_size>0:
                return {"fifa_id":fifa_id,"status":"ok_cached_file","filename":cand,"cdn_url":cdn_url,"renderz_url":renderz_url,"dest":str(dest.relative_to(BASE_DIR)),"size_bytes":dest.stat().st_size,"exact_filename_in_page":filename}
            status2, data = fetch_bytes(cdn_url)
            last_status=status2
            if status2==200 and data[:8]==b'\x89PNG\r\n\x1a\n':
                dest.write_bytes(data)
                return {"fifa_id":fifa_id,"status":"ok","filename":cand,"cdn_url":cdn_url,"renderz_url":renderz_url,"dest":str(dest.relative_to(BASE_DIR)),"size_bytes":len(data),"exact_filename_in_page":filename}
        return {"fifa_id":fifa_id,"status":"cdn_not_found","filename":filename,"cdn_url":CDN_TEMPLATE.format(filename=filename),"renderz_url":renderz_url,"http_status":last_status,"tried":uniq}
    except Exception as e:
        return {"fifa_id":fifa_id,"status":"error","error":str(e),"renderz_url":renderz_url}

def download_one_fast(player):
    fifa_id=player["fifa_id"]
    ovr=player.get("ovr_mobile") or 0
    rarity=player.get("rarity") or "SinRareza"
    rarity_dir=rarity.replace(" ", "_")
    dest_dir=PNG_DIR/rarity_dir
    dest_dir.mkdir(parents=True, exist_ok=True)
    # orden segun OVR: >=80 _AS primero, <80 sin sufijo primero
    if ovr>=80:
        candidates=[f"p{fifa_id}_AS.png", f"p{fifa_id}_AS2.png", f"p{fifa_id}.png", f"p{fifa_id}_AS3.png"]
    else:
        candidates=[f"p{fifa_id}.png", f"p{fifa_id}_AS.png", f"p{fifa_id}_AS2.png"]
    renderz_url=RENDERZ_TEMPLATE.format(fifa_id=fifa_id)
    for filename in candidates:
        cdn_url=CDN_TEMPLATE.format(filename=filename)
        dest=dest_dir/filename
        if dest.exists() and dest.stat().st_size>0:
            return {"fifa_id":fifa_id,"status":"ok_cached_file","filename":filename,"cdn_url":cdn_url,"renderz_url":renderz_url,"dest":str(dest.relative_to(BASE_DIR)),"size_bytes":dest.stat().st_size,"mode":"fast"}
        try:
            status, data=fetch_bytes(cdn_url)
        except Exception as e:
            continue
        if status==200 and data[:8]==b'\x89PNG\r\n\x1a\n':
            dest.write_bytes(data)
            return {"fifa_id":fifa_id,"status":"ok","filename":filename,"cdn_url":cdn_url,"renderz_url":renderz_url,"dest":str(dest.relative_to(BASE_DIR)),"size_bytes":len(data),"mode":"fast"}
    return {"fifa_id":fifa_id,"status":"not_found_cdn","renderz_url":renderz_url,"mode":"fast","tried":candidates}

def export_manifest(db_players, cache):
    rows=[]
    for p in sorted(db_players, key=lambda x: (-(x.get("ovr_mobile") or 0), x["fifa_id"])):
        c=cache.get(int(p["fifa_id"]), {})
        rows.append({
            "fifa_id": p["fifa_id"],
            "name": sanitize(p.get("full_name") or p.get("short_name") or ""),
            "ovr": p.get("ovr_mobile"),
            "position": p.get("position_mobile"),
            "rarity": sanitize(p.get("rarity") or ""),
            "filename": c.get("filename",""),
            "cdn_url": c.get("cdn_url",""),
            "renderz_url": c.get("renderz_url", RENDERZ_TEMPLATE.format(fifa_id=p["fifa_id"])),
            "dest": c.get("dest",""),
            "size_bytes": c.get("size_bytes",""),
            "status": c.get("status","pending"),
        })
    with MANIFEST_CSV.open("w", newline="", encoding="utf-8") as fh:
        w=csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(rows)
    MANIFEST_JSON.write_text(json.dumps({"generated_at":datetime.now(timezone.utc).isoformat(),"count":len(rows),"ok":sum(1 for r in rows if r["status"] in ("ok","ok_cached_file")),"players":rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    ok=sum(1 for r in rows if r["status"] in ("ok","ok_cached_file"))
    total_bytes=sum(int(r["size_bytes"]) for r in rows if str(r["size_bytes"]).isdigit())
    log(f"Manifest: {MANIFEST_CSV.name} ok={ok}/{len(rows)} bytes={total_bytes} ({total_bytes/1024/1024:.1f} MB)")
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--fast", action="store_true", help="Adivina CDN sin pasar por RenderZ (mas rapido, pose puede diferir en casos _AS2)")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--export-only", action="store_true")
    ap.add_argument("--only-ids", type=str, default=None)
    args=ap.parse_args()
    if args.test: args.limit=20

    db_players=load_db()
    log(f"DB base: {len(db_players)} jugadores")
    if args.only_ids:
        wanted={int(x.strip()) for x in args.only_ids.split(",") if x.strip()}
        db_players=[p for p in db_players if int(p["fifa_id"]) in wanted]
    if args.limit:
        db_players=db_players[:args.limit]

    cache={} if args.refresh else load_cache()
    if args.export_only:
        export_manifest(load_db(), cache)
        return

    targets=[p for p in db_players if int(p["fifa_id"]) not in cache]
    log(f"Cache {len(cache)}, pendientes {len(targets)} modo={'fast' if args.fast else 'exact'}")
    fn = download_one_fast if args.fast else download_one_exact
    done=ok=0
    if targets:
        with CACHE.open("a", encoding="utf-8") as fh:
            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                futs={ex.submit(fn,p):p for p in targets}
                for fut in as_completed(futs):
                    res=fut.result()
                    cache[int(res["fifa_id"])]=res
                    fh.write(json.dumps(res, ensure_ascii=False)+"\n"); fh.flush()
                    done+=1
                    if res.get("status") in ("ok","ok_cached_file"): ok+=1
                    if done%100==0 or done==len(targets):
                        log(f"  PNG {done}/{len(targets)} ok={ok}")
    # Manifiesto siempre completo (13.885) aunque esta ejecucion sea --limit/--only-ids
    export_manifest(load_db(), cache)

if __name__=="__main__":
    main()
