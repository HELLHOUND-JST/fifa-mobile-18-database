import urllib.request, re, html, json
from pathlib import Path
BASE=Path(__file__).resolve().parent
pages = [
    ("deco-icons",501152),
    ("carles-puyol-icons",501151),
    ("ruud-gullit-icons",501150),
    ("emmanuel-petit-icons",501268),
    ("lev-yashin-icons",501269),
    ("diego-maradona-icons",501267),
    ("jay-jay-okocha-icons",501351),
    ("filippo-inzaghi-icons",501352),
    ("rio-ferdinand-icons",501350),
    ("marco-van-basten-prime-icons",501461),
    ("lothar-matthaus-prime-icons",501462),
    ("ronaldinho-98-ovr-prime-icons",501493),
    ("carles-puyol-97-ovr-prime-icons",501574),
    ("edwin-van-der-sar-prime-icons",501655),
    ("ruud-gullit-97-ovr-prime-icons",501764),
]
def fetch(url):
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    return urllib.request.urlopen(req,timeout=20).read().decode("utf-8","replace")
rows=[]
for slug,fid in pages:
    url=f"https://www.fifamobileguide.com/{slug}"
    t=fetch(url)
    title=(re.search(r"<h1[^>]*>([^<]+)</h1>", html.unescape(t)) or ["",""])[1]
    m=re.search(r"<table[^>]*class=\"tablepress[^\"]*\"[^>]*>.*?</table>", t, re.S)
    if not m:
        print(slug, 'NO TABLE'); continue
    tbl=m.group(0)
    info={}
    cur="info"
    for row in re.findall(r"<tr.*?</tr>", tbl, re.S):
        cells=[re.sub(r"<[^>]+>","",html.unescape(c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        if not cells: continue
        if cells[0]=="Primary Attributes": cur="primary"; continue
        if cells[0]=="Detailed Attributes": cur="detailed"; continue
        if cur=="info" and len(cells)>=2:
            info[cells[0]]=cells[1]
        else:
            for i in range(0,len(cells),2):
                if i+1<len(cells) and cells[i] and cells[i+1].isdigit():
                    info[cells[i]]=int(cells[i+1])
    rows.append({"slug":slug,"fifa_id":fid,"title":html.unescape(title),"fields":info})
    print("ok",slug, info.get("OVR"), info.get("Position"))
Path(BASE/"data"/"guide_iconos.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print("saved",len(rows))
