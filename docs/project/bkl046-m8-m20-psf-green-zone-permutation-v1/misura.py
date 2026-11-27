"""Enumerate conditional orientation assignments in the frozen M8/M20 green sample."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations, product
import json
from math import factorial, prod
from pathlib import Path


def require(ok,why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return sha256(raw).hexdigest()


def read(path,pin):
    raw=path.read_bytes()
    require(sha(raw)==pin,"Changed bytes: "+path.name)
    return json.loads(raw)


def axial(x,y):
    d=abs(x-y)
    return min(d,24-d)


def analyze(rows,groups,threshold):
    g1=[r[1] for r in rows]
    g2=[r[2] for r in rows]
    original=[axial(x,y) for x,y in zip(g1,g2,strict=True)]
    observed=sum(d<=threshold for d in original)
    observed_sum=sum(original)
    count_hist=Counter()
    sum_hist=Counter()
    joint=0
    for variation in product(*(permutations(group) for group in groups)):
        angles=[axial(g1[i],g2[j]) for group,permuted in zip(groups,variation,strict=True)
                for i,j in zip(group,permuted,strict=True)]
        count=sum(d<=threshold for d in angles)
        total=sum(angles)
        count_hist[count]+=1
        sum_hist[total]+=1
        joint+=int(count>=observed and total<=observed_sum)
    total=prod(factorial(len(g)) for g in groups)
    require(total==sum(count_hist.values())==sum(sum_hist.values()),"Enumeration coverage")
    return dict(assignments=total, observedAgreements=observed, observedAngleSumTicks=observed_sum,
                atLeastObservedAgreements=sum(n for k,n in count_hist.items() if k>=observed),
                atMostObservedAngleSum=sum(n for k,n in sum_hist.items() if k<=observed_sum),
                jointAtLeastAsClose=joint,agreementHistogram=dict(count_hist),angleSumHistogramTicks=dict(sum_hist))


def main():
    cli=ArgumentParser(description=__doc__)
    for name in ("protocol","parent","report"):
        cli.add_argument(name,type=Path)
    a=cli.parse_args()
    raw=a.protocol.read_bytes()
    p=json.loads(raw)
    summ=read(a.parent/"riscontro.json",p["summarySha256"])
    detail=read(a.parent/"tutti-gli-esiti.json",p["detailSha256"])
    require(summ["fullReportSha256"]==p["detailSha256"] and summ["summary"]==detail["summary"],"Source binding")
    step=p["angleStepDegrees"]
    limit=int(p["agreementDegrees"]/step)
    reports={}
    for calibration in ("A","B"):
        source=detail["reports"][calibration]["rows"]
        require(len(source)==len({r["star"] for r in source})==19,"Star roster")
        rows=[]
        for r in source:
            a1,a2=(r["fits"][f"green{k}"] for k in (1,2))
            if not (a1["qualified"] and a2["qualified"]):
                continue
            x,y=(f["angle"]/step for f in (a1,a2))
            require(abs(x-round(x))<=1e-10 and abs(y-round(y))<=1e-10 and 0<=x<24 and 0<=y<24,"Not on axial grid")
            rows.append((r["star"],round(x),round(y)))
        rows.sort()
        observed=summ["summary"][calibration]["greenParities"]
        deltas=[dict(star=name,deltaDegrees=axial(x,y)*step) for name,x,y in rows]
        require(deltas==observed["deltas"] and len(rows)==observed["within15"]==8,"Parent result changed")
        zones=defaultdict(list)
        for i,(name,_,_) in enumerate(rows):
            zones[name.split("-")[0]].append(i)
        by_zone=analyze(rows,list(zones.values()),limit)
        all_stars=analyze(rows,[list(range(len(rows)))],limit)
        reports[calibration]=dict(angles=[dict(star=name,g1=x*step,g2=y*step) for name,x,y in rows],
            zones={name:len(group) for name,group in zones.items()},zoneConstrained=by_zone,unrestricted=all_stars)
    result=dict(schema=p["schema"],protocolSha256=sha(raw),programSha256=sha(Path(__file__).read_bytes()),
                sourceDetailSha256=p["detailSha256"],reports=reports,
                calibrationsProduceSameConditionalAssignments=reports["A"]==reports["B"],
                independentReplications=0,nativeExecutions=0,scientificClosures=0)
    with a.report.open("x",encoding="utf8",newline="\n") as h:
        json.dump(result,h,indent=2,sort_keys=True,allow_nan=False)
        h.write("\n")


if __name__=="__main__":
    main()