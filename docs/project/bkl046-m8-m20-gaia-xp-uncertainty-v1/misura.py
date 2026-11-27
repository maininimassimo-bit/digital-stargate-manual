from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

parser=ArgumentParser()
for name in ("protocol","color","catalog","packages","output"):
    parser.add_argument(name,type=Path)
args=parser.parse_args()
sys.path.insert(0,str(args.packages))
import numpy as np


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def pinned(path,pin):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==pin,f"Changed {path.name}")
    return json.loads(raw)


PIN="6537106ac22f836d6b3c0a4307cd6d8b48b430da0c914b7b7c46c18e4c990710"
plan=pinned(args.protocol,PIN)
baseline=pinned(args.color,plan["colorReport"])
require(baseline["calibrationOrder"]==["A","B"] and baseline["centerOrder"]==["unit","weighted"],
        "Metric order changed")
catalog=pinned(args.catalog,plan["catalogJoin"])["M8M20"]["rows"]
tiles={row["sourceId"]:int(row["rawId"].split("-")[0]) for row in catalog if not row["fit"]}
order=sorted(tiles)
require(len(order)==plan["heldout"],"Held-out Gaia sample changed")
district=np.asarray([tiles[key] for key in order])
unique=np.unique(district)
require(len(unique)==plan["regions"],"Spatial sample changed")
blocks=[np.flatnonzero(district==region) for region in unique]
configurations=list(baseline["models"])
residuals=[]
for model in configurations:
    values=baseline["models"][model]
    rows={row["sourceId"]:row["residualMag"] for row in values["heldout"]}
    require(len(rows)==len(values["heldout"]) and sorted(rows)==order,"Model cohort changed")
    residuals.append(np.abs(np.array([rows[key] for key in order])))
# stars, response models, calibrations, center methods
values=np.stack(residuals,axis=1)


def difference(p90):
    return p90[...,1]-p90[...,0]


def all_scores(sample):
    return difference(np.quantile(sample,.9,axis=0))


point=all_scores(values)
baseline_point=np.asarray([baseline["models"][name]["deltaP90WeightedMinusUnitMag"]
                           for name in configurations])
require(np.array_equal(point,baseline_point),"Source scores did not reproduce")
constant=np.array([[[[.2,.1]]]]*6)
require(np.allclose(all_scores(constant),[[-.1]],atol=1e-14,rtol=0),"Paired score control failed")
random=np.random.default_rng(plan["seed"])
p=plan["probabilities"]
star_draws=random.integers(len(order),size=(plan["starDraws"],len(order)))
star=difference(np.quantile(values[star_draws],.9,axis=1))
draws=list(product(range(len(blocks)),repeat=len(blocks)))
spatial=np.stack([all_scores(values[np.concatenate([blocks[n] for n in draw])]) for draw in draws])
loo=np.stack([all_scores(np.delete(values,n,axis=0)) for n in range(len(order))])
lob=np.stack([all_scores(values[district!=region]) for region in unique])
star_pct=np.quantile(star,p,axis=0)
spatial_pct=np.quantile(spatial,p,axis=0)
report=dict(schema=plan["schema"],protocolSha256=PIN,pointScoresReproduced=True,
            heldout=len(order),regions={str(reg):len(inds) for reg,inds in zip(unique,blocks,strict=True)},
            spatialResamples=len(draws),starResamples=len(star),percentileOrder=p,calibrationOrder=["A","B"],
            results={model:dict(pointMag=point[i].tolist(),starPercentilesMag=star_pct[:,i].tolist(),
                spatialPercentilesMag=spatial_pct[:,i].tolist(),
                deleteOneStarRangeMag=[loo[:,i].min(axis=0).tolist(),loo[:,i].max(axis=0).tolist()],
                deleteOneBlockRangeMag=[lob[:,i].min(axis=0).tolist(),lob[:,i].max(axis=0).tolist()])
                for i,model in enumerate(configurations)},
            nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as out:
    json.dump(report,out,indent=2,allow_nan=False)
    out.write("\n")
