"""Sensitivity of disjoint-exposure orientation to the shared Moffat model bank."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

protocol, prior, mosaics, width_receipt, dependencies, output = map(Path,sys.argv[1:])
raw=protocol.read_bytes()
settings=json.loads(raw)

def pin(path, expected):
    data=path.read_bytes()
    if sha256(data).hexdigest()!=expected:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return data

source=prior/"pose.py"
old_protocol=prior/"protocollo.json"
code=pin(source,settings["programSha256"]).decode()
previous=json.loads(pin(old_protocol,settings["previousProtocolSha256"]))
previous_report=pin(prior/"riscontro.json",settings["previousReportSha256"])

def execute(program,config,output):
    subprocess.run([sys.executable,"-I","-B","-S",str(program),str(config),str(mosaics),
                    str(width_receipt),str(dependencies),str(output)],check=True,
                   capture_output=True,text=True,timeout=100)
    return output.read_bytes()

def replace_once(code,old,new):
    if code.count(old)!=1:
        raise ValueError("REFERENCE_PROGRAM_BOUNDARY_CHANGED")
    return code.replace(old,new)

# Hold the center projection, support, cross-half procedure and test thresholds fixed.
variant=replace_once(code,'shapes=[(q,angle,scale) for q in p["axisRatios"] for angle in\n'
                     '        ([0] if q==1 else range(0,180,p["angleStep"])) for scale in p["widthFactors"]]',
                     'shapes=[(q,angle,scale,beta) for q in p["axisRatios"] for angle in\n'
                     '        ([0] if q==1 else range(0,180,p["angleStep"]))\n'
                     '        for scale in p["widthFactors"] for beta in p["betaGrid"]]')
variant=replace_once(variant,"ratios,angles,scales=shape_array.T","ratios,angles,scales,betas=shape_array.T")
variant=replace_once(variant,'2**(1/p["beta"])','2**(1/betas)')
variant=replace_once(variant,'**(-p["beta"])','**(-betas)')
variant=replace_once(variant,'idx=shapes.index((.65,45,1))','idx=shapes.index((.65,45,1,2.5))')
variant=replace_once(variant,'"circleWidthFactor":float(scales[ci])',
                     '"circleWidthFactor":float(scales[ci]),"circleBeta":float(betas[ci])')

with tempfile.TemporaryDirectory(prefix="banks-",dir=output) as temp:
    work=Path(temp)
    reread=execute(source,old_protocol,work/"baseline.json")
    if reread!=previous_report:
        raise ValueError("BASELINE_REPLAY_DIFFERS")
    reports={"baseline":json.loads(reread)}
    script=work/"pose-modelli.py"
    script.write_text(variant,encoding="utf-8",newline="\n")
    for label,widths,betas in (
        ("widths",settings["extendedWidths"],[previous["beta"]]),
        ("wings",previous["widthFactors"],settings["extendedBeta"]),
        ("widthsAndWings",settings["extendedWidths"],settings["extendedBeta"]),
    ):
        config=work/(label+"-protocollo.json")
        config.write_text(json.dumps({**previous,"widthFactors":widths,"betaGrid":betas},sort_keys=True),
                          encoding="utf-8",newline="\n")
        reports[label]=json.loads(execute(script,config,work/(label+".json")))

def axial(a,b):
    return abs((a-b+90)%180-90)

def positive(report,band):
    return {r["star"]:r["fits"][band]["angle"] for r in report["rows"] if r["fits"][band]["qualified"]}

summary={}
for label,report in reports.items():
    comparisons={}
    for band in ("red","blue"):
        before,after=positive(reports["baseline"],band),positive(report,band)
        intersect=set(before)&set(after)
        comparisons[band]={"qualified":len(after),"common":len(intersect),
                           "stableWithin15":sum(axial(before[key],after[key])<=15 for key in intersect),
                           "lost":sorted(set(before)-set(after)),"new":sorted(set(after)-set(before))}
    summary[label]={"bands":comparisons,"chromaticComparable":report["summary"]["chromaticComparable"]}

receipt={"schema":"BKL046_M8M20_PSF_DISJOINT_MODEL_SENSITIVITY_V1","protocolSha256":sha256(raw).hexdigest(),
         "programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),"baselineReproduced":True,
         "summary":summary,"nativeExecutions":0,"scientificClosures":0}
body=(json.dumps({**receipt,"reports":reports},sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
with (output/"tutti-gli-esiti.json").open("xb") as stream:
    stream.write(body)
receipt["fullReportSha256"]=sha256(body).hexdigest()
with (output/"riscontro.json").open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(receipt,sort_keys=True,indent=2,allow_nan=False)+"\n")
print(json.dumps(summary,sort_keys=True))
