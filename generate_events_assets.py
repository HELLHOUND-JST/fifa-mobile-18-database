#!/usr/bin/env python3
"""
Genera assets de TODAS las cartas de eventos de FIFA Mobile 18 (Season 2):
  1) PNG del jugador de la carta de evento  (players_18/p{base_id}{_VARIANT}.png)
  2) Logo (icono) del programa/evento        (programs_18/program_{program_icon}.png)
  3) Carta completa 256x256                   (backgrounds_18 + club/icon + Knul, same layout as base)

Reglas:
- Excluye base (<500.000) y 8-digit cross-season ids.
- Para PNG jugador: intenta p{base_fifa_id}_{variant}.png, luego p{base_fifa_id}.png.
- Base fifa_id se resuelve desde data/cache_renderz.jsonl (program_ids_excluded).
- Si no hay club_id pero sí program_icon, el icono del programa va en el slot Club.
- Fondo: backgrounds_18/backgrounds_{background_code}.png. Si no existe, fallback a ER3.
- Fuentes Knul: fonts/Knul-Medium.ttf / Knul-Regular.ttf (ya en el repo).
- Salida:
    events_png/                      (cartas PNG jugador de evento)
    events_logos/                    (program icons)
    events_cards/                    (cartas completas por programa)
    events_manifest.csv / .json
"""
from __future__ import annotations
import argparse, csv, json, random, re, time, unicodedata
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
CACHE_EV   = BASE / "data" / "cache_eventos.jsonl"
CACHE_BASE = BASE / "data" / "cache_renderz.jsonl"
ASSETS     = BASE / "assets_cards"
PNG_OUT    = BASE / "events_png"
LOGO_OUT   = BASE / "events_logos"
CARD_OUT   = BASE / "events_cards"
FONT_MED   = BASE / "fonts" / "Knul-Medium.ttf"
FONT_REG   = BASE / "fonts" / "Knul-Regular.ttf"
MANIFEST   = BASE / "events_manifest.csv"
MANIFEST_J = BASE / "events_manifest.json"

CDN = "https://cdn-p2.frzdb.net/fifamobile/images/{kind}/{filename}?v=848rffjv3we"
SIZE = 256
CLUB_X, CLUB_Y, CLUB_S = 49, 118, 40
RATING_X, RATING_Y, RATING_SIZE = 49, 38, 42
POS_X, POS_Y, POS_SIZE = 51, 88, 18
NAME_Y, NAME_SIZE = 170, 20
NAME_MAX_W = 130
SER_BG = "ER3"

_SPECIAL = {"Ł":"L","ł":"l","Ø":"O","ø":"o","ß":"ss","Æ":"AE","æ":"ae","Œ":"OE","œ":"oe","Ð":"D","ð":"d","Þ":"Th","þ":"th","Đ":"D","đ":"d"}
def sanitize(s):
    if s is None: return ""
    s = str(s)
    for k,v in _SPECIAL.items(): s = s.replace(k,v)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9 .'\-/_]", " ", s)
    return re.sub(r"\s+"," ",s).strip()

def RngNum(seed: int) -> float:
    import hashlib
    return int(hashlib.sha256(str(seed).encode()).hexdigest()[:8], 16) / 0xffffffff

def log(m): print(f"[{__import__('datetime').datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

def fetch_bytes(url, timeout=25):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, b""
        except Exception:
            if attempt == 2: return 0, b""
            time.sleep(0.5*(attempt+1))
    return 0, b""

def load_events():
    out=[]
    for line in open(CACHE_EV, encoding="utf-8", errors="replace"):
        line=line.strip()
        if not line: continue
        try: o=json.loads(line)
        except: continue
        if o.get("status")=="ok": out.append(o)
    return out

def build_program_to_base():
    m={}
    for line in open(CACHE_BASE, encoding="utf-8", errors="replace"):
        try: d=json.loads(line)
        except: continue
        if d.get("status")!="ok": continue
        base_id=d.get("fifa_id")
        for p in d.get("program_ids_excluded", []) or []:
            p=int(p)
            if 500000 <= p < 1000000:
                m[p]=int(base_id)
    return m

def event_output_dir(base_dir: Path, icon: str|None, bg: str|None) -> Path:
    key = sanitize(icon or bg or "unknown").replace(" ", "_") or "unknown"
    return base_dir / key

def resolve_player_file(row, program_to_base):
    fid = int(row["fifa_id"])
    base_id = program_to_base.get(fid)
    variant = row.get("action_variant") or ""
    candidates = []
    if base_id:
        if variant:
            candidates.append(f"p{base_id}_{variant}.png")
        candidates.append(f"p{base_id}.png")
    # fallback: some programs reuse own id prefix with suffix
    if variant:
        candidates.append(f"p{fid}_{variant}.png")
    candidates.append(f"p{fid}.png")
    for c in candidates:
        status, data = fetch_bytes(CDN.format(kind="players_18", filename=c))
        if status == 200 and data and data[:8] == b"\x89PNG\r\n\x1a\n":
            return c, data, status
    return None, b"", 0

def download_assets(events, args):
    program_to_base = build_program_to_base()
    rows = []
    done = 0
    PNG_OUT.mkdir(exist_ok=True)
    LOGO_OUT.mkdir(exist_ok=True)
    CARD_OUT.mkdir(exist_ok=True)

    # backgrounds (parallel)
    from concurrent.futures import ThreadPoolExecutor as TPE
    bg_codes = sorted({e.get("background_code") for e in events if e.get("background_code")})
    bg_cache = {}
    bg_dir = ASSETS / "backgrounds"; bg_dir.mkdir(parents=True, exist_ok=True)

    def dl_bg(code):
        path = bg_dir / f"backgrounds_{code}.png"
        if path.exists() and path.stat().st_size > 0:
            return code, Image.open(path), True
        status, data = fetch_bytes(CDN.format(kind="backgrounds_18", filename=f"backgrounds_{code}.png"))
        if status == 200 and data:
            path.write_bytes(data)
            return code, Image.open(path), True
        return code, None, False

    with TPE(max_workers=12) as ex:
        for code, img, ok in ex.map(dl_bg, bg_codes):
            if ok: bg_cache[code] = img
            else: print(f"  ! bg {code} missing, will use ER3", flush=True)
    bg_cache["_fallback"] = Image.open(bg_dir / f"backgrounds_{SER_BG}.png")

    # club logos (parallel)
    club_cache = {}
    club_dir = ASSETS / "clubs"; club_dir.mkdir(parents=True, exist_ok=True)
    club_ids = sorted({int(e["club_id"]) for e in events if e.get("club_id")})

    def dl_club(cid):
        path = club_dir / f"{cid}.png"
        if path.exists() and path.stat().st_size > 0:
            return cid, Image.open(path), True
        status, data = fetch_bytes(CDN.format(kind="clubLogos_18", filename=f"{cid}.png"))
        if status == 200 and data:
            path.write_bytes(data)
            return cid, Image.open(path), True
        return cid, None, False

    with TPE(max_workers=12) as ex:
        for cid, img, ok in ex.map(dl_club, club_ids):
            club_cache[cid] = img

    # program logos (unique, parallel)
    icons = sorted({e.get("program_icon") for e in events if e.get("program_icon")})
    logo_cache = {}

    def dl_icon(icon):
        path = LOGO_OUT / f"program_{icon}.png"
        if path.exists() and path.stat().st_size > 0:
            return icon, Image.open(path), True
        status, data = fetch_bytes(CDN.format(kind="programs_18", filename=f"program_{icon}.png"))
        if status == 200 and data:
            path.write_bytes(data)
            return icon, Image.open(path), True
        return icon, None, False

    with TPE(max_workers=10) as ex:
        for icon, img, ok in ex.map(dl_icon, icons):
            logo_cache[icon] = img
            if not ok: print(f"  ! program icon {icon} missing", flush=True)

    # fonts
    if not FONT_MED.exists() or not FONT_REG.exists():
        raise RuntimeError(f"Faltan fuentes Knul en {FONT_MED} / {FONT_REG}")

    # helpers for composing cards
    def compose(e, bg, club, player, icon_img=None):
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        canvas.alpha_composite(bg.convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS), (0, 0))
        if player is not None:
            pl = player.convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS)
            canvas.alpha_composite(pl, (0, 0))
        if club is not None:
            cl = club.convert("RGBA").resize((CLUB_S, CLUB_S), Image.LANCZOS)
            canvas.alpha_composite(cl, (CLUB_X, CLUB_Y))
        elif icon_img is not None:
            cl = icon_img.convert("RGBA").resize((CLUB_S, CLUB_S), Image.LANCZOS)
            canvas.alpha_composite(cl, (CLUB_X, CLUB_Y))
        draw = ImageDraw.Draw(canvas)
        font_rating = ImageFont.truetype(str(FONT_MED), RATING_SIZE)
        font_pos    = ImageFont.truetype(str(FONT_REG), POS_SIZE)
        font_name   = ImageFont.truetype(str(FONT_MED), NAME_SIZE)
        # rating (shadow)
        ovr = str(e.get("ovr_mobile") or "")
        draw.text((RATING_X, RATING_Y + 1), ovr, font=font_rating, fill=(0, 0, 0, 255))
        draw.text((RATING_X, RATING_Y),     ovr, font=font_rating, fill=(255, 255, 255, 255))
        pos = sanitize(e.get("position_mobile") or "").upper()
        draw.text((POS_X, POS_Y), pos, font=font_pos, fill=(255, 255, 255, 255))
        name = (e.get("short_name") or e.get("page_name") or e.get("title_name") or "").upper()
        name = sanitize(name)
        bbox = draw.textbbox((0, 0), name, font=font_name)
        w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
        cy = NAME_Y + (NAME_SIZE * 1.2) / 2
        if w > NAME_MAX_W:
            pad = 4
            tmp = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))
            td  = ImageDraw.Draw(tmp)
            td.text((pad-bbox[0], pad-bbox[1]), name, font=font_name, fill=(255, 255, 255, 255))
            tmp = tmp.resize((NAME_MAX_W, h + pad*2), Image.LANCZOS)
            x = (SIZE - NAME_MAX_W) // 2
            canvas.alpha_composite(tmp, (x, int(round(cy - (h + pad*2)/2))))
        else:
            x = (SIZE - w) / 2 - bbox[0]
            y = cy - h / 2 - bbox[1]
            draw.text((x, y), name, font=font_name, fill=(255, 255, 255, 255))
        return canvas

    # download player renders + make cards (parallel)
    def one(e):
        fifa_id = int(e["fifa_id"])
        icon = e.get("program_icon") or ""
        bg_code = e.get("background_code") or SER_BG
        event_dir_png  = event_output_dir(PNG_OUT,  icon, bg_code)
        event_dir_card = event_output_dir(CARD_OUT, icon, bg_code)
        event_dir_png.mkdir(parents=True, exist_ok=True)
        event_dir_card.mkdir(parents=True, exist_ok=True)
        player_file = None
        try:
            player_file, player_data, st = resolve_player_file(e, program_to_base)
            player_img = Image.open(__import__("io").BytesIO(player_data)) if player_file else None
        except Exception as ex:
            player_img = None
        bg = bg_cache.get(bg_code) or bg_cache.get("_fallback")
        club = club_cache.get(int(e["club_id"])) if e.get("club_id") else None
        logo_img = logo_cache.get(icon) if icon else None
        out_player = event_dir_png / f"p{fifa_id}.png"
        if player_img is not None:
            player_img.save(out_player)
        out_card = event_dir_card / f"card_{fifa_id}.png"
        try:
            card = compose(e, bg, club, player_img, logo_img)
            card.save(out_card, "PNG")
            card_ok = True
        except Exception as ex:
            card_ok = False
        return {
            "fifa_id": fifa_id, "program_id_detected": fifa_id,
            "page_name": e.get("page_name"), "ovr": e.get("ovr_mobile"),
            "position": e.get("position_mobile"), "background_code": bg_code,
            "program_icon": icon, "club_id": e.get("club_id"),
            "player_png": str(out_player.relative_to(BASE)) if player_img is not None else "",
            "player_file": player_file or "",
            "card": str(out_card.relative_to(BASE)) if card_ok else "",
            "logo_png": str((LOGO_OUT / f"program_{icon}.png").relative_to(BASE)) if icon and icon in logo_cache and logo_cache[icon] is not None else "",
            "program_logo_file": f"program_{icon}.png" if icon else "",
            "status": "ok" if card_ok else "card_error",
        }

    todo = events
    if args.limit: todo = todo[:args.limit]
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(one, e): e for e in todo}
        for fut in as_completed(futs):
            res = fut.result()
            rows.append(res)
            done += 1
            if done % 200 == 0 or done == len(todo):
                log(f"  eventos assets {done}/{len(todo)}")
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--export-only", action="store_true")
    args = ap.parse_args()
    events = load_events()
    print(f"Eventos: {len(events)}")
    rows = download_assets(events, args)
    with MANIFEST.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys() if rows else []), delimiter=";")
        w.writeheader(); w.writerows(rows)
    MANIFEST_J.write_text(json.dumps({"count": len(rows), "ok": sum(1 for r in rows if r["status"]=="ok"), "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK manifest {MANIFEST} ({len(rows)} rows, {sum(1 for r in rows if r['status']=='ok')} card_ok)")

if __name__ == "__main__":
    main()
