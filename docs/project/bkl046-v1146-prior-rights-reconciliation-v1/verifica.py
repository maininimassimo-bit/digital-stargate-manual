"""Reconcile historical rights entries with restored members and embedded values."""
from collections import Counter
from decimal import Decimal
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile

ARCHIVE = "b206e8ec180be461948fe5a55027e1677a52377cf838481ab3bb2666067c55e4"
KNOWLEDGE = "7b11789d0616b54cb002c506f0bd2c4e4cfb123a0569f8c409a09da67b2e567e"
INDEX = "23bbdf2979d549d8e35db428b0c01c8b81c088086f3ef50c6b0083af3627e3f3"
RIGHTS = "769d5d943eb85df9d8d9f32537b8bd3a3b7e38c03c34509b596a3b140364b262"
MEMBER = "objects/Conoscenza-PixInsight-v1.146.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return sha256(data).hexdigest()


def exact_json(path, pin):
    data = path.read_bytes()
    require(digest(data) == pin, "Input digest differs")
    return json.loads(data)


def contents(archive, rows):
    position = 0
    overall = sha256()

    def consume(stream, count):
        nonlocal position
        while count:
            part = stream.read(min(count, 1 << 20))
            require(bool(part), "Premature EOF")
            overall.update(part)
            count -= len(part)
            position += len(part)
            yield part

    result = {}
    with archive.open(MEMBER) as stream:
        for row in rows:
            a, b = row["embeddedByteRange"]
            require(position <= a < b and b - a <= 50 << 20, "Unexpected embedded range")
            for _ in consume(stream, a - position):
                pass
            raw = b"".join(consume(stream, b - a))
            require(digest(raw) == row["embeddedValueSha256"], "Embedded hash differs")
            result[row["ordinal"]] = raw
        for _ in consume(stream, 1153824341 - position):
            pass
        require(not stream.read(1) and overall.hexdigest() == KNOWLEDGE, "Knowledge differs")
    return result


def load_json(raw):
    def unique(pairs):
        result = dict(pairs)
        require(len(result) == len(pairs), "Duplicate JSON key")
        return result

    def bad_constant(token):
        raise ValueError("Nonstandard JSON decimal")

    return json.loads(raw, parse_float=Decimal, parse_int=Decimal,
                      parse_constant=bad_constant, object_pairs_hook=unique)


def compare(a, b):
    if type(a) is not type(b):
        return Counter(typeDifferences=1)
    if isinstance(a, dict):
        differences = Counter(missingKeys=len(a.keys() - b.keys()),
                              extraKeys=len(b.keys() - a.keys()))
        for key in a.keys() & b.keys():
            differences.update(compare(a[key], b[key]))
        return +differences
    if isinstance(a, list):
        differences = Counter(arrayLengthDifference=abs(len(a) - len(b)))
        for x, y in zip(a, b):
            differences.update(compare(x, y))
        return +differences
    return Counter() if a == b else Counter(valueDifferences=1)


def read_member(archive, name):
    prefix, nested, leaf = name.partition("::")
    target = prefix if not nested else "objects/" + prefix
    require(archive.namelist().count(target) == 1, "Missing or duplicate primary member")
    require(archive.getinfo(target).file_size <= 100 << 20, "Unexpected primary size")
    raw = archive.read(target)
    if not nested:
        return raw
    with ZipFile(BytesIO(raw)) as child:
        require(child.namelist().count(leaf) == 1, "Missing or duplicate nested member")
        require(child.getinfo(leaf).file_size <= 50 << 20, "Unexpected nested size")
        return child.read(leaf)


def main():
    archive_path, index_path, rights_path, output = map(Path, sys.argv[1:])
    with archive_path.open("rb") as stream:
        require(file_digest(stream, "sha256").hexdigest() == ARCHIVE, "Capsule digest differs")
    index = exact_json(index_path, INDEX)
    rows = [row for row in index if row["priorAuditMatches"]]
    require(len(rows) == 14, "Unexpected match count")
    rights = exact_json(rights_path, RIGHTS)["rows"]
    entries = []
    with ZipFile(archive_path) as archive:
        embedded = contents(archive, rows)
        for row in rows:
            candidates = row["priorAuditMatches"]
            raw_embedded = embedded[row["ordinal"]]
            expected = row["sourceSha256Declared"]
            statuses = set()
            for candidate in candidates:
                name = candidate["name"]
                prior = rights[name]
                require(prior["status"] == candidate["status"] and prior["sha256"] == expected,
                        "Index and rights entry disagree")
                raw = read_member(archive, name)
                require(digest(raw) == expected, "Archived candidate does not match prior rights entry")
                statuses.add(prior["status"])
            difference = compare(load_json(raw), load_json(raw_embedded))
            entries.append(dict(ordinal=row["ordinal"], sourceSha256=expected,
                                embeddedSha256=digest(raw_embedded), candidates=len(candidates),
                                byteIdentical=raw == raw_embedded, jsonValueEqual=not difference,
                                jsonDifferences=dict(difference), priorStatuses=sorted(statuses)))
    require(not compare({"x": [Decimal("1")]}, {"x": [Decimal("1.00")]}), "Decimal control")
    require(compare({"x": True}, {"x": Decimal(1)}) == Counter(typeDifferences=1), "Type control")
    require(compare([1, 2], [2, 1]) == Counter(valueDifferences=2), "Array order control")
    require(compare({"a": 1}, {"b": 1}) == Counter(missingKeys=1, extraKeys=1), "Key control")
    report = dict(schema="BKL046_V1146_PRIOR_RIGHTS_RECONCILIATION_V1",
                  restoredCapsuleSha256=ARCHIVE, knowledgeSha256=KNOWLEDGE,
                  priorInventorySha256=RIGHTS, embeddedIndexSha256=INDEX, records=len(entries),
                  archivedCandidatesHashVerified=sum(row["candidates"] for row in entries),
                  identicalBytes=sum(row["byteIdentical"] for row in entries),
                  equalJsonValues=sum(row["jsonValueEqual"] for row in entries),
                  priorStatuses=sorted({s for row in entries for s in row["priorStatuses"]}),
                  redistributionClearanceEstablished=False, syntheticComparisonControls=4,
                  scientificClosures=0, entries=entries)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
