"""Score disjoint-star transfer of the measured UVIS1 aperture color term."""
import argparse
from collections import defaultdict
from hashlib import file_digest, sha256
from itertools import combinations
import json
from math import isclose, isfinite, log10
from pathlib import Path
from statistics import median
from zipfile import ZipFile

PIN = "7858085fd8cd2a5357caf6f73cd404b3b47e18aab0c0f246187f2304597a0bcf"


def check(cond, why):
    if not cond:
        raise ValueError(why)


def digest(raw):
    return sha256(raw).hexdigest()


def load(path, pin):
    raw = path.read_bytes()
    check(digest(raw) == pin, f"SHA-256 changed: {path.name}")
    return raw


def archived(path, pins):
    archive, member, fingerprint = pins
    with path.open("rb") as source:
        check(file_digest(source,"sha256").hexdigest()==archive,"Source ZIP changed")
        with ZipFile(source) as bundle:
            check(bundle.namelist().count(member)==1,"Report member ambiguous")
            raw=bundle.read(member)
    check(digest(raw)==fingerprint,"Archived report changed")
    return json.loads(raw)


def color_term(values, radii, pairs):
    a,b = radii
    labels = [f"{x}-{y}" for x,y in pairs]
    check(set(values)=={a,b} and all(set(values[r])==set(labels) for r in radii),"Color coverage differs")
    for r in radii:
        x,y,z = (values[r][name] for name in labels)
        check(all(isfinite(q) for q in (x,y,z)) and isclose(x+z,y,abs_tol=1e-9),"Color closure differs")
    return {name:values[b][name]-values[a][name] for name in labels}


def medians(rows):
    return {color:median(row[color] for row in rows) for color in rows[0]}


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    for name in ("protocol","gd153","grw70","nominal","report"):
        cli.add_argument(name,type=Path)
    args=cli.parse_args()
    p=json.loads(load(args.protocol,PIN))
    gd=archived(args.gd153,p["gd153"])
    grw=archived(args.grw70,p["grw70"])
    nom=archived(args.nominal,p["nominalEE"])
    check(gd["scientificClosures"]==grw["scientificClosures"]==0
          and gd["nativeExecutions"]==grw["nativeExecutions"]==0,"Source scope differs")
    radii=p["radii"]
    pairs=list(combinations(p["bands"],2))
    gd_groups=defaultdict(list)
    for item in gd["colorControls"]:
        value=item["alternatives"]["wcsMidpoint"]
        check(set(value)==set(radii),"Previously qualified GD153 support changed")
        gd_groups[item["visit"]].append(dict(dither=item["dither"],term=color_term(value,radii,pairs)))
    check(len(gd_groups)==2 and sum(map(len,gd_groups.values()))==4,"GD153 visit coverage")
    gd_visits=[dict(visit=v,chip=p["chip"],triplets=rows,term=medians([r["term"] for r in rows]))
               for v,rows in sorted(gd_groups.items())]
    grw_visits=[]
    for item in grw["acceptedCombinedVisits"]:
        if item["chip"] != p["chip"]:
            continue
        term=color_term(item["colors"],radii,pairs)
        check(all(isclose(term[k],v,abs_tol=1e-9) for k,v in item["apertureChangeMillimag"].items()),
              "GRW70 archive aperture growth differs")
        grw_visits.append(dict(visit=item["visit"],chip=item["chip"],batch=item["batch"],
                               term=term))
    check(len(grw_visits)==2 and len({r["visit"] for r in grw_visits})==2,"GRW70 visit coverage")
    lookup={r:dict(zip(p["bands"],nom["eeFractions"][r],strict=True)) for r in radii}
    nominal={f"{x}-{y}":-2500*log10((lookup["10"][x]/lookup["10"][y])/
                                   (lookup["5"][x]/lookup["5"][y])) for x,y in pairs}
    sets={"GD153":gd_visits,"GRW70":grw_visits}
    tests=[]
    summaries=[]
    for fit,test in (("GD153","GRW70"),("GRW70","GD153")):
        train=[r["term"] for r in sets[fit]]
        check(len(train)>=p["minOtherStarVisits"],"Insufficient other-star visits")
        estimate=medians(train)
        group=[]
        for visit in sets[test]:
            actual=visit["term"]
            pred=dict(zero={k:0.0 for k in actual},nominalEE=nominal,otherStar=estimate)
            error={method:{c:actual[c]-value for c,value in values.items()} for method,values in pred.items()}
            row=dict(trainingStar=fit,testStar=test,trainingVisits=[r["visit"] for r in sets[fit]],
                     testVisit=visit["visit"],actual=actual,prediction=pred,error=error)
            tests.append(row)
            group.append(row)
        for label in nominal:
            methods={}
            for method in ("zero","nominalEE","otherStar"):
                values=[abs(r["error"][method][label]) for r in group]
                methods[method]=dict(medianAbsolute=median(values),maxAbsolute=max(values))
            summaries.append(dict(trainingStar=fit,testStar=test,color=label,visits=len(group),errors=methods,
                                  improvedOverZero=sum(abs(r["error"]["otherStar"][label])<abs(r["error"]["zero"][label])
                                                       for r in group)))
    report=dict(schema=p["schema"]+"_RESULT",protocolSha256=PIN,programSha256=digest(Path(__file__).read_bytes()),
                chip=p["chip"],radii=[int(r) for r in radii],cohorts=sets,tests=tests,summary=summaries,
                independentStars=2,scientificClosures=0,nativeExecutions=0)
    with args.report.open("x",newline="\n",encoding="utf-8") as out:
        json.dump(report,out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")


if __name__=="__main__":
    main()