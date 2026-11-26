"""Offline-only fixtures for the exact bilinear post-exit verifier."""
from copy import deepcopy
from io import BytesIO
import json
from pathlib import Path
import runpy
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

root, kit, deps, source, report = map(Path,sys.argv[1:])
sys.path.insert(0,str(deps))
import numpy as np
from astropy.io import fits

verify = runpy.run_path(str(root/"verifica.py"))
digest, parse = verify["digest"], verify["parse"]
raw_cfg = (root/"protocollo.json").read_bytes()
cfg = parse(raw_cfg)
plan = (kit/"protocollo.json").read_bytes()
inputs = kit/"ingressi"
manifest = (inputs/"manifest.json").read_bytes()
comparator = verify["load_comparator"](kit/"confronta.py",cfg["numericComparatorSha256"])


def pack(entries):
    stream = BytesIO()
    with ZipFile(stream,"w",compression=ZIP_DEFLATED) as z:
        for name, value in entries:
            z.writestr(ZipInfo(name),value,compress_type=ZIP_DEFLATED)
    return stream.getvalue()


def encode(value):
    return json.dumps(value,sort_keys=True,separators=(",",":")).encode()


context = {"schema":"BKL046_BILINEAR_EXACT_EXPECTED_CONTEXT_V1","operation":cfg["operation"],
           "request":"offline-request","reservation":"offline-reservation","launchSubjectSha256":"a"*64,
           "processInstanceSha256":"b"*64,"inputManifestSha256":cfg["inputManifestSha256"],
           "processMethod":"DynamicAlignment","pixInsightExeSha256":cfg["pixInsightExeSha256"],
           "processModuleSha256":cfg["processModuleSha256"],"original":{"pid":42,"creationFiletime":"1234","sessionId":1}}
inputs_raw = [(p.name,p.read_bytes()) for p in sorted(source.glob("*.fits"))]
archive = pack(inputs_raw)
envelope = {k:v for k,v in context.items() if k not in ("schema","original")}
envelope.update(schema="BKL046_BILINEAR_ORIGINAL_EXIT_ENVELOPE_V1",
                originalExit={**context["original"],"exitCode":0,"normalCloseObserved":True,"sameOriginalHandle":True},
                outputArchiveBytes=len(archive),outputArchiveSha256=digest(archive),
                outputs={k:{"bytes":len(v),"sha256":digest(v)} for k,v in inputs_raw})


def invoke(ar, env, ctx, explicit_pin=None):
    e, c = encode(env), encode(ctx)
    return verify["verify"](cfg,plan,manifest,inputs,ar,e,explicit_pin or digest(e),c,digest(c),
                            comparator,fits,np)


def expect(label, error, change, ar=archive, ctx=context, pin=None):
    candidate = deepcopy(envelope)
    change(candidate)
    try:
        invoke(ar,candidate,ctx,pin)
    except ValueError as e:
        assert str(e) == error, (label,str(e))
    else:
        raise AssertionError("Fixture wrongly accepted: "+label)
    negatives[label] = error


good = invoke(archive,envelope,context)
assert good["verifiedCases"] == 85 and good["releaseAuthorizedByThisVerifier"] is False
assert good["nativeProvenanceIndependentlyAttested"] is False
negatives={}
expect("untrustedReadback","VERIFIED_READBACK_DIGEST",lambda e:None,pin="f"*64)
expect("foreignRequest","ENVELOPE_CONTEXT",lambda e:e.update(request="foreign"))
expect("foreignReservation","ENVELOPE_CONTEXT",lambda e:e.update(reservation="foreign"))
expect("foreignInstance","ENVELOPE_CONTEXT",lambda e:e.update(processInstanceSha256="f"*64))
expect("foreignBuild","ENVELOPE_CONTEXT",lambda e:e.update(pixInsightExeSha256="f"*64))
expect("pidReused","ORIGINAL_PROCESS_IDENTITY",lambda e:e["originalExit"].update(creationFiletime="6789"))
expect("booleanExit","ORIGINAL_EXIT",lambda e:e["originalExit"].update(exitCode=False))
expect("nonzeroExit","ORIGINAL_EXIT",lambda e:e["originalExit"].update(exitCode=7))
expect("missingClose","ORIGINAL_EXIT",lambda e:e["originalExit"].update(normalCloseObserved=False))
expect("archiveSubstitution","OUTPUT_ARCHIVE_BINDING",lambda e:None,ar=archive[:-1])
expect("itemSubstitution","OUTPUT_MEMBER_DIGEST",lambda e:next(iter(e["outputs"].values())).update(sha256="f"*64))
name = "asymmetric-control-p4.fits"
replacement = dict(inputs_raw)["asymmetric-control-p0.fits"]
changed = pack([(k,replacement if k==name else v) for k,v in inputs_raw])


def substitute(e):
    e.update(outputArchiveBytes=len(changed),outputArchiveSha256=digest(changed))
    e["outputs"][name]={"bytes":len(replacement),"sha256":digest(replacement)}


expect("wrongPhaseConsistentlyRepacked","NUMERIC_CONTRACT",substitute,ar=changed)
with report.open("x",encoding="utf-8",newline="\n") as out:
    json.dump({"schema":"BKL046_BILINEAR_POST_EXIT_OFFLINE_RESULT_V1","protocolSha256":digest(raw_cfg),
               "verifierSha256":digest((root/"verifica.py").read_bytes()),"simulationAccepted":good,
               "refused":negatives,"admissionRequested":False,"nativeExecutions":0,"scientificClosures":0},
              out,indent=2,sort_keys=True)
    out.write("\n")

