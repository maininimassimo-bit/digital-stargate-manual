"""Evaluate full variance transfer across laboratory acquisitions, with disjoint target pairs."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

protocol, parent, output = map(Path, sys.argv[1:4])
raw = protocol.read_bytes()
cfg = json.loads(raw)
dependencies = sys.argv[4:]


def exact(path, expected):
    data = path.read_bytes()
    if sha256(data).hexdigest() != expected:
        raise ValueError(f"Changed input {path.name}")
    return data


program = parent / "misura.py"
policy = parent / "protocollo.json"
exact(policy, cfg["parentProtocol"])
expected = exact(parent / "riscontro.json", cfg["parentReport"])
ns = dict(__name__="lin0_heritage", __file__=str(program))
exec(compile(exact(program, cfg["parentProgram"]), str(program), "exec"), ns)
original = ns["evaluate"]
rows = []


def observe(np, kernel, base, target, raw_mask, plan, band):
    archived, support = original(np, kernel, base, target, raw_mask, plan, band)
    prior = {(r["channel"],r["frame"],r["firstExposure"]):r for r in archived}
    w = np.outer([.5, 1., .5], [.5, 1., .5]).ravel()
    frames = plan["frames"][1:]
    for c, rail in enumerate(raw_mask):
        mask, used = kernel.plan_support(np,rail)
        grid = ~rail[:63,:63].reshape(21,3,21,3).swapaxes(1,2).any(axis=(2,3))
        use = mask.sum() >= plan["minimumSupportBlocks"]
        signal_anchor, empirical_anchor, raw_anchor, gain_anchor = [], [], [], []
        if use:
            for level in frames:
                pairs = ns["pair_images"](base,level,c,20)
                measured = [kernel.evaluate(np,a,b,mask,used) for a,b in pairs]
                signal_anchor.append(float(np.median([m["signal"] for m in measured])))
                empirical_anchor.append(float(np.median([m["sumVariance"] for m in measured])))
                raw_anchor.append(float(np.median([m["inputVariance"] for m in measured])))
                gain_anchor.append(float(w @ ns["shapes"](np,pairs,grid).mean(axis=0) @ w))
            ns["need"](signal_anchor == sorted(set(signal_anchor)), "Changed GAIN levels")
        for frame in frames:
            pairs = ns["pair_images"](target,frame,c,30)
            measures = [kernel.evaluate(np,a,b,mask,used) for a,b in pairs] if use else []
            for i in range(len(pairs)):
                old = prior[c,frame,2*i+1]
                row = dict(band=band, channel=c, frame=frame, firstExposure=2*i+1,
                           referenceMatch=old.get("signalMatch", {}).get("state", old["state"]))
                if not use:
                    rows.append(dict(row, state="INSUFFICIENT_UNCLIPPED_SUPPORT"))
                    continue
                other = [m for j,m in enumerate(measures) if j != i]
                signal = float(np.median([m["signal"] for m in other]))
                observed = measures[i]["sumVariance"]
                baseline = float(np.median([m["sumVariance"] for m in other]))
                row.update(targetSignalFromOtherPairs=signal, targetVariance=observed,
                           lin0Empirical=baseline)
                if not signal_anchor[0] <= signal <= signal_anchor[-1]:
                    rows.append(dict(row, state="OUTSIDE_GAIN_RANGE"))
                    continue
                cross_empirical = float(np.interp(signal,signal_anchor,empirical_anchor))
                cross_raw = float(np.interp(signal,signal_anchor,raw_anchor))
                shape = float(np.interp(signal,signal_anchor,gain_anchor))
                ns["need"](min(observed,baseline,cross_empirical,cross_raw,shape) > 0, "Invalid variance")
                rows.append(dict(row, state="MEASURED", gainEmpirical=cross_empirical,
                                 gainRawCovariance=cross_raw*shape,
                                 gainRawIndependent=cross_raw*float(w@w)))
    return archived,support


ns["evaluate"] = observe
with TemporaryDirectory(dir=output.parent) as temp:
    replay = Path(temp)/"replay"
    sys.argv = [str(program), *dependencies, str(replay), cfg["capture"], str(policy)]
    ns["main"]()
    if (replay/"riscontro.json").read_bytes() != expected:
        raise ValueError("Observed parent did not replay exactly")
if len(rows) != 2880:
    raise ValueError("Changed coverage")
import numpy as np

summary = []
for band in ("lower","upper"):
    for level in (1,5,10):
        group = [r for r in rows if (r["band"],r["frame"]) == (band,level)]
        accepted = [r for r in group if r["state"] == "MEASURED"]
        if len(group) != 480:
            raise ValueError("Incomplete prediction grid")
        item = dict(band=band, frame=level, accepted=len(accepted), refused=len(group)-len(accepted),
                    previousSignalEligibilityChanged=sum(r["state"] != r["referenceMatch"] for r in group))
        if accepted:
            model = {}
            for name in ("lin0Empirical","gainEmpirical","gainRawCovariance","gainRawIndependent"):
                signed = np.array([r[name]/r["targetVariance"]-1 for r in accepted])
                abs_error = abs(signed)
                model[name] = dict(medianAbsolute=float(np.median(abs_error)),
                                   p95Absolute=float(np.quantile(abs_error,.95)),
                                   medianSigned=float(np.median(signed)))
            item["models"] = model
        summary.append(item)
output.mkdir()
detail = ns["save"](output/"dettaglio.json", rows)
ns["save"](output/"riscontro.json",
           dict(schema=cfg["schema"], parentReceiptSha256=cfg["parentReport"],
                detailSha256=detail, rowsVerified=len(rows), summary=summary,
                calibratedDoseMatched=False, nativeExecutions=0, scientificClosures=0))
