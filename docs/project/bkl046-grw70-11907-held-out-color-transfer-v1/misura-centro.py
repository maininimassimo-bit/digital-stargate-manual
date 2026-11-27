"""Test cross-band center prediction on the complete reserved cohort of GRW70 WFC3 visits."""
import argparse
from collections import Counter
from hashlib import sha256
from io import BytesIO
from itertools import combinations
import json
from math import log10
from pathlib import Path
from statistics import median
import sys
import warnings

PIN = "deb03635b4062d073056d2cb5475733e89efcc50d3ffac362b0599f8d550ee0a"


def read(path, expected):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected:
        raise ValueError(f"Input changed: {path.name}")
    return raw


def donor_peak(np, science, dq, aim, protocol):
    half = protocol["donorHalfBoxPx"]
    x, y = np.rint(aim).astype(int)
    height, width = science.shape
    if not (half <= x < width-half and half <= y < height-half):
        return None
    zone = np.s_[y-half:y+half+1,x-half:x+half+1]
    patch = science[zone]
    good = (dq[zone] == 0) & np.isfinite(patch)
    if good.sum() < 2:
        return None
    contrast = patch - np.median(patch[good])
    index = np.argmax(np.where(good,contrast,-np.inf))
    j, i = np.unravel_index(index,patch.shape)
    gy,gx = np.ogrid[:patch.shape[0],:patch.shape[1]]
    outside = good & ((gy-j)**2+(gx-i)**2 > protocol["exclusionAroundPeakPx"]**2)
    if not outside.any():
        return None
    signal, secondary = float(contrast[j,i]),float(contrast[outside].max())
    if signal < protocol["minimumDonorPeakElectrons"] or signal < protocol["minimumProminenceRatio"]*secondary:
        return None
    return dict(xy=[int(x+i-half),int(y+j-half)], signal=signal, secondary=secondary)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("root","previous","dependencies","earlier","first_batch","report"):
        cli.add_argument(name,type=Path)
    cli.add_argument("capture_sha256")
    cli.add_argument("primary_report_sha256")
    a = cli.parse_args()
    home = a.root
    frozen = json.loads(read(home/"protocollo-centro.json", PIN))
    plan = json.loads(read(home/"protocollo.json",frozen["primaryProtocol"]))
    capture = json.loads(read(home/"acquisizione.json",a.capture_sha256))
    initial = json.loads(read(home/"riscontro.json",a.primary_report_sha256))
    if initial["acquisitionSha256"] != a.capture_sha256 or initial["protocolSha256"] != frozen["primaryProtocol"]:
        raise ValueError("Primary report identity changed")
    old = json.loads(read(a.previous/"protocollo.json",plan["cohortProtocolSha256"]))
    code = read(a.previous/"misura.py",plan["measureSha256"])
    scope={"__name__":"verified_helper"}
    exec(compile(code,str(a.previous/"misura.py"),"exec"),scope)
    measure=scope["measure"]

    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS, FITSFixedWarning
    warnings.filterwarnings("ignore",category=FITSFixedWarning)
    if (np.__version__,astropy.__version__) != ("2.3.5","7.2.0"):
        raise ValueError("Runtime differs")
    pams = {int(chip):fits.getdata(BytesIO(read(home/f"UVIS{chip}wfc3_map.fits",pin)))
            for chip,pin in old["pam"].items()}
    items = {entry["file"]:entry for r in capture["records"] for entry in r["entries"]}
    if len(initial["rows"]) != 126 or len(initial["visits"]) != 42:
        raise ValueError("Input scope differs")
    results=[]
    visits=[]
    for visit in initial["visits"]:
        inputs = {}
        visit_rows = [r for r in initial["rows"] if r["visit"]==visit["visit"]]
        if len(visit_rows) != 3:
            raise ValueError("Triplet size changed")
        if any(r["file"] not in items or "seedXY" not in r or r["state"] == "GAIA_SEED_OUT_OF_BOUNDS"
               for r in visit_rows):
            results.extend(dict(file=r["file"], visit=r["visit"], band=r["band"],
                                state="INCOMPLETE_PRIMARY_INPUT") for r in visit_rows)
            visits.append(dict(visit=visit["visit"],colors={},coverage={},state="INCOMPLETE_PRIMARY_INPUT"))
            continue
        for row in visit_rows:
            desc = items[row["file"]]
            with fits.open(BytesIO(read(home/"source"/row["file"],desc["sha256"])),memmap=False) as h:
                sci,err,dq = (h[key,1] for key in ("SCI","ERR","DQ"))
                inputs[row["band"]] = (row,WCS(sci.header,h).celestial,sci.header.copy(),
                                        sci.data.astype(float),err.data.astype(float),dq.data.copy())
        if set(inputs) != set(old["bands"]):
            raise ValueError("Incomplete input bands")
        predictions = {b:donor_peak(np, item[3],item[5],item[0]["seedXY"],frozen) for b,item in inputs.items()}
        attempt=[]
        for band,item in sorted(inputs.items()):
            row,wcs,header,sci,err,dq=item
            donors=[b for b in inputs if b!=band and predictions[b] is not None]
            case={k:row[k] for k in ("band","visit","chip","dither","exptimeSeconds","startMjd","file")}
            case.update(state="DONOR_SUPPORT_REFUSED",fluxCalibratedRadii={},donors={b:predictions[b] for b in donors})
            attempt.append(case)
            results.append(case)
            if len(donors)!=2:
                continue
            points=[np.array(wcs.world_to_pixel_values(*inputs[b][1].pixel_to_world_values(*predictions[b]["xy"])))
                    for b in donors]
            spread=float(np.linalg.norm(points[0]-points[1]))
            case["donorSeparationPx"]=spread
            if not np.isfinite(points).all() or spread>frozen["maximumDonorAgreementPx"]:
                case["state"]="DONOR_DISAGREEMENT"
                continue
            seed=(points[0]+points[1])/2
            case["predictedXY"]=seed.tolist()
            case["gaiaToPredictionPx"]=float(np.linalg.norm(seed-row["seedXY"]))
            height,width=sci.shape
            if not (28 <= seed[0] < width-28 and 28 <= seed[1] < height-28):
                case["state"]="PREDICTED_BOUNDARY"
                continue
            case["state"]=measure(np,sci,err,dq,pams[row["chip"]],seed,header,old,case)
        summary=dict(visit=visit["visit"],colors={},coverage={})
        visits.append(summary)
        if len({(r["chip"],tuple(r["dither"])) for r in attempt})!=1 or visit["spanDays"]>old["maxTripletSpanDays"]:
            continue
        summary["chip"] = attempt[0]["chip"]
        for radius in map(str,old["apertureRadii"]):
            flux={r["band"]:r["fluxCalibratedRadii"][radius] for r in attempt if radius in r["fluxCalibratedRadii"]}
            summary["coverage"][radius]=len(flux)
            if len(flux)==3:
                summary["colors"][radius]={f"{b}-{r}":-2500*log10(flux[b]/flux[r])
                                            for b,r in combinations(old["bands"],2)}
        if len(summary["colors"])==2:
            left,right=summary["colors"]["5"],summary["colors"]["10"]
            summary["apertureChangeMillimag"]={col:right[col]-left[col] for col in left}
    transfer = frozen["transfer"]
    first_batch = json.loads(read(a.first_batch,transfer["firstBatchReportSha256"]))
    early = first_batch["visits"]
    first_roster = {v["visit"] for v in early}
    reserve_roster = {v["visit"] for v in visits}
    if not (len(first_roster) == 20 and len(reserve_roster) == 42
            and first_roster == set(plan["priorFrozenFirstBatch"]) and first_roster.isdisjoint(reserve_roster)
            and set(plan["priorExploratoryVisits"]).isdisjoint(first_roster | reserve_roster)):
        raise ValueError("Visit cohorts overlap or differ")
    first_eligible = [dict(v, batch="first") for v in early if "apertureChangeMillimag" in v]
    reserved_eligible = [dict(v, batch="reserve") for v in visits if "apertureChangeMillimag" in v]
    eligible = first_eligible + reserved_eligible

    def estimate(visit, population):
        pool = [other for other in population if other["visit"] != visit["visit"] and other["chip"] == visit["chip"]]
        result = dict(visit=visit["visit"], chip=visit["chip"], batch=visit["batch"],
                      training=[row["visit"] for row in pool], state="INSUFFICIENT_OTHER_VISITS")
        if len(pool) >= transfer["trainingMinimumOtherVisits"]:
            observed = visit["apertureChangeMillimag"]
            reference = {c:median(row["apertureChangeMillimag"][c] for row in pool) for c in observed}
            result.update(state="SAME_CHIP_VISIT_DISJOINT", predicted=reference, observed=observed,
                          uncorrectedError=observed, error={c:observed[c]-reference[c] for c in reference})
        return result

    def summarize(predictions):
        scored = [row for row in predictions if row["state"] == "SAME_CHIP_VISIT_DISJOINT"]
        return {
            band: dict(cases=len(scored),
                       medianAbsoluteError=median(abs(row["error"][band]) for row in scored),
                       medianAbsoluteUncorrected=median(abs(row["uncorrectedError"][band]) for row in scored),
                       maximumAbsoluteError=max(abs(row["error"][band]) for row in scored),
                       improved=sum(abs(row["error"][band]) < abs(row["uncorrectedError"][band]) for row in scored))
            for band in scored[0]["error"]
        } if scored else {}

    predictions = [estimate(v,eligible) for v in eligible]
    independent = [estimate(v,first_eligible) for v in reserved_eligible]
    previous = json.loads(read(a.earlier,transfer["priorExploratoryReportSha256"]))
    prior_id = transfer["priorExploratoryVisit"]
    prior, = [r for r in previous["visits"] if r["visit"] == prior_id]
    prior_chip, = {r["chip"] for r in previous["rows"] if r["visit"] == prior_id}
    exploratory = [dict(visit=v["visit"], chip=v["chip"],
                        difference={c:value-prior["apertureChangeMillimag"][c]
                                    for c,value in v["apertureChangeMillimag"].items()})
                   for v in eligible if v["chip"] == prior_chip]
    output=dict(schema=frozen["schema"]+"_RESULT",protocolSha256=PIN,
                acquisitionSha256=a.capture_sha256, primaryReportSha256=a.primary_report_sha256,
                visitDisjointPredictions=predictions, reservedPredictionsFromFirstBatch=independent,
                visitDisjointSummary=summarize(predictions), reservedSummary=summarize(independent),
                acceptedCombinedVisits=eligible, earlierExploratoryComparison=exploratory,
                programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                rows=results,visits=visits,stateCounts=Counter(r["state"] for r in results),
                completeAlternateCenterVisits=sum("apertureChangeMillimag" in v for v in visits),
                astrometricFieldTieVerified=False,scientificClosures=0,nativeExecutions=0)
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(output,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()