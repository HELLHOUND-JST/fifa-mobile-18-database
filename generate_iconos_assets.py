#!/usr/bin/env python3
"""
Genera assets de las 69 cartas Icono / Prime Icon / WC Icon de FIFA Mobile 18:

  1) PNG render del jugador de la carta   (CDN players_18  / players_18wc)
  2) Logo del programa                     program_17_ICONS.png / program_17_WCICON.png
       (Prime Icons no muestran icono de programa en RenderZ -> sin logo)
  3) Logo de equipo/club/bandera           icons: clubLogos_18/112658.png (Icon/Prime)
       wx: club_id de bandera por país (flag, ya local para los 11 países)
  4) Carta completa 256x256                (background_LR5 / WC_ICON_M/E + jugador + club + Knul)

Layout exacto RenderZ .player-card-fm18 (igual que base/eventos):
  rating 42px Knul Medium (blanco, sombra negra), posición 18px Knul Regular,
  nombre 20px Knul Medium uppercase centrado (capa comprimida si >130px),
  nombre vertical centrado en top 66.5% con la regla +12px,
  club 40x40 en (49,118).

Salida:
  icons_png/{Icon,Prime_Icon,WC_Icon}/<archivo original CDN>
  icons_logos/program_17_ICONS.png / program_17_WCICON.png  (cuando aplica)
  icons_cards/{Icon,Prime_Icon,WC_Icon}/card_{fifa_id}.png
  icons_manifest.csv / .json
"""
from __future__ import annotations
import argparse, csv, io, json, sys, unicodedata, re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
ICONOS_JSON = BASE / "fifa_mobile_18_iconos.json"
RZ_CACHE   = BASE / "data" / "cache_iconos_rz.jsonl"
ASSETS     = BASE / "assets_cards"
PNG_OUT    = BASE / "icons_png"
LOGO_OUT   = BASE / "icons_logos"
CARD_OUT   = BASE / "icons_cards"
MANIFEST   = BASE / "icons_manifest.csv"
MANIFEST_J = BASE / "icons_manifest.json"
FONT_MED   = BASE / "fonts" / "Knul-Medium.ttf"
FONT_REG   = BASE / "fonts" / "Knul-Regular.ttf"

CDN  = "https://cdn-p2.frzdb.net/fifamobile/images/{kind}/{filename}?v=848rffjv3we"
SIZE = 256
CLUB_X, CLUB_Y, CLUB_S = 49, 118, 40
RATING_X, RATING_Y, RATING_SIZE = 49, 38, 42
POS_X, POS_Y, POS_SIZE = 51, 88, 18
NAME_Y, NAME_SIZE = 170, 20
NAME_MAX_W = 130
SER_BG = "LR5"

# Program icons only for rarities that show them on RenderZ
PROGRAM_FOR_RARITY = {"Icon": "program_17_ICONS.png", "WC Icon": "program_17_WCICON.png"}

def log(m): __import__("builtins").print(f"[{__import__('datetime').datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

def fetch_bytes(url, timeout=25):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, b""
        except Exception:
            if attempt == 2:
                return 0, b""
            time.sleep(0.5*(attempt+1))
    return 0, b""

def is_png(data: bytes) -> bool:
    return bool(data) and data[:8] == b"\x89PNG\r\n\x1a\n"

def out_dir_for(rarity: str) -> str:
    return {"Icon": "Icon", "Prime Icon": "Prime_Icon", "WC Icon": "WC_Icon"}.get(rarity, "Other")

def load_iconos():
    data = json.loads(ICONOS_JSON.read_text(encoding="utf-8"))
    cache = {}
    if RZ_CACHE.exists():
        for line in open(RZ_CACHE, encoding="utf-8", errors="replace"):
            try:
                o = json.loads(line)
                cache[int(o["fifa_id"])] = o
            except Exception:
                pass
    rows = []
    for p in data["players"]:
        fid = int(p["fifa_id"])
        c = cache.get(fid, {})
        action = p["card"]["action_shot"] or c.get("action_shot") or ""
        image_url = c.get("player_image_url") or ""
        bg = p["card"]["background_code"] or c.get("background_code") or SER_BG
        player_kind = "players_18wc" if image_url.startswith("players_18wc/") else "players_18"
        if not action:
            if image_url.startswith("players_18wc/"):
                action = image_url.split("/", 1)[1]          # p570.png
            elif action == "":
                action = image_url.split("/", 1)[1] if "/" in image_url else image_url
        rarity = p["card"]["rarity"]
        rows.append({
            "fifa_id": fid,
            "name": p["name"]["short"],
            "ovr_mobile": p["card"]["ovr"],
            "position_mobile": p["card"]["position"],
            "rarity": rarity,
            "background_code": bg,
            "club_id": p["card"]["club_id"],
            "action_shot": action,
            "player_kind": player_kind,
            "program_icon": PROGRAM_FOR_RARITY.get(rarity, ""),
            "renderz_url": p["card"]["renderz_url"],
        })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    rows = load_iconos()
    if args.limit:
        rows = rows[: args.limit]
    log(f"Iconos: {len(rows)}")

    PNG_OUT.mkdir(exist_ok=True); LOGO_OUT.mkdir(exist_ok=True); CARD_OUT.mkdir(exist_ok=True)
    bc_dir = ASSETS / "backgrounds"; bc_dir.mkdir(parents=True, exist_ok=True)
    cl_dir = ASSETS / "clubs"; cl_dir.mkdir(parents=True, exist_ok=True)
    bg_dir = bc_dir

    # ---------- backgrounds (parallel download if missing) ----------
    wanted_bg = sorted({r["background_code"] for r in rows})

    def dl_bg(code):
        path = bg_dir / f"backgrounds_{code}.png"
        if path.exists() and path.stat().st_size > 0:
            return code, True, "cached"
        status, data = fetch_bytes(CDN.format(kind="backgrounds_18", filename=f"backgrounds_{code}.png"))
        if status == 200 and is_png(data):
            path.write_bytes(data)
            return code, True, "downloaded"
        return code, False, f"status {status}"

    # local copies LR5 exist; WC_ICON_* probably missing -> download
    with ThreadPoolExecutor(max_workers=8) as ex:
        for code, ok, how in ex.map(dl_bg, wanted_bg):
            log(f"  bg {code}: {'ok (' + how + ')' if ok else 'FALTA'}")
    bg_files = {code: bg_dir / f"backgrounds_{code}.png" for code in wanted_bg}
    if not bg_files[SER_BG].exists():
        raise RuntimeError("Falta backgrounds_LR5.png (fallback)")

    # ---------- club / flag logos ----------
    # Icons/Prime: club 112658 (download). WC: club_id bandera (local).
    def dl_club(cid):
        path = cl_dir / f"{cid}.png"
        if path.exists() and path.stat().st_size > 0:
            return int(cid), True
        status, data = fetch_bytes(CDN.format(kind="clubLogos_18", filename=f"{cid}.png"))
        if status == 200 and is_png(data):
            path.write_bytes(data)
            return int(cid), True
        return int(cid), False

    club_ids = sorted({int(r["club_id"]) for r in rows if r["club_id"]})
    club_ok = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for cid, ok in ex.map(dl_club, [str(c) for c in club_ids]):
            club_ok[cid] = ok
    for cid in club_ids:
        log(f"  club {cid}: {'ok' if club_ok[cid] else 'FALTA'}")

    # ---------- program logos ----------
    wanted_program = sorted({r["program_icon"] for r in rows if r["program_icon"]})
    program_ok = {}

    def dl_program(icon):
        path = LOGO_OUT / icon
        if path.exists() and path.stat().st_size > 0:
            return icon, True
        status, data = fetch_bytes(CDN.format(kind="programs_18", filename=icon))
        if status == 200 and is_png(data):
            path.write_bytes(data)
            return icon, True
        return icon, False

    with ThreadPoolExecutor(max_workers=4) as ex:
        for icon, ok in ex.map(dl_program, wanted_program):
            program_ok[icon] = ok
    for icon in wanted_program:
        log(f"  programa {icon}: {'ok' if program_ok[icon] else 'FALTA'}")

    # ---------- fonts ----------
    if not FONT_MED.exists() or not FONT_REG.exists():
        raise RuntimeError(f"Faltan fuentes Knul en {FONT_MED} / {FONT_REG}")

    # ---------- compose ----------
    def compose(e, bg_img, club_img, player_img, program_img):
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        canvas.alpha_composite(bg_img.convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS), (0, 0))
        if player_img is not None:
            pl = player_img.convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS)
            canvas.alpha_composite(pl, (0, 0))
        # slot club: club/bandera si hay; si no, icono de programa; si nada, sin logo
        logo = club_img or program_img
        if logo is not None:
            cl = logo.convert("RGBA").resize((CLUB_S, CLUB_S), Image.LANCZOS)
            canvas.alpha_composite(cl, (CLUB_X, CLUB_Y))
        draw = ImageDraw.Draw(canvas)
        font_rating = ImageFont.truetype(str(FONT_MED), RATING_SIZE)
        font_pos    = ImageFont.truetype(str(FONT_REG), POS_SIZE)
        font_name   = ImageFont.truetype(str(FONT_MED), NAME_SIZE)
        ovr = str(e["ovr_mobile"])
        draw.text((RATING_X, RATING_Y + 1), ovr, font=font_rating, fill=(0, 0, 0, 255))
        draw.text((RATING_X, RATING_Y),     ovr, font=font_rating, fill=(255, 255, 255, 255))
        draw.text((POS_X, POS_Y), e["position_mobile"].upper(), font=font_pos, fill=(255, 255, 255, 255))
        name = re.sub(r"[^A-Za-z0-9 .'\-]", " ", unicodedata.normalize("NFKD", e["name"])).upper()
        name = re.sub(r"\s+", " ", name).strip()
        bbox = draw.textbbox((0, 0), name, font=font_name)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        cy = NAME_Y + (NAME_SIZE * 1.2) / 2
        if w > NAME_MAX_W:
            pad = 4
            tmp = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))
            td = ImageDraw.Draw(tmp)
            td.text((pad - bbox[0], pad - bbox[1]), name, font=font_name, fill=(255, 255, 255, 255))
            tmp = tmp.resize((NAME_MAX_W, h + pad*2), Image.LANCZOS)
            x = (SIZE - NAME_MAX_W) // 2
            canvas.alpha_composite(tmp, (x, int(round(cy - (h + pad*2)/2))))
        else:
            x = (SIZE - w) / 2 - bbox[0]
            y = cy - h / 2 - bbox[1]
            draw.text((x, y), name, font=font_name, fill=(255, 255, 255, 255))
        return canvas

    # ---------- one card job ----------
    def one(e):
        rarity = e["rarity"]
        rdir = out_dir_for(rarity)
        d_png  = PNG_OUT / rdir;  d_png.mkdir(parents=True, exist_ok=True)
        d_card = CARD_OUT / rdir; d_card.mkdir(parents=True, exist_ok=True)
        out_player = d_png / e["action_shot"]
        player_img = None
        player_status = "missing"
        if e["action_shot"]:
            if out_player.exists() and out_player.stat().st_size > 0:
                # validate PNG magic
                with open(out_player, "rb") as fh: magic = fh.read(8)
                if magic == b"\x89PNG\r\n\x1a\n":
                    player_img = Image.open(out_player).convert("RGBA"); player_status = "cached"
            if player_img is None:
                status, data = fetch_bytes(CDN.format(kind=e["player_kind"], filename=e["action_shot"]))
                if status == 200 and is_png(data):
                    out_player.write_bytes(data)
                    player_img = Image.open(io.BytesIO(data)).convert("RGBA")
                    player_status = "downloaded"
                else:
                    player_status = f"status {status}"
        else:
            player_status = "no_action_shot"

        bg_code = e["background_code"]
        bg_path = bg_dir / f"backgrounds_{bg_code}.png"
        if not bg_path.exists():
            bg_path = bg_dir / f"backgrounds_{SER_BG}.png"
            bg_code = SER_BG
        bg_img = Image.open(bg_path).convert("RGBA")

        club_img = None
        if e["club_id"]:
            cp = cl_dir / f"{int(e['club_id'])}.png"
            if cp.exists():
                club_img = Image.open(cp).convert("RGBA")

        # program logo fallback for card slot (not used when club exists, like events)
        prog_path = LOGO_OUT / e["program_icon"] if e["program_icon"] else None
        prog_img = Image.open(prog_path).convert("RGBA") if (prog_path and prog_path.exists()) else None

        card_path = d_card / f"card_{e['fifa_id']}.png"
        try:
            card = compose(e, bg_img, club_img, player_img, prog_img)
            card.save(card_path, "PNG")
            card_ok = True
        except Exception as ex:
            card_ok = False
            log(f"  card {e['fifa_id']} error: {ex}")

        logo_path = None
        if e["program_icon"]:
            lp = LOGO_OUT / e["program_icon"]
            if lp.exists():
                logo_path = lp
        return {
            "fifa_id": e["fifa_id"],
            "rarity": rarity,
            "name": e["name"],
            "ovr": e["ovr_mobile"],
            "position_mobile": e["position_mobile"],
            "background_code": bg_code,
            "club_id": e["club_id"],
            "program_icon": e["program_icon"] or "",
            "player_png": str(out_player.relative_to(BASE)) if player_img is not None else "",
            "player_file": e["action_shot"],
            "player_status": player_status,
            "logo_png": str(logo_path.relative_to(BASE)) if logo_path else "",
            "card": str(card_path.relative_to(BASE)) if card_ok else "",
            "status": "ok" if (card_ok and player_img is not None) else ("card_only" if card_ok else "error"),
        }

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(one, e): e for e in rows}
        done = 0
        out_rows = []
        for fut in as_completed(futs):
            res = fut.result()
            out_rows.append(res)
            done += 1
            if done % 20 == 0 or done == len(rows):
                log(f"  assets {done}/{len(rows)} (ok {sum(1 for r in out_rows if r['status']=='ok')})")

    out_rows.sort(key=lambda r: (r["rarity"], r["fifa_id"]))
    with MANIFEST.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(out_rows)
    MANIFEST_J.write_text(json.dumps({
        "count": len(out_rows),
        "ok": sum(1 for r in out_rows if r["status"] == "ok"),
        "rows": out_rows,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"OK {MANIFEST} ({len(out_rows)} rows)")
    log(f"OK {MANIFEST_J}")
    for path in [PNG_OUT, LOGO_OUT, CARD_OUT]:
        n = len(list(path.rglob("*.png")))
        log(f"{path.name}: {n} png")

if __name__ == "__main__":
    main()
