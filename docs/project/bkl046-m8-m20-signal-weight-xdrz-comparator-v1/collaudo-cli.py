from hashlib import sha256
import json
from pathlib import Path
import runpy
import subprocess
import sys
from tempfile import TemporaryDirectory

program, protocol, prior, kit, calibrated, packages, output = sys.argv[1:]
work=Path(output).parent


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def require(ok, why):
    if not ok:
        raise ValueError(why)


with TemporaryDirectory(dir=work) as root:
    stage=Path(root)
    args=[program,protocol,prior,kit,calibrated,packages]
    fixed=sys.argv
    sys.argv=[*args,str(stage/"internal.json")]
    try:
        scope=runpy.run_path(program,run_name="__main__")
    finally:
        sys.argv=fixed
    config=dict(origin="center0",mask="detector",weightMode="linear_global_scale_per_channel",
                weightScaleRgb=[2.,4.,3.],inputsSha256=scope["plan"]["inputs"],
                oracleSha256=scope["plan"]["oracle"])
    i,w,_,area,_,_=scope["describe"](scope["data"],"signal","B",.7,config)
    np=scope["np"]
    for name,patch in (("intensity",i),("weight",w*np.array([2.,4.,3.])[:,None,None])):
        x0,y0,x1,y1=area
        array=np.zeros((3,48,48),dtype=np.float32)
        array[:,y0:y1,x0:x1]=patch
        scope["fits"].PrimaryHDU(array).writeto(stage/f"{name}.fits")
    request=stage/"request.json"
    request.write_text(json.dumps(dict(geometry="signal",calibration="B",drop=.7,convention=config,
            intensityFile="intensity.fits",intensitySha256=sha(stage/"intensity.fits"),
            weightFile="weight.fits",weightSha256=sha(stage/"weight.fits"))),encoding="utf8")

    def call(label,receipt_pin):
        path=stage/f"{label}.json"
        result=subprocess.run([sys.executable,"-I","-B","-S",*args,str(path),"--request",str(request),
                               "--request-sha256",receipt_pin],capture_output=True,text=True)
        return result,path

    digest=sha(request)
    result,path=call("readback",digest)
    require(result.returncode==0,result.stderr)
    data=json.loads(path.read_bytes())
    require(data["evidence"]=="UNATTESTED_NUMERICAL_COMPARISON" and data["nativeProvenanceVerified"] is False
            and len(data["descriptorSha256ByPose"])==14,"Unattested result was promoted")
    bad,absent=call("wrong-pin","0"*64)
    require(bad.returncode!=0 and not absent.exists() and "Changed request.json" in bad.stderr,"Bad request pin")
    original=(stage/"weight.fits").read_bytes()
    (stage/"weight.fits").write_bytes(original+b"x")
    bad,absent=call("changed-weight",digest)
    require(bad.returncode!=0 and not absent.exists() and "Changed weight.fits" in bad.stderr,"Changed FITS accepted")
    (stage/"weight.fits").write_bytes(original)
    changed=json.loads(request.read_bytes())
    changed["weightFile"]="../weight.fits"
    request.write_text(json.dumps(changed),encoding="utf8")
    bad,absent=call("parent-path",sha(request))
    require(bad.returncode!=0 and not absent.exists() and "local filename" in bad.stderr,"Parent path accepted")
    receipt=dict(schema="BKL046_WEIGHTED_XDRZ_COMPARATOR_CLI_TEST_V1",validSuppliedBytesMarkedUnattested=True,
                 boundDescriptors=14,rejected=["wrongRequestPin","changedFits","parentRelativePath"],
                 nativeExecutions=0,scientificClosures=0)
    with Path(output).open("x",encoding="utf8",newline="\n") as out:
        json.dump(receipt,out,indent=2,sort_keys=True)
        out.write("\n")
