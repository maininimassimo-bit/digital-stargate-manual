from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

parser=ArgumentParser()
for name in ("protocol","weights","baseline","data","packages","output"):
    parser.add_argument(name,type=Path)
args=parser.parse_args()


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def pinned(path,digest):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==digest,f"Changed {path.name}")
    return raw


def execute(path,code,arguments,callbacks=None):
    old=sys.argv
    sys.argv=[str(path),*map(str,arguments)]
    namespace={"__file__":str(path),"__name__":"__main__"}
    if callbacks:
        namespace.update(callbacks)
    try:
        exec(compile(code,str(path),"exec"),namespace)
    finally:
        sys.argv=old
    return namespace


def encode(obj):
    return (json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()


PIN="587ff715874d5747e081c1373d0a698ae3637786250dc7ccc195a451c9bfe299"
plan=json.loads(pinned(args.protocol,PIN))
weights_path=args.weights/"misura.py"
weights_code=pinned(weights_path,plan["weightsCode"])
weights_report=pinned(args.weights/"riscontro.json",plan["weightsReport"])
baseline_path=args.baseline/"confronto.py"
baseline=pinned(baseline_path,plan["commonScaleCode"]).decode("utf8")
pinned(args.baseline/"protocollo.json",plan["commonScalePlan"])
prior=json.loads(pinned(args.baseline/"riscontro.json",plan["commonScaleReport"]))
base=args.data
model_path=base/"BKL046-CFA-M8-M20-geometria-globale-v1"/"riscontro.json"
models=json.loads(pinned(model_path,plan["matrixPrior"]))
lights=base/"BKL046-CFA-M8-M20-v1"
stars=base/"BKL046-CFA-M8-M20-stelle-v1"
geometry=base/"BKL046-CFA-M8-M20-fit-stellare-v1"
calibrators=base/"BKL046-CFA-M8-M20-calibratori-v1"

with TemporaryDirectory(dir=args.output.parent) as temp:
    stage=Path(temp)
    replay=stage/"replay-weights.json"
    state=execute(weights_path,weights_code,(args.weights/"protocollo.json",geometry,lights,
                  base/"BKL046-CFA-M8-M20-affine-v1",stars/"riscontro.json",args.packages,replay))
    require(replay.read_bytes()==weights_report,"Registration replay changed")
    np=state["np"]
    center=state["parent"]["center"]
    train,test=state["train"],state["test"]
    design,xy=state["train_design"],state["train_xy"]
    fit,limits=state["fit"],state["limit"]
    test_xy=state["test_xy"]
    test_design=state["test_design"]
    test_affine=np.column_stack((test_xy,np.ones(len(test_xy))))
    signals=state["signals"]
    derived=[]
    previous=json.loads(weights_report)
    for index,(row,positions,expected) in enumerate(zip(models["referenceToInputAffine"],
            state["observations"],previous["frames"],strict=True),1):
        require(row["member"]==state["old"]["frames"][index-1]["member"],"Stellar frame changed")
        delta=np.array([positions[key] for key in train])-xy
        strength=np.array([min(signals[0][key],signals[index][key]) for key in train])
        weights=np.clip((strength/np.median(strength))**2,1/limits,limits)
        matrices={}
        for tag,key,weight in (("binned","unit",np.ones(len(train))),("mosaic","signal",weights)):
            coeff=fit(design,delta,weight)
            forward=np.eye(3)
            forward[:2,:2]+=coeff[1:].T/2048
            forward[:2,2]=coeff[0]-coeff[1:].T@center/2048
            direct=test_xy+test_design@coeff
            np.testing.assert_allclose((test_affine@forward.T)[:,:2],direct,atol=2e-12,rtol=0)
            p90=np.quantile(np.linalg.norm(direct-np.array([positions[key] for key in test]),axis=1),.9)
            require(abs(p90-expected["p90Px"][key])<1e-10,"Estimator score changed")
            require(np.linalg.det(forward[:2,:2])>0,"Invalid forward mapping")
            matrices[tag]=forward
        landmarks=[]
        for ref in [point["reference"] for point in row["validationLandmarks"]]:
            xy1=np.array([*ref,1.])
            landmarks.append({"reference":ref,**{tag:(m@xy1)[:2].tolist() for tag,m in matrices.items()}})
        derived.append(dict(member=row["member"],validationLandmarks=landmarks,
                            **{tag:m.tolist() for tag,m in matrices.items()}))
    require(len(derived)==plan["frames"],"Unexpected matrix count")
    payload={**models,"referenceToInputAffine":derived}
    # The original receipt is read and pinned by the baseline before this explicit two-arm substitution.
    anchor='mapped=json.loads(predictions_file.read_bytes())'
    require(baseline.count(anchor)==1,"Baseline observer anchor changed")
    altered=baseline.replace(anchor,anchor+"\nmapped = substitute_geometry(mapped)")
    destination=stage/"resampled.json"
    invocation=(args.baseline,calibrators,lights,stars,geometry,args.packages,model_path,destination)
    def substitute_geometry(seen):
        require(seen==models,"Observed matrix prior changed")
        return payload
    execute(baseline_path,altered,invocation,dict(substitute_geometry=substitute_geometry))
    measured=json.loads(destination.read_bytes())

require(measured["frames"]==prior["frames"]==plan["frames"]
        and measured["stars"]==prior["stars"]==plan["targets"],"Changed reconstructed sample")
record=dict(schema=plan["schema"],protocolSha256=PIN,arms=plan["arms"],
            matrixParentSha256=plan["matrixPrior"],weightedGeometryReplayIdentical=True,
            offlineResamplerSha256=plan["commonScaleCode"],frames=measured["frames"],stars=measured["stars"],
            summary=measured["summary"],matrixSha256=sha256(encode(derived)).hexdigest(),
            forwardMatrices=derived,rows=measured["rows"],nativeExecutions=0,scientificClosures=0)
with args.output.open("xb") as stream:
    stream.write(encode(record))
