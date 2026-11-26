"""Resample complete NGC 6341 detector zones across both exposure directions."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys


def need(ok,why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return sha256(raw).hexdigest()


def measure(np,groups,repeats,rng,quantiles):
    arrays=list(groups.values())
    observed=np.median(np.concatenate(arrays),axis=0)
    indices=rng.integers(len(arrays),size=(repeats,len(arrays)))
    draws=np.stack([np.median(np.concatenate([arrays[j] for j in row]),axis=0) for row in indices])
    leave_out=np.stack([np.median(np.concatenate([a for j,a in enumerate(arrays) if j!=i]),axis=0)
                        for i in range(len(arrays))])
    bounds=np.quantile(draws,quantiles,axis=0)
    result=[]
    for j in (0,1):
        result.append(dict(trainingExposure=[5,90][j],median=observed[j].tolist(),
             zoneBootstrapPercentiles=bounds[:,j,:].T.tolist(),
             leaveOneZoneOutMinMax=np.stack([leave_out[:,j].min(axis=0),leave_out[:,j].max(axis=0)]).T.tolist(),
             resamplesNonpositiveOwnMinusZone=int(np.count_nonzero(draws[:,j,0]<=0))))
    return result


def main():
    cli=ArgumentParser(description=__doc__)
    for n in ("plan","parent","dependencies","output"):
        cli.add_argument(n,type=Path)
    args=cli.parse_args()
    raw=args.plan.read_bytes()
    p=json.loads(raw)
    original=args.parent.read_bytes()
    need(sha(original)==p["parentReport"],"Parent report changed")
    parent=json.loads(original)
    need(parent["nativeExecutions"]==parent["scientificClosures"]==0,"Scope changed")
    sys.path.insert(0,str(args.dependencies))
    import numpy as np
    need(np.__version__=="2.3.5","NumPy version changed")
    rng=np.random.Generator(np.random.PCG64(p["seed"]))
    source=parent["rows"]
    universe={}
    for row in source:
        phases=universe.setdefault(row["star"],{})
        j=row["trainingExposure"]
        need(j in (0,1) and j not in phases,"Direction roster changed")
        phases[j]=row
    need(len(universe)==736 and all(len(row)==2 for row in universe.values()),"Source count changed")
    by_chip={1:defaultdict(list),2:defaultdict(list)}
    reasons=Counter()
    for star in sorted(universe):
        a,b=(universe[star][i] for i in (0,1))
        need(a["chip"]==b["chip"] and a["zone"]==b["zone"] and a["zone"][0]==a["chip"],"Zone pairing changed")
        if a["state"]!="MEASURED" or b["state"]!="MEASURED":
            reasons.update([a["state"]+"|"+b["state"]])
            continue
        for row in (a,b):
            need(abs(row["ownGain"]-row["zoneGain"]-row["ownMinusZone"])<1e-12,"Unpaired metric")
        by_chip[a["chip"]][tuple(a["zone"])].append([[r[key] for key in p["metrics"]] for r in (a,b)])
    result=[]
    for chip,zones in by_chip.items():
        groups={key:np.asarray(zones[key]) for key in sorted(zones)}
        need(len(groups)>1,"Too few zones")
        stats=measure(np,groups,p["replicates"],rng,p["quantiles"])
        for row in stats:
            prior=next(x for x in parent["summary"] if (x["chip"],x["trainingExposure"])==(chip,row["trainingExposure"]))
            np.testing.assert_allclose(row["median"],[prior[k] for k in ("ownMinusZoneMedian","ownGainMedian","zoneGainMedian")],
                                       rtol=0,atol=1e-12)
        result.append(dict(chip=chip,stars=sum(len(x) for x in groups.values()),zoneSizes=[
                    dict(zone=k,stars=len(v)) for k,v in groups.items()],stats=stats))
    need(sum(r["stars"] for r in result)==733 and sum(reasons.values())==3,"Paired support changed")
    payload=dict(schema=p["schema"],protocolSha256=sha(raw),programSha256=sha(Path(__file__).read_bytes()),
                 parentReportSha256=p["parentReport"],metrics=p["metrics"],quantiles=p["quantiles"],
                 replicates=p["replicates"],exclusions=dict(reasons),chips=result,
                 fieldPopulationInferenceVerified=False,nativeExecutions=0,scientificClosures=0)
    with args.output.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(payload,f,sort_keys=True,indent=2,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()