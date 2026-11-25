from hashlib import sha256
import json
from pathlib import Path
import sys

folder, field, base, capture, stars, deps, wheel, vc, output = sys.argv[1:]
folder, base, output = map(Path,(folder,base,output))
raw=(folder/"protocollo.json").read_bytes()
pin=sha256(raw).hexdigest()
assert pin=="8be0957616e436d54caabe61d51690e2d5624063832eb088a022213db1fc355c"
p=json.loads(raw)
prior_raw=(base/"riscontro.json").read_bytes()
assert sha256(prior_raw).hexdigest()==p["inputs"][field]
prior=json.loads(prior_raw)
script=base/"riferimenti.py"
source=script.read_bytes()
assert sha256(source).hexdigest()==prior["programSha256"]
prefix, separator, _ = source.decode().partition("\ncomparisons = []\n")
assert separator
namespace={"__file__":str(script)}
args=[str(base),capture,stars,deps,str(output)]
if field=="IC1805":
    args=[str(base),capture,stars,wheel,deps,vc,str(output)]
sys.argv=[str(script),*args]
exec(compile(prefix,str(script),"exec"),namespace)
np=namespace["np"]
groups,common,images,design,scores,train,cell = (
    namespace[k] for k in ("groups","common","images","design","scores","train","cell"))
assert len(groups)==192
coords=np.array([(s[1].start//cell,s[0].start//cell) for s in groups])
test_masks={}
for band,(axis,start) in p["bands"].items():
    idx=coords[:,axis]
    selected=(idx>=start)&(idx<start+p["bandWidthCells"])
    assert selected.sum()==(24 if axis==0 else 32)
    test_masks[band]=selected

def evaluate(data, fit):
    offset, plane=[scores(design,data,fit,n) for n in (1,3)]
    passed=(plane["medianAbsoluteADU"] <= offset["medianAbsoluteADU"]*(1-p["minimumMedianImprovement"])
            and plane["p90AbsoluteADU"] <= offset["p90AbsoluteADU"])
    return {"offset":offset,"plane":plane,"pass":passed}

rows=[]
ordered=list(p["bands"])
for pair in prior["cases"]:
    ref,target=pair["referenceIndex"],pair["targetIndex"]
    delta=images[target]-images[ref]
    data=np.array([np.median(delta[s][common[s]]) for s in groups])
    for i,fit in enumerate((train,~train)):
        assert {"trainParity":i,**evaluate(data,fit)}==pair["folds"][i]
    scores_by_band={name:evaluate(data,~mask) for name,mask in test_masks.items()}
    edge=all(scores_by_band[name]["pass"] for name in ordered[:4])
    inner=all(scores_by_band[name]["pass"] for name in ordered[4:])
    rows.append({"reference":ref,"target":target,"checkerboardPass":pair["passBothFolds"],
                 "allEdgesPass":edge,"allInteriorBandsPass":inner,"bands":scores_by_band})
summary={"pairs":len(rows),
         "checkerboardPass":sum(r["checkerboardPass"] for r in rows),
         "allEdgesPass":sum(r["allEdgesPass"] for r in rows),
         "allInteriorBandsPass":sum(r["allInteriorBandsPass"] for r in rows),
         "checkerboardPassButSomeEdgeFails":sum(r["checkerboardPass"] and not r["allEdgesPass"] for r in rows),
         "bands":{name:{"testCells":int(test_masks[name].sum()),"passed":sum(r["bands"][name]["pass"] for r in rows),
                        "medianPlaneP90ADU":float(np.median([r["bands"][name]["plane"]["p90AbsoluteADU"] for r in rows])),
                        "medianOffsetP90ADU":float(np.median([r["bands"][name]["offset"]["p90AbsoluteADU"] for r in rows]))}
                  for name in ordered}}
out={"schema":"BKL046_DIFFUSE_HELD_OUT_EDGES_V1","field":field,"protocolSha256":pin,
     "parentReportSha256":p["inputs"][field],"programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),
     "summary":summary,"results":rows,"nativeExecutions":0,"scientificClosures":0}
output.write_bytes((json.dumps(out,sort_keys=True,indent=2)+"\n").encode())
print(json.dumps(summary))
