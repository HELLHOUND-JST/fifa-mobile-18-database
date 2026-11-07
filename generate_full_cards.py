#!/usr/bin/env python3
"""
Genera CARTAS COMPLETAS FIFA Mobile 18 base (256x256, tamano original RenderZ)
con la FUENTE ORIGINAL Knul (EA) y posiciones exactas de RenderZ CSS fm18.

NO usa fuente generica. No usa captura/login. Compone desde assets originales CDN:
  - Fondo:      backgrounds_18/backgrounds_{MR4,ER3,GR2,GR3,SR1,BR0}.png (256x256)
  - Jugador:    players_18/p{id}*.png ya descargado en players_png/ (256x256, transparente)
  - Club:       clubLogos_18/{club_id}.png (256x256 -> 40x40 en carta)
  - Texto:      Knul-Medium.woff / Knul-Regular.woff de fonts.frzdb.net -> TTF (fonts/)
                OVR 42px Knul Medium, Posicion 18px Knul Regular, Nombre 20px Knul Medium

Layout exacto RenderZ .player-card-fm18 (256x256):
  background/action-shot: 100% absolute (0,0,256,256)
  club:    40x40, top 46%, left 19%        -> x=48.64, y=117.76
  rating:  42px, top 15%, left 19.3%, width 28%, left, blanco, shadow 0/0.5px negro
  position:18px, top 34.5%, left 20%, width 19%, left, uppercase, blanco
  name:    20px, top 66.5%, width 100%, center, uppercase, blanco, nowrap
           + compresion horizontal si ancho > 130px (ej. CRISTIANO RONALDO 189px -> scale 0.688)
           (RenderZ mide con .name-width-helper y aplica transform scaleX)

Salida:
  cards_full/           (por rareza, ej. Master_Rare/p20801_AS.png -> pero nombre final card_20801.png)
  cards_full_manifest.csv/json

Uso:
  python generate_full_cards.py --test
  python generate_full_cards.py --limit 100
  python generate_full_cards.py
  python generate_full_cards.py --only-ids 20801,158023,235329,167495
"""
from __future__ import annotations
import argparse, csv, json, random, re, unicodedata
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
FONTS_DIR = BASE_DIR / "fonts"
CARDS_DIR = BASE_DIR / "cards_full"
ASSETS_DIR = BASE_DIR / "assets_cards"  # fondos + clubs cache
ASSETS_DIR.mkdir(exist_ok=True)
FONTS_DIR.mkdir(exist_ok=True)
CARDS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

CDN_BG = "https://cdn-p2.frzdb.net/fifamobile/images/backgrounds_18/backgrounds_{code}.png?v=848rffjv3we"
CDN_CLUB = "https://cdn-p2.frzdb.net/fifamobile/images/clubLogos_18/{club_id}.png?v=848rffjv3we"
FONT_MEDIUM_URL = "https://fonts.frzdb.net/Knul-Medium.woff"
FONT_REGULAR_URL = "https://fonts.frzdb.net/Knul-Regular.woff"

DB_JSON = BASE_DIR / "fifa_mobile_18_base.json"
CACHE_CARDS = DATA_DIR / "cache_full_cards.jsonl"
MANIFEST_CSV = BASE_DIR / "cards_full_manifest.csv"
MANIFEST_JSON = BASE_DIR / "cards_full_manifest.json"

USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"]

def sanitize(s):
    if s is None: return ""
    s=str(s)
    # nombres en carta: ASCII sin tildes, uppercase (como RenderZ: name es short uppercase)
    s=unicodedata.normalize("NFKD", s)
    s="".join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r"[^A-Za-z0-9 .'\-]", " ", s)
    return re.sub(r"\s+"," ",s).strip()

def fetch_bytes(url, timeout=25):
    for attempt in range(3):
        try:
            req=urllib.request.Request(url, headers={"User-Agent": random.choice(USER_AGENTS)})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, b""
        except Exception as e:
            if attempt==2: raise
            import time; time.sleep(0.5)
    return 0, b""

def log(m): print(f"[{__import__('datetime').datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

def ensure_fonts():
    med_ttf = FONTS_DIR/"Knul-Medium.ttf"
    reg_ttf = FONTS_DIR/"Knul-Regular.ttf"
    if med_ttf.exists() and reg_ttf.exists():
        return med_ttf, reg_ttf
    # descargar woff y convertir con fontTools
    from fontTools.ttLib import TTFont
    for url, name in [(FONT_MEDIUM_URL,"Knul-Medium"), (FONT_REGULAR_URL,"Knul-Regular")]:
        woff = FONTS_DIR/f"{name}.woff"
        if not woff.exists():
            status, data = fetch_bytes(url)
            if status!=200: raise RuntimeError(f"font {url} HTTP {status}")
            woff.write_bytes(data)
            print(f" font descargada {name} {len(data)}")
        ttf = FONTS_DIR/f"{name}.ttf"
        if not ttf.exists():
            f=TTFont(woff); f.flavor=None; f.save(ttf)
            print(f" font convertida {ttf}")
    return med_ttf, reg_ttf

def download_assets(db_players):
    # fondos
    codes = sorted(set(p["background_code"] for p in db_players if p.get("background_code")))
    bg_dir = ASSETS_DIR/"backgrounds"; bg_dir.mkdir(exist_ok=True)
    for code in codes:
        dest = bg_dir/f"backgrounds_{code}.png"
        if dest.exists() and dest.stat().st_size>0: continue
        status, data = fetch_bytes(CDN_BG.format(code=code))
        if status!=200: print(f" ! fondo {code} HTTP {status}")
        else: dest.write_bytes(data); print(f" fondo {code} {len(data)}")
    # clubs
    club_ids = sorted(set(int(p["club_id"]) for p in db_players if p.get("club_id")))
    club_dir = ASSETS_DIR/"clubs"; club_dir.mkdir(exist_ok=True)
    missing=[cid for cid in club_ids if not (club_dir/f"{cid}.png").exists()]
    print(f" clubs: {len(club_ids)} total, {len(missing)} por descargar")
    def dl(cid):
        status, data = fetch_bytes(CDN_CLUB.format(club_id=cid))
        if status==200 and data[:8]==b'\x89PNG\r\n\x1a\n':
            (club_dir/f"{cid}.png").write_bytes(data)
            return (cid, True)
        return (cid, False)
    if missing:
        with ThreadPoolExecutor(max_workers=12) as ex:
            for cid, ok in ex.map(dl, missing):
                if not ok: print(f"  ! club {cid} fallo")
    print(f" clubs listos en {club_dir}")

def load_db():
    d=json.load(open(DB_JSON, encoding="utf-8"))
    return d["players"]

def find_player_png(fifa_id, rarity):
    # buscar en players_png/ por rareza y cualquier variante
    rarity_dir = (rarity or "SinRareza").replace(" ", "_")
    folder = BASE_DIR/"players_png"/rarity_dir
    if folder.exists():
        # p{id}.png, p{id}_AS.png, p{id}_AS2.png, p{id}_X.png?
        for cand in folder.glob(f"p{fifa_id}*.png"):
            return cand
    # fallback buscar en cualquier subcarpeta
    for cand in (BASE_DIR/"players_png").rglob(f"p{fifa_id}*.png"):
        return cand
    return None

# Layout fm18 a 256
SIZE=256
CLUB_X = int(round(0.19*SIZE)); CLUB_Y = int(round(0.46*SIZE)); CLUB_S = 40
RATING_X = 0.193*SIZE; RATING_Y = 0.15*SIZE; RATING_SIZE=42
POS_X = 0.20*SIZE; POS_Y = 0.345*SIZE; POS_SIZE=18
NAME_Y = 0.665*SIZE; NAME_SIZE=20; NAME_MAX_W=130  # medido: Ronaldo 189*0.687=130

def compose_card(player, bg_image, club_image, player_image, font_medium_path, font_regular_path):
    # canvas RGBA 256
    canvas = Image.new("RGBA", (SIZE,SIZE), (0,0,0,0))
    # fondo
    bg = bg_image.convert("RGBA").resize((SIZE,SIZE), Image.LANCZOS)
    canvas.alpha_composite(bg, (0,0))
    # jugador
    if player_image is not None:
        pl = player_image.convert("RGBA").resize((SIZE,SIZE), Image.LANCZOS)
        canvas.alpha_composite(pl, (0,0))
    # club 40x40
    if club_image is not None:
        cl = club_image.convert("RGBA").resize((CLUB_S,CLUB_S), Image.LANCZOS)
        canvas.alpha_composite(cl, (CLUB_X,CLUB_Y))
    draw = ImageDraw.Draw(canvas)
    # OVR
    ovr_text = str(player["ovr_mobile"])
    font_rating = ImageFont.truetype(str(font_medium_path), RATING_SIZE)
    # sombra 0,0.5px negro (a 256, 0.5px)
    draw.text((RATING_X, RATING_Y+0.5), ovr_text, font=font_rating, fill=(0,0,0,255))
    draw.text((RATING_X, RATING_Y), ovr_text, font=font_rating, fill=(255,255,255,255))
    # posicion
    pos_text = sanitize(player["position_mobile"]).upper()
    font_pos = ImageFont.truetype(str(font_regular_path), POS_SIZE)
    draw.text((POS_X, POS_Y), pos_text, font=font_pos, fill=(255,255,255,255))
    # nombre: short uppercase, centrado, compresion SOLO horizontal si >130 (como RenderZ transform scaleX)
    # RenderZ: name div top 66.5% (170.2px), height 24px (20px*1.2), texto medido 129.9x23px para Ronaldo.
    # Antes se escalaba tambien en vertical -> texto mas pequeno y centrado alto. Corregido:
    # - altura intacta (20px), solo se comprime ancho a 130px
    # - centro vertical del glifo alineado al centro del div original (170.2+12=182.2px), no al top
    name_text = sanitize(player.get("short_name") or player.get("full_name") or "").upper()
    font_name = ImageFont.truetype(str(font_medium_path), NAME_SIZE)
    bbox = draw.textbbox((0,0), name_text, font=font_name)
    text_w = bbox[2]-bbox[0]
    text_h = bbox[3]-bbox[1]
    name_center_y = NAME_Y + (NAME_SIZE*1.2)/2  # 182.2px a 256
    if text_w > NAME_MAX_W:
        pad=4
        tmp = Image.new("RGBA", (text_w+pad*2, text_h+pad*2), (0,0,0,0))
        td = ImageDraw.Draw(tmp)
        td.text((pad-bbox[0], pad-bbox[1]), name_text, font=font_name, fill=(255,255,255,255))
        # SOLO horizontal: ancho -> NAME_MAX_W, alto intacto
        tmp = tmp.resize((NAME_MAX_W, text_h+pad*2), Image.LANCZOS)
        x = (SIZE-NAME_MAX_W)//2
        # centrar verticalmente el glifo en name_center_y
        y = int(round(name_center_y - (text_h+pad*2)/2))
        canvas.alpha_composite(tmp, (x,y))
    else:
        x = (SIZE-text_w)/2 - bbox[0]
        # y tal que el centro del glifo quede en name_center_y
        y = name_center_y - text_h/2 - bbox[1]
        draw.text((x,y), name_text, font=font_name, fill=(255,255,255,255))
    return canvas

def _work_one(args_tuple):
    p, med_ttf, reg_ttf, overwrite = args_tuple
    from PIL import Image as _Image
    fifa_id=int(p["fifa_id"])
    rarity=p.get("rarity") or "SinRareza"
    rarity_dir=rarity.replace(" ","_")
    out_dir=CARDS_DIR/rarity_dir; out_dir.mkdir(parents=True, exist_ok=True)
    out_path=out_dir/f"card_{fifa_id}.png"
    if out_path.exists() and out_path.stat().st_size>0 and not overwrite:
        return {"fifa_id":fifa_id,"name":sanitize(p.get("full_name")),"ovr":p.get("ovr_mobile"),"position":p.get("position_mobile"),"rarity":rarity,"player_png":"","background":p.get("background_code"),"club_id":p.get("club_id"),"dest":str(out_path.relative_to(BASE_DIR)),"size_bytes":out_path.stat().st_size,"status":"ok"}
    player_path=find_player_png(fifa_id, rarity)
    if player_path is None:
        return {"fifa_id":fifa_id,"status":"missing_player_png"}
    try:
        bg_path=ASSETS_DIR/"backgrounds"/f"backgrounds_{p['background_code']}.png"
        bg=_Image.open(bg_path)
        club_path=ASSETS_DIR/"clubs"/f"{p['club_id']}.png"
        club=_Image.open(club_path) if club_path.exists() else None
        player_img=_Image.open(player_path)
        card=compose_card(p, bg, club, player_img, med_ttf, reg_ttf)
        card.save(out_path, "PNG")
        return {"fifa_id":fifa_id,"name":sanitize(p.get("full_name")),"ovr":p.get("ovr_mobile"),"position":p.get("position_mobile"),"rarity":rarity,"player_png":player_path.name,"background":p.get("background_code"),"club_id":p.get("club_id"),"dest":str(out_path.relative_to(BASE_DIR)),"size_bytes":out_path.stat().st_size,"status":"ok"}
    except Exception as e:
        return {"fifa_id":fifa_id,"status":"error","error":str(e)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--only-ids", type=str, default=None)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--overwrite", action="store_true", help="Regenerar aunque exista")
    ap.add_argument("--offset", type=int, default=0)
    args=ap.parse_args()
    if args.test:
        args.only_ids="20801,158023,167495,235329,212218"

    med_ttf, reg_ttf = ensure_fonts()
    print(f"Fuentes originales Knul: {med_ttf} / {reg_ttf}", flush=True)

    db_players = load_db()
    if args.only_ids:
        wanted={int(x.strip()) for x in args.only_ids.split(",") if x.strip()}
        db_players=[p for p in db_players if int(p["fifa_id"]) in wanted]
    if args.offset:
        db_players=db_players[args.offset:]
    if args.limit:
        db_players=db_players[:args.limit]
    print(f"Jugadores a generar: {len(db_players)} workers={args.workers} overwrite={args.overwrite}", flush=True)

    all_players = load_db()
    download_assets(all_players)

    from concurrent.futures import ThreadPoolExecutor, as_completed
    manifest=[]
    done=0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs={ex.submit(_work_one, (p, med_ttf, reg_ttf, args.overwrite)): p for p in db_players}
        for fut in as_completed(futs):
            res=fut.result()
            manifest.append(res)
            done+=1
            if done%500==0 or done==len(db_players):
                print(f"  {done}/{len(db_players)}", flush=True)

    # manifest completo (siempre 13.885)
    all_manifest_map={m["fifa_id"]:m for m in manifest}
    full=[]
    for p in sorted(load_db(), key=lambda x: (-(x.get("ovr_mobile") or 0), x["fifa_id"])):
        m=all_manifest_map.get(int(p["fifa_id"]), {"fifa_id":int(p["fifa_id"]),"status":"pending"})
        full.append({"fifa_id":int(p["fifa_id"]),"name":sanitize(p.get("full_name")),"ovr":p.get("ovr_mobile"),"position":p.get("position_mobile"),"rarity":p.get("rarity"), **{k:m.get(k,"") for k in ("player_png","background","club_id","dest","size_bytes","status")}})
    with MANIFEST_CSV.open("w", newline="", encoding="utf-8") as fh:
        w=csv.DictWriter(fh, fieldnames=list(full[0].keys()), delimiter=";"); w.writeheader(); w.writerows(full)
    MANIFEST_JSON.write_text(json.dumps({"count":len(full),"ok":sum(1 for r in full if r["status"]=="ok"),"players":full}, ensure_ascii=False, indent=2), encoding="utf-8")
    ok=sum(1 for r in full if r["status"]=="ok")
    print(f"OK cartas completas ok={ok}/{len(full)} -> {CARDS_DIR}")

if __name__=="__main__":
    main()
