from hashlib import sha256
import json
from pathlib import Path
import runpy
import subprocess
import sys
from tempfile import TemporaryDirectory

program,*command,output=sys.argv[1:]

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

with TemporaryDirectory(dir=Path(output).parent) as tmp:
    directory=Path(tmp)
    original=sys.argv
    sys.argv=[program,*command,str(directory/"selftest.json")]
    try:
        scope=runpy.run_path(program,run_name="__main__")
    finally:
        sys.argv=original
    selection=dict(geometry="signal",calibration="A",drop=.7,origin="edge05",mask="reference",
                   inputSha256=scope["previous"]["plan"]["inputs"],
                   fullOracleSha256=scope["plan"]["fullOracle"])
    intensity,weight,_=scope["expected"](selection)
    fits=scope["fits"]
    files=[directory/name for name in ("intensity.fits","weight.fits")]
    fits.PrimaryHDU(intensity.astype("float32")).writeto(files[0])
    reports={}
    for label,factor,expected in (("matched",weight.max(),"UNIQUE_NUMERICAL_HYPOTHESIS"),
                                  ("unresolved",weight.max()*1.04,"UNRESOLVED")):
        fits.PrimaryHDU((weight/factor).astype("float32")).writeto(files[1],overwrite=True)
        request=directory/f"{label}-request.json"
        request.write_text(json.dumps(dict(selection=selection,intensity=files[0].name,weight=files[1].name,
                                           intensitySha256=digest(files[0]),weightSha256=digest(files[1]))),
                           encoding="utf8")
        result=directory/f"{label}-receipt.json"
        subprocess.run([sys.executable,"-I","-B","-S",program,*command,str(result),
                        "--request",str(request),"--request-sha256",digest(request)],check=True)
        record=json.loads(result.read_bytes())
        if record["status"]!=expected or record["evidence"]!="UNATTESTED_NUMERICAL_COMPARISON" or (
                record["nativeProvenanceVerified"] is not False):
            raise ValueError("CLI result changed status or provenance")
        if label=="matched" and record["matchingHypotheses"]!=["global_expected_peak"]:
            raise ValueError("CLI classified the wrong model")
        reports[label]=dict(status=record["status"],hypotheses=record["matchingHypotheses"])
with Path(output).open("x",encoding="utf8",newline="\n") as out:
    json.dump(dict(schema="BKL046_XDRZ_FULL_MAP_CLASSIFIER_CLI_V1",cases=reports,
                   nativeProvenanceVerified=False,admissionRequested=False),out,indent=2,sort_keys=True)
    out.write("\n")
