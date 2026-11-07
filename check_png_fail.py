import urllib.request, re
for i in [215082,193930]:
    req=urllib.request.Request(f'https://renderz.app/18/player/{i}',headers={'User-Agent':'Mozilla/5.0'})
    html=urllib.request.urlopen(req).read().decode('utf-8','replace')
    m=re.search(r'<h1[^>]*>([^<]+)</h1>',html)
    print(i, m.group(1) if m else '')
    print(sorted(set(re.findall(r'players_18/([^"\']+\.png)',html)))[:10])
    # probar variantes CDN
    for suffix in ["_AS","_AS2","_X",""]:
        url=f"https://cdn-p2.frzdb.net/fifamobile/images/players_18/p{i}{suffix}.png?v=848rffjv3we"
        try:
            req2=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            r=urllib.request.urlopen(req2,timeout=15)
            data=r.read()
            print(" ",suffix, r.status, len(data))
        except Exception as e:
            print(" ",suffix, e)
