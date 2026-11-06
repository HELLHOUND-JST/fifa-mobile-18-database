#!/usr/bin/env python3
"""
Version limpia del JSON:
- Mantiene: fifa_id, name, card (ovr/pos/club/rareza/fondo/season), age, stats (primary/detailed/goalkeeping)
- Quita: links, todo sofifa_fifa18_console (excepto age), stats.source/source_description/guide_extra, metadata de origen
- Tipos: int para numeros, null para no aplicable
Salida: fifa_mobile_18_base_stats_clean.json + SAMPLE + README_JSON_CLEAN.md
"""
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent
IN_JSON = BASE_DIR / "fifa_mobile_18_base_stats_organized.json"
OUT_JSON = BASE_DIR / "fifa_mobile_18_base_stats_clean.json"
OUT_SAMPLE = BASE_DIR / "fifa_mobile_18_base_stats_clean_SAMPLE.json"

def main():
    data = json.load(open(IN_JSON, encoding="utf-8"))
    players_old = data["players"]
    players = []
    for p in players_old:
        # age solo de sofifa
        age = p["sofifa_fifa18_console"].get("age")
        # Sin *_original: son repeticion de short/full/club (pedido del usuario)
        name = {"short": p["name"].get("short"), "full": p["name"].get("full")}
        card = {k: v for k, v in p["card"].items() if k != "club_original"}
        player = {
            "fifa_id": p["fifa_id"],
            "name": name,
            "age": age,
            "card": card,
            "stats": {
                "primary": p["stats"]["primary"],
                "detailed": p["stats"]["detailed"],
                "goalkeeping": p["stats"]["goalkeeping"],
            }
        }
        players.append(player)

    players.sort(key=lambda x: (-(x["card"]["ovr"] or 0), x["fifa_id"]))

    metadata = {
        "title": "FIFA Mobile 18 (Temporada 2) - Cartas base con estadisticas",
        "version": "1.0-clean",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "season": "FIFA Mobile 18 - Season 2",
        "total_cards": len(players),
        "counts_by_rarity": dict(Counter(p["card"]["rarity"] for p in players)),
        "counts_by_position": dict(Counter(p["card"]["position"] for p in players)),
        "how_to_read": {
            "fifa_id": "ID unico del jugador",
            "name": "short = nombre corto en la carta, full = nombre completo (ASCII sin tildes)",
            "age": "Edad del jugador",
            "card.ovr": "Media FIFA Mobile 18 de la carta base (42-90)",
            "card.position": "Posicion Mobile (GK, CB, ST...)",
            "card.club_id": "ID del club",
            "card.club": "Club (ASCII sin tildes)",
            "card.rarity": "Master Rare / Epic Rare / Gold Rare / Silver Rare / Bronze Rare",
            "card.background_code": "MR4, ER3, GR2, SR1, BR0",
            "stats.primary": "6 atributos principales. Campo: pace/shooting/passing/agility/defending/physical. Portero: gk_diving/gk_positioning/handling/reflexes/passing/physical",
            "stats.detailed": "Detallados. Campo 20: sprint_speed...crossing. Portero 16: sin tiro (finishing/shot_power/long_shot/positioning)",
            "stats.goalkeeping": "Solo porteros: gk_diving, gk_positioning, reflexes, handling. null en el resto",
            "null": "No aplicable (ej. goalkeeping en un ST)",
        }
    }

    schema = {
        "_descripcion": "Cada jugador en 'players' tiene esta forma exacta.",
        "fifa_id": "int - ID unico",
        "name": {"short": "string ASCII - nombre corto", "full": "string ASCII - nombre completo"},
        "age": "int - edad",
        "card": {"ovr": "int 42-90", "position": "string", "club_id": "int", "club": "string ASCII", "rarity": "string", "background_code": "string", "season": "string"},
        "stats": {
            "primary": "object - 6 primarios",
            "detailed": "object - 20 (campo) o 16 (GK) detallados",
            "goalkeeping": "object|null - solo GK",
        }
    }

    clean = {
        "_readme": "JSON limpio FIFA Mobile 18 Base: identidad + carta + edad + stats.",
        "metadata": metadata,
        "schema": schema,
        "players": players,
    }

    OUT_JSON.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK {OUT_JSON} jugadores={len(players)}")

    # Sample: Ronaldo, Neuer, Gibbons
    sample_players = []
    for fid in ["20801", "167495", "235329"]:
        for p in players:
            if str(p["fifa_id"]) == fid:
                sample_players.append(p)
                break
    sample = {
        "_readme": "MUESTRA de fifa_mobile_18_base_stats_clean.json (esquema + 3 ejemplos). Archivo completo: 13.885 jugadores.",
        "metadata": metadata,
        "schema": schema,
        "players_ejemplos": sample_players,
    }
    OUT_SAMPLE.write_text(json.dumps(sample, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK {OUT_SAMPLE}")

if __name__ == "__main__":
    main()
