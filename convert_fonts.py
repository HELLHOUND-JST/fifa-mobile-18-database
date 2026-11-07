import urllib.request
from pathlib import Path
from fontTools.ttLib import TTFont
base=Path(__file__).resolve().parent
fonts_dir=base/"fonts_original"
fonts_dir.mkdir(exist_ok=True)
for name in ["Knul-Medium.woff","Knul-Regular.woff"]:
    url=f"https://fonts.frzdb.net/{name}"
    data=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})).read()
    (fonts_dir/name).write_bytes(data)
    print(name, len(data))
    # convertir woff -> ttf
    font=TTFont(str(fonts_dir/name))
    print(" ", font['name'].getDebugName(1), font['name'].getDebugName(4))
    out = fonts_dir/(name.replace(".woff",".ttf"))
    font.flavor=None
    font.save(str(out))
    print(" ->", out, out.stat().st_size)
