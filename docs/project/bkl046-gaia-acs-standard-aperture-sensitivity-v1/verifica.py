"""Reconcile observed aperture growth with the frozen synthetic Gaia narrow-band ratio."""
from hashlib import sha256
from itertools import product
import json
from math import isclose, isfinite
from pathlib import Path
from statistics import mean
import sys

PLAN_PIN = "5993f49facd8e615a49bcbe9ac8159ec3e25bc6a4d1851b8838effd5c83f339f"


def require(ok, label):
    if not ok:
        raise ValueError(label)


def pinned(path, pin):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == pin, "Input digest changed")
    return json.loads(raw)


def ratios(left, right, key):
    choices = [a[key]/b[key] for a,b in product(left,right)]
    return dict(combinations=len(choices), low=min(choices), high=max(choices),
                ratioOfMeans=mean(x[key] for x in left)/mean(x[key] for x in right))


def evaluate(star, exposures, prediction, covariance, plan):
    left, right = plan["narrowBands"]
    ratio_name = left + "/" + right
    target = prediction["ratios"][ratio_name]
    sigma = covariance["ratios"][ratio_name]["full"]["upperUnknownCross"]
    gaia = target["gaiaFullGridRate"]
    require(gaia > 0 and sigma > 0 and len(exposures["rows"]) == 6, "Unexpected inputs")
    all_rows = {name: [item for item in exposures["rows"] if item["band"] == name]
                for name in (left, right)}
    require(all(len(items) == len({row["file"] for row in items}) == 2
                for items in all_rows.values()), "Exposure roster differs")
    ref_radius = str(plan["radiiPixels"][0])
    rows = []
    for radius in plan["radiiPixels"]:
        selected = {name:[] for name in (left,right)}
        paired_reference = {name:[] for name in (left,right)}
        for name in (left,right):
            for item in all_rows[name]:
                current = item["apertures"][str(radius)]
                start = item["apertures"][ref_radius]
                require(start["state"] == "MEASURED", "Reference aperture unavailable")
                if current["state"] == "MEASURED":
                    require(all(isfinite(current[k]) and current[k] > 0
                                for k in ("rate", "rateExcludingDq64")), "Invalid aperture rate")
                    selected[name].append(current)
                    paired_reference[name].append(start)
        row = dict(radiusPx=radius, numeratorAccepted=len(selected[left]),
                   denominatorAccepted=len(selected[right]),
                   completeRepeatedExposures=all(len(items) == 2 for items in selected.values()))
        if selected[left] and selected[right]:
            actual = ratios(selected[left], selected[right], "rate")
            paired = ratios(paired_reference[left], paired_reference[right], "rate")
            drop = ratios(selected[left], selected[right], "rateExcludingDq64")
            pairwise_growth = [((a["rate"]/b["rate"])/(aa["rate"]/bb["rate"])-1)
                               for (a,aa),(b,bb) in product(zip(selected[left],paired_reference[left]),
                                                            zip(selected[right],paired_reference[right]))]
            current = actual["ratioOfMeans"]
            require(isclose(current, target["observedApertureRate"], rel_tol=1e-12)
                    if radius == int(ref_radius) else current > 0, "Archived ratio differs")
            row.update(observed=actual, pairedThreePixel=paired,
                       apertureGrowth= current/paired["ratioOfMeans"]-1,
                       pairwiseGrowthRange=[min(pairwise_growth),max(pairwise_growth)],
                       omitDq64RelativeShift=drop["ratioOfMeans"]/current-1,
                       furtherDifferentialIncreaseToReachGaia=gaia/current-1,
                       minimumFurtherIncreaseAcrossPairs=gaia/actual["high"]-1,
                       residualLowerBoundAcrossPairsRelativeToGaia=(gaia-actual["high"])/gaia,
                       residualLowerBoundOverGaiaOnlyFormalSigma=(gaia-actual["high"])/gaia/sigma)
            if radius == 10:
                ee = plan["catalogueEEAtHalfArcsecond"]
                row["illustrativeUsingTabulatedEqualEE"] = current * ee[right]/ee[left]
        rows.append(row)
    return dict(gaiaRatio=gaia, calspecInfiniteRatio=target["calspecFullRate"], methods=rows)


def main():
    spec_path, gd71, gd153, photometry, covariance, out = map(Path, sys.argv[1:])
    plan = pinned(spec_path, PLAN_PIN)
    photo = pinned(photometry, plan["gaiaComparisonSha256"])["comparisons"]
    cov = pinned(covariance, plan["gaiaCovarianceSha256"])["targets"]
    control = ratios([{"rate":2.},{"rate":3.}],[{"rate":1.},{"rate":2.}],"rate")
    require(control == dict(combinations=4,low=1.,high=3.,ratioOfMeans=5/3), "Pair-product control failed")
    result = {}
    for star, rows in (("GD71", pinned(gd71, plan["gd71GrowthSha256"])),
                       ("GD153", pinned(gd153, plan["gd153GrowthSha256"]))):
        result[star] = evaluate(star, rows, photo[star], cov[star], plan)
    report = dict(schema="BKL046_GAIAXP_ACS_APERTURE_RESULT_V1", protocolSha256=PLAN_PIN,
                  exposurePairRangesAreConfidenceIntervals=False, calibratedApertureExtrapolation=False,
                  calibratedCteCorrectionApplied=False, targets=result, scientificClosures=0, nativeExecutions=0)
    with out.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write("\n")


if __name__=="__main__":
    main()
