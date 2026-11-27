"""Compare held-out green parity fits with individually and regionally chosen PSF angles."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
from statistics import median
import subprocess
import sys
from tempfile import TemporaryDirectory


def sha(data):
    return sha256(data).hexdigest()


def pin(path,expected):
    data=path.read_bytes()
    if sha(data)!=expected:
        raise ValueError("Changed input: "+path.name)
    return data


def save(path,obj):
    data=(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
    with path.open("xb") as h:
        h.write(data)
    return sha(data)


def main():
    cli=ArgumentParser(description=__doc__)
    for k in ("plan","parity","expanded","pose","mosaics","width","dependencies","output"):
        cli.add_argument(k,type=Path)
    a=cli.parse_args()
    raw=a.plan.read_bytes()
    cfg=json.loads(raw)
    parent=a.parity/"parita.py"
    protocol=a.parity/"protocollo.json"
    pin(protocol,cfg["parityProtocol"])
    detail=a.parity/"tutti-gli-esiti.json"
    pinned=pin(detail,cfg["parityDetail"])
    prefix,marker,_=pin(parent,cfg["parityProgram"]).decode().partition("\nwith tempfile.TemporaryDirectory(")
    if not marker:
        raise ValueError("Parity program boundary")
    injected=r'''import os
reference=json.loads(Path(os.environ["DSG_PSF_GREEN_DETAIL"]).read_bytes())["reports"][p["calibration"]]["rows"]
baseline={r["star"]:r["fits"] for r in reference}
by_angle={int(angle):np.flatnonzero((angles==angle)&(ratios<1)) for angle in sorted(set(angles[elliptical]))}
per_star=[]
for band in ("green1","green2"):
    for star in stars:
        observed=json.loads(json.dumps(evaluate(score_bank[star][band])))
        expected=baseline[star][band]
        assert observed["qualified"]==expected["qualified"]
        if expected["angle"] is None:
            assert observed["angle"] is None
        else:
            np.testing.assert_allclose(observed["angle"],expected["angle"],rtol=0,atol=1e-10)
        for got,want in zip(observed["folds"],expected["folds"],strict=True):
            assert {k:v for k,v in got.items() if k!="heldOutGain"}=={k:v for k,v in want.items() if k!="heldOutGain"}
            if "heldOutGain" in want:
                np.testing.assert_allclose(got["heldOutGain"],want["heldOutGain"],rtol=0,atol=1e-12)
    for fold in (0,1):
        training={star:np.stack(score_bank[star][band][fold]).sum(axis=0) for star in stars}
        held={star:np.stack(score_bank[star][band][1-fold]).sum(axis=0) for star in stars}
        for star in stars:
            zone=star.split("-")[0]
            peers=[s for s in stars if s!=star and s.split("-")[0]==zone]
            row=dict(star=star,zone=zone,band=band,trainingHalf=fold,peers=peers)
            zone_scores={angle:float(np.mean([np.min(training[s][idx]) for s in peers]))
                         for angle,idx in by_angle.items()} if peers else {}
            if not zone_scores or not any(np.isfinite(list(zone_scores.values()))):
                row["state"]="NO_LOCAL_ANGLE"
                per_star.append(row)
                continue
            regional_angle=min(zone_scores,key=lambda angle:(zone_scores[angle],angle))
            zonal=by_angle[regional_angle]
            choices={label:int(indices[np.argmin(training[star][indices])])
                     for label,indices in (("circle",circular),("own",elliptical),("zone",zonal))}
            selected=[choices[key] for key in ("circle","own","zone")]
            row["candidates"]={key:list(shapes[idx]) for key,idx in choices.items()}
            if not all(np.isfinite(training[star][idx]) and np.isfinite(held[star][idx]) for idx in selected):
                row["state"]="INVALID_VALIDATION"
            else:
                cir,own,reg=[float(held[star][idx]) for idx in selected]
                if cir<=0:
                    row["state"]="ZERO_CIRCULAR_VALIDATION_LOSS"
                else:
                    row.update(state="MEASURED",circleLoss=cir,ownGain=(cir-own)/cir,zoneGain=(cir-reg)/cir,
                               ownMinusZoneGain=(reg-own)/cir)
            per_star.append(row)
with output.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(per_star,sort_keys=True,allow_nan=False)+"\n")
'''
    a.output.mkdir()
    tmp_argv=sys.argv
    try:
        sys.argv=[str(parent),str(protocol),str(a.expanded),str(a.pose),str(a.mosaics),str(a.width),str(a.dependencies),str(a.output)]
        context={"__file__":str(parent)}
        exec(compile(prefix,str(parent),"exec"),context)
    finally:
        sys.argv=tmp_argv
    gen=context["gen"].split("\nrows=[]",1)
    if len(gen)!=2:
        raise ValueError("Score-bank boundary")
    all_results={}
    with TemporaryDirectory(prefix="zone-psf-",dir=a.output) as folder:
        tmp=Path(folder)
        script=tmp/"holdout.py"
        script.write_text(gen[0]+"\n"+injected,encoding="utf8",newline="\n")
        ref=tmp/"reference.json"
        ref.write_bytes(pinned)
        for cal in ("A","B"):
            bank=tmp/(cal+"-policy.json")
            out=tmp/(cal+"-rows.json")
            bank.write_text(json.dumps(dict(context["bank"],calibration=cal),sort_keys=True),encoding="utf8")
            env=dict(os.environ,DSG_PSF_GREEN_DETAIL=str(ref),OPENBLAS_NUM_THREADS="1")
            subprocess.run([sys.executable,"-I","-S","-B",str(script),str(bank),str(a.mosaics),
                            str(a.width),str(a.dependencies),str(out)],check=True,timeout=180,env=env)
            all_results[cal]=json.loads(out.read_bytes())
    summary={}
    for cal,rows in all_results.items():
        if len(rows)!=76:
            raise ValueError("Wrong count")
        metrics={}
        for band in ("green1","green2"):
            relevant=[r for r in rows if r["band"]==band]
            usable=[r for r in relevant if r["state"]=="MEASURED"]
            metrics[band]=dict(states=Counter(r["state"] for r in relevant),
                ownGainMedian=median(r["ownGain"] for r in usable),zoneGainMedian=median(r["zoneGain"] for r in usable),
                ownMinusZoneGainMedian=median(r["ownMinusZoneGain"] for r in usable),
                ownStrictlyBetter=sum(r["ownMinusZoneGain"]>1e-12 for r in usable),
                ownStrictlyWorse=sum(r["ownMinusZoneGain"]<-1e-12 for r in usable))
        summary[cal]=metrics
    detail_digest=save(a.output/"tutti-gli-esiti.json",all_results)
    save(a.output/"riscontro.json",dict(schema=cfg["schema"],protocolSha256=sha(raw),
        programSha256=sha(Path(__file__).read_bytes()),detailSha256=detail_digest,
        verifiedParentGreenFits=76,summary=summary,nativeExecutions=0,scientificClosures=0))


if __name__=="__main__":
    main()