from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile

parser=ArgumentParser()
for key in ("protocol","baseline","oracle_source","inputs_source","output"):
    parser.add_argument(key,type=Path)
args=parser.parse_args()


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def pin(path,expected):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==expected,f"Changed {path.name}")
    return raw


def edit(text,old,new):
    require(text.count(old)==1,f"Changed source anchor: {old}")
    return text.replace(old,new)


def run(path,code,out,variables=None):
    old=sys.argv
    sys.argv=[str(path),str(out)]
    values={"__name__":"__main__","__file__":str(path),**(variables or {})}
    try:
        exec(compile(code,str(path),"exec"),values)
    finally:
        sys.argv=old
    return values


PIN="9ccbb8c85807b00945ef13c65de4d79abcc52c26852c7950721e7322770bd930"
plan=json.loads(pin(args.protocol,PIN))
baseline=json.loads(pin(args.baseline,plan["baselineReport"]))
old_oracle=args.oracle_source/"oracolo.zip"
old_inputs=args.inputs_source/"riscontro.zip"
pin(old_oracle,plan["oldOracle"])
pin(old_inputs,plan["oldInputs"])
oracle_path=args.oracle_source/"oracolo.py"
inputs_path=args.inputs_source/"prepara.py"
oracle_program=pin(oracle_path,plan["oracleProgram"]).decode("utf8")
inputs_program=pin(inputs_path,plan["inputsProgram"]).decode("utf8")
rows=baseline["forwardMatrices"]
digest=sha256((json.dumps(rows,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()).hexdigest()
require(digest==plan["baselineMatrices"]==baseline["matrixSha256"]
        and len(rows)==plan["frames"] and baseline["arms"]==["unitAffine","signalAffine"],
        "Unexpected baseline matrices")

def local(ordinal,frame,stamp,model):
    import numpy as np
    row=rows[ordinal-1]
    require(frame["member"]==row["member"] and stamp["star"]==plan["star"],"ROI identity mismatch")
    offset=np.eye(3)
    offset[:2,2]=stamp["cropOriginXY"]
    require(all(v%2==0 for v in stamp["cropOriginXY"]),"Odd CFA stamp origin")
    matrix=np.linalg.inv(offset)@np.asarray(row[model])@offset
    require(np.linalg.det(matrix[:2,:2])>0,"Invalid cropped affine")
    return matrix


oracle_program=edit(oracle_program,'np.asarray(stamp["referenceToFrameAffine"][model])',
                    'local(frame_id, frame, stamp, model)')
oracle_program=edit(oracle_program,
    'np.testing.assert_allclose(deltas[0], prior["unmaskedDeltaPct"], rtol=1e-9, atol=1e-7)\n'
    'np.testing.assert_allclose(deltas[1], prior["zeroWeightRetainedDeltaPct"], rtol=1e-9, atol=1e-7)',
    'require(np.isfinite(deltas).all(), "Candidate mask controls invalid")')
oracle_program=edit(oracle_program,'"BKL046_CFA_M8_M20_REAL_ROI_OFFLINE_ORACLE_V1"',
                    '"BKL046_CFA_M8_M20_SIGNAL_WEIGHT_ROI_ORACLE_V1"')
oracle_program=edit(oracle_program,'"matrixAxes": ["binned", "mosaic"]',
                    '"matrixAxes": ["unit", "signal"], "sourceBaselineSha256": baseline_pin')
oracle_output=args.output/"oracolo.zip"
oracle=run(oracle_path,oracle_program,oracle_output,dict(local=local,baseline_pin=plan["baselineReport"]))
np=oracle["np"]
aperture,annulus=oracle["ap"],oracle["ann"]
# The one-star oracle and the 53-star baseline use common support across all four arm/width cells.
source_rows={r["parity"]:r for r in baseline["rows"] if r["star"]==plan["star"]}
checks={}
for i,band in enumerate(("R","G","B")):
    support=oracle["support"][0,i].all(axis=(0,1))
    radius=oracle["radius"]
    flux=np.asarray([[oracle["net"](item,(radius<=6)&support,(radius>=9)&(radius<=13)&support)
                      for item in width] for width in oracle["data"][0,i]])
    expected=np.asarray(source_rows[band]["flux"])
    np.testing.assert_allclose(flux,expected,atol=plan["fluxNumericalToleranceAdu"],rtol=0)
    checks[band]=float(np.max(np.abs(flux-expected)))

oracle_hash=sha256(oracle_output.read_bytes()).hexdigest()
inputs_program=edit(inputs_program,'ROOT = "O:/BKL046-CFA-M8-M20-ingressi-diagnostici-v1/input/"',
                    'ROOT = candidate_root')
inputs_program=edit(inputs_program,'for model, raw in stamp["referenceToFrameAffine"].items():\n'
                    '                matrix = np.asarray(raw)',
                    'for model, internal in (("unit", "binned"), ("signal", "mosaic")):\n'
                    '                matrix = local(ordinal, frame, stamp, internal)')
inputs_program=edit(inputs_program,'"BKL046_CFA_M8_M20_XDRZ_DIAGNOSTIC_INPUTS_V1"',
                    '"BKL046_CFA_M8_M20_SIGNAL_WEIGHT_XDRZ_DIAGNOSTIC_INPUTS_V1"')
inputs_program=edit(inputs_program,'"oracleSha256": ORACLE_PIN','"oracleSha256": candidate_oracle')
inputs_output=args.output/"ingressi.zip"
run(inputs_path,inputs_program,inputs_output,dict(local=local,candidate_root=plan["candidateRoot"],
                                                 candidate_oracle=oracle_hash))
ns={"x":"http://www.pixinsight.com/xdrz"}
with ZipFile(inputs_output) as new, ZipFile(old_inputs) as old:
    manifest=json.loads(new.read("input-manifest.json"))
    require(manifest["conditionalOnSyntheticResult"] and manifest["oracleSha256"]==oracle_hash,
            "Native prerequisite or oracle linkage changed")
    require(len(manifest["entries"])==plan["expectedInputs"],"Unexpected descriptor count")
    fits=[name for name in manifest["files"] if name.endswith(".fits")]
    require(len(fits)==56 and all(new.read(name)==old.read(name) for name in fits),"FITS bytes changed")
    entries=manifest["entries"]
    for row in entries:
        parsed=ET.fromstring(new.read(row["xdrz"]))
        require(parsed.findtext("x:CFASourceImage",namespaces=ns)==plan["candidateRoot"]+row["mosaic"] and
                parsed.findtext("x:SourceImage",namespaces=ns)==plan["candidateRoot"]+row["auxiliaryRgb"],
                "Wrong candidate asset path")
    selections={}
    for row in entries:
        group=(row["calibration"],row["geometry"],row["origin"],row["mask"])
        selections.setdefault(group,[]).append(row["pose"])
    require(len(selections)==24 and all(sorted(x)==list(range(1,15)) for x in selections.values()),
            "Diagnostic selection roster changed")
report=dict(schema=plan["schema"],protocolSha256=PIN,star=plan["star"],frames=plan["frames"],
            descriptors=len(entries),completeSelections=len(selections),unchangedFits=len(fits),
            maxAbsoluteApertureDifferenceAdu=checks,oracleZipSha256=oracle_hash,
            inputsZipSha256=sha256(inputs_output.read_bytes()).hexdigest(),
            matrixSourceSha256=plan["baselineReport"],conditionalOnSyntheticNativeResult=True,
            admissionRequested=False,nativeExecutions=0,scientificClosures=0)
with (args.output/"riscontro.json").open("x",encoding="utf8",newline="\n") as out:
    json.dump(report,out,indent=2,sort_keys=True,allow_nan=False)
    out.write("\n")
