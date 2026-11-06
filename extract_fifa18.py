#!/usr/bin/env python3
"""
Extractor FIFA Mobile 18 (Temporada 2 / Season 2) - SOLO cartas base, sin programas.

Fuente primaria de media/posicion/club/carta: https://renderz.app/18/player/{fifa_id}
Fuente guia de IDs y datos FIFA18 consola:   https://sofifa.com/?r=180084&set=true

Regla de descarte de programas:
  renderz muestra en cada ficha base una lista de "related cards" con IDs 502xxx, 603xxx, 990xxx...
  Esos IDs NO se insertan como filas. Solo se guarda la ficha cuyo ID == FIFA ID de SoFIFA
  (ej. 20801 Cristiano Ronaldo). Todo ID >= 500000 se considera programa y se excluye.

Salida (ASCII sin tildes ni caracteres especiales para evitar errores en Excel/CSV):
  fifa_mobile_18_base.csv  -> una fila por carta base
  fifa_mobile_18_base.txt  -> misma tabla legible, alineada
  fifa_mobile_18_base.json -> version completa con nombres originales UTF-8
  missing_in_renderz.csv   -> IDs de SoFIFA sin carta base en RenderZ (404)
  programs_excluded.csv    -> IDs de programas detectados en fichas base (NO incluidos en la base)

Registro / actualizacion incremental:
  data/cache_sofifa_list.json  -> lista completa SoFIFA (17976 jugadores aprox)
  data/cache_renderz.jsonl     -> un JSON por línea, append-only, reanuda si se corta
  data/manual_overrides.json   -> correcciones manuales que se aplican al exportar
  data/progress.json           -> contadores y ultima ejecucion

Uso rapido:
  python extract_fifa18.py --test          # prueba con los 10 primeros de SoFIFA
  python extract_fifa18.py --limit 200     # prueba con 200 IDs
  python extract_fifa18.py                 # todo (SoFIFA + RenderZ + export), reanuda solo
  python extract_fifa18.py --export-only   # regenera CSV/TXT/JSON desde cache, sin red
  python extract_fifa18.py --only-ids 20801,158023,190871
  python extract_fifa18.py --set-name 20801 "Cristiano Ronaldo" --set-ovr 20801 90
  python extract_fifa18.py --refresh       # ignora cache y vuelve a descargar todo
"""

from __future__ import annotations
import argparse, csv, json, random, re, sys, time, unicodedata
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.error

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

SOFIFA_BASE = "https://sofifa.com/"
SOFIFA_ROSTER = "180084"
SOFIFA_URL = f"https://sofifa.com/?r={SOFIFA_ROSTER}&set=true"
RENDERZ_TEMPLATE = "https://renderz.app/18/player/{fifa_id}"
SOFIFA_PLAYER_TEMPLATE = "https://sofifa.com/player/{fifa_id}/"

CACHE_SOFIFA = DATA_DIR / "cache_sofifa_list.json"
CACHE_RENDERZ = DATA_DIR / "cache_renderz.jsonl"
OVERRIDES_FILE = DATA_DIR / "manual_overrides.json"
PROGRESS_FILE = DATA_DIR / "progress.json"

CSV_OUT = BASE_DIR / "fifa_mobile_18_base.csv"
TXT_OUT = BASE_DIR / "fifa_mobile_18_base.txt"
JSON_OUT = BASE_DIR / "fifa_mobile_18_base.json"
MISSING_OUT = BASE_DIR / "missing_in_renderz.csv"
PROGRAMS_OUT = BASE_DIR / "programs_excluded.csv"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
]

# ---------- sanitizacion (sin tildes / sin caracteres especiales) ----------
_SPECIAL = {
    "Ł": "L", "ł": "l", "Ø": "O", "ø": "o", "ß": "ss", "Æ": "AE", "æ": "ae",
    "Œ": "OE", "œ": "oe", "Ð": "D", "ð": "d", "Þ": "Th", "þ": "th",
    "Đ": "D", "đ": "d", "Ŋ": "N", "ŋ": "n", "ı": "i",
}
def sanitize(text) -> str:
    """ASCII puro: sin tildes, sin acentos, sin simbolo raro. Seguro para CSV en Excel."""
    if text is None:
        return ""
    s = str(text)
    for k, v in _SPECIAL.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    # solo letras/digitos basicos, punto, guion, apostrofe y espacio
    s = re.sub(r"[^A-Za-z0-9 .'\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def rarity_from_background(code: str) -> str:
    """ER3 -> Epic Rare, MR4 -> Master Rare, BR0 -> Bronze Rare, SR1, GR2..."""
    if not code:
        return ""
    prefix = re.sub(r"\d+$", "", code).upper()
    mapping = {
        "BR": "Bronze Rare", "SR": "Silver Rare", "GR": "Gold Rare",
        "ER": "Epic Rare", "MR": "Master Rare", "CR": "Common Rare",
        "BC": "Bronze Common", "SC": "Silver Common", "GC": "Gold Common",
    }
    return mapping.get(prefix, prefix)

# ---------- red ----------
def fetch_url(url: str, timeout: int = 25) -> tuple[int, str]:
    """Devuelve (status, texto). 404 no es excepcion, se devuelve como status."""
    last_err = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
                return resp.status, body.decode(charset, errors="replace")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception as e:  # red caida, timeout, etc.
            last_err = e
            time.sleep(0.5 * (attempt + 1) + random.random() * 0.5)
    raise RuntimeError(f"No se pudo descargar {url}: {last_err}")

def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# ---------- SoFIFA ----------
def parse_sofifa_page(html: str) -> list[dict]:
    players = []
    # cada fila <tr> contiene un id de jugador
    rows = re.split(r"<tr>", html)
    for row in rows:
        m_id = re.search(r'data-type="player"\s+id="(\d+)"', row)
        if not m_id:
            continue
        fifa_id = int(m_id.group(1))
        m_full = re.search(r'data-tippy-content="([^"]+)"', row)
        full_name = m_full.group(1).strip() if m_full else ""
        # nombre corto: el texto dentro de <a href="/player/...">Texto</a>
        m_short = re.search(r'<a href="/player/[^"]*"[^>]*>([^<]+)</a>', row)
        short_name = m_short.group(1).strip() if m_short else full_name
        flags = re.findall(r'<img title="([^"]+)"[^>]*class="flag', row)
        nationality = flags[0] if flags else ""
        positions = re.findall(r'<span class="pos pos\d+">([^<]+)</span>', row)
        position_sofifa = positions[0] if positions else ""
        def col(name):
            m = re.search(rf'data-col="{name}">([^<]+)</td>', row)
            return m.group(1).strip() if m else ""
        age = col("ae")
        wage = col("wg")
        value = col("vl")
        # Overall / Potential van en <em title="94">94</em>
        ems = re.findall(r'<em title="(\d+)">', row)
        overall = ems[0] if len(ems) > 0 else ""
        potential = ems[1] if len(ems) > 1 else ""
        # total stats es el tercer <em>
        m_tt = re.search(r'data-col="tt"><em>(\d+)</em>', row)
        total_stats = m_tt.group(1) if m_tt else ""
        m_team = re.search(r'<a href="/team/(\d+)/[^"]*/180084/">([^<]+)</a>', row)
        team_id = m_team.group(1) if m_team else ""
        team_name = m_team.group(2).strip() if m_team else ""
        players.append({
            "fifa_id": fifa_id,
            "short_name": short_name or full_name,
            "full_name": full_name or short_name,
            "age": int(age) if age.isdigit() else None,
            "overall_sofifa": int(overall) if overall.isdigit() else None,
            "potential_sofifa": int(potential) if potential.isdigit() else None,
            "total_stats_sofifa": int(total_stats) if total_stats.isdigit() else None,
            "position_sofifa": position_sofifa,
            "positions_sofifa": positions,
            "nationality": nationality,
            "team_id": int(team_id) if team_id.isdigit() else None,
            "team_name": team_name,
            "wage_sofifa": wage,
            "value_sofifa": value,
        })
    return players

def fetch_sofifa_list(refresh: bool = False, limit: int | None = None) -> list[dict]:
    if CACHE_SOFIFA.exists() and not refresh:
        try:
            data = json.loads(CACHE_SOFIFA.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "players" in data:
                plist = data["players"]
                # Si la cache es parcial (de una prueba --test/--limit) y ahora se pide todo sin limit, recargar
                if not data.get("complete", True) and (not limit or (limit and len(plist) < limit)):
                    log("Cache SoFIFA parcial (prueba anterior). Se recarga...")
                else:
                    log(f"SoFIFA cache: {len(plist)} jugadores (sin red). Usa --refresh para recargar.")
                    return plist[:limit] if limit else plist
        except Exception as e:
            log(f"Cache SoFIFA ilegible ({e}), se vuelve a descargar.")
    all_players: dict[int, dict] = {}
    offset = 0
    page = 0
    while True:
        page += 1
        url = f"{SOFIFA_URL}&offset={offset}"
        log(f"SoFIFA pagina {page} offset={offset} ...")
        status, html = fetch_url(url)
        if status != 200 or not html:
            log(f"  ! HTTP {status} en offset {offset}, fin.")
            break
        chunk = parse_sofifa_page(html)
        if not chunk:
            log("  ! Sin jugadores en esta pagina, fin.")
            break
        for p in chunk:
            all_players[p["fifa_id"]] = p
        log(f"  +{len(chunk)} jugadores. Total acumulado {len(all_players)}")
        if limit and len(all_players) >= limit:
            break
        # si la pagina no es completa (75) o no hay Next, termina
        has_next = 'class="button">Next' in html or 'Next <svg' in html
        if len(chunk) < 75 or not has_next:
            log("  Ultima pagina.")
            break
        offset += 75
        time.sleep(0.15)
    players_sorted = sorted(all_players.values(), key=lambda x: (-(x.get("overall_sofifa") or 0), x["fifa_id"]))
    is_complete = not (limit and len(all_players) >= limit)
    # Si es una prueba con --limit, no sobrescribir una cache completa anterior; guardar como parcial
    should_write = is_complete or not CACHE_SOFIFA.exists()
    if should_write:
        CACHE_SOFIFA.write_text(json.dumps({
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source": SOFIFA_URL,
            "count": len(players_sorted),
            "complete": is_complete,
            "players": players_sorted,
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        log(f"SoFIFA guardado en {CACHE_SOFIFA} ({len(players_sorted)} jugadores, complete={is_complete})")
    return players_sorted[:limit] if limit else players_sorted

# ---------- RenderZ ----------
def parse_renderz_page(html: str) -> dict:
    # <h1>Cristiano Ronaldo 90 OVR in FIFA Mobile 18</h1>
    m_h1 = re.search(r"<h1[^>]*>([^<]+?)\s+(\d+)\s+OVR\s+in\s+FIFA Mobile 18</h1>", html)
    full_name = ""
    ovr = None
    if m_h1:
        full_name = m_h1.group(1).strip()
        ovr = int(m_h1.group(2))
    m_bg = re.search(r"backgrounds_18/backgrounds_([A-Za-z0-9]+)\.png", html)
    background_code = m_bg.group(1) if m_bg else ""
    m_club = re.search(r"clubLogos_18/(\d+)\.png", html)
    club_id = int(m_club.group(1)) if m_club else None
    m_pos = re.search(r'class="position[^"]*"[^>]*>([^<]+)</div>', html)
    position = m_pos.group(1).strip() if m_pos else ""
    m_name = re.search(r'class="name[^"]*"[^>]*>([^<]+)</div>', html)
    short_name_card = m_name.group(1).strip() if m_name else ""
    # programas relacionados: IDs /18/player/502xxx, 603xxx, 990xxx... (NO son filas de la base)
    # FIFA IDs base de SoFIFA son < 500000; programas en RenderZ son >= 500000 y de 6 digitos.
    # (IDs de 8 digitos tipo 19020801 son de otras temporadas, no programas de la T2)
    program_ids = sorted({int(x) for x in re.findall(r"/18/player/(\d{6})(?![0-9])", html) if int(x) >= 500000})
    return {
        "full_name_h1": full_name,
        "ovr_mobile": ovr,
        "background_code": background_code,
        "rarity": rarity_from_background(background_code),
        "club_id": club_id,
        "position_mobile": position,
        "short_name_card": short_name_card,
        "program_ids_excluded": program_ids,
    }

def fetch_one_renderz(fifa_id: int) -> dict:
    url = RENDERZ_TEMPLATE.format(fifa_id=fifa_id)
    try:
        status, html = fetch_url(url)
    except Exception as e:
        return {"fifa_id": fifa_id, "status": "error", "error": str(e), "renderz_url": url}
    if status == 404:
        return {"fifa_id": fifa_id, "status": "not_found", "renderz_url": url}
    if status != 200:
        return {"fifa_id": fifa_id, "status": "http_error", "http_status": status, "renderz_url": url}
    parsed = parse_renderz_page(html)
    if parsed["ovr_mobile"] is None:
        return {"fifa_id": fifa_id, "status": "parse_error", "renderz_url": url, **parsed}
    return {"fifa_id": fifa_id, "status": "ok", "renderz_url": url, **parsed}

def load_renderz_cache() -> dict[int, dict]:
    cache: dict[int, dict] = {}
    if not CACHE_RENDERZ.exists():
        return cache
    for line in CACHE_RENDERZ.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            cache[int(obj["fifa_id"])] = obj
        except Exception:
            continue
    return cache

def fetch_renderz_all(sofifa_players: list[dict], workers: int = 8, refresh: bool = False,
                      limit: int | None = None, only_ids: list[int] | None = None):
    cache = {} if refresh else load_renderz_cache()
    targets = [p["fifa_id"] for p in sofifa_players]
    if only_ids:
        targets = [i for i in targets if i in set(only_ids)]
        # ids pedidos que no estan en SoFIFA tambien se intentan
        for i in only_ids:
            if i not in targets:
                targets.append(i)
    if limit:
        targets = targets[:limit]
    todo = [tid for tid in targets if tid not in cache]
    log(f"RenderZ: {len(targets)} IDs objetivo, {len(cache)} en cache, {len(todo)} pendientes.")
    if not todo:
        return cache
    done = 0
    ok = 0
    not_found = 0
    errors = 0
    # append-only: abrimos en modo append y escribimos cada resultado al terminar
    with CACHE_RENDERZ.open("a", encoding="utf-8") as fh:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = {ex.submit(fetch_one_renderz, tid): tid for tid in todo}
            for fut in as_completed(futures):
                tid = futures[fut]
                try:
                    res = fut.result()
                except Exception as e:
                    res = {"fifa_id": tid, "status": "error", "error": str(e), "renderz_url": RENDERZ_TEMPLATE.format(fifa_id=tid)}
                cache[tid] = res
                fh.write(json.dumps(res, ensure_ascii=False) + "\n")
                fh.flush()
                done += 1
                if res.get("status") == "ok":
                    ok += 1
                elif res.get("status") == "not_found":
                    not_found += 1
                else:
                    errors += 1
                if done % 50 == 0 or done == len(todo):
                    log(f"  RenderZ {done}/{len(todo)} (ok={ok}, 404={not_found}, err={errors})")
    save_progress({"renderz_ok": ok, "renderz_404": not_found, "renderz_errors": errors, "renderz_total_intentados": len(todo)})
    return cache

# ---------- registro / progreso / overrides ----------
def save_progress(extra: dict):
    data = {}
    if PROGRESS_FILE.exists():
        try:
            data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data.update(extra)
    data["last_run"] = datetime.now(timezone.utc).isoformat()
    PROGRESS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_overrides() -> dict:
    if not OVERRIDES_FILE.exists():
        return {}
    try:
        return json.loads(OVERRIDES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def apply_overrides(row: dict, overrides: dict) -> dict:
    key = str(row.get("fifa_id"))
    if key in overrides:
        for k, v in overrides[key].items():
            row[k] = v
    return row

# ---------- exportacion ----------
def build_rows(sofifa_players: list[dict], renderz_cache: dict[int, dict]) -> tuple[list[dict], list[dict], list[dict]]:
    sofifa_by_id = {p["fifa_id"]: p for p in sofifa_players}
    rows: list[dict] = []
    missing: list[dict] = []
    programs: list[dict] = []
    overrides = load_overrides()
    for fifa_id in sorted(set(list(sofifa_by_id.keys()) + list(renderz_cache.keys()))):
        r = renderz_cache.get(fifa_id)
        s = sofifa_by_id.get(fifa_id, {})
        if not r or r.get("status") != "ok":
            if s:
                missing.append({
                    "fifa_id": fifa_id,
                    "full_name": sanitize(s.get("full_name", "")),
                    "sofifa_overall": s.get("overall_sofifa", ""),
                    "sofifa_team": sanitize(s.get("team_name", "")),
                    "status": (r or {}).get("status", "no_intentado"),
                    "sofifa_url": SOFIFA_PLAYER_TEMPLATE.format(fifa_id=fifa_id),
                    "renderz_url": RENDERZ_TEMPLATE.format(fifa_id=fifa_id),
                })
            continue
        # programas detectados en esta ficha base (excluidos)
        for pid in r.get("program_ids_excluded", []):
            programs.append({
                "program_id": pid,
                "base_fifa_id": fifa_id,
                "base_name": sanitize(r.get("full_name_h1", "")),
                "program_url": RENDERZ_TEMPLATE.format(fifa_id=pid),
            })
        full_original = r.get("full_name_h1") or s.get("full_name") or ""
        short_original = r.get("short_name_card") or s.get("short_name") or ""
        row = {
            "fifa_id": fifa_id,
            "short_name": sanitize(short_original),
            "full_name": sanitize(full_original),
            "position_mobile": sanitize(r.get("position_mobile", "")),
            "ovr_mobile": r.get("ovr_mobile", ""),
            "club_id": r.get("club_id", "") if r.get("club_id") is not None else "",
            "club_name": sanitize(s.get("team_name", "")),
            "background_code": sanitize(r.get("background_code", "")),
            "rarity": sanitize(r.get("rarity", "")),
            "sofifa_overall": s.get("overall_sofifa", "") if s.get("overall_sofifa") is not None else "",
            "sofifa_potential": s.get("potential_sofifa", "") if s.get("potential_sofifa") is not None else "",
            "sofifa_age": s.get("age", "") if s.get("age") is not None else "",
            "sofifa_position": sanitize(s.get("position_sofifa", "")),
            "nationality": sanitize(s.get("nationality", "")),
            "renderz_url": r.get("renderz_url", RENDERZ_TEMPLATE.format(fifa_id=fifa_id)),
            "sofifa_url": SOFIFA_PLAYER_TEMPLATE.format(fifa_id=fifa_id),
            "season": "Season 2 (FIFA Mobile 18)",
            # campos originales (solo para JSON, el CSV/TXT ya van sanitizados)
            "_full_name_original": full_original,
            "_short_name_original": short_original,
            "_club_name_original": s.get("team_name", ""),
            "_nationality_original": s.get("nationality", ""),
        }
        row = apply_overrides(row, overrides)
        rows.append(row)
    rows.sort(key=lambda x: (-(int(x["ovr_mobile"]) if str(x["ovr_mobile"]).isdigit() else 0), x["fifa_id"]))
    return rows, missing, programs

CSV_FIELDS = ["fifa_id", "short_name", "full_name", "position_mobile", "ovr_mobile", "club_id", "club_name",
              "background_code", "rarity", "sofifa_overall", "sofifa_potential", "sofifa_age",
              "sofifa_position", "nationality", "renderz_url", "sofifa_url", "season"]

def export_all(rows: list[dict], missing: list[dict], programs: list[dict]):
    # CSV (ASCII sanitizado, UTF-8 sin BOM para que Excel lo abra bien)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in CSV_FIELDS})
    # TXT legible y alineado
    max_name = max([len(r["full_name"]) for r in rows], default=30)
    max_name = min(max(max_name, 20), 42)
    with TXT_OUT.open("w", encoding="utf-8") as fh:
        fh.write("FIFA MOBILE 18 - TEMPORADA 2 - CARTAS BASE (sin programas)\n")
        fh.write("Fuente RenderZ: https://renderz.app/18/player/{fifa_id}  |  Guia SoFIFA: https://sofifa.com/?r=180084&set=true\n")
        fh.write(f"Total cartas base: {len(rows)}  |  Generado: {datetime.now(timezone.utc).isoformat()}\n")
        fh.write("Nombres en ASCII sin tildes ni caracteres especiales (ver JSON para nombres originales).\n\n")
        fh.write(f"{'ID':<7} {'OVR':<4} {'POS':<5} {'NOMBRE':<{max_name}} {'CLUB':<28} {'FONDO':<6} {'RARIDAD'}\n")
        fh.write("-" * (7 + 1 + 4 + 1 + 5 + 1 + max_name + 1 + 28 + 1 + 6 + 1 + 14) + "\n")
        for r in rows:
            fh.write(f"{r['fifa_id']:<7} {r['ovr_mobile']:<4} {r['position_mobile']:<5} {r['full_name']:<{max_name}} {r['club_name']:<28} {r['background_code']:<6} {r['rarity']}\n")
    # JSON completo (con originales UTF-8)
    json_rows = []
    for r in rows:
        jr = {k: r.get(k, "") for k in CSV_FIELDS}
        jr["full_name_original"] = r.get("_full_name_original", "")
        jr["short_name_original"] = r.get("_short_name_original", "")
        jr["club_name_original"] = r.get("_club_name_original", "")
        jr["nationality_original"] = r.get("_nationality_original", "")
        json_rows.append(jr)
    JSON_OUT.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "season": "FIFA Mobile 18 Season 2",
        "source_renderz": "https://renderz.app/18/player/{fifa_id}",
        "source_sofifa": SOFIFA_URL,
        "note": "Solo cartas base. Programas (IDs >= 500000 en RenderZ) excluidos y listados en programs_excluded.csv",
        "count": len(json_rows),
        "players": json_rows,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    # missing
    with MISSING_OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["fifa_id", "full_name", "sofifa_overall", "sofifa_team", "status", "sofifa_url", "renderz_url"])
        w.writeheader()
        w.writerows(missing)
    # programas excluidos (deduplicado por program_id)
    seen = {}
    for p in programs:
        seen[p["program_id"]] = p
    with PROGRAMS_OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["program_id", "base_fifa_id", "base_name", "program_url"])
        w.writeheader()
        for pid in sorted(seen):
            w.writerow(seen[pid])
    save_progress({"export_rows": len(rows), "export_missing": len(missing), "export_programs_distinct": len(seen)})
    log(f"Exportado: {CSV_OUT.name} ({len(rows)} filas), {TXT_OUT.name}, {JSON_OUT.name}, {MISSING_OUT.name} ({len(missing)}), {PROGRAMS_OUT.name} ({len(seen)} programas excluidos)")

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser(description="FIFA Mobile 18 Season 2 - cartas base (sin programas)")
    ap.add_argument("--test", action="store_true", help="Prueba rapida: 10 primeros IDs de SoFIFA")
    ap.add_argument("--limit", type=int, default=None, help="Limitar a N IDs de SoFIFA (prueba)")
    ap.add_argument("--workers", type=int, default=8, help="Hilos concurrentes para RenderZ (defecto 8)")
    ap.add_argument("--refresh", action="store_true", help="Ignorar cache y descargar todo de nuevo")
    ap.add_argument("--export-only", action="store_true", help="Solo regenerar CSV/TXT/JSON desde cache")
    ap.add_argument("--only-ids", type=str, default=None, help='Solo estos IDs, ej. "20801,158023"')
    ap.add_argument("--set-name", nargs=2, metavar=("ID", "NOMBRE"), action="append", default=[],
                    help='Correccion manual, ej. --set-name 20801 "Cristiano Ronaldo"')
    ap.add_argument("--set-ovr", nargs=2, metavar=("ID", "OVR"), action="append", default=[],
                    help='Correccion manual de OVR, ej. --set-ovr 20801 91')
    args = ap.parse_args()

    # overrides manuales
    if args.set_name or args.set_ovr:
        ov = load_overrides()
        for fid, nombre in args.set_name:
            ov.setdefault(str(fid), {})["full_name"] = sanitize(nombre)
        for fid, ovr in args.set_ovr:
            ov.setdefault(str(fid), {})["ovr_mobile"] = int(ovr)
        OVERRIDES_FILE.write_text(json.dumps(ov, ensure_ascii=False, indent=2), encoding="utf-8")
        log(f"Overrides guardados en {OVERRIDES_FILE}: {ov}")

    if args.test:
        args.limit = 10

    only_ids = None
    if args.only_ids:
        only_ids = [int(x.strip()) for x in args.only_ids.split(",") if x.strip()]

    if args.export_only:
        log("Modo --export-only: leyendo caches...")
        sofifa_players = []
        if CACHE_SOFIFA.exists():
            sofifa_players = json.loads(CACHE_SOFIFA.read_text(encoding="utf-8"))["players"]
        renderz_cache = load_renderz_cache()
        if not renderz_cache:
            log("! No hay cache de RenderZ. Ejecuta sin --export-only primero.")
            sys.exit(1)
        rows, missing, programs = build_rows(sofifa_players, renderz_cache)
        export_all(rows, missing, programs)
        return

    sofifa_players = fetch_sofifa_list(refresh=args.refresh, limit=args.limit)
    renderz_cache = fetch_renderz_all(
        sofifa_players, workers=args.workers, refresh=args.refresh,
        limit=args.limit, only_ids=only_ids,
    )
    rows, missing, programs = build_rows(sofifa_players, renderz_cache)
    export_all(rows, missing, programs)
    log("Listo. Revisa fifa_mobile_18_base.csv / .txt / .json")
    log("Para actualizar despues: vuelve a ejecutar el mismo comando (reanuda solo) o usa --export-only tras editar data/manual_overrides.json")

if __name__ == "__main__":
    main()
