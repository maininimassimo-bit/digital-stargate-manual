"""Test the geometry of joint DQ support without estimating flux."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


def read(path, expected):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == expected, path
    return raw


def sample_mask(np, valid, points, policy):
    rounded = np.floor(points+.5).astype(int)
    base = np.floor(points).astype(int)
    xy, offsets = {
        "nearest": (rounded, (0,)),
        "four": (base, (0,1)),
        "sixteen": (base, (-1,0,1,2)),
    }[policy]
    result = np.ones(len(points),dtype=bool)
    h,w = valid.shape
    for y in offsets:
        for x in offsets:
            a,b = xy[:,0]+x,xy[:,1]+y
            inside = (a>=0)&(a<w)&(b>=0)&(b<h)
            good = np.zeros(len(points),dtype=bool)
            good[inside] = valid[b[inside],a[inside]]
            result &= good
    return result


def assess(np, masks, groups):
    both = masks[0]&masks[1]
    either = masks[0]|masks[1]
    return {label:{
        "gridPoints": int(mask.sum()),
        "firstUncovered": int(np.count_nonzero(mask&~masks[0])),
        "secondUncovered": int(np.count_nonzero(mask&~masks[1])),
        "jointUncovered": int(np.count_nonzero(mask&~either)),
        "bothSupported": int(np.count_nonzero(mask&both)),
    } for label,mask in groups.items()}


def main():
    parser=argparse.ArgumentParser()
    for name in ("protocol","sourceA","sourceB","dependencies","report"):
        parser.add_argument(name,type=Path)
    a=parser.parse_args()
    raw=a.protocol.read_bytes()
    p=json.loads(raw)
    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS
    assert (np.__version__,astropy.__version__)==("2.3.5","7.2.0")
    allgood=np.ones((6,6),dtype=bool)
    test=np.array([[0.,0.],[5.,5.],[2.25,2.25]])
    assert sample_mask(np,allgood,test,"nearest").tolist()==[True,True,True]
    assert sample_mask(np,allgood,test,"four").tolist()==[True,False,True]
    assert sample_mask(np,allgood,test,"sixteen").tolist()==[False,False,True]

    pairs={}
    n_files=0
    for root,pin in zip((a.sourceA,a.sourceB),p["sources"],strict=True):
        report=json.loads(read(root/"riscontro.json",pin["report"]))
        capture=json.loads(read(root/"acquisizione.json",pin["capture"]))
        by_name={row["file"]:row for assoc in capture["associations"] for row in assoc["rows"]}
        assert len(by_name)==len(report["rows"])
        for row in report["rows"]:
            name=row["file"]
            path=root/"source"/name
            assert len(read(path,by_name[name]["sha256"]))==by_name[name]["bytes"]
            n_files+=1
            key=(row["visit"],int(row["chip"]),row["band"])
            pairs.setdefault(key,[]).append((path,row))
    assert n_files==48 and len(pairs)==24
    outcomes=[]
    for (visit,chip,band),items in sorted(pairs.items()):
        assert len(items)==2
        items.sort(key=lambda item:item[1]["dither"])
        row={"visit":visit,"chip":chip,"band":band,"inputs":[x[1]["file"] for x in items],
             "states":[x[1]["state"] for x in items]}
        outcomes.append(row)
        if any(x["state"]=="MODE_OR_CALIBRATION_REFUSED" or "gaiaPixelXY" not in x for _,x in items):
            row["status"]="MODE_OR_WCS_REFUSED"
            continue
        wcs=[]
        valid=[]
        centers=[]
        for path,x in items:
            with fits.open(path,memmap=False) as h:
                sci=h["SCI",1]
                q=h["DQ",1].data
                assert h[0].header["EXPFLAG"]=="NORMAL" and h[0].header["SCAN_TYP"]=="N"
                assert sci.header["CCDCHIP"]==chip and q.shape==sci.data.shape
                wcs.append(WCS(sci.header,h).celestial)
                valid.append((q==0)&np.isfinite(sci.data))
                centers.append(np.array(x["gaiaPixelXY"]))
        x0,y0=centers[0]
        xp,yp=wcs[1].world_to_pixel_values(*wcs[0].pixel_to_world_values(x0,y0))
        adjust=centers[1]-[xp,yp]
        assert np.isfinite(adjust).all() and np.linalg.norm(adjust)<.01
        row["wcsCenterCrossCheckPx"]=float(np.linalg.norm(adjust))
        row["status"]="GEOMETRIC_MASK_ONLY"
        row["phases"]=[]
        for phase in p["phases"]:
            xy=np.mgrid[-10:11,-10:11][::-1].reshape(2,-1).T+phase
            r2=np.sum(xy**2,axis=1)
            masks={"core3":r2<=9,"r5":r2<=25,"r10":r2<=100}
            a_xy=xy+centers[0]
            right=np.stack(wcs[1].world_to_pixel_values(*wcs[0].pixel_to_world_values(*a_xy.T)),axis=1)+adjust
            assert np.isfinite(right).all()
            phase_row={"phaseXY":phase,"counts":{}}
            for policy in p["policies"]:
                good=[sample_mask(np,v,g,policy) for v,g in zip(valid,(a_xy,right),strict=True)]
                phase_row["counts"][policy]=assess(np,good,masks)
            row["phases"].append(phase_row)
    groups={}
    for visit in sorted({r["visit"] for r in outcomes}):
        group=[r for r in outcomes if r["visit"]==visit]
        assert len(group)==3
        groups[visit]={}
        for policy in p["policies"]:
            if any(r["status"]!="GEOMETRIC_MASK_ONLY" for r in group):
                groups[visit][policy]=None
                continue
            groups[visit][policy]={
                label:{
                    "completeInAllBandsAtNominalPhase":all(r["phases"][0]["counts"][policy][label]["jointUncovered"]==0 for r in group),
                    "completeInAllBandsAtAllPhases":all(v["counts"][policy][label]["jointUncovered"]==0 for r in group for v in r["phases"]),
                 } for label in ("core3","r5","r10")
            }
    out={"schema":"BKL046_GD153_DITHER_DQ_UNION_RESULT_V1","programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),
         "protocolSha256":sha256(raw).hexdigest(),"pairs":outcomes,"visitCoverage":groups,
         "measuredAstrometricRegistration":False,"fluxEstimated":False,
         "nativeExecutions":0,"scientificClosures":0}
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(out,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()
