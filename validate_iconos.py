import csv, json, sys, re
from pathlib import Path

BASE = Path(__file__).resolve().parent
SKILL_BOOSTS = {
    "composed","counter","gk diving","captain","generalist","aggresion","shooting",
    "acceleration","physical","holding","passing","defending","strength","awareness",
    "long passing","tackling","short passing","marking","speed","ball control",
    "set pieces","balanced","reactions","crossing","long shoots","handling","pace",
    "dribbling","positioning","heading","shot power","agility","finishing",
    "gk positioning","reflexes","gk generalist","second striker",
}
OUT_CSV, OUT_TXT, OUT_JSON = BASE/"fifa_mobile_18_iconos.csv", BASE/"fifa_mobile_18_iconos.txt", BASE/"fifa_mobile_18_iconos.json"
fails = []

# --- CSV checks ---
raw = OUT_CSV.read_text(encoding="utf-8")
if '\x00' in raw: fails.append("CSV contains NUL")
rows = list(csv.DictReader(open(OUT_CSV, encoding="utf-8"), delimiter=";"))
print("rows:", len(rows))
if len(rows) != 69: fails.append(f"expected 69 rows, got {len(rows)}")
base_cols = list(rows[0].keys())
for i, r in enumerate(rows):
    if list(r.keys()) != base_cols: fails.append(f"row {i} column order mismatch")
    if any(v is None for v in r.values()): fails.append(f"row {i} has missing fields")
    if r["skill_boost"] not in SKILL_BOOSTS: fails.append(f"row {i} invalid boost: {r['skill_boost']!r}")
    if not (85 <= int(r["ovr_mobile"]) <= 99): fails.append(f"row {i} ovr out of range {r['ovr_mobile']}")
    if r["position_mobile"] not in ("GK","CB","RB","LB","RWB","LWB","CDM","CM","CAM","LM","RM","LW","RW","LF","RF","ST","CF"): fails.append(f"row {i} odd pos {r['position_mobile']}")
    if r["rarity"] not in ("Icon","Prime Icon","WC Icon"): fails.append(f"row {i} odd rarity {r['rarity']}")
    is_gk = r["position_mobile"] == "GK"
    gk_fields = ["gk_diving","gk_positioning","reflexes","handling"]
    for f in gk_fields:
        if is_gk and not r[f]: fails.append(f"row {i} GK missing {f}")
    for f, v in r.items():
        if f in ("pace","shooting","passing","agility","defending","physical","sprint_speed","acceleration","strength","ball_control","dribbling","heading","finishing","shot_power","long_shot","positioning","tackling","marking","aggression","composure","awareness","reactions","free_kick","short_passing","long_passing","crossing","gk_diving","gk_positioning","reflexes","handling"):
            if v == "":
                if not ((is_gk and f in ("pace","shooting","agility","defending")) or r["stats_source"] == "guide_original"):
                    fails.append(f"row {i} {f} empty but expected value")
                continue
            iv = int(v)
            if iv < 0: fails.append(f"row {i} {f}={v} negative")
            if iv > 200: fails.append(f"row {i} stats {f}={v} out of 0-200")
    for k in ("name","full_name","nationality","position_real","foot","clubs","honors","rarity","background_code","action_shot","renderz_url","skill_boost"):
        v = r[k]
        if any(ord(c) > 127 for c in v): fails.append(f"row {i} {k} not ASCII: {v!r}")
    ts = r.get("total_stats","")
    if ts and not ts.isdigit():
        fails.append(f"row {i} total_stats not integer: {ts!r}")

# guide-original boosts preserved?
guide_like = [r for r in rows if r["stats_source"] == "guide_original"]
print("guide rows:", len(guide_like))
if len(guide_like) != 15: fails.append(f"expected 15 guide rows, got {len(guide_like)}")
for r in guide_like:
    print("  guide:", r["fifa_id"], r["name"], "boost:", r["skill_boost"])

# --- TXT checks ---
txt = OUT_TXT.read_text(encoding="utf-8")
if any(ord(c) > 127 for c in txt): fails.append("TXT not pure ASCII")
print("txt lines:", len(txt.splitlines()))

# --- JSON checks ---
data = json.loads(OUT_JSON.read_text(encoding="utf-8"))
players = data["players"]
print("json players:", len(players), "metadata:", data["metadata"])
if len(players) != 69: fails.append("JSON players != 69")
for p in players:
    b = p["skill_boost"]
    if b not in SKILL_BOOSTS: fails.append(f"json {p['fifa_id']} bad boost {b!r}")
    for k in ("short","full"):
        if any(ord(c) > 127 for c in p["name"][k]): fails.append(f"json {p['fifa_id']} name.{k} not ASCII")
    for k in ("nationality","foot","real_position","clubs","honors"):
        if any(ord(c) > 127 for c in p.get(k,"")): fails.append(f"json {p['fifa_id']} {k} not ASCII")
    # cross-check stats vs CSV row
    cid = str(p["fifa_id"])
    row = next(r for r in rows if r["fifa_id"] == cid)
    for k, v in p["stats"].items():
        cv = row[k] if k in row else None
        if (v is None) != (cv in (None, "")):
            fails.append(f"json {p['fifa_id']} stat {k} mismatch json={v} csv={cv}")

# --- non-ASCII census ---
for f in [OUT_CSV, OUT_TXT, OUT_JSON, BASE/"fifa_mobile_18_skill_boost_iconos.txt"]:
    if not f.exists():
        fails.append(f"missing {f}")
        continue
    b = f.read_bytes()
    non = [x for x in b if x > 127]
    print(f.name, "non-ascii bytes:", len(non))

print("FAILURES:" if fails else "ALL CHECKS PASSED")
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
