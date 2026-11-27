"""Index exact serialized spans for rights review without copying matched text."""
from bisect import bisect_right
from collections import Counter
from hashlib import file_digest, sha256
import json
import mmap
from pathlib import Path
import re
import sys
from tempfile import TemporaryFile
from zipfile import ZipFile

spec_path, capsule_path, index_path, private_out, out = map(Path, sys.argv[1:])
spec = json.loads(spec_path.read_bytes())


def require(ok, message):
    if not ok:
        raise ValueError(message)


with capsule_path.open("rb") as archive_file:
    require(file_digest(archive_file, "sha256").hexdigest() == spec["capsule"], "Changed capsule")
index_bytes = index_path.read_bytes()
require(sha256(index_bytes).hexdigest() == spec["embeddedIndex"], "Changed embedded index")
inventory = json.loads(index_bytes)
require([row["ordinal"] for row in inventory] == list(range(1, 709)), "Changed ordinals")
starts = [row["embeddedByteRange"][0] for row in inventory]
ends = [row["embeddedByteRange"][1] for row in inventory]
require(all(a < b for a, b in zip(starts, ends, strict=True))
        and all(a < b for a, b in zip(ends[:-1], starts[1:], strict=True)), "Overlapping intervals")

# Bounded marker families intentionally do not try to interpret the rights of a reference.
patterns = {
    "localPath": rb"(?i:[A-Z]:\\{1,4}(?:Users|DigitalStarGate|Codex|Program Files|DSG-CAL)\\{1,4}|\\\\(?:[0-9]{1,3}\.){3}[0-9]{1,3}\\)",
    "gaiaArchive": rb"(?i:gea\.esac\.esa\.int|archives\.esac\.esa\.int|gaia\.aip\.de|gaia-dpci)",
    "otherDataArchive": rb"(?i:mast\.stsci\.edu|archive\.stsci\.edu|vizier\.(?:cds|u-strasbg)|cdsarc\.cds\.unistra\.fr|irsa\.ipac\.caltech\.edu)",
    "vendorReference": rb"(?i:pixinsight\.com|pleiades-astrophoto\.com|#include\s+[<][A-Za-z0-9_/]+\.jsh[>])",
    "attachmentEncoding": rb'(?i:"(?:base64|contentBase64|artifactBytesBase64)"\s*:|"data:(?:image|application)/[a-z0-9.+-]+;base64,)',
}
top_keys = re.compile(rb'^  "([a-zA-Z][a-zA-Z0-9_]{0,100})": ', re.M)
counts = {label: Counter() for label in patterns}
in_reports = {label: set() for label in patterns}
rows_by_marker = {row["ordinal"]: Counter() for row in inventory}
with ZipFile(capsule_path) as archive, TemporaryFile(dir=out.parent) as work:
    member = "objects/Conoscenza-PixInsight-v1.146.json"
    require(archive.namelist().count(member) == 1, "Unexpected knowledge entry")
    digest = sha256()
    with archive.open(member) as stream:
        while data := stream.read(1 << 20):
            work.write(data)
            digest.update(data)
    require(work.tell() == spec["size"] and digest.hexdigest() == spec["knowledge"], "Changed knowledge")
    work.flush()
    with mmap.mmap(work.fileno(), 0, access=mmap.ACCESS_READ) as raw:
        require(raw[:3] == b"{\r\n" and raw[-3:].strip() == b"}", "Unknown serializer")
        sections = [(match.start(), match[1].decode("ascii")) for match in top_keys.finditer(raw)]
        require(len(sections) >= 10 and len({name for _, name in sections}) == len(sections),
                "Unexpected serialized section boundaries")
        offsets = [start for start, _ in sections]
        section_for = lambda position: sections[bisect_right(offsets, position) - 1][1]
        require(section_for(starts[0]) == section_for(ends[-1]) == "recentEvidenceContents",
                "Changed evidence section")
        by_size = dict((name, end - start) for (start, name), end in
                       zip(sections, offsets[1:] + [len(raw)], strict=True))
        for label, rule in patterns.items():
            for match in re.finditer(rule, raw):
                pos = match.start()
                section = section_for(pos)
                counts[label][section] += 1
                index = bisect_right(starts, pos) - 1
                if index >= 0 and match.end() <= ends[index]:
                    in_reports[label].add(index + 1)
                    rows_by_marker[index + 1][label] += 1

        def span(a, b):
            return dict(start=a, endExclusive=b,
                        sha256=sha256(memoryview(raw)[a:b]).hexdigest())

        serialized = [dict(section=name, markers={label: hits[name] for label, hits in counts.items()},
                           **span(start, end))
                      for (start, name), end in zip(sections, offsets[1:] + [len(raw)], strict=True)]
        prefix = span(0, offsets[0])
        embedded = []
        for row in inventory:
            number = row["ordinal"]
            start, end = row["embeddedByteRange"]
            binding = span(start, end)
            require(binding["sha256"] == row["embeddedValueSha256"], "Changed embedded value")
            matches = len(row["priorAuditMatches"])
            markers = dict(rows_by_marker[number])
            if matches:
                queue = "RECHECK_PRIOR_MATCH"
            elif markers:
                queue = "EXAMINE_MARKERS"
            else:
                queue = "REVIEW_WITHOUT_MARKERS"
            embedded.append(dict(ordinal=number, priorMatches=matches, markers=markers,
                                 queue=queue, **binding))

require(prefix["start"] == 0 and prefix["endExclusive"] == serialized[0]["start"]
        and all(a["endExclusive"] == b["start"] for a, b in zip(serialized, serialized[1:]))
        and serialized[-1]["endExclusive"] == spec["size"], "Incomplete interval coverage")
grouping = Counter(row["queue"] for row in embedded)
sections_with_markers = sum(any(row["markers"].values()) for row in serialized)
review = dict(schema="BKL046_V1146_EXACT_RIGHTS_REVIEW_QUEUE_V1", knowledgeSha256=spec["knowledge"],
              prefix=prefix, sections=serialized, embedded=embedded, clearanceEstablished=False)
raw_queue = (json.dumps(review, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
report = dict(schema="BKL046_V1146_EXACT_RIGHTS_REVIEW_SUMMARY_V1", knowledgeSha256=spec["knowledge"],
              exactBytes=spec["size"], sectionCount=len(serialized),
              sectionsWithMarkers=sections_with_markers, embeddedCount=len(embedded),
              embeddedByQueue=dict(grouping), queueSha256=sha256(raw_queue).hexdigest(),
              completeSpanCoverage=True, matchingValuesExported=False,
              completeRedistributionClearanceEstablished=False, scientificClosures=0)
with private_out.open("xb") as stream:
    stream.write(raw_queue)
with out.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(report, stream, indent=2, sort_keys=True, allow_nan=False)
    stream.write("\n")
