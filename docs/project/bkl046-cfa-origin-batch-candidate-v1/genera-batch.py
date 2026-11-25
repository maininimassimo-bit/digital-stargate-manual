from hashlib import sha256
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

source, plan_dir, prior, native_inputs, output = map(Path,sys.argv[1:])

def digest(data):
    return sha256(data).hexdigest()

def read(path,pin):
    raw=path.read_bytes()
    if digest(raw)!=pin:
        raise ValueError("input differs: "+path.name)
    return raw

original_sha="0b91c52cc63eb0196f1e9ba5ac6774ebb7a9d28478392358976ae8f7138a87ec"
plan_sha="ab70f00fae2063a3693280036b6bfe166afabdc0a24abec43f761192a31d167a"
original=read(source,original_sha).decode()
plan=json.loads(read(plan_dir/"piano.json",plan_sha))
oracle=json.loads(read(prior/"riscontro.json",plan["originReport"]))
evidence=json.loads(read(native_inputs/"manifest.json","6fd2da645650a19f4654276607612c0af5ba193734a0087fc221058aab4fe16b"))
ns={"d":"http://www.pixinsight.com/xdrz"}
source_pins={}
inputs={}
cases={}
for case in plan["cases"]:
    origin=case["origin"]
    files=[]
    for label in "abc":
        name=f"shear-{label}-{case['matrix']}-origin{origin:.1f}.xdrz"
        pin=oracle["fixtureSha256"]["xdrz/"+name]
        raw=read(prior/"xdrz"/name,pin)
        tree=ET.fromstring(raw)
        attributes=tree.find("d:AlignmentOrigin",ns).attrib
        assert attributes=={"x":f"{origin:.1f}","y":f"{origin:.1f}"}
        assert tree.find("d:RejectionMap",ns) is None
        for kind in ("SourceImage","CFASourceImage"):
            source_name=Path(tree.find(f"d:{kind}",ns).text).name
            source_pins[source_name]=evidence["files"][source_name]
            read(native_inputs/source_name,source_pins[source_name])
        files.append(name)
        inputs[name]=pin
    cases[case["id"]]={"files":files,"rejection":False}
assert len(inputs)==12 and len(source_pins)==6

def replace_once(text,old,new):
    if text.count(old)!=1:
        raise ValueError("expected exact source anchor: "+old)
    return text.replace(old,new,1)

header=(
    "/* Offline candidate for the separate CFA origin experiment. */\n"
    "var CFA_CONTROL_CASES = "+json.dumps(cases,indent=2)+";\n"
)
byte_fixtures="O:/BKL046-CFA-origine-fattoriale-v1/prodotti/xdrz/"
case_fn=original[original.index("var CFA_FIXTURE"):original.index("var CFA_PLAN_SHA256")]
case_fn=replace_once(case_fn,"O:/BKL046-CFA-XDRZ-tre-ingressi-v1/fixture/",byte_fixtures)
old=r"^O:\/BKL046-CFA-XDRZ-esecuzioni-v1\/[A-Za-z0-9_-]{12,64}$"
new=r"^O:\/BKL046-CFA-origine-nativa-v1\/[0-9a-f-]{36}\/outputs$"
case_fn=replace_once(case_fn,old,new)
trailer=r'''
var ORIGIN_PLAN_SHA256 = "@PLAN@";
var ORIGIN_OPERATION = "BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001";

function runOriginBatch(binding) {
   cfaRequire(binding && binding.operation === ORIGIN_OPERATION &&
              binding.planSha256 === ORIGIN_PLAN_SHA256, "Unexpected origin experiment binding");
   cfaRequire(typeof binding.reservation === "string" &&
              /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(binding.reservation),
              "Invalid experiment reservation");
   var root = "O:/BKL046-CFA-origine-nativa-v1/" + binding.reservation;
   var outputs = root + "/outputs";
   cfaRequire(File.directoryExists(root) && File.directoryExists(outputs), "Missing experiment directories");
   var eventsFile = root + "/events.txt";
   var doneFile = root + "/batch.done.json";
   cfaRequire(!File.exists(eventsFile) && !File.exists(doneFile), "Existing experiment transcript or marker");
   var labels = Object.keys(CFA_CONTROL_CASES);
   cfaRequire(labels.length === 4, "Unexpected case count");
   labels.forEach(function (label) {
      cfaRequire(!File.exists(outputs + '/' + label + '-rgb.fits') &&
                 !File.exists(outputs + '/' + label + '-weight.fits'), "Output namespace already used");
   });
   var events = [];
   labels.forEach(function (label) {
      var lines = runCfaXdrzCase(label, outputs);
      cfaRequire(lines.length === 2, "Missing experiment evidence");
      events = events.concat(lines);
   });
   cfaRequire(events.length === 8, "Incomplete origin experiment transcript");
   var text = events.join("\n") + "\n";
   File.writeTextFile(eventsFile,text);
   cfaRequire(File.readTextFile(eventsFile) === text, "Origin transcript readback differs");
   cfaRequire(!File.exists(doneFile), "Unexpected existing marker");
   var done = JSON.stringify({schema:"BKL046_CFA_ORIGIN_BATCH_MARKER_V1",scope:"OUTPUT_MARKER_NOT_ADMISSION",
      operation:ORIGIN_OPERATION,planSha256:ORIGIN_PLAN_SHA256,reservation:binding.reservation,cases:labels}) + "\n";
   File.writeTextFile(doneFile,done);
   cfaRequire(File.readTextFile(doneFile) === done, "Origin marker readback differs");
}
'''.replace("@PLAN@",plan_sha)
batch=(header+case_fn+trailer).encode()
(output/"batch-origine.js").write_bytes(batch)
result={"schema":"BKL046_CFA_ORIGIN_PJSR_CANDIDATE_V1","operation":"BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001",
        "planSha256":plan_sha,"parentBatchSha256":original_sha,"candidateSha256":digest(batch),
        "caseOrder":list(cases),"xdrzSha256":inputs,"fitsInputsSha256":source_pins,
        "status":"OFFLINE_ONLY","coordinatorAdmissionRequested":False,"nativeExecutions":0}
(output/"batch-manifest.json").write_bytes((json.dumps(result,indent=2,sort_keys=True)+"\n").encode())
