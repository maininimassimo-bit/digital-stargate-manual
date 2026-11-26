from argparse import ArgumentParser
from hashlib import file_digest,sha256
from io import BytesIO
from itertools import product
import json
from pathlib import Path
import sys
from zipfile import ZipFile

p=ArgumentParser()
for n in ("protocol","calibration","packages","output"):
    p.add_argument(n,type=Path)
args=p.parse_args()
sys.path.insert(0,str(args.packages))
import numpy as np
from astropy.io import fits


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def pin(path,h):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==h,f"Changed {path.name}")
    return raw


PIN="310aacfbd8b5dde232414e014277694eb81a7eae0b2d14ae5cf5d16ca60760b1"
plan=json.loads(pin(args.protocol,PIN))
receipt=json.loads(pin(args.calibration/"riscontro.json",plan["calibrationReceipt"]))
size=plan["width"]
tiles=[(x,y) for y,x in product(plan["y"],plan["x"])]
train_tiles=np.array([(row+col)%2==0 for row,col in product(range(len(plan["y"])),range(len(plan["x"])))])
roles=np.array([pair in plan["calibrationPairs"] for pair in range(7)])
require(len(tiles)==35 and all(g%2==0 for xy in tiles for g in xy),"Unexpected ROI parity")
require(np.flatnonzero(~roles).tolist()==plan["validationPairs"],"Pair assignments differ")


def extract(kind,name,expected):
    path=args.calibration/name
    with path.open("rb") as stream:
        require(file_digest(stream,"sha256").hexdigest()==expected,f"Changed {name}")
    members=receipt["sourceMembers"][kind]
    require(len(members)==15,"Unexpected chronology or frame count")
    result,dates=[],[]
    with ZipFile(path) as archive:
        for entry in members[:14]:
            raw=archive.read(entry["file"])
            require(sha256(raw).hexdigest()==entry["sha256"],"Invalid calibration exposure")
            with fits.open(BytesIO(raw),memmap=False,uint=True) as hdus:
                img,head=hdus[0].data,hdus[0].header
                require(img.shape==(4176,6248) and head["BAYERPAT"]=="RGGB"
                        and float(head["EXPTIME"])==3.,"Invalid Bayer exposure geometry")
                dates.append(head["DATE-OBS"])
                result.append([[img[y0+j:y0+size:2,x0+i:x0+size:2].astype(float)
                                for j,i in product((0,1),repeat=2)] for x0,y0 in tiles])
    require(dates==sorted(set(dates)),"Calibration date order changed")
    return np.asarray(result).reshape(7,2,len(tiles),4,size//2,size//2)


flats=extract("flat","Flats_3s.zip",plan["flats"])
dark=extract("shortDark","Offsets_3s.zip",plan["shortDarks"])
levels=np.median(dark[roles].reshape(-1,*dark.shape[2:]),axis=0)
dark_plane=np.median(levels,axis=(-1,-2),keepdims=True)
mask=(levels-dark_plane)<=plan["hotDarkAboveMedian"]
rows=[]
for i in range(7):
    for c,parity in enumerate(plan["parities"]):
        a,b=flats[i,:,:,c]
        d1,d2=dark[i,:,:,c]
        valid=mask[:,c]&(a<plan["rawSaturationAdu"])&(b<plan["rawSaturationAdu"])
        ratios=[]
        for t in np.flatnonzero(train_tiles):
            m=valid[t]
            background=levels[t,c][m]
            ratios.append(np.mean(a[t][m]-background)/np.mean(b[t][m]-background))
        alpha=float(np.median(ratios))
        require(np.isfinite(alpha) and .75<alpha<1.25,"Illumination shift outside guard")
        for t,m in enumerate(valid):
            require(m.sum()>=plan["minimumValidPerParity"],"Insufficient tile support")
            fa,fb,base=a[t][m],b[t][m],levels[t,c][m]
            signal=float(np.mean((fa+alpha**2*fb)/(1+alpha**2)-base))
            flat_variance=float(np.var((fa-alpha*fb)/np.sqrt(1+alpha**2),ddof=1))
            dark_variance=float(np.var((d1[t][m]-d2[t][m])/np.sqrt(2.),ddof=1))
            require(signal>0 and flat_variance>0 and dark_variance>0,"Degenerate physical measurement")
            rows.append(dict(pair=i,tile=t,parity=parity,trainPair=bool(roles[i]),trainTile=bool(train_tiles[t]),
                usableSamples=int(m.sum()),flatSignalAdu=signal,flatTemporalVarianceAdu2=flat_variance,
                darkTemporalVarianceAdu2=dark_variance,illuminationRatio=alpha))


def fit(x,y):
    center=np.mean(x)
    denom=np.sum((x-center)**2)
    require(denom>0,"No signal variation")
    slope=np.sum((x-center)*(y-np.mean(y)))/denom
    return float(slope),float(np.mean(y)-slope*center)


known=np.arange(1.,5.)
np.testing.assert_allclose(fit(known,2.4*known+12),[2.4,12],atol=1e-12,rtol=0)
summary={}
for parity in plan["parities"]:
    group=[r for r in rows if r["parity"]==parity]
    train=[r for r in group if r["trainPair"] and r["trainTile"]]
    test=[r for r in group if not r["trainPair"] and not r["trainTile"]]
    def values(rs,k):
        return np.array([r[k] for r in rs])
    x,y=values(train,"flatSignalAdu"),values(train,"flatTemporalVarianceAdu2")
    tx,ty=values(test,"flatSignalAdu"),values(test,"flatTemporalVarianceAdu2")
    slope,offset=fit(x,y)
    predicted=tx*slope+offset
    flat=np.full_like(tx,y.mean())
    def p90(est):
        return float(np.quantile(abs(est-ty)/ty,.9)*100)
    def pair_slope(i):
        sub=[r for r in train if r["pair"]!=i]
        return fit(values(sub,"flatSignalAdu"),values(sub,"flatTemporalVarianceAdu2"))[0]
    slopes=[pair_slope(i) for i in plan["calibrationPairs"]]
    summary[parity]=dict(train=len(train),heldout=len(test),fitSlopeAdu=slope,fitInterceptAdu2=offset,
        trainSignalSpanAdu=[float(x.min()),float(x.max())],
        independentTileAndPairP90Pct=dict(signalModel=p90(predicted),constantModel=p90(flat)),
        heldoutSignalSpanAdu=[float(tx.min()),float(tx.max())],
        heldoutDarkVarianceMedianAdu2=float(np.median(values(test,"darkTemporalVarianceAdu2"))),
        heldoutFlatVarianceMedianAdu2=float(np.median(ty)),
        dropOneTrainingPairSlopeRangeAdu=[min(slopes),max(slopes)])
report=dict(schema=plan["schema"],protocolSha256=PIN,numberOfExposuresPerKind=14,numberOfTiles=len(tiles),
            tiles=tiles,parityResults=summary,rows=rows,gainCalibrated=False,nativeExecutions=0,scientificClosures=0)
with args.output.open("x",encoding="utf8",newline="\n") as out:
    json.dump(report,out,indent=2,allow_nan=False)
    out.write("\n")
