"""Test directional dependence on the exact archived Roman row bands."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return sha256(raw).hexdigest()


def read(path,pin):
    raw=path.read_bytes()
    require(sha(raw)==pin,"Changed input: "+path.name)
    return raw


def load(path,pin):
    module=ModuleType(path.stem)
    exec(compile(read(path,pin),str(path),"exec"),vars(module))
    return module


def weight_terms(np, x, y):
    kernel=np.outer([1-y,y],[1-x,x])
    support=np.zeros((3,3))
    for i in range(2):
        for j in range(2):
            support[i:i+2,j:j+2]+=kernel
    return float(np.sum(support**2)),float(4*np.sum(kernel**2))


def evaluate(np,a,b,mask,support,x,y,full,diag):
    delta=(b-a)/np.sqrt(2.)
    v=delta[:63,:63]
    if (x,y)==(.5,.5):
        shifted=(v[:-1,:-1]+v[1:,:-1]+v[:-1,1:]+v[1:,1:])/4
    else:
        shifted=(1-y)*((1-x)*v[:-1,:-1]+x*v[:-1,1:])+y*((1-x)*v[1:,:-1]+x*v[1:,1:])
    blocks=shifted.reshape(31,2,31,2).swapaxes(1,2).reshape(31,31,4)[mask]
    measured=np.var(blocks.sum(axis=1),ddof=1)
    empirical_diag=np.trace(np.cov(blocks,rowvar=False,ddof=1))
    variance=np.var(v[support],ddof=1)
    require(min(measured,empirical_diag,variance)>0,"Nonpositive variance")
    return dict(empiricalRatio=float(measured/empirical_diag),fullError=float(abs(full*variance/measured-1)),
                diagonalError=float(abs(diag*variance/measured-1)))


def compare(np, spatial, kernel, base, cfg, band, frames):
    phases=cfg["phases"]
    data=[]
    reference=base["newBandComparisons"][band]
    for i,phase in enumerate(phases):
        x,y=phase
        full,diag=weight_terms(np,x,y)
        evaluate_phase=lambda np,a,b,m,s:evaluate(np,a,b,m,s,x,y,full,diag)
        worker=type("Kernel",(),{"plan_support":staticmethod(kernel.plan_support),"evaluate":staticmethod(evaluate_phase)})
        spatial_cfg=json.loads((base["root"]/"protocollo.json").read_bytes())
        captures=base["capture"]["captures"]
        files={(r["exposure"],r["frame"]):r for r in captures if r["band"]==band}
        rows,_=spatial.calculate(np,worker,frames,base["root"]/"cattura"/"source",files,spatial_cfg["minRetainedBlocks"])
        require(len(rows)==len(reference)==960,"Band coverage")
        for row,ref in zip(rows,reference,strict=True):
            require(spatial.row_key(row)==spatial.row_key(ref) and row["state"]==ref["state"],"Paired support changed")
            if row["state"]=="MEASURED":
                if (x,y)==(0,0):
                    require(row["fullError"]==row["diagonalError"],"Zero-shift predictions differ")
                if (x,y)==(.5,.5):
                    np.testing.assert_allclose([row["fullError"],row["diagonalError"],row["empiricalRatio"]],
                        [ref["fullError"],ref["diagonalError"],ref["sumToEmpiricalDiagonal"]],rtol=1e-12)
            data.append(dict(row,phaseIndex=i,band=band))
    return data


def summary(np,rows,cfg):
    result=[]
    for band in ("lower","upper"):
        for frame in (1,5,10):
            groups=[[r for r in rows if r["phaseIndex"]==i and r["band"]==band and r["frame"]==frame
                     and r["state"]=="MEASURED"] for i in range(len(cfg["phases"]))]
            require(all(len(g)==320 for g in groups),"Unexpected masked comparison count")
            records=[]
            for phase,group in zip(cfg["phases"],groups,strict=True):
                records.append(dict(phase=phase,comparisons=len(group),
                     fullErrorMedian=float(np.median([r["fullError"] for r in group])),
                     diagonalErrorMedian=float(np.median([r["diagonalError"] for r in group])),
                     empiricalRatioMedian=float(np.median([r["empiricalRatio"] for r in group]))))
            x,y=groups[1:3]
            require(all((a["firstExposure"],a["channel"])==(b["firstExposure"],b["channel"])
                         for a,b in zip(x,y,strict=True)),"Axis pairing")
            diffs=[a["fullError"]-b["fullError"] for a,b in zip(x,y,strict=True)]
            result.append(dict(band=band,frame=frame,phases=records,
                               xMinusYHalfShiftFullErrorQuantiles=np.quantile(diffs,[.05,.5,.95]).tolist()))
    return result


def save(path,data):
    raw=(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
    with path.open("xb") as f:
        f.write(raw)
    return sha(raw)


def main():
    cli=ArgumentParser(description=__doc__)
    for name in ("policy","spatial","ramp","channels","dependencies","output"):
        cli.add_argument(name,type=Path)
    a=cli.parse_args()
    raw=a.policy.read_bytes()
    cfg=json.loads(raw)
    spatial_file=a.spatial/"misura.py"
    spatial=load(spatial_file,cfg["spatialProgram"])
    kernel=load(a.channels/"misura.py",cfg["channelsProgram"])
    a.output.mkdir()
    replay=a.output/"replay-spatial.json"
    subprocess.run([sys.executable,"-I","-S","-B",str(spatial_file),str(a.spatial),str(a.ramp),str(a.channels),
                    str(a.dependencies),str(replay),cfg["spatialCapture"]],check=True)
    base=json.loads(read(replay,cfg["spatialReport"]))
    base["root"]=a.spatial
    base["capture"]=json.loads(read(a.spatial/"cattura"/"acquisizione.json",cfg["spatialCapture"]))
    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    require(np.__version__=="2.3.5","NumPy version")
    frames=[0,1,5,10]
    rows=[r for band in ("lower","upper") for r in compare(np,spatial,kernel,base,cfg,band,frames)]
    detail=save(a.output/"tutti-gli-esiti.json",rows)
    save(a.output/"riscontro.json",dict(schema=cfg["schema"],protocolSha256=sha(raw),
        programSha256=sha(Path(__file__).read_bytes()),spatialReportSha256=cfg["spatialReport"],
        detailSha256=detail,comparisons=len(rows),halfHalfParentComparisons=1920,summary=summary(np,rows,cfg),
        nativeExecutions=0,scientificClosures=0))


if __name__=="__main__":
    main()