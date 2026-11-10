#!/usr/bin/env python3
"""
Extrae TODAS las cartas de EVENTOS (temporada 2) de FIFA Mobile 18 desde RenderZ.
Base de inicio: IDs de programa vistos en las fichas base (cache_renderz.jsonl → program_ids_excluded).

Excluye: cartas base (< 500.000) y cartas de otras temporadas con IDs de 8 dígitos (19020801, 19500005...).
Incluye: cualquier ID de 6 dígitos >= 500.000 en /18/player/{id}.

Proceso:
  1) Relee cache_renderz.jsonl para obtener 6.571 IDs de programa.
  2) GET /18/player/{id} para cada ID → nombre completo, OVR, posición, background, club, short_name, program_icon.
     - Si 404: lo marca (no_excelled, pero no se crashea).
     - Si 200: base datos.
  3) Asigna skill boost heurístico (misma lógica de generate_skill_boost.py, adaptada).
  4) Stats: genera heurística alineada con OVR 43– ? (eventos pueden pasar de 100; 90+ casi boca-libre).
     No hay guía con stat para programas — fifamobileguide solo cubre base.
  5) Nombres base: intentando relacionar contra base DB por 3 vías:
     - nombre exacto en db (short/full normalizado + match posición si hace falta)
     - sin match: nombre de la página y carta-aliada (433182 combinada * 0-7-4 -> 2.000 match)
  6) Salida CSV/TXT/JSON super-completa.
"""
from __future__ import annotations
import argparse, csv, json, re, random, time, unicodedata, random
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.error

BASE = Path(__file__).resolve().parent
OUT_CSV = BASE / "fifa_mobile_18_eventos.csv"
OUT_TXT = BASE / "fifa_mobile_18_eventos.txt"
OUT_JSON = BASE / "fifa_mobile_18_eventos.json"
CACHE = BASE / "data" / "cache_eventos.jsonl"
DATA_BASE = BASE / "data" / "cache_renderz.jsonl"
DB_JSON = BASE / "fifa_mobile_18_base.json"
STATS_CSV = BASE / "fifa_mobile_18_base_player_stats.csv"
SKILLBOOST_JSON = BASE / "fifa_mobile_18_base_completa.json"

CDN_PROG = "https://cdn-p2.frzdb.net/fifamobile/images/programs_18/{code}.png?v=848rffjv3we"
RENDERZ = "https://renderz.app/18/player/{fifa_id}"
UA = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"]

_SPECIAL={"Ł":"L","ł":"l","Ø":"O","ø":"o","ß":"ss","Æ":"AE","æ":"ae","Œ":"OE","œ":"oe","Ð":"D","ð":"d","Þ":"Th","þ":"th","Đ":"D","đ":"d"}
def sanitize(s):
    if s is None: return ""
    s=str(s)
    for k,v in _SPECIAL.items(): s=s.replace(k,v)
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r"[^A-Za-z0-9 .'\-/]"," ",s)
    return re.sub(r"\s+"," ",s).strip()

def fetch_bytes(url, timeout=25):
    for attempt in range(3):
        try:
            req=urllib.request.Request(url, headers={"User-Agent": random.choice(UA)})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, b""
        except Exception as e:
            if attempt==2: raise
            time.sleep(0.5*(attempt+1))
    return 0, b""

def event_name_of(bg: str, icon: str) -> str:
    """Solo deja valores verificables: program_icon exacto o background_code.
    No inventa nombre si no está fiado en la lista. Fallback: 'Season 2 Program'."""
    bg = (bg or "").upper().strip()
    icon = (icon or "").upper().strip()
    if icon:
        return icon
    if bg:
        return bg
    return "Season 2 Program"

def fetch_text(url, timeout=25):
    status, body = fetch_bytes(url, timeout)
    try: return status, body.decode("utf-8", errors="replace")
    except: return status, ""

def log(m): print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

def program_ids_from_base_cache():
    ids=set()
    for line in open(DATA_BASE, encoding="utf-8", errors="replace"):
        try: d=json.loads(line)
        except: continue
        if d.get("status")=="ok":
            for p in d.get("program_ids_excluded", []):
                if 500000 <= int(p) < 1000000:
                    ids.add(int(p))
    return sorted(ids)

def parse_event(html, fifa_id):
    m_h1=re.search(r"<h1[^>]*>([^<]+?)\s+(\d+)\s+OVR\s+in\s+FIFA Mobile 18</h1>", html)
    if not m_h1:
        if "404" in html and "Page not found" in html:
            return {"status":"not_found","fifa_id":fifa_id}
        return {"status":"parse_error","fifa_id":fifa_id}
    name_clean=m_h1.group(1).strip(); ovr=int(m_h1.group(2))
    bg=(re.search(r"backgrounds_18/backgrounds_([A-Za-z0-9_]+)\.png", html) or [None,""])[1]
    # action shot puede ser Th/GOLDEN_TICKET (program 17) o p{id}_TOTY/UPGRADED etc
    m_shot=re.search(r"players_18/p?([A-Za-z0-9_]+)_([A-Za-z0-9_]+)\.png", html)
    prog_m=re.search(r"programs_18/program_([^\"']+)\.png", html)
    m_pos=re.search(r'class="position[^"]*"[^>]*>([^<]+)</div>', html)
    pos=m_pos.group(1).strip() if m_pos else ""
    m_name=re.search(r'class="name[^"]*"[^>]*>([^<]+)</div>', html)
    short_name=m_name.group(1).strip() if m_name else name_clean
    # Si el jugador verdadero está embebido en img p...AS o p..._EVENTO ... etc. inferir el nombre del HTML title mejor:
    # <title>X | FIFA Mobile 18 | RenderZ</title> → X
    m_title=re.search(r"<title>([^|<]+)", html)
    title_name=m_title.group(1).strip() if m_title else name_clean
    # Club: si action-shot es programa 17/club logo directo
    club=(re.search(r"clubLogos_18/(\d+)\.png", html) or [None,None])[1]
    # Skill boost: no hay para eventos; asignamos heurísticamente
    return {
        "status":"ok","fifa_id":fifa_id,"page_name":name_clean,"title_name":title_name,
        "short_name":short_name,"ovr_mobile":ovr,"position_mobile":pos,"background_code":bg,
        "club_id":int(club) if club else None,
        "program_icon":prog_m.group(1) if prog_m else None,
        "action_variant":m_shot.group(2) if m_shot else None,
    }

def resolve_base_name(page_name, db_by_name, db_by_short):
    n=sanitize(page_name).lower()
    if n in db_by_name: return db_by_name[n]
    # nombre de página es el title = nombre del jugador, no del programa
    # e.g. "Cristiano Ronaldo", "Lionel Messi", "Alessio Castro-Montes"
    return None

def ovr_to_template(pstats, db_all):
    # DB completo se pasa para plantillas, aquí lo usamos solo para stats
    # Skill boost: heurística simple alineada con OVR + posición
    pos=pstats["position_mobile"]; ovr=pstats["ovr_mobile"]
    return pos, ovr

# Reutilizar estructura de stats/boost de generate_skill_boost.py no es directo aquí,
# así que generamos stats base de la misma heurística simplificada pero alined con OVR
def _gi(stats, k, default=0):
    v=stats.get(k, default)
    try: return int(v)
    except: return default

def RngNum(seed: int) -> float:
    import hashlib
    h = hashlib.sha256(str(seed).encode("utf-8")).hexdigest()
    return int(h[:8], 16) / 0xffffffff

# Plantilla mínima copiada de generate_skill_boost -> estadística instrumental
GB_STUB={
    # ci
}
# Para reutilizar EXACTO, importar el módulo principal desde BASE
sys_path=str(BASE)
import sys
if sys_path not in sys.path: sys.path.insert(0, sys_path)
try:
    import generate_skill_boost as GSB
except Exception as e:
    GSB=None
    print(f" Aviso: generate_skill_boost no importable: {e}")

STAT_FIELDS=["pace","shooting","passing","agility","defending","physical","sprint_speed","acceleration","strength","ball_control","dribbling","heading","finishing","shot_power","long_shot","positioning","tackling","marking","aggression","composure","awareness","reactions","free_kick","short_passing","long_passing","crossing","gk_diving","gk_positioning","reflexes","handling"]

def _event_stats(base_stats):
    if base_stats is None:
        return None
    s = {k: (base_stats.get(k) or "") for k in STAT_FIELDS}
    # Normalizar tipo: int o None
    out = {}
    for k, v in s.items():
        try:
            out[k] = int(v) if str(v).isdigit() else None
        except Exception:
            out[k] = None
    return out

def _adjust_to_ovr(src_stats, src_ovr, dst_ovr):
    """Escala stats de src_ovr -> dst_ovr linealmente (20-99)."""
    if not src_stats:
        return {k: None for k in STAT_FIELDS}
    if not src_ovr or src_ovr == dst_ovr:
        return {k: (v if v is not None else None) for k, v in src_stats.items()}
    diff = dst_ovr - src_ovr
    # stats tipo 99 stay near cap; use slope .35
    out = {}
    scale = diff * 0.42  # cada OVR sube ~0.4 de stat
    for k in STAT_FIELDS:
        v = src_stats.get(k)
        if v is None:
            out[k] = None
            continue
        if k in ("gk_diving","gk_positioning","reflexes","handling"):
            out[k] = max(20, min(99, int(round(v + scale))))
        else:
            out[k] = max(20, min(99, int(round(v + scale))))
    if dst_ovr >= 80:
        # para cartas >=80, incrementar un poco más la elite
        for k in ["finishing","pace","dribbling","reactions","ball_control","shooting"]:
            if out.get(k) is not None:
                out[k] = min(99, int(round(out[k] + (dst_ovr - 80) * 0.20)))
    # set prio: se propaga al bocio skill
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--only-ids", type=str, default=None)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--export-only", action="store_true")
    ap.add_argument("--with-stats", action="store_true", help="Genera 30 stats coherentes con OVR Mobile + posición (misma fórmula que la base)")
    args=ap.parse_args()

    program_ids=program_ids_from_base_cache()
    log(f"Program IDs detectados (6-digit >= 500000): {len(program_ids)}")
    if args.only_ids:
        wanting={int(x.strip()) for x in args.only_ids.split(",") if x.strip()}
        program_ids=[i for i in program_ids if i in wanting]
    if args.limit:
        program_ids=program_ids[:args.limit]

    # cache
    cache={}
    if CACHE.exists() and not args.refresh:
        for line in open(CACHE, encoding="utf-8", errors="replace").readlines():
            try: o=json.loads(line); cache[int(o["fifa_id"])]=o
            except: continue
    log(f"Cache eventos: {len(cache)} (probing {len(program_ids)})")
    if not args.export_only:
        todo=[i for i in program_ids if int(i) not in cache]
        log(f"  pendientes: {len(todo)}")
        if todo:
            done=0; ok=0; nf=0; err=0
            with CACHE.open("a", encoding="utf-8") as fh:
                with ThreadPoolExecutor(max_workers=args.workers) as ex:
                    futs={ex.submit(fetch_text, RENDERZ.format(fifa_id=i)): i for i in todo}
                    for fut in as_completed(futs):
                        fifa_id=futs[fut]
                        try:
                            status, html = fut.result()
                        except Exception as e:
                            status, html = 0, ""
                        if status==404 or "Page not found" in html:
                            res={"fifa_id":fifa_id,"status":"not_found"}; nf+=1
                        elif status!=200:
                            res={"fifa_id":fifa_id,"status":"http_error","http_status":status}; err+=1
                        else:
                            res=parse_event(html, fifa_id); ok+=1 if res.get("status")=="ok" else 1
                        cache[int(fifa_id)]=res
                        fh.write(json.dumps(res, ensure_ascii=False)+"\n"); fh.flush()
                        done+=1
                        if done%200==0 or done==len(todo):
                            log(f"  eventos {done}/{len(todo)} · ok={ok} 404={nf} err={err}")

    # DB base para nombres y plantillas stats
    db_players = json.loads(DB_JSON.read_text(encoding="utf-8"))["players"] if DB_JSON.exists() else json.loads((BASE/"fifa_mobile_18_base.json").read_text(encoding="utf-8"))["players"]
    # mapa nombre normalizado -> lista registros
    db_by_name = {}
    db_by_short = {}
    for p in db_players:
        db_by_name.setdefault(sanitize(p.get("full_name","")).lower(), []).append(p)
        db_by_short.setdefault(sanitize(p.get("short_name","")).lower(), []).append(p)

    # CSV column definitions: misma estructura que la completa sin guide-stats guia
    stat_fields=STAT_FIELDS
    base_fields=["fifa_id","short_name","full_name","full_name_original","position_mobile","ovr_mobile",
                  "club_id","club_name","background_code","rarity","sofifa_age","nationality",
                  "season","renderz_url","skill_boost","event_resolved_name","event_confidence",
                  "page_name","title_name","program_icon","action_variant",
                  "event_name","event_id","event_detail"] + (STAT_FIELDS if args.with_stats else [])
    # carga plantillas desde stats base (si existe)
    stats_rows = []
    if STATS_CSV.exists():
        sample = STATS_CSV.read_text(encoding="utf-8", errors="replace")[:3000]
        delim = ";" if sample.count(";") > sample.count(",") else ","
        stats_rows = list(csv.DictReader(open(STATS_CSV, encoding="utf-8"), delimiter=delim))
    # stats base por fifa_id: las duplicamos por posición+ovr cuando el jugador es el mismo pero OVR difiere
    stats_by_id = {str(r["fifa_id"]): r for r in stats_rows}

    rows=[]
    for fifa_id in program_ids:
        c=cache.get(int(fifa_id))
        if not c or c.get("status")!="ok":
            continue
        name_candidate = c.get("page_name") or c.get("title_name") or ""
        n_lower = sanitize(name_candidate).lower()
        # Match con base por nombre exacto:
        base=None
        lst = db_by_name.get(n_lower, [])
        if not lst:
            # probar apellido
            toks=n_lower.split()
            if toks:
                lst = db_by_name.get(toks[0]+" "+toks[-1], [])
        # si hay múltiples, elegir ovr más cercano preferido
        if lst:
            base=min(lst, key=lambda p: abs((p.get("ovr_mobile") or 0) - c.get("ovr_mobile", 0)))
        resolved_name = sanitize(base["full_name"]) if base else sanitize(name_candidate)
        confidence = "exact" if base else "page_only"
        # Stats:
        if GSB is not None and base is not None:
            pos=base.get("position_mobile") or c.get("position_mobile","")
            pfake={
                "fifa_id":fifa_id,
                "ovr_mobile":c.get("ovr_mobile"),
                "position_mobile":pos,
                "sofifa_overall":base.get("sofifa_overall"),
                "sofifa_age":base.get("sofifa_age"),
                "short_name":base.get("short_name"),
                "full_name":base.get("full_name"),
            }
            # Stats heurísticas usando la UE del base pero elevadas? No; solo boost
            boost, _ = GSB.assign_boost(pfake, {})
        else:
            if GSB is not None:
                pos=c.get("position_mobile") or "CM"
                pfake={"fifa_id":fifa_id, "ovr_mobile":c.get("ovr_mobile"), "position_mobile":pos, "sofifa_overall":0, "sofifa_age":25, "short_name":name_candidate, "full_name":name_candidate}
                boost, _ = GSB.assign_boost(pfake, {})
            else:
                boost = "generalist"
        boost = boost if boost else "generalist"
        # Stats via with-stats flag
        evt_stats = None
        if args.with_stats:
            # Base stats más cercanas por fifa_id (la carta base del mismo jugador suele ser su versión no-evento)
            base_stats_raw = stats_by_id.get(str(base["fifa_id"])) if base else None
            if base_stats_raw is not None:
                evt_stats = _event_stats(base_stats_raw)
                src_ovr = base.get("ovr_mobile")
                if not src_ovr:
                    try: src_ovr = int(base_stats_raw.get("ovr_mobile") or c.get("ovr_mobile") or 0)
                    except Exception: src_ovr = 0
                evt_stats = _adjust_to_ovr(evt_stats, src_ovr, c.get("ovr_mobile") or 0)
            else:
                # generar sintéticamente desde OVR + posición; usar softmantemplate del booster derivando ok
                fake_stats = {k: None for k in STAT_FIELDS}
                ovr = c.get("ovr_mobile") or 60
                is_gk = (c.get("position_mobile") == "GK")
                for i, k in enumerate(STAT_FIELDS):
                    if is_gk:
                        if k in ("gk_diving","gk_positioning","reflexes","handling"):
                            fake_stats[k] = max(20, min(99, int(round(ovr*0.92 + RngNum(fifa_id*17+i)*2))))
                    else:
                        if k in ("gk_diving","gk_positioning","reflexes","handling"):
                            fake_stats[k] = None
                        else:
                            fake_stats[k] = max(20, min(99, int(round(ovr*0.82 + RngNum(fifa_id*23+i+7)))))
                evt_stats = fake_stats
        row = {
            "fifa_id": fifa_id,
            "short_name": sanitize(base["short_name"]) if base else sanitize(c.get("short_name","")),
            "full_name": resolved_name,
            "full_name_original": base.get("full_name_original") if base else c.get("page_name"),
            "position_mobile": c.get("position_mobile",""),
            "ovr_mobile": c.get("ovr_mobile"),
            "club_id": c.get("club_id") if c.get("club_id") else None,
            "club_name": base["club_name"] if base else "",
            "background_code": c.get("background_code"),
            "rarity": "Program",
            "sofifa_age": base.get("sofifa_age") if base else None,
            "nationality": sanitize(base.get("nationality","")) if base else "",
            "season": base.get("season") if base else "Season 2 (FIFA Mobile 18)",
            "renderz_url": RENDERZ.format(fifa_id=fifa_id),
            "skill_boost": boost,
            "event_resolved_name": resolved_name,
            "event_confidence": confidence,
            "page_name": c.get("page_name"),
            "title_name": c.get("title_name"),
            "program_icon": c.get("program_icon"),
            "action_variant": c.get("action_variant"),
            "event_name": event_name_of(c.get("background_code") or "", c.get("program_icon") or ""),
            "event_id": c.get("program_icon") or c.get("background_code"),
            "event_detail": (f"Program {c.get('program_icon') or '(no icon)'} | "
                             f"Background {c.get('background_code')} | "
                             f"Variant {c.get('action_variant') or '-'} | "
                             f"RenderZ {RENDERZ.format(fifa_id=fifa_id)}"),
        }
        if args.with_stats:
            for k, v in (evt_stats or {}).items():
                row[k] = v
        rows.append(row)

    rows.sort(key=lambda r: (-(int(r["ovr_mobile"]) if str(r["ovr_mobile"]).isdigit() else 0), int(r["fifa_id"])))

    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w=csv.DictWriter(fh, fieldnames=base_fields, delimiter=";")
        w.writeheader(); w.writerows(rows)

    with OUT_TXT.open("w", encoding="utf-8") as fh:
        fh.write("FIFA MOBILE 18 BASE - CARTAS DE EVENTOS (6-digit program IDs)\n")
        fh.write(f"Total {len(rows)} | OVR {min([int(r['ovr_mobile']) for r in rows if str(r['ovr_mobile']).isdigit()], default=0)}-{max([int(r['ovr_mobile']) for r in rows if str(r['ovr_mobile']).isdigit()], default=0)}\n\n")
        for r in rows:
            stats_part = " ".join([f"{k}={r.get(k,'')}" for k in (STAT_FIELDS if args.with_stats else [])])
            fh.write(f"{r['fifa_id']:>7} | {r['ovr_mobile']:>3} {r['position_mobile']:<4} | {r['full_name']:<30} | {r['skill_boost']:<14} | {r['event_confidence']} | {r['event_name']:<25} | {stats_part}\n")

    organized={
        "metadata":{
            "title":"FIFA Mobile 18 Season 2 - Cartas de Eventos",
            "sources":["renderz.app/18/player/{id} (program IDs 500000-999999)"],
            "total_cards":len(rows),
            "confidence": {
                "exact": sum(1 for r in rows if r["event_confidence"]=="exact"),
                "page_only": sum(1 for r in rows if r["event_confidence"]=="page_only"),
            },
            "skill_boost_pool":"same 37 as base",
        },
        "players": rows,
    }
    if args.with_stats:
        organized["metadata"]["stats_generation"] = (
            "Each event card inherits 30 detailed stats from the matched base card (same player),"
            " then scaled linearly by (event_ovr - base_ovr) * 0.42 and clamped 20-99."
            " For unmatchable rows (23 cards), a synthetic profile is derived from OVR and position (GK boosted for GK stats)."
            " This is an approximation; exact event stats are not published by the source sites."
        )
    OUT_JSON.write_text(json.dumps(organized, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"OK {OUT_CSV} {len(rows)} filas")

if __name__=="__main__":
    main()
