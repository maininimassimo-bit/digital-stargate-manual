import json
import sys
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

parser = ArgumentParser()
for name in ("protocol","parent","capture","geometry","previous","packages","output"):
    parser.add_argument(name,type=Path)
args = parser.parse_args()


def require(condition, why):
    if not condition:
        raise ValueError(why)


def exact(path, expected):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest()==expected, f"Changed {path.name}")
    return raw


PIN="7629e457d2a6222e2a8e785361cc04442f0175db905d298e8aa4bc0ec4f058e5"
plan=json.loads(exact(args.protocol,PIN))
program=args.parent/"refit.py"
original=exact(program,plan["sourceCode"]).decode("utf8")
report=exact(args.parent/"riscontro.json",plan["sourceReport"])
parent={"__name__":"__main__","__file__":str(program)}
signals={}


def observe(index,key,g1,g2,x,y):
    np=parent["np"]
    half=parent["r"]+2
    inside,ring=parent["inside"],parent["ring"]
    ratios=[]
    for image in (g1,g2):
        patch=image[y-half:y+half+1,x-half:x+half+1].astype(float)
        background=patch[ring]
        sky=np.median(background)
        noise=max(1.,1.4826*np.median(np.abs(background-sky)))
        ratios.append((patch[inside].max()-sky)/noise)
    strength=min(ratios)
    require(np.isfinite(strength) and strength>0,"Invalid green noise proxy")
    signals.setdefault(index,{})[key]=strength


def observe_after(text, anchor, callback):
    require(text.count(anchor)==1,"Changed observer anchor")
    return text.replace(anchor,anchor+"\n"+callback)


body=observe_after(original,"                                             peak=peak,integerPreview=(x,y))",
                   "                        observe(frame_index,key,g1,g2,x,y)")
body=observe_after(body,"                        rows[key]=(origin+pixel_pitch*q).tolist()",
                   "                        observe(frame_index,key,g1,g2,xpos,ypos)")
parent["observe"]=observe
with TemporaryDirectory(dir=args.output.parent) as scratch:
    replay=Path(scratch)/"replay.json"
    old_argv=sys.argv
    sys.argv=[str(program),*map(str,(args.parent,args.capture,args.geometry,args.previous,args.packages,replay))]
    try:
        exec(compile(body,str(program),"exec"),parent)
    finally:
        sys.argv=old_argv
    require(replay.read_bytes()==report,"Frozen stellar fit did not replay exactly")

np=parent["np"]
old=json.loads(report)
train,test,observations=(parent[k] for k in ("training","testing","observations"))
require((len(train),len(test),len(observations)) ==
        (plan["trainingTracks"],plan["testTracks"],plan["frames"]),"Frozen cohort changed")
train_design,test_design=parent["fit_x"],parent["test_x"]
train_xy,test_xy=parent["fit_xy"],parent["test_xy"]
fit,solve=parent["fit"],parent["solve"]
huber=parent["p"]["huberPx"]
steps=parent["p"]["huberSteps"]
limit=np.sqrt(plan["weightRatioCap"])


def mixed_fit(x,y,weights):
    first=fit(x,y,weights)
    mixed=first
    for _ in range(steps):
        residual=np.linalg.norm(x@mixed-y,axis=1)
        mixed=fit(x,y,weights*huber/np.maximum(huber,residual))
    return first,mixed


coef=np.array(((.6,-.35),(.11,.45),(-.25,.22)))
fake=train_design@coef
for beta in mixed_fit(train_design,fake,np.linspace(.25,4,len(train))):
    require(np.allclose(beta,coef,rtol=0,atol=1e-12),"Signal-weighted fixture drift")
rows=[]
raw={key:[] for key in plan["estimators"]}
for number,positions in enumerate(observations,1):
    displacement=np.array([positions[k] for k in train])-train_xy
    actual=np.array([positions[k] for k in test])-test_xy
    strength=np.array([min(signals[0][k],signals[number][k]) for k in train])
    weights=np.clip((strength/np.median(strength))**2,1/limit,limit)
    coefficients=(*solve(train_design,displacement),*mixed_fit(train_design,displacement,weights))
    p90={}
    for key,beta in zip(plan["estimators"],coefficients,strict=True):
        errors=np.linalg.norm(actual-test_design@beta,axis=1)
        p90[key]=float(np.quantile(errors,.9))
        raw[key].append(errors)
    for key,legacy in (("unit","stellarAffine"),("huber","stellarHuber")):
        require(abs(p90[key]-old["frames"][number-1]["p90"][legacy])<2e-9,"Prior P90 changed")
    rows.append(dict(ordinal=number,p90Px=p90))

summary={}
for key,base in (("unit","unit"),("huber","unit"),("signal","unit"),("signalHuber","huber")):
    summary[key]=dict(
        pooledP90Px=float(np.quantile(np.concatenate(raw[key]),.9)),
        framesAtThreshold=sum(row["p90Px"][key]<=plan["thresholdPx"] for row in rows),
        comparison=base,
        framesImproved=sum(row["p90Px"][key]<row["p90Px"][base] for row in rows),
    )
result=dict(schema=plan["schema"],protocolSha256=PIN,sourceReportReplayedExactly=True,
            trainingTracks=len(train),heldoutTracks=len(test),heldoutPairs=len(test)*len(rows),
            frames=rows,summary=summary,nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as out:
    json.dump(result,out,indent=2,allow_nan=False)
    out.write("\n")
