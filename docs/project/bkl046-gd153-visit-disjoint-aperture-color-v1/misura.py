"""Compare nominal and visit-disjoint chromatic aperture-growth corrections."""
import argparse
from hashlib import file_digest, sha256
from itertools import combinations
import json
import math
from pathlib import Path
from statistics import median
from zipfile import ZipFile


def digest(data):
    return sha256(data).hexdigest()


def chromatic(growth, a, b):
    return -2500 * math.log10(growth[a] / growth[b])


def metric(errors):
    values = sorted(abs(x) for x in errors)
    if not values:
        return None
    return {"count":len(values), "medianAbsMillimag":median(values), "maximumAbsMillimag":max(values)}


def main():
    ap=argparse.ArgumentParser()
    for n in ("protocol","source","report"):
        ap.add_argument(n,type=Path)
    a=ap.parse_args()
    raw=a.protocol.read_bytes()
    p=json.loads(raw)
    with a.source.open("rb") as f:
        assert file_digest(f,"sha256").hexdigest()==p["sourceArchive"]
    with ZipFile(a.source) as kit:
        data=kit.read(p["sourceMember"])
    assert digest(data)==p["sourceReport"]
    source=json.loads(data)
    assert len(source["rows"])==48 and len(source["triplets"])==16
    bands=p["bands"]
    low,high=p["radii"]
    nominal={b:source["eeFractions"][str(high)][i]/source["eeFractions"][str(low)][i]
             for i,b in enumerate(bands)}
    assert chromatic({"X":2,"Y":2},"X","Y")==0
    output={}
    for background in p["backgrounds"]:
        inner,outer=(f"{background}:r{k}" for k in (low,high))
        joined={}
        for row in source["rows"]:
            key=(row["visit"],tuple(row["dither"]))
            group=joined.setdefault(key,{})
            band=row["band"]
            assert band not in group
            measurements=row.get("measurements",{})
            group[band]=(measurements[outer]["rate"]/measurements[inner]["rate"]
                         if inner in measurements and outer in measurements else None)
        per_color={}
        for blue,red in combinations(bands,2):
            color=f"{blue}-{red}"
            measurements=[]
            for triplet in source["triplets"]:
                visit=triplet["visit"]
                dither=tuple(triplet["dither"])
                methods=triplet["measurements"]
                if inner not in methods or outer not in methods:
                    continue
                measured=methods[outer]["rawMillimag"][color]-methods[inner]["rawMillimag"][color]
                growth=joined[(visit,dither)]
                assert math.isclose(measured,chromatic(growth,blue,red),abs_tol=1e-8)
                ep=chromatic(nominal,blue,red)
                measured_after=methods[outer]["eeMillimag"][color]-methods[inner]["eeMillimag"][color]
                assert math.isclose(measured_after,measured-ep,abs_tol=1e-8)
                measurements.append({"visit":visit,"dither":dither,"rawGrowthMillimag":measured,
                                     "nominalMillimag":ep,"residualNominalMillimag":measured-ep})
            predictions=[]
            for observation in measurements:
                visit=observation["visit"]
                dither=observation["dither"]
                by_visit={}
                at_same_dither=[]
                for other in measurements:
                    if other["visit"]==visit:
                        continue
                    actual=other["rawGrowthMillimag"]
                    by_visit.setdefault(other["visit"],[]).append(actual)
                    if other["dither"]==dither:
                        at_same_dither.append(actual)
                recovered=median([median(v) for v in by_visit.values()]) if len(by_visit)>=2 else None
                phase=median(at_same_dither) if len(at_same_dither)>=2 else None
                predictions.append({**observation,"comparisonVisits":len(by_visit),
                                    "sameDitherComparisonVisits":len(at_same_dither),
                                    "allDithersHeldOutPrediction":recovered,"sameDitherHeldOutPrediction":phase})
            subsets={}
            for mode in ("allDithersHeldOutPrediction","sameDitherHeldOutPrediction"):
                common=[x for x in predictions if x[mode] is not None]
                subsets[mode]={"visits":len({x["visit"] for x in common}),
                               "uncorrected":metric([x["rawGrowthMillimag"] for x in common]),
                               "nominal":metric([x["residualNominalMillimag"] for x in common]),
                               "transferred":metric([x["rawGrowthMillimag"]-x[mode] for x in common])}
            per_color[color]={"triplets":predictions,"matchedSupportMetrics":subsets,
                                  "allObservedMetrics":{
                                      "visits":len({x["visit"] for x in predictions}),
                                      "uncorrected":metric([x["rawGrowthMillimag"] for x in predictions]),
                                      "nominal":metric([x["residualNominalMillimag"] for x in predictions])}}
        output[background]=per_color
    result={"schema":"BKL046_GD153_VISIT_DISJOINT_COLOR_APERTURE_RESULT_V1",
            "programSha256":digest(Path(__file__).read_bytes()),"protocolSha256":digest(raw),
            "sourceReportSha256":p["sourceReport"],"comparisons":output,
            "independentTargets":1,"nativeExecutions":0,"scientificClosures":0}
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()
