from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

parser = ArgumentParser()
for key in ("protocol", "source", "data", "vc", "dependencies", "output"):
    parser.add_argument(key, type=Path)
args = parser.parse_args()


def require(test, reason):
    if not test:
        raise ValueError(reason)


def exact(path, digest):
    data = path.read_bytes()
    require(sha256(data).hexdigest() == digest, f"Changed {path.name}")
    return data


PIN = "4202c6564379060ee373c658ce74f987083007344244247e2b1851c61c821a92"
plan = json.loads(exact(args.protocol, PIN))
source_path = args.source/"confronto.py"
source_code = exact(source_path, plan["sourceCode"]).decode("utf8")
source_report = exact(args.source/"riscontro.json", plan["sourceReport"])
parent = {"__name__":"__main__", "__file__":str(source_path)}
signal = {}
rows = []
all_errors = {}


def observe_signal(member, key, image, seed):
    np = parent["np"]
    radius = parent["radius"]
    dx, dy, ring, core = (parent[name] for name in ("dx","dy","ring","core"))
    x, y = np.rint(seed).astype(int)
    patch = image[y-radius:y+radius+1, x-radius:x+radius+1].astype(float)
    ratios = []
    for oy,ox in ((0,1),(1,0)):
        parity = ((dy+y)%2==oy)&((dx+x)%2==ox)
        sky = patch[parity&ring]
        med = np.median(sky)
        noise = max(1.,1.4826*np.median(np.abs(sky-med)))
        ratios.append((patch[parity&core].max()-med)/noise)
    proxy = min(ratios)
    require(np.isfinite(proxy) and proxy>0, "Invalid peak-to-noise proxy")
    signal.setdefault(member["member"],{})[key] = proxy


def model(x, y, test, weights, kind):
    np = parent["np"]
    w = weights/weights.sum()
    x0,y0 = w@x,w@y
    dx,dy = x-x0,y-y0
    if kind == "similarity":
        norm = w@np.sum(dx*dx,axis=1)
        a = (w@np.sum(dx*dy,axis=1))/norm
        b = (w@(dx[:,0]*dy[:,1]-dx[:,1]*dy[:,0]))/norm
        matrix = np.array(((a,b),(-b,a)))
    else:
        factor = np.sqrt(w)[:,None]
        matrix,_,rank,_ = np.linalg.lstsq(dx*factor,dy*factor,rcond=None)
        require(rank==2, "Weighted affine rank")
    return (test-x0)@matrix+y0


def observe_pair(member, train, test, reference, target):
    np = parent["np"]
    reference_key=parent["members"][0]["member"]
    source_proxy,target_proxy = signal[reference_key],signal[member["member"]]
    strength = np.array([min(source_proxy[k],target_proxy[k]) for k in train])
    limit = np.sqrt(plan["weightRatioCap"])
    weights = np.clip((strength/np.median(strength))**2,1/limit,limit)
    x,y,tx,ty = (np.array([points[k] for k in keys]) for keys in (train,test) for points in (reference,target))
    result = {}
    for kind in plan["models"]:
        estimates = {}
        for label, w in (("unit",np.ones(len(x))),("weighted",weights)):
            errors = np.linalg.norm(model(x,y,tx,w,kind)-ty,axis=1)
            all_errors.setdefault((kind,label),[]).append(errors)
            estimates[label] = float(np.quantile(errors,.9))
        result[kind] = estimates
    rows.append(dict(sequenceOrdinal=len(rows)+1,training=len(train),heldout=len(test),p90Px=result))
    del signal[member["member"]]


def instrument(text, line, callback):
    require(text.count(line)==1, "The source observer anchor changed")
    return text.replace(line,line+"\n"+callback)


body = instrument(source_code, "                found[key] = np.mean(centers,axis=0)",
                  "                observe_signal(frame, key, decoded.raw_image_visible, seed)")
body = instrument(body, "        detector_error=goal-matrix(ref)@detector_to_target",
                  "        observe_pair(member, train, test, found_ref, target)")
parent.update(observe_signal=observe_signal,observe_pair=observe_pair)
with TemporaryDirectory(dir=args.output.parent) as temp:
    replay = Path(temp)/"replay.json"
    previous_argv=sys.argv
    sys.argv=[str(source_path),*map(str,(args.data,args.vc,args.dependencies,replay))]
    try:
        exec(compile(body,str(source_path),"exec"),parent)
    finally:
        sys.argv=previous_argv
    require(replay.read_bytes()==source_report, "Independent field baseline did not replay exactly")

np = parent["np"]
x = np.array(((10.,11.),(12.,17.),(15.,10.),(20.,20.)))
w = np.array((.25,2.,4.))
for kind,matrix in (("similarity",((.98,.02),(-.02,.98))),("affine",((1.02,.08),(.04,.97)))):
    y = x@np.array(matrix)+np.array((2.,-8.))
    require(np.allclose(model(x[:3],y[:3],x[3:],w,kind),y[3:],atol=1e-10,rtol=0),
            f"Synthetic control failed: {kind}")
require(len(rows)==plan["expectedComparisons"] and sum(r["heldout"] for r in rows)==plan["expectedHeldoutPairs"],
        "Unexpected evaluation coverage")
summary={}
for kind in plan["models"]:
    pairs = np.array([[r["p90Px"][kind][key] for key in ("unit","weighted")] for r in rows])
    delta = pairs[:,1]-pairs[:,0]
    summary[kind]=dict(
        pooledP90Px={key:float(np.quantile(np.concatenate(all_errors[kind,key]),.9))
                     for key in ("unit","weighted")},
        framesImproved=int((delta<0).sum()),framesWorse=int((delta>0).sum()),framesTied=int((delta==0).sum()),
        medianPairedP90ChangePx=float(np.median(delta)),
        framesAtThreshold={key:int((pairs[:,i]<=plan["diagnosticP90Px"]).sum())
                           for i,key in enumerate(("unit","weighted"))})
report=dict(schema=plan["schema"],protocolSha256=PIN,frozenFieldBaselineReplayedExactly=True,
            frameComparisons=len(rows),heldoutPairs=sum(r["heldout"] for r in rows),
            summary=summary,frames=rows,nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as stream:
    json.dump(report,stream,indent=2,allow_nan=False)
    stream.write("\n")
