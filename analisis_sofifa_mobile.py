import csv, statistics
db=list(csv.DictReader(open('fifa_mobile_18_base.csv',encoding='utf-8'),delimiter=';'))
matched=[r for r in db if int(r['ovr_mobile'])>=80]
# use guide matched list to get console vs mobile
guide=list(csv.DictReader(open('guide_base_stats.csv',encoding='utf-8'),delimiter=';'))
byid={r['fifa_id']:r for r in db}
deltas=[]
for g in guide:
    if g['fifa_id']:
        d=byid.get(g['fifa_id'])
        if d and d['sofifa_overall']:
            deltas.append(int(d['sofifa_overall'])-int(d['ovr_mobile']))
print("matched count",len(deltas),"delta mean",statistics.mean(deltas),"sd",statistics.pstdev(deltas),"min",min(deltas),"max",max(deltas))
# all db delta
alldeltas=[int(r['sofifa_overall'])-int(r['ovr_mobile']) for r in db if r['sofifa_overall']]
print("all db delta mean",statistics.mean(alldeltas),"sd",statistics.pstdev(alldeltas))
# per ovr bucket
from collections import defaultdict
buckets=defaultdict(list)
for r in db:
    if r['sofifa_overall']:
        buckets[int(r['ovr_mobile'])].append(int(r['sofifa_overall']))
for ovr in sorted(buckets)[:10]:
    print(ovr, len(buckets[ovr]), round(statistics.mean(buckets[ovr]),1))
for ovr in sorted(buckets)[-10:]:
    print(ovr, len(buckets[ovr]), round(statistics.mean(buckets[ovr]),1))
