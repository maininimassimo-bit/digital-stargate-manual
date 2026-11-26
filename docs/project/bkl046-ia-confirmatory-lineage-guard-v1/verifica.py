"""Verify that candidate IA partitions do not reuse observed source evidence."""
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

protocol, root, output=map(Path,sys.argv[1:])
raw=protocol.read_bytes()
cfg=json.loads(raw)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def checked(relative, pin):
    data=(root/relative).read_bytes()
    require(sha256(data).hexdigest()==pin, "Changed lineage input")
    return json.loads(data)


inputs={name:checked(*loc) for name,loc in cfg["inputs"].items()}
gain=inputs["gain"]["captures"]
lin0=inputs["lin0"]["records"]
require({r["exposure"] for r in gain}==set(range(1,21)) and len(gain)==160,"Invalid GAIN data grid")
require([r["exposure"] for r in lin0]==list(range(1,31)),"Invalid LIN0 data grid")
require(inputs["native64"]["independentConfirmationUnits"]==0 and inputs["cross"]["rowsVerified"]==2880,
        "Changed historical classification")

m8pins={pair[1] for pair in inputs["m8"]["inputs"]["archivePins"].values()}
require(len(m8pins)==4,"Unexpected M8/M20 roots")
source_digests={
    "romanGain":{r["sha256"] for r in gain},
    "romanLin0":{m["sha256"] for r in lin0 for m in r["members"][1:]},
    "m8m20Calibrators":{inputs["m8"]["inputs"]["archivePins"][k][1] for k in ("dark","flat","shortDark")},
    "m8m20Images":m8pins,
    "ic1805":{inputs["ic1805"]["archive"]},
    "m51":{r["sha256"] for r in inputs["m51"]["exposures"]},
}
require(all(re.fullmatch("[a-f0-9]{64}", h) for pins in source_digests.values() for h in pins),
        "Invalid data digest")
observed={}
gain_identifier={str(row["metadata"]["DETECTOR"]) for row in inputs["gainRamp"]["records"]}
lin_identifier={row["url"].rsplit("/",1)[-1].split("_",1)[0] for row in lin0}
require(gain_identifier==lin_identifier=={"21816"}
        and inputs["gain"]["sourceCaptureSha256"]==cfg["inputs"]["gainRamp"][1],
        "Roman detector lineage changed")
detectors={"romanGain":"ROMAN-21816","romanLin0":"ROMAN-21816"}
for id,pins in source_digests.items():
    observed[id]=dict(pins=pins, parents=(), detector=detectors.get(id,id),
                      previouslyExposed=True, lineageKnown=True)
observed["romanCross"]=dict(pins=set(),parents=("romanGain","romanLin0"),detector="ROMAN-21816",
                            previouslyExposed=True,lineageKnown=True)
observed["m8m20Resolved"]=dict(pins=set(),parents=("m8m20Images",),detector="m8m20Images",
                               previouslyExposed=True,lineageKnown=True)
observed["native64"]=dict(pins=set(),parents=(),detector=None,previouslyExposed=True,lineageKnown=False)


def ancestry(graph, path, seen=frozenset()):
    if path in seen or path not in graph:
        raise ValueError("Unknown or cyclic data lineage")
    node=graph[path]
    children=[ancestry(graph,name,seen|{path}) for name in node["parents"]]
    return ({path}|set().union(*(s for s, _ in children)),
            node["pins"]|set().union(*(s for _, s in children)))


def check(graph, training, held, scope):
    require(scope in ("session","detector"),"Unknown transfer objective")
    require(bool(training) and bool(held),"No candidate partition")
    train_roots,train_pins=set(),set()
    for name in training:
        roots,pins=ancestry(graph,name)
        train_roots.update(roots)
        train_pins.update(pins)
    reasons=set()
    if not train_pins or any(not graph[node]["lineageKnown"] for node in train_roots):
        reasons.add("INCOMPLETE_TRAINING_LINEAGE")
    if scope=="detector" and any(graph[node]["detector"] is None for node in train_roots):
        reasons.add("UNKNOWN_TRAINING_DETECTOR")
    held_pins=set()
    held_roots=set()
    for key in held:
        roots,pins=ancestry(graph,key)
        if not pins or any(not graph[node]["lineageKnown"] for node in roots):
            reasons.add("INCOMPLETE_LINEAGE")
        if any(graph[node]["previouslyExposed"] for node in roots):
            reasons.add("PREVIOUSLY_EXPOSED")
        if roots & train_roots or roots & held_roots:
            reasons.add("SHARED_DATA_ANCESTOR")
        if pins & train_pins or pins & held_pins:
            reasons.add("SHARED_EXACT_BYTES")
        held_pins.update(pins)
        held_roots.update(roots)
        if scope=="detector":
            origins={graph[node]["detector"] for node in roots}
            if None in origins:
                reasons.add("UNKNOWN_DETECTOR")
            if origins & {graph[node]["detector"] for node in train_roots}:
                reasons.add("SHARED_DETECTOR")
    return sorted(reasons)


cases={
    "gainToLin0BySession":check(observed,["romanGain"],["romanLin0"],"session"),
    "gainToLin0ByDetector":check(observed,["romanGain"],["romanLin0"],"detector"),
    "gainToCrossDerived":check(observed,["romanGain"],["romanCross"],"session"),
    "opticalCalibratorsToResolved":check(observed,["m8m20Calibrators"],["m8m20Resolved"],"session"),
    "otherOpticalSourcesToM51":check(observed,["ic1805","m8m20Images"],["m51"],"session"),
    "native64AsHeldOut":check(observed,["romanGain"],["native64"],"session"),
}
require(cases["gainToLin0BySession"]==["PREVIOUSLY_EXPOSED"],"Independent-session classifier drift")
require("SHARED_DETECTOR" in cases["gainToLin0ByDetector"],"Missing common detector")
require({"SHARED_DATA_ANCESTOR","SHARED_EXACT_BYTES"}.issubset(cases["gainToCrossDerived"]),"Missing transitive overlap")
require("SHARED_EXACT_BYTES" in cases["opticalCalibratorsToResolved"],"Missing shared calibration")
require("INCOMPLETE_LINEAGE" in cases["native64AsHeldOut"],"Incomplete cohort promoted")

test_graph=dict(observed)
test_graph["syntheticFresh"]=dict(pins={sha256(b"development fixture only").hexdigest()},parents=(),
                                  detector="synthetic",previouslyExposed=False,lineageKnown=True)
require(check(test_graph,["romanGain"],["syntheticFresh"],"detector")==[],"Positive fixture rejected")
require("SHARED_EXACT_BYTES" in check(test_graph,["romanGain"],["syntheticFresh","syntheticFresh"],"detector"),
        "Duplicate held unit accepted")
require("INCOMPLETE_TRAINING_LINEAGE" in check(test_graph,["native64"],["syntheticFresh"],"detector"),
        "Incomplete training lineage accepted")
test_graph["cycle"]=dict(pins=set(),parents=("cycle",),detector=None,
                         previouslyExposed=False,lineageKnown=False)
try:
    check(test_graph,["romanGain"],["cycle"],"session")
except ValueError:
    pass
else:
    raise ValueError("Cyclic lineage accepted")

report=dict(schema=cfg["schema"],protocolSha256=sha256(raw).hexdigest(),historicPartitions=cases,
            archivedLocalObjectsIndexed={key:len(pins) for key,pins in source_digests.items()},
            romanGainToLin0SharedCapturedHashes=len(source_digests["romanGain"]&source_digests["romanLin0"]),
            confirmatoryPartitionsAdmitted=sum(not reasons for reasons in cases.values()),
            syntheticPositiveControlPassed=True,duplicateControlRejected=True,cycleControlRejected=True,
            independentConfirmationUnits=0,providerCalls=0,nativeExecutions=0,scientificClosures=0)
with output.open("x",encoding="utf-8",newline="\n") as stream:
    json.dump(report,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write("\n")
