"""Check fixed geometric rejection rules for the GD153 three-color stress cases."""
import argparse
from collections import defaultdict
from hashlib import file_digest, sha256
from itertools import combinations
import json
from math import floor, isclose, isfinite, log10
from pathlib import Path
from zipfile import ZipFile

PROTOCOL_PIN = "33ced3f47be5a2e4fda01d928bfae696609a700518fd23e9a28ef2a6634f953d"


def expect(condition, message):
    if not condition:
        raise ValueError(message)


def read_report(path, pins):
    archive_pin, member, report_pin = pins
    with path.open("rb") as stream:
        expect(file_digest(stream, "sha256").hexdigest() == archive_pin, "Source ZIP changed")
    with ZipFile(path) as archive:
        expect(archive.namelist().count(member) == 1, "Ambiguous report member")
        raw = archive.read(member)
    expect(sha256(raw).hexdigest() == report_pin, "Source report changed")
    return json.loads(raw)


def case_key(row):
    return row["policy"], row["maskVisit"], row["maskChip"], row["referenceVisit"], tuple(row["dither"])


def color_error(first, second):
    if first is None or second is None or first <= -1 or second <= -1:
        return None
    expect(isfinite(first) and isfinite(second), "Non-finite recovered flux ratio")
    return -2500 * log10((1 + first) / (1 + second))


def construct(p, clean, masked, reference):
    bands = p["bands"]
    clean_index = {(r["visit"], tuple(r["dither"]), r["band"]): r["file"] for r in clean["rows"]}
    expect(len(clean_index) == len(clean["rows"]) == 48, "Clean exposure coverage differs")
    templates = {}
    for triplet in clean["triplets"]:
        if p["aperture"] not in triplet["measurements"]:
            continue
        visit, dither = triplet["visit"], tuple(triplet["dither"])
        expect(triplet["spanDays"] <= p["maxSpanDays"], "Triplet time span differs")
        for band in bands:
            name = clean_index[visit, dither, band]
            expect(name not in templates, "Duplicate clean exposure")
            templates[name] = (visit, dither, band)
    expect(len(templates) == 12 and len({t[0] for t in templates.values()}) == 2, "Clean triplet coverage differs")
    groups = defaultdict(dict)
    for row in masked["tests"]:
        template = templates.get(row["truthExposure"])
        if template is None:
            continue
        visit, dither, band = template
        expect((visit, band) == (row["truthVisit"], row["band"]), "Exposure identity differs")
        key = (row["policy"], row["maskVisit"], row["maskChip"], visit, dither)
        group = groups[key]
        expect(band not in group and type(row["coreMissing"]) is int and type(row["missing"]) is int
               and 0 <= row["coreMissing"] <= row["missing"], "Mask geometry differs")
        group[band] = row

    frozen = {case_key(row): row for row in reference["cases"]}
    expect(len(frozen) == len(reference["cases"]) == 56 and set(frozen) == set(groups), "Stress case coverage differs")
    cases = []
    for key, group in sorted(groups.items()):
        expect(set(group) == set(bands), "Incomplete color triplet")
        old = frozen[key]
        maximum = max(row["missing"] for row in group.values())
        maximum_core = max(row["coreMissing"] for row in group.values())
        expect(bool(maximum) == old["anyMissing"] and bool(maximum_core) == old["anyCoreMissing"],
               "Geometry disagrees with frozen color stress")
        error = {method: [] for method in p["methods"]}
        for blue, red in combinations(bands, 2):
            for method in p["methods"]:
                measured = color_error(group[blue]["relativeSignedError"][method],
                                       group[red]["relativeSignedError"][method])
                recorded = old["colors"][f"{blue}-{red}"][method]
                expect(measured is recorded or measured is not None and recorded is not None
                       and isclose(measured, recorded, abs_tol=1e-11), "Frozen color error differs")
                error[method].append(measured)
        worst = {method: None if None in values else max(map(abs, values)) for method, values in error.items()}
        cases.append(dict(policy=key[0], maskVisit=key[1], maskChip=key[2], referenceVisit=key[3], dither=key[4],
                          perBand={band: dict(total=row["missing"], core=row["coreMissing"]) for band, row in group.items()},
                          maxMissingPerBand=maximum, maxCoreMissingPerBand=maximum_core,
                          maxAbsoluteColorErrorMillimag=worst))
    return cases


def p90(samples):
    if not samples:
        return None
    ordered = sorted(samples)
    i = 0.9 * (len(ordered) - 1)
    low = floor(i)
    return ordered[low] + (i - low) * (ordered[min(low + 1, len(ordered) - 1)] - ordered[low])


def score(rows, methods, limits):
    summary = {}
    for method in methods:
        samples = [row["maxAbsoluteColorErrorMillimag"][method] for row in rows]
        measured = [sample for sample in samples if sample is not None]
        summary[method] = dict(measured=len(measured), p90WorstColor=p90(measured),
                               maxWorstColor=max(measured, default=None),
                               withinAllColors={str(limit): sum(sample <= limit for sample in measured)
                                                for limit in limits})
    return summary


def summarize(p, cases):
    result = []
    for policy in p["policies"]:
        population = [row for row in cases if row["policy"] == policy]
        expect(len(population) == 28 and len({r["maskVisit"] for r in population}) >= 2, "Unbalanced comparison")
        gates = {"all": population}
        for cap in p["gateCapOnMissingPerBand"]:
            name = "core-complete" if cap is None else f"core-complete-cap-{cap}"
            gates[name] = [row for row in population if row["maxCoreMissingPerBand"] == 0
                           and (cap is None or row["maxMissingPerBand"] <= cap)]
        for name, selected in gates.items():
            partitions = {}
            for field in ("referenceVisit", "maskVisit"):
                partitions[field] = []
                for value in sorted({row[field] for row in population}):
                    group = [row for row in selected if row[field] == value]
                    partitions[field].append(dict(visit=value, kept=len(group),
                                                  pool=sum(row[field] == value for row in population),
                                                  scores=score(group, p["methods"], p["limitsMillimag"])))
            result.append(dict(policy=policy, gate=name, kept=len(selected), pool=len(population),
                               scores=score(selected, p["methods"], p["limitsMillimag"]), byVisit=partitions))
    return result


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("protocol", "clean", "masked", "color", "report"):
        cli.add_argument(name, type=Path)
    args = cli.parse_args()
    raw = args.protocol.read_bytes()
    expect(sha256(raw).hexdigest() == PROTOCOL_PIN, "Protocol changed")
    p = json.loads(raw)
    clean, masked, reference = (read_report(getattr(args, key), p["inputs"][key])
                                for key in ("clean", "masked", "color"))
    cases = construct(p, clean, masked, reference)
    summary = summarize(p, cases)
    full = [row for row in summary if row["gate"] == "core-complete-cap-0"]
    expect(all(not row["kept"] or all(s["maxWorstColor"] is not None and s["maxWorstColor"] <= 1e-10 for s in row["scores"].values())
               for row in full), "Apertures with full support must be unchanged")
    output = dict(schema="BKL046_GD153_HELDOUT_MASK_GEOMETRIC_COLOR_COVERAGE_RESULT_V1",
                  protocolSha256=PROTOCOL_PIN, programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  referenceTriplets=4, referenceVisits=2, independentTargets=1,
                  maskVisitCount=len({case["maskVisit"] for case in cases}),
                  caseCount=len(cases), cases=cases, summary=summary, scientificClosures=0, nativeExecutions=0,
                  actualDamagedExposureColorVerified=False)
    with args.report.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(output, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()