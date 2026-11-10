import urllib.request, re
ids = [502406, 500003, 500614, 217215]
for fifa_id in ids:
    try:
        req = urllib.request.Request(f"https://renderz.app/18/player/{fifa_id}", headers={"User-Agent": "Mozilla/5.0"})
        t = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
        players = sorted(set(re.findall(r"players_18/([^\"']+\.png)", t)))
        progs   = sorted(set(re.findall(r"programs_18/([^\"']+\.png)", t)))
        bgs     = sorted(set(re.findall(r"backgrounds_18/([^\"']+\.png)", t)))
        clubs   = sorted(set(re.findall(r"clubLogos_18/([^\"']+\.png)", t)))
        print(fifa_id, "players:", players)
        print("   programs:", progs, "backgrounds:", bgs, "clubs:", clubs)
    except Exception as e:
        print(fifa_id, "ERR", e)
