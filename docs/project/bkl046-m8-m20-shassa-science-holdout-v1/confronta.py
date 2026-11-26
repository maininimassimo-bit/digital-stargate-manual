"""Compare three fixed H-alpha layouts on measured differential science frames."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


def read(path, expected):
    data = path.read_bytes()
    assert sha256(data).hexdigest() == expected, path.name
    return data


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "layouts", "injection", "reference", "joint", "dependencies", "output"):
        parser.add_argument(name, type=Path)
    a = parser.parse_args()
    raw = a.protocol.read_bytes()
    p = json.loads(raw)
    layouts = json.loads(read(a.layouts, p["layoutPin"]))["layoutCells"]
    assert list(sorted(layouts)) == ["globalLowest", "original", "stratifiedLowest"]
    held = {i for ids in layouts.values() for i in ids}
    assert len(held) == 15
    inj_report = json.loads(read(a.injection / "riscontro.json", p["injectionReportPin"]))
    inj_protocol = a.injection / "protocollo.json"
    read(inj_protocol, inj_report["protocolSha256"])
    read(a.joint, p["jointPin"])
    prog = a.injection / "iniezioni.py"
    prefix, marker, _ = read(prog, p["injectionProgramPin"]).decode().partition("\ncontrol = fit(")
    assert marker
    argv = sys.argv
    sys.argv = list(map(str, (prog, inj_protocol, a.reference, a.joint, a.dependencies, a.output)))
    scope = {"__file__": str(prog)}
    try:
        exec(compile(prefix, str(prog), "exec"), scope)
    finally:
        sys.argv = argv
    assert scope["p"]["peakAdu"] == 2
    assert scope["p"]["relativeTolerance"] == p["profileTolerance"]
    np = scope["np"]
    images, groups, common, x, y, signals, signal_bins = (scope[k] for k in (
        "images", "groups", "common", "x", "y", "signals", "signal_bins"))
    cases = scope["joint"]["cases"]
    assert len(cases) == p["pairCount"] == len({(r["reference"], r["target"]) for r in cases})
    supports = [common[s] for s in groups]
    check = np.array([i for i in range(len(groups)) if i not in held])
    assert (len(groups), len(check)) == (192, 177)
    assert all(s.any() for s in supports)
    design = np.array([[1., float(x[s].mean()), float(y[s].mean())] for s in groups])
    estimators = {}
    for name, ids in layouts.items():
        matrix = design[ids]
        pinvs = [np.linalg.pinv(matrix[:, :n]) for n in (1, 3)]
        for n, inv in zip((1, 3), pinvs, strict=True):
            np.testing.assert_allclose(inv @ matrix[:, :n], np.eye(n), atol=1e-12, rtol=0)
        estimators[name] = dict(zip(("offset", "plane"), pinvs, strict=True))

    def stats(bins, vector, n):
        err = np.abs(bins[check] - design[check, :n] @ vector)
        med, p90 = np.quantile(err, [.5, .9])
        return {"medianAdu": float(med), "p90Adu": float(p90)}

    results = []
    for pair in cases:
        ref, target = pair["reference"], pair["target"]
        delta = images[target] - images[ref]
        cell_data = [delta[s][good] for s, good in zip(groups, supports, strict=True)]
        observed = np.asarray([np.median(v) for v in cell_data])
        row = {"reference": ref, "target": target, "layouts": {}}
        for name, ids in layouts.items():
            item = {}
            for kind, inv in estimators[name].items():
                n = inv.shape[0]
                before = inv @ observed[ids]
                injected = {}
                for feature, signal in signals.items():
                    after_cells = [np.median(cell_data[i] + signal_bins[feature][i]) for i in ids]
                    after = inv @ after_cells
                    injected[feature] = scope["assess"](signal, before, after)
                    no_change = scope["assess"](signal, before, before)
                    assert no_change == {"relativeFluxError": 0., "relativeL2": 0., "pass": True}
                item[kind] = {"holdout": stats(observed, before, n), "injections": injected}
            baseline, plane = [item[key]["holdout"] for key in ("offset", "plane")]
            item["planePass"] = (plane["medianAdu"] <= (1 - p["relativeMedianGainMinimum"]) * baseline["medianAdu"]
                                 and plane["p90Adu"] <= baseline["p90Adu"])
            row["layouts"][name] = item
        results.append(row)
    summary = {}
    for name in layouts:
        rows = [r["layouts"][name] for r in results]
        matched = sum(
            r["layouts"][name]["plane"]["holdout"]["medianAdu"] <= r["layouts"]["original"]["plane"]["holdout"]["medianAdu"]
            and r["layouts"][name]["plane"]["holdout"]["p90Adu"] <= r["layouts"]["original"]["plane"]["holdout"]["p90Adu"]
            for r in results
        )
        summary[name] = {"planePasses": sum(row["planePass"] for row in rows),
                         "planeNoWorseThanOriginalBoth": matched,
                         "passesByReference": {str(ref): sum(r["layouts"][name]["planePass"]
                                               for r in results if r["reference"] == ref)
                                               for ref in sorted({r["reference"] for r in results})}}
        for kind in ("offset", "plane"):
            summary[name][kind] = {
                "medianOfHeldOutMedianAdu": float(np.median([r[kind]["holdout"]["medianAdu"] for r in rows])),
                "medianOfHeldOutP90Adu": float(np.median([r[kind]["holdout"]["p90Adu"] for r in rows])),
                "injections": {feature: {
                    "passes": sum(r[kind]["injections"][feature]["pass"] for r in rows),
                    "medianAbsoluteRelativeFluxError": float(np.median(
                        [abs(r[kind]["injections"][feature]["relativeFluxError"]) for r in rows])),
                    "medianRelativeL2": float(np.median([r[kind]["injections"][feature]["relativeL2"] for r in rows])),
                } for feature in signals}
            }

    def save(name, value):
        data = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
        with (a.output / name).open("xb") as stream:
            stream.write(data)
        return sha256(data).hexdigest()

    full = save("tutti-gli-esiti.json", {"cases": results, "layoutCells": layouts, "heldOutCells": check.tolist()})
    doc = {"schema": "BKL046_M8M20_SHASSA_SCIENCE_HOLDOUT_RESULT_V1",
           "protocolSha256": sha256(raw).hexdigest(), "programSha256": sha256(Path(__file__).read_bytes()).hexdigest(),
           "cases": len(results), "heldOutCells": len(check), "pairedReferences": len({r["reference"] for r in results}),
           "fullReportSha256": full, "summary": summary, "coobservedBroadbandAnchors": 0,
           "nativeExecutions": 0, "scientificClosures": 0}
    save("riscontro.json", doc)


if __name__ == "__main__":
    main()
