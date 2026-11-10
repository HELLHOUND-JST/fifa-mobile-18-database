#!/usr/bin/env python3
"""
Reconciliación RÁPIDA entre guide_base_stats.csv (277) y fifa_mobile_18_base.csv para producir
GUIDE_BY_FIFA_ID = { fifa_id: guide_boost } dentro de generate_skill_boost.py
"""
import csv, json, re, unicodedata
from pathlib import Path
BASE=Path(__file__).resolve().parent
def sanitize(s):
    if s is None: return ""
    s=str(s)
    _SPECIAL={"Ł":"L","ł":"l","Ø":"O","ø":"o","ß":"ss","Æ":"AE","æ":"ae","Œ":"OE","œ":"oe","Ð":"D","ð":"d","Þ":"Th","þ":"th","Đ":"D","đ":"d"}
    for k,v in _SPECIAL.items(): s=s.replace(k,v)
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r"[^A-Za-z0-9 .'\-]"," ", s)
    return re.sub(r"\s+"," ",s).strip()

sample = Path(BASE/"fifa_mobile_18_base.csv").read_text(encoding="utf-8", errors="replace")[:2000]
delim = ";" if sample.count(";") > sample.count(",") else ","
db = list(csv.DictReader(open(BASE/"fifa_mobile_18_base.csv",encoding="utf-8"), delimiter=delim))

# guide desde cache (tiene nombre + ovr + skill_boosts)
guide = []
for line in open(BASE/"data/cache_guide_stats.jsonl", encoding="utf-8", errors="replace"):
    if not line.strip(): continue
    try:
        o=json.loads(line)
        if o.get("status")=="ok":
            o["skill_boosts"]=sanitize(o.get("skill_boosts",""))
            guide.append(o)
    except: pass

# índice DB por (ovr, apellido último token normalizado, prefijo nombre completo normalizado)
def norm(s): return sanitize(s).lower()
by_full_ovr={}
by_surname_ovr={}
for r in db:
    ovr=r["ovr_mobile"]
    if not ovr: continue
    n=norm(r["full_name"])
    by_full_ovr[(int(ovr), n)]=r
    surname=n.split()[-1]
    by_surname_ovr.setdefault((int(ovr), surname), []).append(r)

GUIDE_MAP = {
    "aggression":"aggresion","aggresion":"aggresion","reflexes":"reflexes","generalist":"generalist",
    "balanced":"balanced","pace":"pace","speed":"speed","acceleration":"acceleration","agility":"agility",
    "shooting":"shooting","defending":"defending","tackling":"tackling","marking":"marking","heading":"heading",
    "short passing":"short passing","long passing":"long passing","passing":"passing","crossing":"crossing",
    "long shots":"long shoots","long shoots":"long shoots","dribbling":"dribbling","finishing":"finishing",
    "handling":"handling","gk diving":"gk diving","gk positioning":"gk positioning","holding":"holding",
}

GUIDE_BY_FIFA_ID={}
unmatched=[]
for g in guide:
    ovr=int(g.get("ovr",0))
    name=norm(g.get("player_name",""))
    match=None
    if (ovr, name) in by_full_ovr:
        match=by_full_ovr[(ovr,name)]
    else:
        # shorthand: guia "Lewandowski" ... no; guide names are usually full
        surname=name.split()[-1]
        lst=by_surname_ovr.get((ovr, surname), [])
        if len(lst)==1: match=lst[0]
        elif len(lst)>1:
            # desambiguar por nombre: el de DB que sea sufijo/prefijo del guide name
            for c in lst:
                cn=norm(c["full_name"]); 
                if(cn in name or name in cn):
                    match=c; break
    if not match:
        unmatched.append((g.get("player_name"), ovr, g.get("skill_boosts")))
        continue
    sb=g.get("skill_boosts","").lower().strip()
    # quitar dobles espacios
    sb=re.sub(r"\s+"," ", sb)
    sb=GUIDE_MAP.get(sb, sb)
    GUIDE_BY_FIFA_ID[str(match["fifa_id"])] = {"boost": sb, "guide_url": g.get("url","")}

print("guide total", len(guide), "matched", len(GUIDE_BY_FIFA_ID), "unmatched", len(unmatched))
for u in unmatched[:20]:
    print("  unmatched:", u)
# imprimir líneas python para pegar en generate
with open(BASE/"_guide_by_fifa_id.py","w",encoding="utf-8") as f:
    f.write("GUIDE_BY_FIFA_ID = {\n")
    for fid, d in GUIDE_BY_FIFA_ID.items():
        url=d["guide_url"].replace("'","\\'")
        f.write(f"  '{fid}': {{'boost': '{d['boost']}', 'guide_url': '{url}'}},\n")
    f.write("}\n")
print("saved _guide_by_fifa_id.py")
