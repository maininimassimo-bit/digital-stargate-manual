from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

parser = ArgumentParser()
for name in ("protocol","weights","photometry","data","packages","output"):
    parser.add_argument(name,type=Path)
args=parser.parse_args()


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def pinned(path,digest):
    data=path.read_bytes()
    require(sha256(data).hexdigest()==digest,f"Changed {path.name}")
    return data


def execute(source,body,arguments):
    saved=sys.argv
    sys.argv=[str(source),*map(str,arguments)]
    space={"__name__":"__main__","__file__":str(source)}
    try:
        exec(compile(body,str(source),"exec"),space)
    finally:
        sys.argv=saved
    return space


def write(path,data):
    with path.open("x",encoding="utf8",newline="\n") as out:
        json.dump(data,out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")


PIN="a085b58a2699adb0854aef96f306acfc3c91f2cb3f656005553b87d79ba3a132"
plan=json.loads(pinned(args.protocol,PIN))
source=args.weights/"misura.py"
weighted_code=pinned(source,plan["weightsCode"])
weighted_prior=pinned(args.weights/"riscontro.json",plan["weightsReport"])
photometry=args.photometry/"fotometria.py"
phot_code=pinned(photometry,plan["photometryCode"])
photometry_prior=pinned(args.photometry/"riscontro.json",plan["photometryReport"])
pinned(args.photometry/"protocollo-fotometria.json",plan["photometryProtocol"])
paired_file=args.photometry/"predizioni.json"
frozen=json.loads(pinned(paired_file,plan["cohort"]))
root=args.data
lights=root/"BKL046-CFA-M8-M20-v1"
stars=root/"BKL046-CFA-M8-M20-stelle-v1"
geometry=root/"BKL046-CFA-M8-M20-fit-stellare-v1"
calibration=root/"BKL046-CFA-M8-M20-calibratori-v1"
with TemporaryDirectory(dir=args.output.parent) as scratch:
    work=Path(scratch)
    weighted_replay=work/"weight-replay.json"
    state=execute(source,weighted_code,(
        args.weights/"protocollo.json",geometry,lights,root/"BKL046-CFA-M8-M20-affine-v1",
        stars/"riscontro.json",args.packages,weighted_replay))
    require(weighted_replay.read_bytes()==weighted_prior,"Weighted training replay changed")
    np=state["np"]
    train,test=state["train"],state["test"]
    training_x,training_xy=state["train_design"],state["train_xy"]
    test_design,test_xy=state["test_design"],state["test_xy"]
    signals=state["signals"]
    fits=state["fit"]
    new_predictions=[]
    previous=json.loads(weighted_prior)
    fit_differences=[]
    for i,(row,positions,prior) in enumerate(zip(
            frozen["predictions"],state["observations"],previous["frames"],strict=True),1):
        require(row["member"]==state["old"]["frames"][i-1]["member"],"Unexpected frame ordering")
        index=[test.index(key) for key in row["ids"]]
        require(len(set(index))==len(index),"Repeated evaluation star")
        movement=np.array([positions[k] for k in train])-training_xy
        strength=np.array([min(signals[0][k],signals[i][k]) for k in train])
        limit=state["limit"]
        weights=np.clip((strength/np.median(strength))**2,1/limit,limit)
        base=test_xy+test_design@fits(training_x,movement,np.ones(len(train)))
        weighted=test_xy+test_design@fits(training_x,movement,weights)
        actual=np.array([positions[k] for k in test])
        for key,centers in (("unit",base),("signal",weighted)):
            p90=np.quantile(np.linalg.norm(actual-centers,axis=1),.9)
            require(abs(p90-prior["p90Px"][key])<1e-10,"Unexpected astrometric readback")
        fit_differences.extend(np.linalg.norm(weighted[index]-base[index],axis=1))
        new_predictions.append(dict(member=row["member"],ids=row["ids"],
                                    binned=base[index].tolist(),mosaic=weighted[index].tolist()))
    require(len(fit_differences)==plan["pairs"],"Aperture cohort changed")
    derived=work/"signal-predictions.json"
    write(derived,dict(sourceReceiptSha256=frozen["sourceReceiptSha256"],summary=frozen["summary"],
                       predictions=new_predictions))
    run_args=(args.photometry,calibration,lights,stars,geometry,args.packages)
    photo_replay=work/"photo-replay.json"
    execute(photometry,phot_code,(*run_args,paired_file,photo_replay))
    require(photo_replay.read_bytes()==photometry_prior,"Frozen photometry replay changed")
    measured=work/"photo-signal.json"
    execute(photometry,phot_code,(*run_args,derived,measured))
    new=json.loads(measured.read_bytes())

result=dict(schema=plan["schema"],protocolSha256=PIN,weightedAndPhotometricBaselinesReplayedExactly=True,
            rawAssociations=len(fit_differences),pairedCenterShiftP90Px=float(np.quantile(fit_differences,.9)),
            summary=new["summary"],excluded=new["excluded"],nativeExecutions=0,scientificClosures=0)
require(sum(x["measurements"] for x in new["summary"].values())+sum(new["excluded"].values())==
        plan["pairs"]*4,"Incomplete measurement accounting")
write(args.output,result)
