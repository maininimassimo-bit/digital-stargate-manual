from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path
from statistics import median, quantiles
import sys

root, photometry, comparisons, output = map(Path,sys.argv[1:])
p_raw = (root/"protocollo.json").read_bytes()
p_hash = sha256(p_raw).hexdigest()
assert p_hash == "0629e27bad615c65ddd26dd95d923f3907d49ae24179be3296bb60f058e6bfaf"
p = json.loads(p_raw)

def checked(path,key):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != p[key]:
        raise ValueError(f"changed evidence: {key}")
    return json.loads(raw)

flux = checked(photometry,"photometrySHA256")
pairs = checked(comparisons,"pairsSHA256")
frames = {row["index"]:row["member"] for row in pairs["frames"]}
database = {}
for row in flux["rows"]:
    if row["parity"] in p["greenParities"]:
        key = (row["member"],row["parity"],row["star"])
        assert key not in database
        assert all(math.isfinite(v) and v > 0 for line in row["flux"] for v in line)
        database[key] = row["flux"]

def percentile90(values):
    return quantiles(values,n=10,method="inclusive")[-1]

def measure(ref, target):
    cohorts = [{star for member,parity,star in database if member==m and parity==g}
               for m,g in product((ref,target),p["greenParities"])]
    common = sorted(set.intersection(*cohorts))
    tiles = {star:star.split("-",1)[0] for star in common}
    groups = sorted(set(tiles.values()),key=int)
    assert len(common) >= p["minimumStars"] and len(groups) >= p["minimumTiles"]
    variants = []
    for green, cal, center in product(p["greenParities"], p["calibrations"], p["centers"]):
        ratios = {
            star: math.log(database[(ref,green,star)][cal][center]/database[(target,green,star)][cal][center])
            for star in common
        }
        full = median(ratios.values())
        results, held_out, raw_residuals = [], [], []
        for group in groups:
            fitted = median(v for star,v in ratios.items() if tiles[star]!=group)
            measured = [v for star,v in ratios.items() if tiles[star]==group]
            deviations = [100*math.expm1(v-fitted) for v in measured]
            held_out.extend(deviations)
            raw_residuals.extend(100*math.expm1(v) for v in measured)
            results.append({"withheldTile":group,"testStars":len(measured),"fittedScale":math.exp(fitted),
                            "heldOutSignedMedianPercent":median(deviations)})
        variants.append({"parity":green,"calibration":cal,"center":center,"fullScale":math.exp(full),
                         "heldOutP90AbsolutePercent":percentile90(list(map(abs,held_out))),
                         "unscaledP90AbsolutePercent":percentile90(list(map(abs,raw_residuals))),
                         "folds":results})
    scales = [f["fittedScale"] for v in variants for f in v["folds"]]
    low,high = min(scales),max(scales)
    return {"stars":len(common),"tiles":len(groups),"variants":variants,
            "observedScaleEnvelope":[low,high],
            "envelopeEntirelyAboveUnity": low>1,
            "envelopeEntirelyBelowUnity": high<1,
            "bands":[{"percent":band, "entireEnvelopeOutside": low>1+band/100 or high<1-band/100,
                      "entireEnvelopeInside": low>=1-band/100 and high<=1+band/100}
                     for band in p["decisionBandsPercent"]]}

rows = []
for pair in pairs["cases"]:
    ref,target = pair["referenceIndex"],pair["targetIndex"]
    rows.append({"referenceIndex":ref,"targetIndex":target,
                 **measure(frames[ref],frames[target])})
n = len(rows)
assert n == 27
summary = {
    "pairs":n,"starsMin":min(r["stars"] for r in rows),"starsMax":max(r["stars"] for r in rows),
    "distinctTilesEachPair":sorted(set(r["tiles"] for r in rows)),
    "overallScaleEnvelope":[min(r["observedScaleEnvelope"][0] for r in rows),
                             max(r["observedScaleEnvelope"][1] for r in rows)],
    "bands":[{"percent":b,
              "pairsEntirelyOutside":sum(r["bands"][i]["entireEnvelopeOutside"] for r in rows),
              "pairsEntirelyInside":sum(r["bands"][i]["entireEnvelopeInside"] for r in rows)}
             for i,b in enumerate(p["decisionBandsPercent"])],
}
variants = [v for r in rows for v in r["variants"]]
summary["variantFits"] = len(variants)
summary["heldOutP90Improved"] = sum(v["heldOutP90AbsolutePercent"]<v["unscaledP90AbsolutePercent"] for v in variants)
summary["medianOfHeldOutP90AbsolutePercent"] = median(v["heldOutP90AbsolutePercent"] for v in variants)
summary["medianOfUnscaledP90AbsolutePercent"] = median(v["unscaledP90AbsolutePercent"] for v in variants)
report = {"schema":"BKL046_M8_M20_STELLAR_SCALE_V1","protocolSHA256":p_hash,
          "authorities":{"photometry":p["photometrySHA256"],"pairs":p["pairsSHA256"]},
          "programSHA256":sha256(Path(__file__).read_bytes()).hexdigest(),
          "summary":summary,"rows":rows,"nativeExecutions":0,"scientificClosures":0}
output.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n",encoding="utf-8",newline="\n")
