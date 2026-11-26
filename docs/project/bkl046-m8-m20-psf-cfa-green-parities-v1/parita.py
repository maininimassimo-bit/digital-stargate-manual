"""Use the two green CFA parities as a control for PSF orientation comparisons."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

protocol, expanded, previous, mosaics, width_receipt, dependencies, output=map(Path,sys.argv[1:])
raw=protocol.read_bytes()
cfg=json.loads(raw)

def pin(path, expected):
    data=path.read_bytes()
    if sha256(data).hexdigest()!=expected:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return data

expanded_settings=expanded/"protocollo.json"
pin(expanded_settings,cfg["expandedProtocolSha256"])
baseline=json.loads(pin(expanded/"tutti-gli-esiti.json",cfg["expandedReportSha256"]))
source=expanded/"modelli.py"
prefix,marker,_=pin(source,cfg["expandedProgramSha256"]).decode().partition("\nwith tempfile.TemporaryDirectory(")
assert marker
sys.argv=[str(source),str(expanded_settings),str(previous),str(mosaics),str(width_receipt),
          str(dependencies),str(output)]
ns={"__file__":str(source)}
exec(compile(prefix,str(source),"exec"),ns)
replace=ns["replace_once"]
gen=ns["variant"]
gen=replace(gen,'score_bank={star:{band:[[],[]] for band in ("red","blue")} for star in stars}',
            'channels=("red","blue","green1","green2")\n'
            'score_bank={star:{band:[[],[]] for band in channels} for star in stars}')
gen=replace(gen,'            for i,(band,par) in enumerate((("red",0),("blue",1))):\n'
            '                support=inside & (xx%2==par)&(yy%2==par)',
            '            width_r,width_b=old["fwhmNativePxRedBlue"]\n'
            '            width_g=(width_r+width_b)/2\n'
            '            for band,px,py,width in (("red",0,0,width_r),("blue",1,1,width_b),\n'
            '                                     ("green1",1,0,width_g),("green2",0,1,width_g)):\n'
            '                support=inside & (xx%2==px)&(yy%2==py)')
gen=replace(gen,'bank=library(ax,ay,old["fwhmNativePxRedBlue"][i])','bank=library(ax,ay,width)')
base=ns["previous"]
bank={**base,"widthFactors":ns["settings"]["extendedWidths"],"betaGrid":ns["settings"]["extendedBeta"]}

with tempfile.TemporaryDirectory(prefix="parities-",dir=output) as temp:
    work=Path(temp)
    program=work/"four-parities.py"
    program.write_text(gen,encoding="utf-8",newline="\n")
    reports={}
    for cal in ("A","B"):
        plan=work/(cal+"-protocollo.json")
        plan.write_text(json.dumps({**bank,"calibration":cal},sort_keys=True),encoding="utf-8",newline="\n")
        out=work/(cal+".json")
        completed=subprocess.run([sys.executable,"-I","-B","-S",str(program),str(plan),str(mosaics),
                                 str(width_receipt),str(dependencies),str(out)],
                                 capture_output=True,text=True,timeout=110)
        if completed.returncode!=0:
            raise RuntimeError(completed.stderr)
        reports[cal]=json.loads(out.read_bytes())

old=baseline["reports"]["widthsAndWings"]["rows"]
for left,right in zip(old,reports["A"]["rows"],strict=True):
    assert left["star"]==right["star"] and left["phaseInParityGrid"]==right["phaseInParityGrid"]
    assert all(left["fits"][band]==right["fits"][band] for band in ("red","blue"))
    assert left["chromaticAngleDifference"]==right["chromaticAngleDifference"]

def axial(a,b):
    return abs((a-b+90)%180-90)

def describe(pairs):
    values=[]
    for ident,first,second in pairs:
        if first["qualified"] and second["qualified"]:
            values.append({"star":ident,"deltaDegrees":axial(first["angle"],second["angle"])})
    return {"comparable":len(values),"within15":sum(r["deltaDegrees"]<=15 for r in values),"deltas":values}

summary={}
channels=("red","blue","green1","green2")
for cal,serialized in reports.items():
    rows=serialized["rows"]
    summary[cal]={"qualified":{band:sum(r["fits"][band]["qualified"] for r in rows) for band in channels}}
    for label,a,b in (("greenParities","green1","green2"),("redBlue","red","blue")):
        summary[cal][label]=describe((r["star"],r["fits"][a],r["fits"][b]) for r in rows)
summary["calibrationRepeat"]={}
for band in channels:
    combo=[]
    for left,right in zip(reports["A"]["rows"],reports["B"]["rows"],strict=True):
        assert left["star"]==right["star"]
        combo.append((left["star"],left["fits"][band],right["fits"][band]))
    summary["calibrationRepeat"][band]=describe(combo)

receipt={"schema":"BKL046_M8M20_PSF_CFA_GREEN_PARITY_V1","protocolSha256":sha256(raw).hexdigest(),
         "programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),"redBlueBaselineExactlyReproduced":True,
         "summary":summary,"nativeExecutions":0,"scientificClosures":0}
full=(json.dumps({**receipt,"reports":reports},sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
with (output/"tutti-gli-esiti.json").open("xb") as stream:
    stream.write(full)
receipt["fullReportSha256"]=sha256(full).hexdigest()
with (output/"riscontro.json").open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(receipt,sort_keys=True,indent=2,allow_nan=False)+"\n")
print(json.dumps({k:{v:summary[k][v] for v in ("qualified","greenParities","redBlue")} for k in ("A","B")}))
