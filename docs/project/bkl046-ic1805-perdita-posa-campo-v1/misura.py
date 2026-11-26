from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path

parser = ArgumentParser()
for name in ("geometry", "associations", "omissions", "output"):
    parser.add_argument(name, type=Path)
args = parser.parse_args()


def read_pinned(path, expected):
    data = path.read_bytes()
    if sha256(data).hexdigest() != expected:
        raise ValueError(f"Changed evidence: {path.name}")
    return json.loads(data)


geometry = read_pinned(args.geometry, "e3d06b80ec65272d117e251c43d212c8eae01740c121d98472edd3cbba208c5b")
associations = read_pinned(args.associations, "a7d0c4d58cb59d6898aa597e3faf94cbbc40b94871dcb41f8f54028586d812a9")
omissions = read_pinned(args.omissions, "b8e8ccd6dc0ff766805db16f07e58b481da849572c929bdb145d18f9f32f2aac")
frames = associations["rows"]
stars = {row["referenceOrdinal"]: row for row in geometry["rows"]}
if len(stars) != 72 or len(frames) != 38 or len({row["member"] for row in frames}) != 38:
    raise ValueError("Unexpected cohort or duplicate frame")
if any(row["status"] != "evaluated" or len(set(row["testOrdinals"])) != row["test"]
       for row in frames):
    raise ValueError("Incomplete or ambiguous frame associations")

# The producer checked all ordered associations before appending shifts to index % 2.
# Its first visit built the reference and never appended its own shift.
frame_indexes = {}
for ordinal, star in stars.items():
    matches = [[], []]
    for index, frame in enumerate(frames):
        if ordinal in frame["testOrdinals"]:
            matches[index % 2].append(index)
    if list(map(len, matches)) != star["matchedPerHalf"]:
        raise ValueError(f"Changed frame cardinality for {ordinal}")
    frame_indexes[ordinal] = matches

summaries = []
for width in (1, 0.7):
    rows = [next(item for item in star["tests"] if item["width"] == width)
            for star in omissions["rows"]]
    if [star["ordinal"] for star in omissions["rows"]] != list(stars):
        raise ValueError("Changed star order")
    nominal = sum(row["previouslyNominalTwo"] for row in rows)
    results = [
        dict(frameOrdinal=index + 1, half=index % 2 + 1,
             archiveMemberNameSha256=sha256(frame["member"].encode()).hexdigest(),
             matchedStars=0, starsStillAtLeastTwo=nominal, starsCrossingBelowTwo=0,
             starsCrossingAboveTwo=0, starsWithEmptyCell=0)
        for index, frame in enumerate(frames)
    ]
    for ordinal, row in zip(stars, rows, strict=True):
        matches = frame_indexes[ordinal]
        seen = set()
        for case in row["cases"]:
            index = matches[case["half"]][case["omittedLocalOrdinal"]]
            if index in seen:
                raise ValueError("Duplicate omission for a star")
            seen.add(index)
            item = results[index]
            item["matchedStars"] += 1
            passed_before = row["previouslyNominalTwo"]
            passed_after = case["minEffectiveCount"] >= 2 - 1e-12
            item["starsStillAtLeastTwo"] += int(passed_after) - int(passed_before)
            item["starsCrossingBelowTwo"] += int(passed_before and not passed_after)
            item["starsCrossingAboveTwo"] += int(passed_after and not passed_before)
            item["starsWithEmptyCell"] += int(case["minPositiveCount"] == 0)
        if len(seen) != sum(map(len, matches)):
            raise ValueError("Incomplete omissions")
    if sum(row["matchedStars"] for row in results) != 2021:
        raise ValueError("Unexpected omission count")
    for row in results:
        row["netReductionInStarsAtLeastTwo"] = nominal - row["starsStillAtLeastTwo"]
    summaries.append(dict(width=width, nominalStarsAtLeastTwo=nominal,
                          greatestNetLoss=max(row["netReductionInStarsAtLeastTwo"] for row in results),
                          greatestLoss=max(row["starsCrossingBelowTwo"] for row in results),
                          framesWithCoverageLoss=sum(row["starsCrossingBelowTwo"] > 0 for row in results),
                          framesWithEmptyCell=sum(row["starsWithEmptyCell"] > 0 for row in results),
                          frames=results))
result = dict(schema="BKL046_IC1805_CFA_FIELD_EXPOSURE_LOSS_V1",
              associationProducerSha256="7773d661ef973170a305b36f776b5c6533203ca43c0b7804a5ea4ef22994ef14",
              referenceIsDeletionCandidate=False, scienceClosures=0, widths=summaries)
with args.output.open("x", encoding="utf-8", newline="\n") as out:
    json.dump(result, out, indent=2, allow_nan=False)
    out.write("\n")
