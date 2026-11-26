"""Locate which channels and local windows contribute to the Roman transfer tail."""
from hashlib import sha256
import json
from pathlib import Path
import sys

protocol, forecast, prior_dir, decoder, kernel_path, lin_root, gain_root, packages, output = map(Path,sys.argv[1:])
raw = protocol.read_bytes()
spec = json.loads(raw)


def exact(path, pin):
    data = path.read_bytes()
    if sha256(data).hexdigest() != pin:
        raise ValueError(f"Changed input {path.name}")
    return data


def program(path, pin):
    env = dict(__name__="tail_diagnostic")
    exec(compile(exact(path,pin),str(path),"exec"),env)
    return env


def require(ok, message):
    if not ok:
        raise ValueError(message)


base = program(decoder,spec["decoder"])
kernel = program(kernel_path,spec["kernel"])
prior = json.loads(exact(prior_dir/"riscontro.json",spec["prior"]))
details = json.loads(exact(forecast/"dettaglio.json",spec["detail"]))
lin = json.loads(exact(lin_root/"acquisizione.json",spec["linCapture"]))
gain = json.loads(exact(gain_root/"acquisizione.json",spec["gainCapture"]))
sources = [dict(m,exposure=r["exposure"]) for r in lin["records"] for m in r["members"][1:]]
sys.path.insert(0,str(packages))
import numpy as np
require(np.__version__=="2.3.5","Unexpected NumPy")
frames=(0,1,5,10)
bands=("lower","upper")
w=np.array([[.25,.5,.25],[.5,1.,.5],[.25,.5,.25]])


def scores(sample):
    matrix=np.asarray([[abs(row["gainEmpirical"]/row["targetVariance"]-1),
                        abs(row["lin0Empirical"]/row["targetVariance"]-1)] for row in sample])
    p95=100*np.quantile(matrix,.95,axis=0)
    return dict(gainP95=float(p95[0]),lin0P95=float(p95[1]),differencePoints=float(p95[0]-p95[1]))


summaries={}
all_rows=[]
for band in bands:
    sample=[r for r in details if r["band"]==band and r["state"]=="MEASURED"]
    keyed={(r["channel"],r["firstExposure"]):r for r in sample}
    require(len(sample)==len(keyed)==480,"Cohort")
    intact=scores(sample)
    expected=next(row["differencePercentagePoints"] for row in prior["summary"]
                  if row["band"]==band and row["percentile"]==95 and row["model"]=="gainEmpirical")
    np.testing.assert_allclose(intact["differencePoints"],expected,atol=1e-12,rtol=0)
    channel_omissions=[dict(channel=c,**scores([r for r in sample if r["channel"]!=c])) for c in range(32)]
    pair_omissions=[dict(firstExposure=p,**scores([r for r in sample if r["firstExposure"]!=p]))
                    for p in range(1,30,2)]

    _, gain_rail=base["decode"](np,gain_root/"source",gain["captures"],band,20,frames)
    lin_values, lin_rail=base["decode"](np,lin_root/"source",sources,band,30,frames)
    cells=[]
    for c, rail in enumerate(gain_rail|lin_rail):
        retained, _=kernel["plan_support"](np,rail)
        area=np.argwhere(retained)
        for i,(a,b) in enumerate(base["pair_images"](lin_values,1,c,30)):
            row=keyed[c,2*i+1]
            blocks=np.lib.stride_tricks.sliding_window_view(((b-a)/np.sqrt(2))[:63,:63],(3,3))[::2,::2]
            projection=blocks[retained].reshape(-1,9)@w.ravel()
            np.testing.assert_allclose(np.var(projection,ddof=1),row["targetVariance"],rtol=1e-12,atol=1e-10)
            weights=(projection-np.mean(projection))**2
            order=np.argsort(weights)[::-1]
            top=order[0]
            total=weights.sum()
            e=100*abs(row["gainEmpirical"]/row["targetVariance"]-1)
            ref=100*abs(row["lin0Empirical"]/row["targetVariance"]-1)
            cells.append(dict(band=band,channel=c,firstExposure=2*i+1,windowCount=len(area),
                              largestWindowXY=[int(z)*2 for z in area[top][::-1]],
                              topOnePct=float(weights[top]/total*100),
                              topFivePct=float(weights[order[:5]].sum()/total*100),
                              gainErrorPct=e,lin0ErrorPct=ref,
                              observedVariance=row["targetVariance"]))
    ranked=sorted(cells,key=lambda r:r["gainErrorPct"],reverse=True)
    tail_channels={}
    for row in ranked[:24]:
        c=str(row["channel"])
        tail_channels[c]=tail_channels.get(c,0)+1
    summaries[band]=dict(intact=intact,channelOmissions=channel_omissions,pairOmissions=pair_omissions,
                         topFiveRows=ranked[:5],topTwentyFourRowsByChannel=tail_channels)
    all_rows.extend(cells)

require(len(all_rows)==960,"Incomplete variance recovery")
output.mkdir()
detail=json.dumps(all_rows,sort_keys=True,indent=2,allow_nan=False)+"\n"
(output/"dettaglio.json").write_bytes(detail.encode())
report=dict(schema=spec["schema"],protocolSha256=sha256(raw).hexdigest(),detailSha256=sha256(detail.encode()).hexdigest(),
            windowsVerifiedAgainstAllRows=960,summaries=summaries,exploratoryOnly=True,
            nativeExecutions=0,scientificClosures=0)
(output/"riscontro.json").write_bytes((json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n").encode())
