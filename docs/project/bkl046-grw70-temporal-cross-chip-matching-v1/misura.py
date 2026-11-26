"""Match GRW70 visits across UVIS chips before comparing aperture terms."""
import argparse
from collections import defaultdict
from functools import cache
from hashlib import file_digest, sha256
import json
from math import isfinite
from pathlib import Path
from statistics import median
from zipfile import ZipFile

PIN = "a38130ee9b36439a534dddc6fb108d4106cf4f60f83ce82a8f078d9f29b97f5a"


def need(ok,message):
    if not ok:
        raise ValueError(message)


def inputs(path, pin, reports):
    result=[]
    with path.open("rb") as stream:
        need(file_digest(stream,"sha256").hexdigest()==pin,"Source ZIP changed")
        with ZipFile(stream) as archive:
            names=archive.namelist()
            for name,digest in reports:
                need(names.count(name)==1,"Ambiguous ZIP report")
                raw=archive.read(name)
                need(sha256(raw).hexdigest()==digest,"Source report changed")
                result.append(json.loads(raw))
    return result


def gather(primary,relative,cohort,count):
    rows=defaultdict(list)
    for row in primary["rows"]:
        rows[row["visit"]].append(row)
    need(len(rows)==len(relative["visits"])==count,"Visit roster changed")
    result=[]
    for item in relative["visits"]:
        label=item["visit"]
        cases=rows[label]
        need(len(cases)==3 and {r["band"] for r in cases}=={"F438W","F606W","F814W"},"Band roster changed")
        need(all("startMjd" in r and "chip" in r for r in cases),"Missing exposure header identity")
        chip,={r["chip"] for r in cases}
        need(chip in (1,2),"Unexpected chip")
        center=median(r["startMjd"] for r in cases)
        need(isfinite(center),"Invalid visit epoch")
        colors=item["colors"]
        need(set(colors)<={"5","10"} and all(len(r)==3 and all(isfinite(v) for v in r.values())
                                             for r in colors.values()),"Invalid colors")
        result.append(dict(visit=label,cohort=cohort,chip=chip,timeMjd=center,colors=colors))
    return result


def closest_pairs(left,right,window):
    left=sorted(left,key=lambda r:(r["timeMjd"],r["visit"]))
    right=sorted(right,key=lambda r:(r["timeMjd"],r["visit"]))

    @cache
    def solve(i,j):
        if i==len(left) or j==len(right):
            return 0,0.0,()
        options=[solve(i+1,j),solve(i,j+1)]
        delta=abs(right[j]["timeMjd"]-left[i]["timeMjd"])
        if delta<=window:
            count, span, ids=solve(i+1,j+1)
            options.append((count+1,span+delta,((left[i]["visit"],right[j]["visit"]),)+ids))
        return min(options,key=lambda x:(-x[0],x[1],x[2]))

    return solve(0,0)[2]


def difference(second,first):
    need(set(second)==set(first),"Color endpoints differ")
    return {k:second[k]-first[k] for k in second}


def summarize(values):
    if not values:
        return {}
    return {k:dict(median=median(r[k] for r in values),
                   minimum=min(r[k] for r in values),maximum=max(r[k] for r in values))
            for k in values[0]}


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    for name in ("protocol","exploratory","first","reserve","report"):
        cli.add_argument(name,type=Path)
    a=cli.parse_args()
    raw=a.protocol.read_bytes()
    need(sha256(raw).hexdigest()==PIN,"Protocol changed")
    p=json.loads(raw)
    # A greedy nearest-pair assignment would lose one match in this fixture.
    sample=lambda names,seq:[dict(visit=k,timeMjd=x) for k,x in zip(names,seq,strict=True)]
    need(closest_pairs(sample(["l0","l1"],[0.,1.]),sample(["r0","r1"],[.9,1.8]),1.)==
         (("l0","r0"),("l1","r1")),"Matching fixture failed")
    visits=[]
    for label,archive_sha,meta_sha,relative_sha,count in p["inputs"]:
        primary,relative=inputs(getattr(a,label),archive_sha,
                               [("riscontro.json",meta_sha),("riscontro-centro.json",relative_sha)])
        visits.extend(gather(primary,relative,label,count))
    by_name={r["visit"]:r for r in visits}
    need(len(by_name)==len(visits)==70,"Cohort visit coverage differs")
    groups=dict(metadata=visits,r5=[r for r in visits if "5" in r["colors"]],
                both=[r for r in visits if set(r["colors"])=={"5","10"}])
    result=[]
    for name,group in groups.items():
        left=[r for r in group if r["chip"]==1]
        right=[r for r in group if r["chip"]==2]
        nearest=min((abs(y["timeMjd"]-x["timeMjd"]) for x in left for y in right),default=None)
        for limit in p["windowsDays"]:
            pairs=[]
            for x,y in closest_pairs(left,right,limit):
                first,second=by_name[x],by_name[y]
                row=dict(uvis1=x,uvis2=y,windowDays=limit,
                         timeDeltaDays=second["timeMjd"]-first["timeMjd"])
                if name in ("r5","both"):
                    row["colorUVIS2MinusUVIS1At5"]=difference(second["colors"]["5"],first["colors"]["5"])
                if name=="both":
                    transform=lambda item:difference(item["colors"]["10"],item["colors"]["5"])
                    row["apertureGrowthUVIS2MinusUVIS1"]=difference(transform(second),transform(first))
                pairs.append(row)
            result.append(dict(coverage=name,windowDays=limit,nUVIS1=len(left),nUVIS2=len(right),
                               nearestCrossChipDays=nearest,pairs=pairs,
                               color5Summary=summarize([r["colorUVIS2MinusUVIS1At5"] for r in pairs
                                                         if "colorUVIS2MinusUVIS1At5" in r]),
                               apertureGrowthSummary=summarize([r["apertureGrowthUVIS2MinusUVIS1"] for r in pairs
                                                                  if "apertureGrowthUVIS2MinusUVIS1" in r])))
    output=dict(schema=p["schema"]+"_RESULT",protocolSha256=PIN,
                programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),visits=visits,
                temporalMatching=result,causalChipEffectVerified=False,scientificClosures=0,nativeExecutions=0)
    with a.report.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(output,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    main()