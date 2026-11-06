import urllib.request, urllib.parse, json, time, csv, sys, ssl
CTX = ssl._create_unverified_context()
ids=[]
with open('fifa_mobile_18_base.csv',encoding='utf-8-sig') as f:
    sample=f.read(2048)
    f.seek(0)
    delim=';' if ';' in sample.splitlines()[0] else ','
    print('delimiter', delim)
    r=csv.DictReader(f, delimiter=delim)
    for i,row in enumerate(r):
        if i<30:
            ids.append((int(row['fifa_id']), row['full_name'], row['ovr_mobile']))
print(ids[:5], flush=True)
def check(url):
    api=f"https://archive.org/wayback/available?url={urllib.parse.quote(url, safe='')}&timestamp=2019"
    req=urllib.request.Request(api, headers={'User-Agent':'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=20, context=CTX) as resp:
            txt=resp.read().decode('utf-8','replace')
            j=json.loads(txt)
            closest=j.get('archived_snapshots',{}).get('closest')
            return closest
    except Exception as e:
        return {'error':str(e)[:200]}
for fid,name,ovr in ids:
    url=f"https://fifarenderz.com/18/player/{fid}"
    c=check(url)
    print(fid, name, ovr, c, flush=True)
    time.sleep(1.2)
