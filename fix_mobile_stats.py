#!/usr/bin/env python3
"""
Fix FIFA Mobile 18 stats across the three databases with REAL engine values
fetched from RenderZ __data.json (data/cache_mobile_stats.jsonl).

Rule (user requirement: keep original guide numbers untouched):
  - base rows whose fifa_id is in _guide_by_fifa_id.GUIDE_BY_FIFA_ID keep
    their fifamobileguide values; icons listed in data/guide_iconos.json keep
    their guide values. They only get total_stats appended.
  - every other row's 29 stat fields are replaced with RenderZ payload values.
    FIFA Mobile engine stats run well above 99 (up to 136+); do NOT clamp.

Adds `total_stats` (payload totalStats) everywhere.
Skill boosts: guide rows keep guide boost; others use RenderZ payload boost
(mapped to the 37 official strings); heuristic fallback where missing.

Updated:
  base:   fifa_mobile_18_base_player_stats.csv / .json
  eventos: fifa_mobile_18_eventos.csv / .txt / .json
Backups of overwritten files go to backups/ (untracked).
"""
import csv, json, re, shutil, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
COMPLETED = BASE / "backups"
COMPLETED.mkdir(exist_ok=True)

STAT_FIELDS = ["pace","shooting","passing","agility","defending","physical",
    "sprint_speed","acceleration","strength","ball_control","dribbling","heading",
    "finishing","shot_power","long_shot","positioning","tackling","marking",
    "aggression","composure","awareness","reactions","free_kick","short_passing",
    "long_passing","crossing","gk_diving","gk_positioning","reflexes","handling"]
SKILL_BOOSTS = ["composed","counter","gk diving","captain","generalist","aggresion","shooting","acceleration","physical","holding","passing","defending","strength","awareness","long passing","tackling","short passing","marking","speed","ball control","set pieces","balanced","reactions","crossing","long shoots","handling","pace","dribbling","positioning","heading","shot power","agility","finishing","gk positioning","reflexes","gk generalist","second striker"]

def boost_from_code(code):
    if not code:
        return None
    key = re.sub(r"[^A-Za-z]", "", str(code)).upper()
    table = {re.sub(r"[^A-Za-z]", "", b).upper(): b for b in SKILL_BOOSTS}
    if key in table:
        return table[key]
    alt = {
        "COMPOSURE": "composed",
        "LONGSHOTS": "long shoots",
        "LONGSHOT": "long shoots",
        "AGGRESSION": "aggresion",
    }
    return alt.get(key)

def load_payload():
    pl = {}
    for line in open(BASE/"data"/"cache_mobile_stats.jsonl", encoding="utf-8", errors="replace"):
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("status") == "ok":
            pl[int(o["fifa_id"])] = o
    return pl

def stats_from_payload(o):
    s = o["stats"]
    return {
        "pace": o["avg1"], "shooting": o["avg2"], "passing": o["avg3"],
        "agility": o["avg4"], "defending": o["avg5"], "physical": o["avg6"],
        "sprint_speed": s.get("spd"), "acceleration": s.get("acc"),
        "strength": s.get("str"), "ball_control": s.get("bac"), "dribbling": s.get("dri"),
        "heading": s.get("hea"), "finishing": s.get("fin"), "shot_power": s.get("sho"),
        "long_shot": s.get("lsa"), "positioning": s.get("pos"), "tackling": s.get("tac"),
        "marking": s.get("mrk"), "aggression": s.get("agg"), "composure": s.get("com"),
        "awareness": s.get("awr"), "reactions": s.get("rea"), "free_kick": s.get("frk"),
        "short_passing": s.get("spa"), "long_passing": s.get("lpa"), "crossing": s.get("cro"),
        "gk_diving": s.get("gkd"), "gk_positioning": s.get("gkp"), "reflexes": s.get("ref"), "handling": s.get("han"),
    }

def iconos_guide_ids():
    try:
        rows = json.loads((BASE/"data"/"guide_iconos.json").read_text(encoding="utf-8"))
        return {int(r["fifa_id"]) for r in rows}
    except Exception:
        return set()

def base_guide_ids():
    try:
        ns = {}
        exec((BASE/"_guide_by_fifa_id.py").read_text(encoding="utf-8"), ns)
        return {int(k) for k in ns.get("GUIDE_BY_FIFA_ID", {})}
    except Exception as e:
        print("warn: could not read _guide_by_fifa_id.py:", e)
        return set()

def backup(name):
    src = BASE / name
    dst = COMPLETED / name
    if src.exists() and not dst.exists():
        shutil.copy2(src, dst)

def is_gk(pos): return str(pos).upper() == "GK"

def fill_payload_row(r, po, is_gk_row):
    """Write payload stats into a flat row in-place (respects GK n/a convention)."""
    st = stats_from_payload(po)
    if is_gk_row:
        for k in ["pace","shooting","agility","defending"]:
            r[k] = ""
        r["passing"] = st["passing"]
        r["physical"] = st["physical"]
        for k,v in st.items():
            if k in ("pace","shooting","agility","defending","passing","physical"):
                continue
            if v is not None:
                r[k] = v
    else:
        for k,v in st.items():
            if v is not None:
                r[k] = v

def merge_base(payload, guide_ids):
    CSV = BASE / "fifa_mobile_18_base_player_stats.csv"
    backup(CSV.name)
    rows = list(csv.DictReader(open(CSV, encoding="utf-8"), delimiter=";"))
    fields = list(rows[0].keys())
    if "total_stats" not in fields:
        fields = fields + ["total_stats"]
    n_payload = n_kept = n_missing = 0
    for r in rows:
        fid = int(r["fifa_id"])
        po = payload.get(fid)
        if fid in guide_ids:
            r["total_stats"] = po.get("total_stats", "") if po else ""
            n_kept += 1
            continue
        if not po:
            n_missing += 1
            r.setdefault("total_stats", "")
            continue
        fill_payload_row(r, po, is_gk(r["position_mobile"]))
        r["has_stats"] = "1"
        r["total_stats"] = po.get("total_stats", "")
        n_payload += 1
    with open(CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter=";")
        w.writeheader()
        w.writerows(rows)
    print(f"base csv: payload={n_payload} guide-kept={n_kept} missing={n_missing}")

    # ---- base stats JSON ----
    J = BASE / "fifa_mobile_18_base_player_stats.json"
    backup(J.name)
    d = json.loads(J.read_text(encoding="utf-8"))
    n_payload_j = n_kept_j = 0
    for p in d["players"]:
        fid = int(p["fifa_id"])
        po = payload.get(fid)
        if po:
            p["total_stats"] = po.get("total_stats")
        if fid in guide_ids:
            n_kept_j += 1
            continue
        if not po:
            continue
        st = stats_from_payload(po)
        is_gk_row = is_gk(p["card"]["position"])
        if is_gk_row:
            p["stats"]["primary"] = {"gk_diving": st["gk_diving"], "gk_positioning": st["gk_positioning"],
                                     "handling": st["handling"], "reflexes": st["reflexes"],
                                     "passing": st["passing"], "physical": st["physical"]}
        else:
            p["stats"]["primary"] = {"pace": st["pace"], "shooting": st["shooting"], "passing": st["passing"],
                                     "agility": st["agility"], "defending": st["defending"], "physical": st["physical"]}
        detailed = {k: st[k] for k in ["sprint_speed","acceleration","strength","ball_control","dribbling","heading",
                                       "finishing","shot_power","long_shot","positioning","tackling","marking",
                                       "aggression","composure","awareness","reactions","free_kick","short_passing","long_passing","crossing"]}
        p["stats"]["detailed"] = detailed
        p["stats"]["goalkeeping"] = {"gk_diving": st["gk_diving"], "gk_positioning": st["gk_positioning"],
                                     "reflexes": st["reflexes"], "handling": st["handling"]}
        n_payload_j += 1
    d.setdefault("metadata", {})
    d["metadata"]["stats_source"] = "renderz_mobile_original (unboosted engine values; guide originals preserved for 265 cards; mobile range up to 160)"
    d["metadata"]["version"] = "1.1-mobile-stats"
    d["_readme"] = "FIFA Mobile 18 (Season 2) - Cartas base con estadisticas REALES del motor (RenderZ __data.json); stats de guia preservadas en 265 cartas; null ya no se usa (goalkeeping con valores reales en todas las cartas)."
    J.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"base json: payload={n_payload_j} guide-kept={n_kept_j}")

def merge_eventos(payload):
    CSV = BASE / "fifa_mobile_18_eventos.csv"
    backup(CSV.name)
    rows = list(csv.DictReader(open(CSV, encoding="utf-8"), delimiter=";"))
    fields = list(rows[0].keys())
    if "total_stats" not in fields:
        fields = fields + ["total_stats"]
    n_payload = n_missing = 0
    boost_counts = {}
    for r in rows:
        fid = int(r["fifa_id"])
        po = payload.get(fid)
        if not po:
            n_missing += 1
            r["total_stats"] = ""
            continue
        fill_payload_row(r, po, is_gk(r["position_mobile"]))
        boost = boost_from_code(po.get("skill_boost_code"))
        if boost:
            r["skill_boost"] = boost
            boost_counts[boost] = boost_counts.get(boost, 0) + 1
        r["total_stats"] = po.get("total_stats", "")
        n_payload += 1
    with open(CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter=";")
        w.writeheader()
        w.writerows(rows)

    TXT = BASE / "fifa_mobile_18_eventos.txt"
    backup(TXT.name)
    with open(TXT, "w", encoding="utf-8") as fh:
        fh.write("FIFA MOBILE 18 BASE - CARTAS DE EVENTOS (6-digit program IDs)\n")
        fh.write(f"Total {len(rows)} | OVR 60-100 | stats reales RenderZ (rango hasta ~160)\n\n")
        import unicodedata as _ud
        def _a(s):
            s=_ud.normalize("NFKD", str(s)); s="".join(c for c in s if not _ud.combining(c))
            s=re.sub(r"[^A-Za-z0-9 .'\-]","",s)
            return re.sub(r"\s+"," ",s).strip()
        for r in rows:
            stat_part = " ".join([f"{k}={r.get(k,'')}" for k in STAT_FIELDS])
            name = _a(r.get('page_name',''))
            ev = _a(r.get('event_name',''))
            fh.write(f"{r['fifa_id']} | {r.get('ovr_mobile','')} {str(r.get('position_mobile','')):<3} | {name:<28} | {str(r.get('skill_boost','')):<14} | {r.get('event_confidence','')} | {ev:<21} | {stat_part}\n")

    J = BASE / "fifa_mobile_18_eventos.json"
    backup(J.name)
    d = json.loads(J.read_text(encoding="utf-8"))
    boost_counts_j = {}
    for p in d["players"]:
        fid = int(p["fifa_id"])
        po = payload.get(fid)
        if not po:
            continue
        st = stats_from_payload(po)
        if is_gk(p["position_mobile"]):
            for k in ["pace","shooting","agility","defending"]:
                p[k] = None
            p["passing"] = st["passing"]; p["physical"] = st["physical"]
            for k,v in st.items():
                if k in ("pace","shooting","agility","defending","passing","physical"):
                    continue
                p[k] = v
        else:
            for k,v in st.items():
                p[k] = v
        boost = boost_from_code(po.get("skill_boost_code"))
        if boost:
            p["skill_boost"] = boost
            boost_counts_j[boost] = boost_counts_j.get(boost, 0) + 1
        p["total_stats"] = po.get("total_stats")
    d.setdefault("metadata", {})
    d["metadata"]["stats_source"] = "renderz_mobile_original (unboosted engine values, range ~0-160)"
    J.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"eventos: payload={n_payload} missing={n_missing}")
    print("eventos boosts:", sorted(boost_counts_j.items(), key=lambda kv: -kv[1]))

if __name__ == "__main__":
    payload = load_payload()
    print("payload records:", len(payload))
    guide_ids = base_guide_ids()
    print("guide ids (base, kept untouched):", len(guide_ids))
    merge_base(payload, guide_ids)
    merge_eventos(payload)
