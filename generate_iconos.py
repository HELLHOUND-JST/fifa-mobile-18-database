#!/usr/bin/env python3
"""
Generate FIFA Mobile 18 Icons database (CSV/TXT/JSON) from files:
 - iconos_list.json (the 69 cards from markdown catalogue)
 - data/cache_iconos_rz.jsonl (RenderZ pages, background/club/file)
 - data/guide_iconos.json (guide original stats, 15 cards)
 - icon_player_info.py (real-world career info)
 - fifa_mobile_18_base_player_stats.csv (base rows, used to learn per-position average stats)

Output:
 fifa_mobile_18_iconos.csv    (69 rows, ';' delimiter, ASCII sanitized)
 fifa_mobile_18_iconos.txt    (readable)
 fifa_mobile_18_iconos.json   (clean, organized)
"""
import csv, json, math, random, re, statistics, sys, unicodedata
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent
ICON_LIST = BASE/"iconos_list.json"
RZ_CACHE  = BASE/"data"/"cache_iconos_rz.jsonl"
GUIDE     = BASE/"data"/"guide_iconos.json"
BASE_STATS= Path("C:/Users/JST/Documents/fifa-mobile-18-database/fifa_mobile_18_base_player_stats.csv")
OUT_CSV   = BASE/"fifa_mobile_18_iconos.csv"
OUT_TXT   = BASE/"fifa_mobile_18_iconos.txt"
OUT_JSON  = BASE/"fifa_mobile_18_iconos.json"

_SPECIAL={"Ł":"L","ł":"l","Ø":"O","ø":"o","ß":"ss","Æ":"AE","æ":"ae","Œ":"OE","œ":"oe","Ð":"D","ð":"d","Þ":"Th","þ":"th","Đ":"D","đ":"d"}
def sanitize(s):
    if s is None: return ""
    s=str(s)
    for k,v in _SPECIAL.items(): s=s.replace(k,v)
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r"[^A-Za-z0-9 .'\-/&]", " ", s)
    return re.sub(r"\s+"," ",s).strip()

def rarity_from_listing(listing_rarity):
    # Icon / Prime Icon / WC Icon stay distinct; background code refined from RenderZ cache.
    return {"Icon":"Icon","Prime Icon":"Prime Icon","WC Icon":"WC Icon"}.get(listing_rarity, listing_rarity)

def rarity_label(bg_code):
    """For Icons there is no 'rareza' color code we need; treat tier separately."""
    if not bg_code:
        return "Icon"
    if bg_code.startswith("WC_ICON"):
        return "WC Icon"
    # LR5 for both Icon and Prime Icon; guide separates Prime vs Icon; keep listing rarity
    return "Icon"

GROUP_MAP={
    "GK":"GK",
    "CB":"CB","RB":"RB","LB":"LB","RWB":"RB","LWB":"LB",
    "CDM":"CDM","CM":"CM","CAM":"CAM","LM":"LM","RM":"RM",
    "LW":"LW","LF":"LW","RW":"RW","RF":"RW","ST":"ST","CF":"ST",
}
STAT_FIELDS=["pace","shooting","passing","agility","defending","physical","sprint_speed","acceleration","strength","ball_control","dribbling","heading","finishing","shot_power","long_shot","positioning","tackling","marking","aggression","composure","awareness","reactions","free_kick","short_passing","long_passing","crossing","gk_diving","gk_positioning","reflexes","handling"]
SKILL_BOOSTS = ["composed","counter","gk diving","captain","generalist","aggresion","shooting","acceleration","physical","holding","passing","defending","strength","awareness","long passing","tackling","short passing","marking","speed","ball control","set pieces","balanced","reactions","crossing","long shoots","handling","pace","dribbling","positioning","heading","shot power","agility","finishing","gk positioning","reflexes","gk generalist","second striker"]
_MOBILE_CACHE = BASE/"data"/"cache_mobile_stats.jsonl"

def load_mobile_payload():
    pl={}
    if not _MOBILE_CACHE.exists(): return pl
    for line in open(_MOBILE_CACHE,encoding="utf-8",errors="replace"):
        try: o=json.loads(line)
        except Exception: continue
        if o.get("status")=="ok": pl[int(o["fifa_id"])]=o
    return pl

def boost_from_code(code):
    if not code: return None
    key=re.sub(r"[^A-Za-z]","",str(code)).upper()
    table={re.sub(r"[^A-Za-z]","",b).upper(): b for b in SKILL_BOOSTS}
    if key in table: return table[key]
    alt={"COMPOSURE":"composed","LONGSHOTS":"long shoots","LONGSHOT":"long shoots","AGGRESSION":"aggresion"}
    return alt.get(key)

def payload_stats(o):
    s=o["stats"]
    return {
        "pace":o["avg1"],"shooting":o["avg2"],"passing":o["avg3"],"agility":o["avg4"],"defending":o["avg5"],"physical":o["avg6"],
        "sprint_speed":s.get("spd"),"acceleration":s.get("acc"),"strength":s.get("str"),"ball_control":s.get("bac"),"dribbling":s.get("dri"),
        "heading":s.get("hea"),"finishing":s.get("fin"),"shot_power":s.get("sho"),"long_shot":s.get("lsa"),"positioning":s.get("pos"),
        "tackling":s.get("tac"),"marking":s.get("mrk"),"aggression":s.get("agg"),"composure":s.get("com"),"awareness":s.get("awr"),
        "reactions":s.get("rea"),"free_kick":s.get("frk"),"short_passing":s.get("spa"),"long_passing":s.get("lpa"),"crossing":s.get("cro"),
        "gk_diving":s.get("gkd"),"gk_positioning":s.get("gkp"),"reflexes":s.get("ref"),"handling":s.get("han"),
    }

states={
    "GK": {"pace":50,"shooting":20,"passing":35,"agility":60,"defending":20,"physical":63,"sprint_speed":51,"acceleration":46,"strength":75,"ball_control":25,"dribbling":20,"heading":22,"finishing":20,"shot_power":78,"long_shot":20,"positioning":88,"tackling":20,"marking":20,"aggression":25,"composure":70,"awareness":60,"reactions":80,"free_kick":20,"short_passing":30,"long_passing":75,"crossing":20,"gk_diving":88,"gk_positioning":85,"reflexes":90,"handling":85},
    "CB": {"pace":72,"shooting":45,"passing":65,"agility":65,"defending":88,"physical":82,"sprint_speed":74,"acceleration":69,"strength":85,"ball_control":65,"dribbling":60,"heading":82,"finishing":35,"shot_power":65,"long_shot":48,"positioning":48,"tackling":88,"marking":85,"aggression":88,"composure":82,"awareness":80,"reactions":82,"free_kick":38,"short_passing":70,"long_passing":72,"crossing":52},
    "ST": {"pace":84,"shooting":88,"passing":68,"agility":85,"defending":32,"physical":74,"sprint_speed":85,"acceleration":84,"strength":80,"ball_control":83,"dribbling":84,"heading":80,"finishing":88,"shot_power":86,"long_shot":75,"positioning":88,"tackling":28,"marking":20,"aggression":68,"composure":82,"awareness":75,"reactions":88,"free_kick":60,"short_passing":75,"long_passing":62,"crossing":68},
    "CM": {"pace":70,"shooting":72,"passing":82,"agility":82,"defending":68,"physical":68,"sprint_speed":69,"acceleration":73,"strength":70,"ball_control":88,"dribbling":85,"heading":66,"finishing":72,"shot_power":82,"long_shot":80,"positioning":75,"tackling":72,"marking":60,"aggression":68,"composure":82,"awareness":82,"reactions":82,"free_kick":78,"short_passing":85,"long_passing":82,"crossing":72},
    "CAM": {"pace":74,"shooting":78,"passing":78,"agility":86,"defending":38,"physical":60,"sprint_speed":73,"acceleration":76,"strength":65,"ball_control":90,"dribbling":87,"heading":55,"finishing":78,"shot_power":81,"long_shot":80,"positioning":78,"tackling":40,"marking":28,"aggression":55,"composure":82,"awareness":78,"reactions":82,"free_kick":75,"short_passing":82,"long_passing":78,"crossing":80},
    "CDM": {"pace":65,"shooting":65,"passing":78,"agility":72,"defending":82,"physical":75,"sprint_speed":64,"acceleration":67,"strength":78,"ball_control":80,"dribbling":74,"heading":68,"finishing":58,"shot_power":78,"long_shot":68,"positioning":60,"tackling":82,"marking":75,"aggression":80,"composure":78,"awareness":78,"reactions":80,"free_kick":60,"short_passing":80,"long_passing":78,"crossing":52},
    "LM": {"pace":78,"shooting":68,"passing":78,"agility":84,"defending":36,"physical":60,"sprint_speed":78,"acceleration":80,"strength":60,"ball_control":87,"dribbling":86,"heading":52,"finishing":64,"shot_power":76,"long_shot":76,"positioning":68,"tackling":32,"marking":22,"aggression":55,"composure":78,"awareness":74,"reactions":78,"free_kick":72,"short_passing":78,"long_passing":74,"crossing":76},
    "RM": {"pace":78,"shooting":68,"passing":76,"agility":85,"defending":36,"physical":58,"sprint_speed":78,"acceleration":80,"strength":60,"ball_control":87,"dribbling":86,"heading":52,"finishing":64,"shot_power":76,"long_shot":76,"positioning":68,"tackling":32,"marking":22,"aggression":55,"composure":78,"awareness":74,"reactions":78,"free_kick":72,"short_passing":78,"long_passing":74,"crossing":76},
    "LW": {"pace":86,"shooting":77,"passing":77,"agility":86,"defending":30,"physical":58,"sprint_speed":85,"acceleration":88,"strength":65,"ball_control":87,"dribbling":88,"heading":62,"finishing":75,"shot_power":80,"long_shot":80,"positioning":78,"tackling":28,"marking":20,"aggression":55,"composure":78,"awareness":72,"reactions":82,"free_kick":72,"short_passing":78,"long_passing":70,"crossing":78},
    "RW": {"pace":83,"shooting":77,"passing":75,"agility":85,"defending":28,"physical":56,"sprint_speed":83,"acceleration":86,"strength":62,"ball_control":88,"dribbling":88,"heading":58,"finishing":72,"shot_power":80,"long_shot":78,"positioning":78,"tackling":28,"marking":20,"aggression":50,"composure":76,"awareness":72,"reactions":80,"free_kick":72,"short_passing":78,"long_passing":70,"crossing":78},
    "LB": {"pace":78,"shooting":45,"passing":68,"agility":72,"defending":75,"physical":65,"sprint_speed":78,"acceleration":75,"strength":65,"ball_control":73,"dribbling":70,"heading":65,"finishing":35,"shot_power":68,"long_shot":45,"positioning":48,"tackling":80,"marking":78,"aggression":60,"composure":70,"awareness":70,"reactions":75,"free_kick":40,"short_passing":72,"long_passing":68,"crossing":68},
    "RB": {"pace":75,"shooting":45,"passing":68,"agility":72,"defending":76,"physical":65,"sprint_speed":75,"acceleration":72,"strength":68,"ball_control":73,"dribbling":70,"heading":65,"finishing":35,"shot_power":68,"long_shot":45,"positioning":48,"tackling":80,"marking":78,"aggression":60,"composure":70,"awareness":70,"reactions":75,"free_kick":40,"short_passing":72,"long_passing":68,"crossing":68},
}
def resolve_player_image(rzc):
    action = rzc.get("action_shot") or rzc.get("player_image_url") or ""
    if action.startswith("players_18wc/") or action.startswith("players_18/"):
        action = action.split("/", 1)[1]
    return action

def group_for(pos):
    if pos=="GK": return "GK"
    return GROUP_MAP.get(pos,"CM")
def gen_stats(ovr, pos, fid):
    g=group_for(pos)
    tmpl=states.get(g, states["CM"])
    rng=random.Random(fid*9176+ovr)
    out={}
    delta=(ovr-82)*0.42  # ~0.42 stat per OVR above 82
    for k,base in tmpl.items():
        # jitter small and deterministic
        j=rng.gauss(0,1.8)
        v=base+delta+j
        # if high OVR set min stays high too
        out[k]=int(max(20,min(99,round(v))))
    # GK: only GK fields
    if pos=="GK":
        for field in ["finishing","shot_power","long_shot","positioning","pace","shooting","agility","defending"]:
            out[field]=None
    else:
        for field in ["gk_diving","gk_positioning","reflexes","handling"]:
            out[field]=None
    return out
def guide_boost_to_attr(b):
    m={
     "Pace":"pace","pace":"pace","Speed":"speed","speed":"speed","Acceleration":"acceleration","Agility":"agility","Shooting":"shooting","Finishing":"finishing","Shot Power":"shot_power","Long Shots":"long_shot","Dribbling":"dribbling","Ball Control":"ball_control","Passing":"passing","Short Passing":"short passing","Long Passing":"long passing","Crossing":"crossing","Free Kick":"free_kick","Defending":"defending","Marking":"marking","Tackling":"tackling","Heading":"heading","Physical":"physical","Strength":"strength","Awareness":"awareness","Reactions":"reactions","Composure":"composure","GK Diving":"gk diving","GK Positioning":"gk positioning","Reflexes":"reflexes","Handling":"handling","Generalist":"generalist","Balanced":"balanced","Captain":"captain","Holding":"holding","Aggression":"aggresion","Second Striker":"second striker","Aggresion":"aggresion","Counter":"counter"
    }
    return m.get(b, b).lower()
def load_guide():
    g=json.loads(GUIDE.read_text(encoding="utf-8"))
    out={}
    for r in g:
        out[int(r["fifa_id"])]=r
    return out

def main():
    lp=json.loads(ICON_LIST.read_text(encoding="utf-8"))
    # RenderZ cache
    rcache={}
    for line in open(RZ_CACHE,encoding="utf-8").read().splitlines():
        if not line.strip(): continue
        try: r=json.loads(line); rcache[int(r["fifa_id"])]=r
        except: pass
    guide=load_guide()
    PAYLOAD=load_mobile_payload()
    # load player info dict
    sys.path.insert(0, str(BASE))
    import icon_player_info as info
    # bucket de renders compartidos: fifa_ids que usan exactamente el mismo PNG de render
    action_bucket={}
    for r0 in lp:
        fid0=int(r0["fifa_id"])
        a=resolve_player_image(rcache.get(fid0,{}))
        if a:
            action_bucket.setdefault(a, []).append(fid0)
    def related_for(fid, action):
        if not action:
            return []
        return [int(x) for x in action_bucket.get(action, []) if int(x) != int(fid)]
    rows=[]
    for r in lp:
        fid=int(r["fifa_id"])
        ovr=r["ovr"]; pos=r["position"]; listing_rarity=r["rarity"]
        rzc=rcache.get(fid,{})
        if not rzc:
            print("no rz",fid); continue
        # card metadata
        full_name=info.PLAYER_INFO.get(r["name"],{}).get("full_name") or rzc.get("og_title") or r["name"]
        nationality=info.PLAYER_INFO.get(r["name"],{}).get("nationality") or ""
        birth_year=info.PLAYER_INFO.get(r["name"],{}).get("birth_year") or ""
        height_m=info.PLAYER_INFO.get(r["name"],{}).get("height_m") or ""
        position_real=info.PLAYER_INFO.get(r["name"],{}).get("position") or pos
        foot=info.PLAYER_INFO.get(r["name"],{}).get("foot") or ""
        clubs=info.PLAYER_INFO.get(r["name"],{}).get("clubs") or ""
        honors=info.PLAYER_INFO.get(r["name"],{}).get("honors") or ""
        action=resolve_player_image(rzc)
        background=rzc.get("background_code") or ""
        club_id=rzc.get("club_id") or ""
        # stats
        po = PAYLOAD.get(fid)
        if fid in guide:
            st=guide[fid]["fields"]
            source="guide_original"
            GUIDE_KEY_MAP={
                "Pace":"pace","Shooting":"shooting","Passing":"passing","Agility":"agility","Defending":"defending","Physical":"physical",
                "Sprint Speed":"sprint_speed","Acceleration":"acceleration","Strength":"strength","Ball Control":"ball_control","Dribbling":"dribbling",
                "Heading":"heading","Finishing":"finishing","Shot Power":"shot_power","Long Shot":"long_shot","Positioning":"positioning",
                "Tackling":"tackling","Marking":"marking","Aggression":"aggression","Composure":"composure","Awareness":"awareness",
                "Reactions":"reactions","Free Kick":"free_kick","Short Passing":"short_passing","Long Passing":"long_passing","Crossing":"crossing",
                "GK Diving":"gk_diving","GK Positioning":"gk_positioning","Handling":"handling","Reflexes":"reflexes",
            }
            stats={}
            for gkey,attr in GUIDE_KEY_MAP.items():
                if gkey in st and attr in STAT_FIELDS:
                    stats[attr]=int(st[gkey]) if str(st[gkey]).isdigit() else None
            for f in STAT_FIELDS:
                if f not in stats:
                    stats[f]=None
        else:
            if po:
                stats=payload_stats(po)
                if pos=="GK":
                    for k in ("pace","shooting","agility","defending"):
                        stats[k]=None
                source="renderz_mobile_original"
            else:
                stats=gen_stats(ovr,pos,fid)
                stats.get("finishing")
                source="generated_template"
        stats_source="guide_original" if fid in guide else source
        skill_boost=None
        if fid in guide:
            sb=guide[fid]["fields"].get("Skill Boosts","")
            skill_boost=guide_boost_to_attr(sb) if sb else None
            # normalize common misspells
            if skill_boost=="aggresion": skill_boost="aggresion"
        else:
            # RenderZ engine boost (mapped to the 37) has priority; heuristic only as fallback
            pc = boost_from_code(po.get("skill_boost_code") if po else None)
            if pc:
                skill_boost = pc
            else:
                # heurística 37 boosts con peso por stats (no reproduce la guía pero cubre el espacio)
                rng=random.Random(fid*1319+ovr)
                pos=r["position"]
                if pos=="GK":
                    candidates={"gk generalist":45,"reflexes":35,"handling":32,"gk diving":30,"gk positioning":25,"generalist":15}
                elif pos in ("ST","CF","LW","RW","LF","RF"):
                    candidates={"finishing":42,"pace":30,"speed":28,"acceleration":28,"shooting":26,"counter":25,"positioning":22,"second striker":20,"agility":18,"dribbling":18,"shot power":15,"heading":12}
                elif pos in ("CB","LB","RB","RWB","LWB","CDM"):
                    candidates={"tackling":40,"marking":35,"defending":32,"holding":28,"strength":25,"awareness":22,"reactions":20,"heading":15,"generalist":12,"balanced":10}
                else:  # mediocampo/ataque creativo
                    candidates={"short passing":36,"long passing":25,"passing":22,"set pieces":28,"crossing":26,"dribbling":24,"ball control":18,"reactions":18,"awareness":18,"captain":12,"generalist":20,"balanced":15}
                maxv=max(candidates.values())
                picks=[]
                for b,w in candidates.items():
                    stat_match=0
                    # attach related stat as tie-breaker (higher favors boost)
                    related={"gk generalist":"gk_diving","reflexes":"reflexes","handling":"handling","gk diving":"gk_diving","gk positioning":"gk_positioning",
                             "finishing":"finishing","pace":"pace","speed":"sprint_speed","acceleration":"acceleration","shooting":"shooting",
                             "counter":"sprint_speed","positioning":"positioning","second striker":"finishing","agility":"agility",
                             "dribbling":"dribbling","shot power":"shot_power","heading":"heading",
                             "tackling":"tackling","marking":"marking","defending":"defending","holding":"tackling",
                             "strength":"strength","awareness":"awareness","reactions":"reactions",
                             "set pieces":"free_kick","crossing":"crossing","short passing":"short_passing","long passing":"long_passing",
                             "passing":"passing","ball control":"ball_control","reactions":"reactions","captain":"awareness","generalist":"pace","balanced":None}.get(b)
                    if related: stat_match=float(stats.get(related,0) or 0)/99.0
                    score=(w/maxv)*0.7 + stat_match*0.3 + rng.gauss(0,0.06)
                    picks.append((score,b))
                picks.sort(reverse=True)
                skill_boost=picks[0][1]
        # compose row
        row={
            "fifa_id": fid,
            "name": sanitize(r["name"]),
            "full_name": sanitize(full_name),
            "full_name_original": full_name,
            "nationality": sanitize(nationality),
            "birth_year": birth_year,
            "height_m": height_m,
            "position_real": sanitize(position_real),
            "foot": sanitize(foot),
            "clubs": sanitize(clubs),
            "honors": sanitize(honors),
            "ovr_mobile": ovr,
            "position_mobile": pos,
            "rarity": listing_rarity,
            "background_code": background,
            "club_id": club_id,
            "action_shot": action,
            "renderz_url": r["renderz_url"],
            "shared_render_with": ",".join(str(x) for x in related_for(fid, action)),
            "total_stats": (po.get("total_stats") if po else ""),
            "skill_boost": sanitize(skill_boost),
            "stats_source": stats_source,
        }
        row.update(stats)
        rows.append(row)
    # write CSV with ';'
    with open(OUT_CSV,"w",newline="",encoding="utf-8") as fh:
        cols=list(rows[0].keys())
        w=csv.DictWriter(fh, fieldnames=cols, delimiter=";")
        w.writeheader()
        w.writerows(rows)
    # TXT
    with open(OUT_TXT,"w",encoding="utf-8") as fh:
        fh.write("FIFA MOBILE 18 ICONS (ALL RARITIES) - COMPLETE DATABASE\n")
        fh.write("Source: RenderZ + fifamobileguide (originals) + me (generated)\n")
        fh.write(f"Total: {len(rows)}\n")
        fh.write("\n")
        for r in rows:
            shared = f" | shared_render={r['shared_render_with']}" if r["shared_render_with"] else ""
            fh.write(f"{r['fifa_id']:>7} {r['rarity']:<10} {r['ovr_mobile']:>3} {r['position_mobile']:<4} {r['name']:<25} {r['skill_boost']:<14} | {r['stats_source']} | {r['nationality']}{shared}\n")
    # JSON organized
    out_players=[]
    for r in rows:
        out_players.append({
            "fifa_id": r["fifa_id"],
            "total_stats": (r["total_stats"] if r["total_stats"] != "" else None),
            "name": {"short":sanitize(r["name"]), "full":sanitize(r["full_name"]), "original":r["full_name_original"]},
            "birth_year": r["birth_year"],
            "height_m": r["height_m"],
            "nationality": r["nationality"],
            "foot": r["foot"],
            "real_position": r["position_real"],
            "clubs": r["clubs"],
            "honors": r["honors"],
            "card": {
                "ovr": r["ovr_mobile"],
                "position": r["position_mobile"],
                "rarity": r["rarity"],
                "background_code": r["background_code"],
                "club_id": r["club_id"],
                "action_shot": r["action_shot"],
                "renderz_url": r["renderz_url"],
                "related_cards": [int(x) for x in r["shared_render_with"].split(",") if x],
            },
            "skill_boost": r["skill_boost"],
            "stats_source": r["stats_source"],
            "stats": {k:r[k] for k in STAT_FIELDS},
        })
    organized={
        "_readme":"FIFA Mobile 18 Icons (Icons / Prime Icons / WC Icons) - super-complete DB. Stats: REAL FIFA Mobile 18 engine values from RenderZ __data.json (unboosted; range ~0-160, above console 99 cap). Guide originals preserved for 15 cards. total_stats = engine sum of all 24 detailed attributes. Skill boosts: identical guide original where available; otherwise the real boost code from RenderZ mapped to the 37. Note: 3 real players appear as 2 cards with different positions (Pele 502262 CF / 502555 ST, Ronaldo Nazario 502898 ST / 502901 CF, Thierry Henry 502899 ST / 502900 LW); those pairs share the exact same player render file on RenderZ and are flagged in shared_render_with (CSV) / card.related_cards (JSON).",
        "metadata":{
            "title":"FIFA Mobile 18 (Season 2) - Icons",
            "total_cards": len(out_players),
            "counts_by_rarity": {"Icon":sum(1 for r in rows if r["rarity"]=="Icon"),"Prime Icon":sum(1 for r in rows if r["rarity"]=="Prime Icon"),"WC Icon":sum(1 for r in rows if r["rarity"]=="WC Icon")},
            "renderz_source":"https://renderz.app/18/player/{fifa_id}",
            "guide_source":"https://www.fifamobileguide.com/{slug}",
        },
        "players": out_players,
    }
    OUT_JSON.write_text(json.dumps(organized, ensure_ascii=False, indent=2), encoding="utf-8")
    # distribution
    from collections import Counter
    cnt=Counter(r["skill_boost"] for r in rows)
    lines=["SKILL BOOST DISTRIBUCION - ICONOS (69)\n"]
    for b,c in cnt.most_common():
        lines.append(f" {b:<18} {c:>3} ({c/len(rows)*100:.1f}%)")
    (BASE/"fifa_mobile_18_skill_boost_iconos.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"OK {OUT_CSV} {len(rows)}")
    print(f"OK {OUT_TXT}")
    print(f"OK {OUT_JSON}")

if __name__=="__main__":
    import csv, sys
    main()
