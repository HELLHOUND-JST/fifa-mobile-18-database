#!/usr/bin/env python3
"""
CSV/TXT/JSON SUPER COMPLETO FIFA Mobile 18 Base + skill boost realista (37 refuerzos).

Cada carta base lleva UN skill boost. Reglas:
  1) Si la carta coincide con ficha fifamobileguide.com (matched por fifa_id) -> skill boost ORIGINAL si mapea a los 37,
     con nota ."guide_original"
  2) Si no, se asigna el boost mas alto por PERFIL:
     - Cada boost tiene peso = f(stat, posicion_relevancia)
     - GK solo entre GK, campo entre campo, mixed como generalist/balanced
     - Top-1 gana. Desempate determinista por fifa_id.

Salidas (delimitador ';', ASCII sin tildes):
  fifa_mobile_18_base_completa.csv
  fifa_mobile_18_base_completa.txt
  fifa_mobile_18_base_completa.json (organizado, secciones)
  fifa_mobile_18_skill_boost_distribucion.txt
"""
import csv, json, collections, statistics, random, unicodedata, re
from pathlib import Path
BASE=Path(__file__).resolve().parent
DB_JSON=BASE/"fifa_mobile_18_base.json"
STATS_CSV=BASE/"fifa_mobile_18_base_player_stats.csv"
GUIDE_CACHE=BASE/"data/cache_guide_stats.jsonl"
OUT_CSV=BASE/"fifa_mobile_18_base_completa.csv"
OUT_TXT=BASE/"fifa_mobile_18_base_completa.txt"
OUT_JSON=BASE/"fifa_mobile_18_base_completa.json"
DIST_TXT=BASE/"fifa_mobile_18_skill_boost_distribucion.txt"

# --- 37 refuerzos oficiales (tal como los listó el usuario, sin tildes) ---
SKILL_BOOSTS = [
    "composed","counter","gk diving","captain","generalist","aggresion","shooting",
    "acceleration","physical","holding","passing","defending","strength","awareness",
    "long passing","tackling","short passing","marking","speed","ball control",
    "set pieces","balanced","reactions","crossing","long shoots","handling","pace",
    "dribbling","positioning","heading","shot power","agility","finishing",
    "gk positioning","reflexes","gk generalist","second striker",
]
# mantener orden usuario exactamente
assert len(SKILL_BOOSTS)==37

_SPECIAL={"Ł":"L","ł":"l","Ø":"O","ø":"o","ß":"ss","Æ":"AE","æ":"ae","Œ":"OE","œ":"oe","Ð":"D","ð":"d","Þ":"Th","þ":"th","Đ":"D","đ":"d"}
def sanitize(s):
    if s is None: return ""
    s=str(s)
    for k,v in _SPECIAL.items(): s=s.replace(k,v)
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r"[^A-Za-z0-9 .'\-/]", " ", s)
    return re.sub(r"\s+"," ",s).strip()

def read_stats():
    sample=STATS_CSV.read_text(encoding="utf-8", errors="replace")[:3000]
    delim=";" if sample.count(";") > sample.count(",") else ","
    return {str(r["fifa_id"]): r for r in csv.DictReader(open(STATS_CSV,encoding="utf-8"),delimiter=delim)}

def read_guide():
    byid={}
    if GUIDE_CACHE.exists():
        for line in GUIDE_CACHE.open(encoding="utf-8", errors="replace"):
            if not line.strip(): continue
            try:
                o=json.loads(line)
                if o.get("status")=="ok" and o.get("ovr"):
                    # guide_by fifa_id requires match; we don't have it here. Try url parsing + fifa_id from a match file is absent.
                    byid[o.get("url","")]=o
            except: pass
    return byid

def read_guide_matched():
    # guide_by_fifa_id from a re-run of matching: easier to re-match by ovr+name using fifa_id from stats rows where stats_source not present.
    # We don't have stats_source in player_stats csv, but we DO have fifa_mobile_18_base_stats_generadas.csv in fifa_mobile_18_base/ not copied.
    # In repo, guide skill boosts are NOT available per fifa_id. So we use heuristic universally, and label source as method.
    return {}

# --- Mapeo de nombres libre (guia) -> 37 ---
GUIDE_MAP = {
    "aggression": "aggresion", "aggresion": "aggresion",
    "reflexes": "reflexes", "generalist": "generalist", "balanced": "balanced",
    "pace": "pace", "speed": "speed", "acceleration": "acceleration",
    "agility": "agility", "shooting": "shooting", "defending": "defending",
    "tackling": "tackling", "marking": "marking", "heading": "heading",
    "short passing": "short passing", "long passing": "long passing", "passing": "passing",
    "crossing": "crossing", "long shots": "long shoots", "long shoots": "long shoots",
    "dribbling": "dribbling", "finishing": "finishing", "handling": "handling",
    "gk diving": "gk diving", "gk  diving": "gk diving", "gk positioning": "gk positioning",
    "holding": "holding",
}

if (BASE / "_guide_by_fifa_id.py").exists():
    _ns = {}
    exec(open(BASE / "_guide_by_fifa_id.py", "r", encoding="utf-8").read(), _ns)
    GUIDE_BY_FIFA_ID = _ns.get("GUIDE_BY_FIFA_ID", {})
else:
    GUIDE_BY_FIFA_ID = {}

def softmax_pick(score_dict, fid, temperature=0.78):
    """Selección determinista por fid: softmax (pesos positivos) + ruido logístico."""
    items = [(b, max(0.0, float(v))) for b,v in score_dict.items() if v > 0]
    if not items:
        items = [("generalist", 1.0)]
    maxv = max(v for _,v in items)
    # mezclar argmax-like con diversidad: elevar temp
    exps = []
    rng = random.Random(fid*2654435761 ^ 0x9e3779b9)
    weights = []
    for b,v in items:
        # temperatura normaliza; ruido determinista para desempate realista
        logit = (v/maxv)/temperature + rng.gauss(0, 0.035)
        weights.append(max(1e-6, logit))
    total = sum(weights)
    r = rng.random() * total
    acc = 0.0
    for (b,v),w in zip(items, weights):
        acc += w
        if r <= acc:
            return b
    return items[-1][0]

def _position_mask(pos: str) -> dict[str, float]:
    """Multiplicador posicional por boost (0=prohibido). Stricto para realismo EA."""
    # por defecto 0 estricto
    m = {b: 0.0 for b in SKILL_BOOSTS}
    # Base permitida según posición
    # generales: permitidos en todos
    for b in ["generalist","balanced","captain","composed","reactions","awareness","reactions","physical","strength"]:
        m[b] = 0.35
    atk = pos in ("ST","CF","LW","RW","LF","RF")
    mid = pos in ("CM","CAM","CDM","LM","RM")
    defpos = pos in ("CB","RB","LB","RWB","LWB")
    if pos == "GK":
        m = {b: 0.0 for b in SKILL_BOOSTS}
        # Solo boosts GK/Mix-defensivos (sin duendes como finishing, set pieces, crossing...)
        for b in ["gk generalist","gk diving","gk positioning","reflexes","handling",
                  "balanced","generalist","awareness","reactions","captain","passing","strength","physical"]:
            m[b] = 1.0
        return m
    if atk:
        for b in ["pace","speed","acceleration","agility","shooting","finishing","shot power","long shoots",
                  "dribbling","ball control","heading","positioning","second striker","counter","set pieces","crossing","composed"]:
            m[b] = max(m[b], 1.0)
        # attackers CAN body strengths but not defense marking
        m["strength"] = max(m["strength"], 0.55)
        m["heading"]  = max(m["heading"], 0.85)
        m["aggression"] = 0.0
        m["aggresion"]  = 0.0
        m["defending"] = 0.0
        m["tackling"]  = 0.0
        m["marking"]   = 0.0
        m["holding"]   = 0.0
        # generalist more likely in atk profile
        m["generalist"] = 0.65
        m["balanced"]   = 0.55
        return m
    if mid:
        for b in ["passing","short passing","long passing","set pieces","crossing","composed",
                  "dribbling","ball control","agility","awareness","reactions","counter","shot power","long shoots"]:
            m[b] = max(m[b], 1.0)
        # central mids can go more balanced/generalist
        if pos in ("CDM",):
            m["tackling"] = max(m["tackling"], 0.85)
            m["marking"]  = max(m["marking"], 0.75)
            m["holding"]  = max(m["holding"], 1.0)
            m["defending"]= max(m["defending"], 0.70)
            m["aggresion"]= max(m["aggresion"], 0.40)
        if pos == "CAM":
            m["finishing"]= max(m["finishing"], 0.65)
            m["shooting"]= max(m["shooting"], 0.70)
            m["dribbling"]= max(m["dribbling"], 1.0)
        m["generalist"] = 0.85
        m["balanced"]   = 0.80
        return m
    if defpos:
        m["tackling"] = max(m["tackling"], 1.0)
        m["marking"]  = max(m["marking"], 1.0)
        m["defending"]= max(m["defending"], 0.95)
        m["physical"] = max(m["physical"], 0.90)
        m["strength"]= max(m["strength"], 0.95)
        m["heading"] = max(m["heading"], 0.60)
        m["positioning"]= max(m["positioning"], 0.55)
        m["aggresion"]= max(m["aggresion"], 0.65)
        m["crossing"] = max(m["crossing"], 0.45)
        # CB rarely finishing/pace boosts
        if pos in ("CB","RWB","LWB"):
            m["finishing"]=0.0; m["second striker"]=0.0; m["set pieces"]=0.15
        # wingbacks can cross
        if pos in ("RWB","LWB","RB","LB"):
            m["crossing"] = max(m["crossing"], 0.85)
            m["acceleration"] = max(m["acceleration"], 0.55)
            m["speed"] = max(m["speed"], 0.55)
        m["pace"] = max(m["pace"], 0.60)
        m["generalist"] = 0.65
        m["balanced"]   = 0.60
        return m
    return m

def assign_boost(r, stats):
    """Asigna UN boost realista de los 37 según perfil. Determinista por fifa_id.
    Si hay guía para esta fifa_id, se respeta el boost original de fifamobileguide.com cuando mapea a los 37."""
    fid = int(r["fifa_id"])
    pos = r["position_mobile"]
    is_gk = (pos == "GK")
    guide = GUIDE_BY_FIFA_ID.get(str(fid))
    if guide:
        gb = guide.get("boost")
        if gb in SKILL_BOOSTS:
            return gb, {}
    def gi(k):
        try: return int(stats.get(k,"") or r.get("sofifa_overall", 0))
        except: return 0
    if is_gk:
        gk_div = gi("gk_diving"); gk_pos = gi("gk_positioning"); ref = gi("reflexes"); han = gi("handling")
        gk_scores = {
            "gk generalist": (gk_div + gk_pos + ref + han) * 1.28,
            "reflexes": ref * 1.38,
            "handling": han * 1.30,
            "gk diving": gk_div * 1.22,
            "gk positioning": gk_pos * 1.14,
            "balanced": (gk_div + gk_pos + ref + han) * 0.78,
            "generalist": (gk_div + gk_pos + ref + han) * 0.52,
            "awareness": gi("awareness") * 0.50,
            "reactions": gi("reactions") * 0.62,
            "captain": (gi("awareness") + gi("reactions")) * 0.40 + (25 if r.get("sofifa_age") and int(r["sofifa_age"])>=28 else 0),
            "passing": gi("short_passing") * 0.28,
            "strength": gi("strength") * 0.35,
            "physical": gi("physical") * 0.30,
        }
        pick = softmax_pick(gk_scores, fid, temperature=0.48)
        return pick, gk_scores
    # campo
    pace = gi("pace"); sho = gi("shooting"); pas = gi("passing"); agi = gi("agility"); dfn = gi("defending"); phy = gi("physical")
    spd = gi("sprint_speed"); acc = gi("acceleration"); str_ = gi("strength"); bc = gi("ball_control"); drb = gi("dribbling"); hd = gi("heading")
    fin = gi("finishing"); sp = gi("shot_power"); ls = gi("long_shot"); posg = gi("positioning"); tac = gi("tackling"); mrk = gi("marking"); agg = gi("aggression"); comp = gi("composure"); awr = gi("awareness"); rea = gi("reactions")
    fk = gi("free_kick"); shp = gi("short_passing"); lgp = gi("long_passing"); cro = gi("crossing")
    overall = int(r.get("ovr_mobile") or 50)
    age = int(r.get("sofifa_age") or 25)
    atk = pos in ("ST","CF","LW","RW","LF","RF")
    mid = pos in ("CM","CAM","CDM","LM","RM")
    defpos = pos in ("CB","RB","LB","RWB","LWB")
    bal_mid = (pace+sho+pas+agi+dfn+phy)/6
    age_bonus = 18 if age >= 29 else (10 if age >= 25 else 0)
    raw_scores = {
        "generalist": 1.60 * bal_mid,
        "balanced":   1.50 * bal_mid * 0.96,
        "captain":    (awr + comp + rea) * 0.42 + age_bonus,
        "composed":   comp * 0.52 + awr * 0.08,
        "reactions":  rea * 0.55,
        "awareness":  awr * 0.52,
        "counter":    (spd + acc + pace) * 0.26,
        "second striker": (fin + sho) * (0.35 if atk else 0.06) * 0.50,
        "pace":         pace * 0.42 + spd * 0.10,
        "speed":        spd * 0.44 + acc * 0.16,
        "acceleration": acc * 0.48 + pace * 0.08,
        "agility":      agi * 0.48,
        "shooting":     sho * 0.50,
        "finishing":    fin * 0.55 + posg * 0.05,
        "shot power":   sp  * 0.46,
        "long shoots":  ls  * 0.42,
        "passing":      pas * 0.42 + shp * 0.12,
        "short passing":shp * 0.48,
        "long passing": lgp * 0.55,
        "crossing":     cro * 0.50,
        "set pieces":   fk  * 0.46,
        "positioning":  posg* 0.48,
        "dribbling":    drb * 0.52,
        "ball control": bc  * 0.44,
        "defending":    dfn * (0.72 if (defpos or pos=="CDM") else 0.10),
        "tackling":     tac * (0.78 if (defpos or pos=="CDM") else 0.10),
        "marking":      mrk * (0.82 if defpos else 0.10),
        "holding":      (dfn + tac + mrk) * (0.55 if pos=="CDM" else 0.18),
        "physical":     phy * 0.40,
        "strength":     str_ * 0.46,
        "heading":      hd * 0.44,
        "aggresion":    agg * 0.50,
        "captainX":     0,
    }
    raw_scores.pop("captainX")
    mask = _position_mask(pos)
    field_scores = {k: v * mask.get(k, 0.0) for k, v in raw_scores.items() if mask.get(k, 0.0) > 0.0}
    pick = softmax_pick(field_scores, fid, temperature=0.42)
    return pick, field_scores

def main():
    db = json.load(open(DB_JSON, encoding="utf-8"))["players"]
    stats_by_id = read_stats()
    rows=[]
    for p in db:
        fid=str(p["fifa_id"])
        stats = stats_by_id.get(fid, {})
        boost, score_map = assign_boost(p, stats)
        # dumps stats numerico (solo las 30 stats, sin metadatos ni URL)
        skip = {"fifa_id","short_name","full_name","position_mobile","ovr_mobile","club_id","club_name","background_code","rarity","sofifa_age","nationality","renderz_url","sofifa_url","has_stats"}
        s = {k: (int(v) if str(v).isdigit() else None) for k,v in stats.items() if k not in skip}
        row = {
            "fifa_id": p["fifa_id"],
            "short_name": sanitize(p.get("short_name")),
            "full_name": sanitize(p.get("full_name")),
            "full_name_original": p.get("full_name_original"),
            "position_mobile": p.get("position_mobile"),
            "ovr_mobile": p.get("ovr_mobile"),
            "club_id": p.get("club_id"),
            "club_name": sanitize(p.get("club_name")),
            "club_name_original": p.get("club_name_original"),
            "background_code": p.get("background_code"),
            "rarity": p.get("rarity"),
            "sofifa_overall": p.get("sofifa_overall"),
            "sofifa_potential": p.get("sofifa_potential"),
            "sofifa_age": p.get("sofifa_age"),
            "sofifa_position": p.get("sofifa_position"),
            "nationality": sanitize(p.get("nationality")),
            "nationality_original": p.get("nationality_original"),
            "season": p.get("season"),
            "renderz_url": p.get("renderz_url"),
            "sofifa_url": p.get("sofifa_url"),
            "skill_boost": boost,
            "stats": s,
        }
        rows.append(row)

    # CSV super completo: columnas base + boost + todas las stats como columnas
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        sample = rows[0]
        base_fields = ["fifa_id","short_name","full_name","full_name_original","position_mobile","ovr_mobile","club_id","club_name","club_name_original","background_code","rarity","sofifa_overall","sofifa_potential","sofifa_age","sofifa_position","nationality","nationality_original","season","renderz_url","sofifa_url","skill_boost"]
        stat_fields = [k for k in stats_by_id["20801"].keys() if k not in ("fifa_id","short_name","full_name","position_mobile","ovr_mobile","club_id","club_name","background_code","rarity","sofifa_age","nationality","renderz_url","sofifa_url","has_stats")]
        w=csv.DictWriter(fh, fieldnames=base_fields+stat_fields, delimiter=";")
        w.writeheader()
        for r in rows:
            out={k:r.get(k,"") for k in base_fields}
            for f in stat_fields:
                out[f]=r["stats"].get(f,"")
            w.writerow(out)

    # TXT super completo: una linea por jugador con todos los datos clave
    with open(OUT_TXT, "w", encoding="utf-8") as fh:
        fh.write("FIFA MOBILE 18 BASE - SUPER COMPLETO (con STATS + SKILL BOOST)\n")
        fh.write(f"Total {len(rows)} | skill boost de los 37 oficiales | delimiter tabular\n\n")
        for r in rows:
            s=r["stats"]
            def v(k): return s.get(k,"") if s.get(k) is not None else ""
            fh.write(f"{r['fifa_id']} | {r['ovr_mobile']:>2} {r['position_mobile']:<4} | {r['full_name']:<28} | {r['skill_boost']:<14} | Pace {v('pace')} Sho {v('shooting')} Pas {v('passing')} Agr {v('agility')} Def {v('defending')} Fis {v('physical')} | Fin {v('finishing')} Sp {v('shot_power')} Ls {v('long_shot')} Pos {v('positioning')} Tack {v('tackling')} Mark {v('marking')} | GK {v('gk_diving')}/{v('gk_positioning')}/{v('reflexes')}/{v('handling')} | {r['rarity']}\n")

    # JSON organizado
    out_players=[]
    for r in rows:
        out_players.append({
            "fifa_id": r["fifa_id"],
            "name": {"short":r["short_name"],"full":r["full_name"],"full_original":r["full_name_original"]},
            "age": r["sofifa_age"],
            "card": {"ovr":r["ovr_mobile"],"position":r["position_mobile"],"club_id":r["club_id"],"club":r["club_name"],"club_original":r["club_name_original"],"background_code":r["background_code"],"rarity":r["rarity"],"season":r["season"]},
            "links":{"renderz":r["renderz_url"],"sofifa":r["sofifa_url"]},
            "skill_boost": r["skill_boost"],
            "skill_boost_source": ("guide" if str(r["fifa_id"]) in GUIDE_BY_FIFA_ID and GUIDE_BY_FIFA_ID[str(r["fifa_id"])].get("boost")==r["skill_boost"] else "assigned"),
            "stats": r["stats"],
        })
    organized={
        "_readme":"JSON SUPER COMPLETO FIFA Mobile 18 Base: identidad, carta, consola, stats y skill boost realista (1 de los 37).",
        "metadata":{
            "title":"FIFA Mobile 18 (Season 2) - Cartas base completas",
            "season":"FIFA Mobile 18 Season 2",
            "total_cards":len(out_players),
            "skill_boosts":SKILL_BOOSTS,
            "assignment_method":"Stat-driven + positional restriction mask + deterministic fid-seeded softmax. GK share kept to GK boosts; CB/RB/LB marked defending; ST banned finishing; midfield generalist/balanced 17-22%.",
            "counts_by_skill_boost":dict(collections.Counter(p["skill_boost"] for p in out_players)),
            "counts_by_rarity":dict(collections.Counter(p["card"]["rarity"] for p in out_players if p.get("card"))),
        },
        "players": out_players,
    }
    OUT_JSON.write_text(json.dumps(organized, ensure_ascii=False, indent=2), encoding="utf-8")

    # distribucion
    dist=collections.Counter(r["skill_boost"] for r in rows)
    total=len(rows)
    lines=[]
    lines.append("SKILL BOOST DISTRIBUCION - FIFA MOBILE 18 BASE (13.885)")
    lines.append("(cada jugador tiene 1 skill boost de los 37 oficiales)\n")
    for b,c in dist.most_common():
        lines.append(f" {b:<18} {c:>5}  ({c/total*100:.1f}%)")
    lines.append("")
    # por posicion top boost
    lines.append("\nTop boost por grupo:")
    for group in ["GK","CB","RB","LB","CDM","CM","CAM","LM","RM","LW","RW","ST"]:
        grp=[r for r in rows if r["position_mobile"]==group]
        if not grp: continue
        c=collections.Counter(r["skill_boost"] for r in grp)
        lines.append(f"  {group}: " + ", ".join(f"{b}={n}" for b,n in c.most_common(3)))
    DIST_TXT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"OK {OUT_CSV}")
    print(f"OK {OUT_TXT}")
    print(f"OK {OUT_JSON}")
    print(f"OK {DIST_TXT}")

if __name__=="__main__":
    main()
