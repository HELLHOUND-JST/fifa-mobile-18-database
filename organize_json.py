#!/usr/bin/env python3
"""
Reorganiza el JSON de estadisticas en una estructura clara y documentada.

Entrada:
  fifa_mobile_18_base.json              (base RenderZ/SoFIFA con tipos correctos y nombres originales)
  fifa_mobile_18_base_stats_generadas.csv (stats: 271 originales guia + 13.614 generadas, delimitador ';')
  guide_base_stats.json                 (extra guia: skill_boosts, league, country, url)

Salida principal:
  fifa_mobile_18_base_stats_organized.json  (estructura por secciones, tipos int/null, documentado)
  fifa_mobile_18_base_stats_organized_SAMPLE.json (solo esquema + 3 ejemplos, para ver rapido)
  README_JSON.md

Estructura de cada jugador:
  {
    "fifa_id": int,
    "name": {"short","full","short_original","full_original"},
    "card": {"ovr","position","club_id","club","club_original","rarity","background_code","season"},
    "sofifa_fifa18_console": {"overall","potential","age","position","nationality","nationality_original"},
    "links": {"renderz","sofifa","guide"},
    "stats": {
      "source": "guide_original" | "generated_template_sofifa",
      "source_description": "...",
      "primary": {...},       // 6 primarios (campo) o 6 de portero (GK)
      "detailed": {...},      // 20 detallados (campo) o 16 detallados (GK, sin tiro)
      "goalkeeping": {...} | null,  // solo GK: gk_diving, gk_positioning, reflexes, handling
      "guide_extra": {...} | null   // solo guide_original: skill_boosts, league, country, last_updated
    }
  }
"""
from __future__ import annotations
import csv, json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent
DB_JSON = BASE_DIR / "fifa_mobile_18_base.json"
GEN_CSV = BASE_DIR / "fifa_mobile_18_base_stats_generadas.csv"
GUIDE_JSON = BASE_DIR / "guide_base_stats.json"
OUT_JSON = BASE_DIR / "fifa_mobile_18_base_stats_organized.json"
OUT_SAMPLE = BASE_DIR / "fifa_mobile_18_base_stats_organized_SAMPLE.json"

def to_int_or_none(v):
    if v is None or v == "":
        return None
    try:
        return int(v)
    except:
        return None

def read_gen_csv():
    rows = list(csv.DictReader(open(GEN_CSV, encoding="utf-8"), delimiter=";"))
    by_id = {str(r["fifa_id"]): r for r in rows}
    return by_id

def main():
    db = json.load(open(DB_JSON, encoding="utf-8"))
    db_players = db["players"]
    gen_by_id = read_gen_csv()
    guide = json.load(open(GUIDE_JSON, encoding="utf-8"))
    guide_by_id = {str(p["fifa_id"]): p for p in guide["players"] if p.get("fifa_id")}

    # stats fields mapping
    PRIMARY_FIELD = ["pace","shooting","passing","agility","defending","physical"]
    PRIMARY_GK = ["gk_diving","gk_positioning","handling","reflexes","passing","physical"]
    DETAILED_FIELD = ["sprint_speed","acceleration","strength","ball_control","dribbling","heading","finishing","shot_power","long_shot","positioning","tackling","marking","aggression","composure","awareness","reactions","free_kick","short_passing","long_passing","crossing"]
    DETAILED_GK = ["sprint_speed","acceleration","strength","ball_control","dribbling","heading","tackling","marking","aggression","composure","awareness","reactions","free_kick","short_passing","long_passing","crossing"]
    GK_FIELDS = ["gk_diving","gk_positioning","reflexes","handling"]

    players = []
    counts = Counter()
    for p in db_players:
        fid = str(p["fifa_id"])
        g = gen_by_id.get(fid, {})
        is_gk = p["position_mobile"] == "GK"
        source = g.get("stats_source", "generated_template_sofifa")
        counts[source] += 1

        # stats con tipos correctos
        if is_gk:
            primary = {k: to_int_or_none(g.get(k)) for k in PRIMARY_GK}
            detailed = {k: to_int_or_none(g.get(k)) for k in DETAILED_GK}
            goalkeeping = {k: to_int_or_none(g.get(k)) for k in GK_FIELDS}
        else:
            primary = {k: to_int_or_none(g.get(k)) for k in PRIMARY_FIELD}
            detailed = {k: to_int_or_none(g.get(k)) for k in DETAILED_FIELD}
            goalkeeping = None

        guide_extra = None
        guide_url_obj = g.get("guide_url") or None
        if fid in guide_by_id:
            gp = guide_by_id[fid]
            guide_extra = {
                "skill_boosts": gp.get("guide_skill_boosts") or None,
                "league": gp.get("guide_league") or None,
                "country": gp.get("guide_country") or None,
                "program": gp.get("guide_program") or None,
                "rarity_in_guide": gp.get("guide_rarity") or None,
                "last_updated_in_guide": gp.get("guide_last_updated") or None,
                "match_method": gp.get("match_method"),
            }
            if not guide_url_obj:
                guide_url_obj = gp.get("guide_url")

        player = {
            "fifa_id": p["fifa_id"],
            "name": {
                "short": p.get("short_name"),
                "full": p.get("full_name"),
                "short_original": p.get("short_name_original"),
                "full_original": p.get("full_name_original"),
            },
            "card": {
                "ovr": p.get("ovr_mobile"),
                "position": p.get("position_mobile"),
                "club_id": p.get("club_id"),
                "club": p.get("club_name"),
                "club_original": p.get("club_name_original"),
                "rarity": p.get("rarity"),
                "background_code": p.get("background_code"),
                "season": p.get("season"),
            },
            "sofifa_fifa18_console": {
                "overall": p.get("sofifa_overall"),
                "potential": p.get("sofifa_potential"),
                "age": p.get("sofifa_age"),
                "position": p.get("sofifa_position"),
                "nationality": p.get("nationality"),
                "nationality_original": p.get("nationality_original"),
            },
            "links": {
                "renderz": p.get("renderz_url"),
                "sofifa": p.get("sofifa_url"),
                "guide": guide_url_obj,
            },
            "stats": {
                "source": source,
                "source_description": (
                    "Estadisticas ORIGINALES de fifamobileguide.com, no modificadas ni un numero."
                    if source == "guide_original" else
                    "Generadas con plantilla por posicion (guia 277) + escalado a OVR Mobile + delta SoFIFA overall + jitter determinista por fifa_id. Ver README_STATS_GENERADAS.md"
                ),
                "primary": primary,
                "detailed": detailed,
                "goalkeeping": goalkeeping,
                "guide_extra": guide_extra,
            }
        }
        # Nota especial para el error de fuente Bale
        if fid == "173731":
            player["stats"]["_nota_fuente"] = "La guia trae Heading 866 para Bale (error tipografico en la fuente, deberia ser 86). Se conserva tal cual por fidelidad; no se usa para plantillas."
        players.append(player)

    # Orden ya viene por ovr desc en DB, pero asegurar
    players.sort(key=lambda x: (-(x["card"]["ovr"] or 0), x["fifa_id"]))

    metadata = {
        "title": "FIFA Mobile 18 (Temporada 2) - Cartas base con estadisticas completas",
        "version": "1.0-organized",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "season": "FIFA Mobile 18 - Season 2",
        "total_cards": len(players),
        "counts": dict(counts),
        "counts_by_rarity": dict(Counter(p["card"]["rarity"] for p in players)),
        "counts_by_position": dict(Counter(p["card"]["position"] for p in players)),
        "sources": [
            {"name": "RenderZ", "url": "https://renderz.app/18/player/{fifa_id}", " aporta": "OVR Mobile, posicion, club_id, fondo/rareza (solo carta base, sin programas)"},
            {"name": "SoFIFA FIFA18 r=180084", "url": "https://sofifa.com/?r=180084&set=true", "aporta": "Guia de FIFA IDs (17.933) + overall/potential/age/equipo consola"},
            {"name": "FIFAMobileGuide.com", "url": "https://www.fifamobileguide.com/post-sitemap.xml", "aporta": "Estadisticas detalladas Mobile para 277 cartas base 80-90 (271 coinciden con RenderZ)"},
        ],
        "generation_method_for_generated": "Plantilla por posicion (guia) + escalado lineal a OVR Mobile (slope=media_stat/media_ovr) + delta SoFIFA overall + jitter determinista por fifa_id. Primarios derivados 50% de detallados. Rango generadas 20-99.",
        "known_issues": [
            "Gareth Bale (173731) Heading 866 en la guia (error de fuente). Conservado tal cual en guide_original.",
            "Porteros en la guia: Free Kick 8-19 (<20). Conservado tal cual en guide_original; generadas se acotan a 20-99.",
            "La guia es de dic-2017/ene-2018: algunos clubes difieren de SoFIFA sep-2018 por fichajes de enero (Aubameyang, Coutinho, Zlatan...).",
            "6 cartas solo en la guia sin FIFA ID en RenderZ/SoFIFA: Gaitan, Bakambu, Marchetti, Mascherano, Nasri, Sneijder (ver guide_coverage.csv).",
            "16 cartas base >=80 sin ficha en la guia (ver guide_coverage.csv). Esas si tienen stats generadas en este JSON.",
        ],
        "how_to_read": {
            "fifa_id": "ID unico del jugador (igual en RenderZ /18/player/{id} y SoFIFA). Clave para unir fuentes.",
            "card.ovr": "Media FIFA Mobile 18 (42-90). La carta base. Ronaldo 90 es el maximo (Master Rare).",
            "stats.source": "guide_original = numero real de la guia, no tocar. generated_template_sofifa = generado coherente (ver metodo).",
            "stats.primary": "6 atributos principales. Campo: pace/shooting/passing/agility/defending/physical. Portero: gk_diving/gk_positioning/handling/reflexes/passing/physical.",
            "stats.detailed": "20 detallados en campo (sprint_speed...crossing). En portero son 16 (sin finishing/shot_power/long_shot/positioning).",
            "stats.goalkeeping": "Solo porteros: gk_diving, gk_positioning, reflexes, handling. null en no-porteros.",
            "stats.guide_extra": "Solo guide_original: skill_boosts, league, country, last_updated. null en generadas.",
            "null": "Significa no aplicable (ej. goalkeeping en un ST, finishing en un GK). No es 0.",
            "name.*_original": "Nombre con tildes tal como viene de la fuente (UTF-8). name.short/full = ASCII sin tildes.",
        },
        "files_related": [
            "fifa_mobile_18_base.csv (13.885 base sin stats, ';')",
            "fifa_mobile_18_base_stats_generadas.csv (misma base + stats planas, ';')",
            "guide_base_stats.csv (277 guia con stats)",
            "guide_coverage.csv (faltantes)",
            "README_JSON.md (guia de este JSON)",
            "README_STATS_GENERADAS.md (metodo de generacion)",
        ]
    }

    schema = {
        "_descripcion": "Diccionario de campos. Cada jugador en 'players' tiene exactamente esta forma (con null donde no aplica).",
        "fifa_id": "int - ID unico FIFA",
        "name": {
            "short": "string ASCII - nombre corto en la carta (ej. Messi)",
            "full": "string ASCII - nombre completo sanitizado (ej. Lionel Messi)",
            "short_original": "string UTF-8 - nombre corto original con tildes",
            "full_original": "string UTF-8 - nombre completo original",
        },
        "card": {
            "ovr": "int 42-90 - media Mobile",
            "position": "string - posicion Mobile (GK, CB, ST, LW...)",
            "club_id": "int - ID club FIFA (igual en RenderZ y SoFIFA)",
            "club": "string ASCII - club sanitizado",
            "club_original": "string UTF-8 - club original",
            "rarity": "string - Master Rare / Epic Rare / Gold Rare / Silver Rare / Bronze Rare",
            "background_code": "string - MR4, ER3, GR2, SR1, BR0",
            "season": "string - Season 2 (FIFA Mobile 18)",
        },
        "sofifa_fifa18_console": {
            "overall": "int|null - media FIFA 18 consola",
            "potential": "int|null - potencial consola",
            "age": "int|null - edad en FIFA 18",
            "position": "string - posicion consola (puede diferir 1 de Mobile)",
            "nationality": "string ASCII - nacionalidad principal",
            "nationality_original": "string UTF-8",
        },
        "links": {
            "renderz": "string - https://renderz.app/18/player/{fifa_id} (carta base)",
            "sofifa": "string - https://sofifa.com/player/{fifa_id}/",
            "guide": "string|null - ficha con stats en fifamobileguide.com (solo guide_original)",
        },
        "stats": {
            "source": "string - guide_original | generated_template_sofifa",
            "primary": "object - 6 primarios (ver how_to_read)",
            "detailed": "object - 20 (campo) o 16 (GK) detallados",
            "goalkeeping": "object|null - solo GK",
            "guide_extra": "object|null - solo guide_original",
        }
    }

    organized = {
        "_readme": "JSON ORGANIZADO FIFA Mobile 18 Base con estadisticas. Empieza por metadata y schema para entender cada campo, luego 'players'. Cada jugador agrupa identidad, carta, consola, links y stats (primary/detailed/goalkeeping). Numeros como int, no aplicable como null. Ver README_JSON.md",
        "metadata": metadata,
        "schema": schema,
        "players": players,
    }

    OUT_JSON.write_text(json.dumps(organized, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK {OUT_JSON} jugadores={len(players)}")

    # Sample: esquema + 3 ejemplos (Ronaldo guide campo, Neuer guide GK, Gibbons generado 42 RB)
    sample_players = []
    for fid in ["20801", "167495", "235329"]:
        for p in players:
            if str(p["fifa_id"]) == fid:
                sample_players.append(p)
                break
    sample = {
        "_readme": "MUESTRA reducida de fifa_mobile_18_base_stats_organized.json (esquema completo + 3 ejemplos). El archivo completo tiene 13.885 jugadores.",
        "metadata": metadata,
        "schema": schema,
        "players_ejemplos": sample_players,
    }
    OUT_SAMPLE.write_text(json.dumps(sample, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK {OUT_SAMPLE}")

if __name__ == "__main__":
    main()
