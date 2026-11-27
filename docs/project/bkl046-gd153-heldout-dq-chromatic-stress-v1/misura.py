"""Propagate exact retained GD153 aperture errors to matched three-band colors."""
import argparse
from collections import defaultdict
from hashlib import file_digest, sha256
from itertools import combinations
import json
from math import floor, log10
from pathlib import Path
from statistics import median
from zipfile import ZipFile


def sha(data):
    return sha256(data).hexdigest()


def verified_report(archive,check,file):
    with archive.open("rb") as data:
        assert file_digest(data,"sha256").hexdigest()==check["archive"]
    with ZipFile(archive) as z:
        raw=z.read(file)
    assert sha(raw)==check["report"]
    return json.loads(raw)


def p90(values):
    if not values:
        return None
    values=sorted(values)
    index=.9*(len(values)-1)
    low=floor(index)
    return values[low]+(index-low)*(values[min(low+1,len(values)-1)]-values[low])


def effect(a,b):
    if a is None or b is None or a<=-1 or b<=-1:
        return None
    return -2500*log10((1+a)/(1+b))


def main():
    cli=argparse.ArgumentParser()
    for n in ("protocol","cleanArchive","maskedArchive","report"):
        cli.add_argument(n,type=Path)
    a=cli.parse_args()
    raw=a.protocol.read_bytes()
    p=json.loads(raw)
    clean=verified_report(a.cleanArchive,p["clean"],"riscontro-verificato.json")
    masked=verified_report(a.maskedArchive,p["masked"],"riscontro.json")
    assert effect(.01,.01)==0 and effect(None,0) is None
    bands=p["bands"]
    methods=p["methods"]
    index={(row["visit"],tuple(row["dither"]),row["band"]):row["file"] for row in clean["rows"]}
    assert len(index)==len(clean["rows"])==48
    templates={}
    for triplet in clean["triplets"]:
        measures=triplet["measurements"]
        if p["requireAperture"] not in measures:
            continue
        assert triplet["spanDays"]<=p["maxTripletSpanDays"]
        visit=triplet["visit"]
        dither=tuple(triplet["dither"])
        ids={band:index[visit,dither,band] for band in bands}
        for band,identity in ids.items():
            assert identity not in templates
            templates[identity]=(visit,dither,band)
    assert len(templates)==12 and len({v[0] for v in templates.values()})==2
    grouped=defaultdict(dict)
    for test in masked["tests"]:
        item=templates.get(test["truthExposure"])
        if item is None:
            continue
        visit,dither,band=item
        assert visit==test["truthVisit"] and band==test["band"]
        group=grouped[test["policy"],test["maskVisit"],test["maskChip"],visit,dither]
        assert band not in group
        group[band]=test
    cases=[]
    for (policy,mask_visit,chip,visit,dither),group in sorted(grouped.items()):
        assert set(group)==set(bands)
        cases.append({
            "policy":policy,"maskVisit":mask_visit,"maskChip":chip,"referenceVisit":visit,
            "dither":dither,"anyMissing":any(row["missing"] for row in group.values()),
            "anyCoreMissing":any(row["coreMissing"] for row in group.values()),
            "colors":{f"{b}-{r}":{method:effect(group[b]["relativeSignedError"][method],
                                                 group[r]["relativeSignedError"][method]) for method in methods}
                      for b,r in combinations(bands,2)}
        })
    assert len(cases)==56
    summary=[]
    for policy in p["policies"]:
        for subset in ("all","anyMissing","anyCoreMissing"):
            keep=[row for row in cases if row["policy"]==policy and (subset=="all" or row[subset])]
            for b,r in combinations(bands,2):
                color=f"{b}-{r}"
                for method in methods:
                    samples=[abs(row["colors"][color][method]) for row in keep if row["colors"][color][method] is not None]
                    rows_by_visit=defaultdict(list)
                    for row in keep:
                        e=row["colors"][color][method]
                        if e is not None:
                            rows_by_visit[row["referenceVisit"]].append(abs(e))
                    summary.append({"policy":policy,"subset":subset,"color":color,"method":method,
                                    "cases":len(keep),"measured":len(samples),
                                    "p90AbsoluteMillimag":p90(samples),
                                    "withinTenMillimag":sum(x<=p["reportingThresholdMillimag"] for x in samples),
                                    "visitConditionalP90Millimag":{k:p90(v) for k,v in rows_by_visit.items()}})
    output={"schema":"BKL046_GD153_HELDOUT_DQ_CHROMATIC_STRESS_RESULT_V1",
            "protocolSha256":sha(raw),"programSha256":sha(Path(__file__).read_bytes()),
            "referenceTriplets":4,"referenceVisits":2,"independentTargets":1,
            "cases":cases,"summary":summary,"actualDamagedExposureColorVerified":False,
            "nativeExecutions":0,"scientificClosures":0}
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(output,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()
